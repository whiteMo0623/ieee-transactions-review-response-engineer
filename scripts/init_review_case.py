#!/usr/bin/env python3
"""Create one planning file, or locate an existing case for non-destructive resumption."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ID_PATTERN = r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}"


def existing(value: str | None, directory: bool = False) -> Path | None:
    if value is None:
        return None
    path = Path(value).expanduser().resolve(strict=True)
    if not (path.is_dir() if directory else path.is_file()):
        raise ValueError(f"Expected {'directory' if directory else 'file'}: {path}")
    return path


def yaml_string(value: Path | str | None) -> str:
    return json.dumps(str(value) if value is not None else None, ensure_ascii=False)


def git_revision(path: Path) -> str | None:
    """Git and an existing commit are optional; bound the read-only probes."""
    try:
        commit = subprocess.run(
            ['git', '-C', str(path), 'rev-parse', '--verify', 'HEAD'],
            capture_output=True, text=True, timeout=10, check=False,
        )
        if commit.returncode:
            return None
        status = subprocess.run(
            ['git', '-C', str(path), 'status', '--porcelain=v1'],
            capture_output=True, text=True, timeout=10, check=False,
        )
        suffix = ' (dirty)' if status.stdout.strip() else ''
        if status.returncode:
            suffix = ' (worktree status unavailable)'
        return commit.stdout.strip() + suffix
    except (OSError, subprocess.TimeoutExpired):
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('comment_id', help='Safe single-component ID such as R2-C4')
    parser.add_argument('--root', default='response_exp', help='Case parent directory')
    parser.add_argument('--resume', action='store_true', help='Reuse existing plan unchanged; pass only ID and --root')
    for flag in ('paper-tex', 'paper-pdf', 'code-root', 'review-comments', 'word-file', 'previous-cases'):
        parser.add_argument('--' + flag)
    comment = parser.add_mutually_exclusive_group()
    comment.add_argument('--comment-file')
    comment.add_argument('--comment-text')
    args = parser.parse_args()
    try:
        if not re.fullmatch(ID_PATTERN, args.comment_id):
            raise ValueError('comment_id must use letters, digits, _ or -, start with a letter/digit, and be at most 64 characters')
        if re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])', args.comment_id):
            raise ValueError('comment_id cannot be a reserved filesystem name')
        root = Path(args.root).expanduser().resolve()
        case_dir = root / args.comment_id
        if case_dir.is_symlink():
            raise ValueError('Case directory must not be a symlink')
        if args.resume:
            if any(getattr(args, x) is not None for x in ('paper_tex','paper_pdf','code_root','review_comments','word_file','previous_cases','comment_file','comment_text')):
                raise ValueError('--resume reuses recorded inputs; pass only comment_id, --root and --resume')
            plan = case_dir / 'response-plan.md'
            text = plan.read_text(encoding='utf-8')
            front = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
            ids = re.findall(r'(?m)^comment_id:[ \t]*(.*?)\s*$', front.group(1)) if front else []
            if len(ids) != 1:
                raise ValueError('Existing plan needs one comment_id in frontmatter')
            raw = ids[0]
            stored_id = json.loads(raw) if raw.startswith('"') else raw.strip("'")
            if stored_id != args.comment_id:
                raise ValueError('Existing plan comment_id does not match requested case')
            print(f'RESUME (unchanged): {plan}')
            return 0
        missing = [name for name in ('paper_tex','paper_pdf','code_root','review_comments') if not getattr(args, name)]
        if missing:
            raise ValueError('New cases require: ' + ', '.join('--' + n.replace('_','-') for n in missing))
        if args.comment_file is None and args.comment_text is None:
            raise ValueError('New cases require --comment-file (UTF-8 text) or --comment-text')
        paper_tex = existing(args.paper_tex)
        paper_pdf = existing(args.paper_pdf)
        code_root = existing(args.code_root, directory=True)
        review_comments = existing(args.review_comments)
        word_file = existing(args.word_file)
        previous_cases = None
        if args.previous_cases:
            requested = Path(args.previous_cases).expanduser().resolve()
            # First case: no older evidence exists when the requested previous root is this new root.
            if requested != root or requested.exists():
                previous_cases = existing(args.previous_cases, directory=True)
        comment_file = existing(args.comment_file)
        comment_text = comment_file.read_text(encoding='utf-8') if comment_file else args.comment_text
        if not comment_text.strip():
            raise ValueError('Original comment must not be empty')
        if case_dir.exists():
            raise ValueError(f'Case exists; read its plan or use --resume without reinitializing: {case_dir}')
        revision = git_revision(code_root)
        content = f'''---
comment_id: {yaml_string(args.comment_id)}
experiment_required: undecided
code_files: []
result_files: []
approved_artifacts: {{}}
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

<!-- TODO：核验 LaTeX/PDF 版本及相关代码路径；记录意见类型、证据门槛和所需事实。 -->

## 与既往意见的关系及复用判定

<!-- TODO：先从完整 review_comments 筛选相关意见；未处理者只记录关联，已处理者先查对应 response-plan.md，仅在拟复用时核查其引用证据；没有关联时写明理由。 -->

## 回复思路与实验设计

<!-- TODO：将 experiment_required 改为 true 或 false 并说明理由；若为 true，写明适用的设计、完整预算、验证早停及种子约定。code_files/result_files 用单行 JSON 数组列出实际文件，允许绝对路径或相对本案件目录的路径；不复制外部入口来凑目录。 -->

## 实际结果与证据映射

<!-- TODO：先记录意见类型，按主文件规则形成开场候选；结果支持的解释单独记录，不默认作为首句。再记录实际数值、来源文件/字段、生成代码、证据映射及必要边界。复用既往证据时保留真实来源；没有经验性结果时说明依据。 -->

## Word 更新记录

<!-- TODO：记录阶段（回复/正文同步）、目标块、备份归属与路径、当前 Word 路径及回读/视觉 QA 结论。分别记录回复、正文落实和修改区同步状态；待落实的正文改动写清内容、位置、重叠关系。正文编辑可预写完成时态，但实验/分析/证明须实际完成。所有相关内容一致后才标记可提交。用户明确要求额外产物时，将案件内相对路径和请求依据写入 approved_artifacts；不得自行授权例外。 -->
'''
        # All inputs and optional revision probes have succeeded before mutation.
        case_dir.mkdir(parents=True, exist_ok=False)
        plan = case_dir / 'response-plan.md'
        created = False
        try:
            with plan.open('x', encoding='utf-8') as stream:
                created = True
                stream.write(content)
        except OSError:
            if created:
                plan.unlink(missing_ok=True)
            try:
                case_dir.rmdir()
            except OSError:
                pass
            raise
        print(case_dir)
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    raise SystemExit(main())
