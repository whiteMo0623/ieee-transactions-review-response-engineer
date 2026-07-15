#!/usr/bin/env python3
"""Initialize one isolated, traceable reviewer-comment case."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


DIRECTORIES = (
    "inputs",
    "notes",
    "experiments/src",
    "experiments/configs",
    "experiments/logs",
    "experiments/raw",
    "experiments/processed",
    "experiments/figures",
    "response",
    "delivery",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(value: str | None) -> dict | None:
    if value is None:
        return None
    path = Path(value).expanduser().resolve(strict=True)
    if not path.is_file():
        raise ValueError(f"Expected a file: {path}")
    return {"path": str(path), "sha256": sha256(path), "size": path.stat().st_size}


def tree_record(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    file_count = 0
    for item in sorted(path.rglob("*"), key=lambda candidate: candidate.relative_to(path).as_posix()):
        if not item.is_file():
            continue
        relative = item.relative_to(path).as_posix()
        item_hash = sha256(item)
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(item_hash.encode("ascii"))
        digest.update(b"\n")
        file_count += 1
    return {"provenance_mode": "directory-sha256", "tree_sha256": digest.hexdigest(), "file_count": file_count}


def directory_record(value: str | None, prefer_git: bool = False) -> dict | None:
    if value is None:
        return None
    path = Path(value).expanduser().resolve(strict=True)
    if not path.is_dir():
        raise ValueError(f"Expected a directory: {path}")
    record: dict[str, object] = {"path": str(path)}
    if prefer_git:
        probe = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
            check=False,
            capture_output=True,
            text=True,
        )
        if probe.returncode == 0 and probe.stdout.strip() == "true":
            commit = subprocess.run(
                ["git", "-C", str(path), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            status = subprocess.run(
                ["git", "-C", str(path), "status", "--porcelain=v1"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
            record.update({"provenance_mode": "git", "git_commit": commit, "git_dirty": bool(status), "git_status": status})
            return record
    record.update(tree_record(path))
    return record


def write_new(path: Path, content: str) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("comment_id", help="Stable ID such as reviewer-2-comment-3")
    parser.add_argument("--root", default="review_response_cases", help="Parent directory")
    parser.add_argument("--paper-tex", required=True)
    parser.add_argument("--paper-pdf", required=True)
    parser.add_argument("--latex-root", help="LaTeX source root; defaults to the main .tex parent")
    parser.add_argument("--code-root", required=True)
    comment = parser.add_mutually_exclusive_group(required=True)
    comment.add_argument("--comment-file")
    comment.add_argument("--comment-text")
    parser.add_argument("--word-template")
    parser.add_argument("--previous-cases")
    args = parser.parse_args()

    case_dir = Path(args.root).expanduser().resolve() / args.comment_id
    if case_dir.exists():
        raise FileExistsError(f"Case already exists: {case_dir}")
    for relative in DIRECTORIES:
        (case_dir / relative).mkdir(parents=True, exist_ok=False)

    comment_text: str
    comment_source: dict[str, object]
    if args.comment_file:
        record = file_record(args.comment_file)
        assert record is not None
        comment_text = Path(str(record["path"])).read_text(encoding="utf-8")
        comment_source = record
    else:
        comment_text = args.comment_text
        comment_source = {"inline": True, "sha256": hashlib.sha256(comment_text.encode()).hexdigest()}
    write_new(case_dir / "inputs/original-comment.md", comment_text.rstrip() + "\n")

    manifest = {
        "schema_version": 1,
        "comment_id": args.comment_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "experiment_required": None,
        "inputs": {
            "paper_tex": file_record(args.paper_tex),
            "paper_pdf": file_record(args.paper_pdf),
            "latex_root": directory_record(args.latex_root or str(Path(args.paper_tex).expanduser().resolve().parent), prefer_git=True),
            "code_root": directory_record(args.code_root, prefer_git=True),
            "comment_source": comment_source,
            "word_template": file_record(args.word_template),
            "previous_cases": directory_record(args.previous_cases),
        },
    }
    write_new(case_dir / "case.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    write_new(case_dir / "notes/paper-understanding.md", "# 论文理解\n\n<!-- TODO: 写入带来源位置的完整论文事实底座。 -->\n")
    write_new(case_dir / "notes/code-paper-map.md", "# 论文—代码映射\n\n<!-- TODO: 写入关键代码路径、配置和论文对应关系。 -->\n")
    write_new(
        case_dir / "analysis-and-experiment-plan.md",
        "# 单条审稿意见分析与实验方案\n\n"
        "## 意见理解\n\n<!-- TODO -->\n\n## 现有证据与缺口\n\n<!-- TODO -->\n\n"
        "## 与既往意见的关系及复用判定\n\n<!-- TODO -->\n\n## 处理方案\n\n<!-- TODO -->\n\n"
        "## 必要实验\n\n<!-- TODO -->\n\n## 结论判定规则\n\n<!-- TODO -->\n",
    )
    write_new(
        case_dir / "experiments/manifest.json",
        json.dumps({"schema_version": 1, "planned_seeds": [], "planned_runs": [], "runs": []}, indent=2) + "\n",
    )
    write_new(case_dir / "response/author-response.md", "")
    write_new(case_dir / "response/manuscript-changes.md", "")
    write_new(case_dir / "response/evidence-ledger.json", "[]\n")
    print(case_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
