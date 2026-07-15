#!/usr/bin/env python3
"""Audit the compact output contract for one reviewer-comment case."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


REQUIRED_HEADINGS = (
    "## 原始意见",
    "## 意见理解、证据缺口与相关论文/代码",
    "## 与既往意见的关系及复用判定",
    "## 回复思路与实验设计",
    "## 实际结果与证据映射",
    "## Word 更新记录",
)
CODE_SUFFIXES = {".py", ".sh", ".ps1", ".m", ".r", ".jl", ".ipynb"}
RESULT_SUFFIXES = {".json", ".csv", ".tsv", ".parquet", ".npz", ".npy", ".xlsx"}
FORBIDDEN_TOP_LEVEL = {"case.json", "inputs", "notes", "response", "delivery", "qa"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def metadata(text: str, key: str) -> str | bool | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    if not match:
        return None
    value = match.group(1)
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "null":
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_dir")
    args = parser.parse_args()
    root = Path(args.case_dir).expanduser().resolve(strict=True)
    errors: list[str] = []

    plan = root / "response-plan.md"
    if not plan.is_file() or plan.stat().st_size == 0:
        errors.append("Missing or empty response-plan.md")
        text = ""
    else:
        text = plan.read_text(encoding="utf-8")
        if "TODO" in text:
            errors.append("response-plan.md contains unresolved TODO markers")
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                errors.append(f"response-plan.md lacks heading: {heading}")

    experiment_required = metadata(text, "experiment_required")
    if not isinstance(experiment_required, bool):
        errors.append("experiment_required must be true or false")

    experiment = root / "experiment"
    if experiment_required is True:
        files = [path for path in experiment.rglob("*") if path.is_file()] if experiment.is_dir() else []
        if not any(path.suffix.lower() in CODE_SUFFIXES for path in files):
            errors.append("experiment/ has no runnable analysis or experiment code")
        if not any(path.suffix.lower() in RESULT_SUFFIXES for path in files):
            errors.append("experiment/ has no machine-readable actual result")
    elif experiment.is_dir() and any(path.is_file() for path in experiment.rglob("*")):
        errors.append("experiment_required is false but experiment/ is not empty")

    for name in FORBIDDEN_TOP_LEVEL:
        if (root / name).exists():
            errors.append(f"Redundant default artifact exists: {name}")
    for cache in root.rglob("__pycache__"):
        if cache.is_dir():
            errors.append(f"Python cache must be removed: {cache.relative_to(root)}")
    for page in root.rglob("page-*.png"):
        errors.append(f"Rendered QA page must remain temporary: {page.relative_to(root)}")
    case_docx = list(root.rglob("*.docx"))
    if case_docx:
        errors.append("DOCX must be updated at the user-specified path, not copied into the case directory")

    comment_id = metadata(text, "comment_id")
    word_value = metadata(text, "word_file")
    if word_value:
        word = Path(str(word_value)).expanduser()
        if not word.is_file() or word.suffix.lower() != ".docx":
            errors.append(f"Specified Word file is missing or invalid: {word}")
        elif not isinstance(comment_id, str) or not comment_id:
            errors.append("comment_id is missing; cannot determine backup name")
        else:
            backup = word.with_name(f"{word.stem}.before-{comment_id}{word.suffix}")
            if not backup.is_file():
                errors.append(f"Adjacent pre-edit backup is missing: {backup}")
            elif sha256(backup) == sha256(word):
                errors.append("Word file is identical to its pre-edit backup; target response may not have been written")

    if errors:
        print("AUDIT FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("AUDIT PASSED: compact case")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
