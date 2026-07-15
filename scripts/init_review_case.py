#!/usr/bin/env python3
"""Create a compact single-comment response case with one planning file."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def existing_file(value: str | None) -> Path | None:
    if value is None:
        return None
    path = Path(value).expanduser().resolve(strict=True)
    if not path.is_file():
        raise ValueError(f"Expected a file: {path}")
    return path


def existing_dir(value: str | None) -> Path | None:
    if value is None:
        return None
    path = Path(value).expanduser().resolve(strict=True)
    if not path.is_dir():
        raise ValueError(f"Expected a directory: {path}")
    return path


def yaml_string(value: Path | str | None) -> str:
    if value is None:
        return "null"
    return json.dumps(str(value), ensure_ascii=False)


def git_revision(path: Path) -> str | None:
    probe = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
        check=False,
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0 or probe.stdout.strip() != "true":
        return None
    commit = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    dirty = bool(
        subprocess.run(
            ["git", "-C", str(path), "status", "--porcelain=v1"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    )
    return f"{commit}{' (dirty)' if dirty else ''}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("comment_id", help="Stable ID such as R2-C4")
    parser.add_argument("--root", default="response_exp", help="Parent directory")
    parser.add_argument("--paper-tex", required=True)
    parser.add_argument("--paper-pdf", required=True)
    parser.add_argument("--code-root", required=True)
    parser.add_argument("--review-comments", required=True)
    comment = parser.add_mutually_exclusive_group(required=True)
    comment.add_argument("--comment-file")
    comment.add_argument("--comment-text")
    parser.add_argument("--word-file")
    parser.add_argument("--previous-cases")
    args = parser.parse_args()

    paper_tex = existing_file(args.paper_tex)
    paper_pdf = existing_file(args.paper_pdf)
    code_root = existing_dir(args.code_root)
    review_comments = existing_file(args.review_comments)
    word_file = existing_file(args.word_file)
    previous_cases = existing_dir(args.previous_cases)
    assert paper_tex is not None and paper_pdf is not None and code_root is not None
    assert review_comments is not None

    if args.comment_file:
        comment_file = existing_file(args.comment_file)
        assert comment_file is not None
        comment_text = comment_file.read_text(encoding="utf-8")
    else:
        comment_text = args.comment_text

    case_dir = Path(args.root).expanduser().resolve() / args.comment_id
    case_dir.mkdir(parents=True, exist_ok=False)
    plan = case_dir / "response-plan.md"
    revision = git_revision(code_root)
    content = f"""---
comment_id: {yaml_string(args.comment_id)}
experiment_required: undecided
paper_tex: {yaml_string(paper_tex)}
paper_pdf: {yaml_string(paper_pdf)}
code_root: {yaml_string(code_root)}
code_revision: {yaml_string(revision)}
review_comments: {yaml_string(review_comments)}
word_file: {yaml_string(word_file)}
previous_cases: {yaml_string(previous_cases)}
---

# {args.comment_id} 回复思路与实验设计

## 原始意见

> {comment_text.strip().replace(chr(10), chr(10) + '> ')}

## 意见理解、证据缺口与相关论文/代码

<!-- TODO -->

## 与既往意见的关系及复用判定

<!-- TODO：先从完整 review_comments 筛选相关意见；未处理者只记录关联，已处理者先查对应 response-plan.md，仅在拟复用时核查其引用证据。 -->

## 回复思路与实验设计

<!-- TODO：将 experiment_required 改为 true 或 false；若为 true，写全实验设计。 -->

## 实际结果与证据映射

<!-- TODO：写入真实结果、来源文件/字段和结论边界。 -->

## Word 更新记录

<!-- TODO：记录目标块、备份路径、最终 Word 路径和验证结论。 -->
"""
    plan.write_text(content, encoding="utf-8")
    print(case_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
