#!/usr/bin/env python3
"""Check case artifacts and explicit references; not scientific or Word-content QA."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from zipfile import BadZipFile, ZipFile
from xml.etree import ElementTree

REQUIRED_HEADINGS = (
    "## 原始意见", "## 意见理解、证据缺口与相关论文/代码",
    "## 与既往意见的关系及复用判定", "## 回复思路与实验设计",
    "## 实际结果与证据映射", "## Word 更新记录",
)
RESULT_SUFFIXES = {".json", ".csv", ".tsv", ".parquet", ".npz", ".npy", ".xlsx"}
FORBIDDEN_TOP_LEVEL = {
    "case.json", "inputs", "notes", "response", "delivery", "qa",
    "paper-understanding.md", "code-paper-map.md", "evidence-summary.md",
    "evidence-ledger.json", "case-summary.md",
}
ID_PATTERN = r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}"


def metadata(text: str) -> dict:
    """Read the documented flat frontmatter (JSON inline lists/maps; no YAML dependency)."""
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        raise ValueError("Missing frontmatter at start of response-plan.md")
    fields = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.fullmatch(r"([a-z_]+):[ \t]*(.*)", line)
        if not item:
            raise ValueError("Use flat frontmatter with one-line JSON arrays/objects")
        key, raw = item.groups()
        if key in fields:
            raise ValueError(f"Duplicate frontmatter key: {key}")
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            if raw.startswith(('"', '[', '{')):
                raise ValueError(f"Invalid JSON value for {key}")
            value = raw[1:-1].replace("''", "'") if raw.startswith("'") and raw.endswith("'") else raw
        fields[key] = value
    return fields


def path_at(root: Path, value: str) -> Path:
    p = Path(value).expanduser()
    return (p if p.is_absolute() else root / p).resolve()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def check_docx(path: Path) -> None:
    if path.suffix.lower() != '.docx':
        raise ValueError(f"Expected DOCX: {path}")
    with ZipFile(path) as z:
        ElementTree.fromstring(z.read('[Content_Types].xml'))
        doc = ElementTree.fromstring(z.read('word/document.xml'))
        if doc.tag != '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}document':
            raise ValueError(f"Invalid Word document root: {path}")


def check_result(path: Path) -> None:
    if path.suffix.lower() not in RESULT_SUFFIXES:
        raise ValueError(f"Unsupported result format: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Empty result file: {path}")
    if path.suffix.lower() == '.json':
        data = json.loads(path.read_text(encoding='utf-8-sig'))
        if data is None or data == {} or data == [] or data == '':
            raise ValueError(f"Empty JSON result: {path}")
    elif path.suffix.lower() in {'.csv', '.tsv'}:
        with path.open(encoding='utf-8-sig', newline='') as f:
            rows = (row for row in csv.reader(f, delimiter='\t' if path.suffix.lower()=='.tsv' else ',') if any(s.strip() for s in row))
            if next(rows, None) is None or next(rows, None) is None:
                raise ValueError(f"Result table needs header and data rows: {path}")


def audit(root: Path) -> list[str]:
    root = root.expanduser().resolve(strict=True)
    errors = []
    text = (root / 'response-plan.md').read_text(encoding='utf-8')
    fields = metadata(text)
    # Do not flag the reviewer's literal TODO wording as an unfinished author section.
    sections = re.split(r'(?m)^(## [^\n]+)\s*$', text)
    for heading in REQUIRED_HEADINGS:
        indexes = [i for i in range(1, len(sections), 2) if sections[i].strip() == heading]
        if len(indexes) != 1:
            errors.append(f"Expected one section: {heading}")
            continue
        content = sections[indexes[0] + 1]
        visible = re.sub(r'<!--.*?-->', '', content, flags=re.S).strip()
        if not visible or not re.search(r'\w', visible):
            errors.append(f"Empty section: {heading}; state not applicable with a reason if needed")
        if heading != REQUIRED_HEADINGS[0] and re.search(r'\b(?:TODO|TBD)\b', content):
            errors.append(f"Unresolved placeholder in {heading}")

    required = fields.get('experiment_required')
    if not isinstance(required, bool):
        errors.append('experiment_required must be true or false')
    for key in ('code_files', 'result_files'):
        values = fields.get(key, [])
        if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
            errors.append(f'{key} must be a one-line JSON array of file paths')
            continue
        if required is True and not values:
            errors.append(f'New experiments require explicit {key} references in frontmatter')
        for value in values:
            p = path_at(root, value)
            try:
                if not p.is_file() or p.stat().st_size == 0:
                    raise ValueError(f'Missing or empty {key} reference: {p}')
                if key == 'result_files':
                    check_result(p)
            except (OSError, ValueError) as exc:
                errors.append(str(exc))
    # A false experiment flag may legitimately retain reused figures and external results.
    approved = fields.get('approved_artifacts', {})
    if not isinstance(approved, dict):
        errors.append('approved_artifacts must be a JSON object mapping relative paths to user-request reasons')
        approved = {}
    exceptions = []
    for name, reason in approved.items():
        if not isinstance(name, str) or not isinstance(reason, str) or not reason.strip():
            errors.append('Each approved artifact needs a path and a nonempty user-request reason')
            continue
        p = path_at(root, name)
        if Path(name).is_absolute() or p == root or root not in p.parents:
            errors.append(f'Artifact exception must identify a child path within the case: {name}')
        else:
            exceptions.append(p)
    def exempt(p: Path) -> bool:
        return any(p.resolve() == e or e in p.resolve().parents for e in exceptions)

    word = backup = None
    value = fields.get('word_file')
    cid = fields.get('comment_id')
    if not isinstance(cid, str) or not re.fullmatch(ID_PATTERN, cid):
        errors.append('comment_id must be a safe single directory name (letters, digits, _ or -; max 64)')
    if not isinstance(value, str) or not value.strip():
        errors.append('word_file is required for final artifact audit')
    else:
        word = path_at(root, value)
        if isinstance(cid, str) and re.fullmatch(ID_PATTERN, cid):
            backup = word.with_name(f'{word.stem}.before-{cid}{word.suffix}')
        for p in (word, backup):
            if p is None:
                continue
            try:
                check_docx(p)
            except (OSError, ValueError, BadZipFile, KeyError, ElementTree.ParseError) as exc:
                errors.append(f'Word/backup missing or invalid: {p}: {exc}')
        if word.is_file() and backup and backup.is_file() and sha256(word) == sha256(backup):
            errors.append('Word bytes equal the pre-edit backup; verify whether the intended update is missing')

    for name in FORBIDDEN_TOP_LEVEL:
        p = root / name
        if p.exists() and not exempt(p):
            errors.append(f'Redundant default artifact: {name}; user-requested exceptions belong in approved_artifacts')
    for p in root.rglob('*'):
        if exempt(p):
            continue
        if p.name == '__pycache__' or (p.is_file() and re.fullmatch(r'page-.*\.png', p.name)):
            errors.append(f'Remove temporary artifact before audit: {p.relative_to(root)}')
        if p.is_file() and p.suffix.lower() == '.docx' and p.resolve() not in (word, backup):
            # Other cases may share the same user-specified response file and need their own backups.
            sibling_backup = word is not None and p.parent.resolve() == word.parent and re.fullmatch(
                re.escape(word.stem) + r'\.before-' + ID_PATTERN + re.escape(word.suffix), p.name)
            if not sibling_backup:
                errors.append(f'Unexpected DOCX copy: {p.relative_to(root)}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case_dir')
    args = parser.parse_args()
    try:
        root = Path(args.case_dir).expanduser().resolve(strict=True)
        errors = audit(root)
    except (OSError, ValueError, RuntimeError) as exc:
        errors = [str(exc)]
    if errors:
        print('AUDIT FAILED')
        for error in errors:
            print(f'- {error}')
        return 1
    print('AUDIT PASSED: artifact checks only; file changes do not prove target edits, scientific validity, visual QA, or submission readiness.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
