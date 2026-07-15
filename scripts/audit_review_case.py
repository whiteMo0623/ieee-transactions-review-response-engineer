#!/usr/bin/env python3
"""Audit the structural and provenance completeness of a review case."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PLAN_FILES = (
    "case.json",
    "inputs/original-comment.md",
    "notes/paper-understanding.md",
    "notes/code-paper-map.md",
    "analysis-and-experiment-plan.md",
)
RESULT_DIRS = (
    "experiments/src",
    "experiments/configs",
    "experiments/logs",
    "experiments/raw",
    "experiments/processed",
)
FINAL_FILES = (
    "response/author-response.md",
    "response/evidence-ledger.json",
)


def load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid JSON {path}: {exc}")
        return None


def require_nonempty_files(root: Path, paths: tuple[str, ...], errors: list[str]) -> None:
    for relative in paths:
        path = root / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Missing or empty file: {relative}")


def require_nonempty_dirs(root: Path, paths: tuple[str, ...], errors: list[str]) -> None:
    for relative in paths:
        path = root / relative
        if not path.is_dir() or not any(item.is_file() for item in path.rglob("*")):
            errors.append(f"Missing or empty directory: {relative}")


def audit_plan(root: Path, errors: list[str]) -> None:
    require_nonempty_files(root, PLAN_FILES, errors)
    for relative in ("notes/paper-understanding.md", "notes/code-paper-map.md", "analysis-and-experiment-plan.md"):
        path = root / relative
        if path.is_file() and "TODO" in path.read_text(encoding="utf-8"):
            errors.append(f"Unresolved placeholder in: {relative}")
    case = load_json(root / "case.json", errors)
    if isinstance(case, dict):
        inputs = case.get("inputs", {})
        for key in ("paper_tex", "paper_pdf", "latex_root", "code_root", "comment_source"):
            if not inputs.get(key):
                errors.append(f"case.json lacks required input: {key}")
        if not isinstance(case.get("experiment_required"), bool):
            errors.append("case.json experiment_required must be true or false")


def audit_results(root: Path, errors: list[str]) -> None:
    case = load_json(root / "case.json", errors)
    if isinstance(case, dict) and case.get("experiment_required") is False:
        return
    require_nonempty_dirs(root, RESULT_DIRS, errors)
    manifest_path = root / "experiments/manifest.json"
    manifest = load_json(manifest_path, errors)
    if not isinstance(manifest, dict):
        return
    seeds = manifest.get("planned_seeds")
    planned_runs = manifest.get("planned_runs")
    runs = manifest.get("runs")
    if not isinstance(seeds, list) or not seeds:
        errors.append("experiments/manifest.json has no planned_seeds")
    if not isinstance(planned_runs, list) or not planned_runs:
        errors.append("experiments/manifest.json has no planned_runs")
    elif len(planned_runs) != len(set(planned_runs)):
        errors.append("experiments/manifest.json planned_runs contains duplicate IDs")
    if not isinstance(runs, list) or not runs:
        errors.append("experiments/manifest.json has no runs")
        return
    completed_seeds = set()
    completed_ids = set()
    required = {"id", "question_id", "status", "seed", "command", "config", "log", "raw_result", "exit_code"}
    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            errors.append(f"Run {index} is not an object")
            continue
        missing = sorted(required - run.keys())
        if missing:
            errors.append(f"Run {index} lacks fields: {', '.join(missing)}")
        if run.get("status") != "completed" or run.get("exit_code") != 0:
            errors.append(f"Run {run.get('id', index)} is not successfully completed")
        else:
            completed_seeds.add(run.get("seed"))
            completed_ids.add(run.get("id"))
        for field in ("config", "log", "raw_result"):
            value = run.get(field)
            if value and not (root / value).is_file():
                errors.append(f"Run {run.get('id', index)} references missing {field}: {value}")
    if isinstance(seeds, list) and not set(seeds).issubset(completed_seeds):
        errors.append("Not every planned seed has at least one completed run")
    if isinstance(planned_runs, list) and not set(planned_runs).issubset(completed_ids):
        errors.append("Not every planned run ID is successfully completed")


def audit_final(root: Path, require_docx: bool, errors: list[str]) -> None:
    require_nonempty_files(root, FINAL_FILES, errors)
    ledger = load_json(root / "response/evidence-ledger.json", errors)
    if not isinstance(ledger, list) or not ledger:
        errors.append("response/evidence-ledger.json has no evidence entries")
    else:
        seen_ids = set()
        for index, entry in enumerate(ledger):
            if not isinstance(entry, dict):
                errors.append(f"Evidence entry {index} is not an object")
                continue
            missing = sorted({"id", "claim", "source"} - entry.keys())
            if missing:
                errors.append(f"Evidence entry {index} lacks fields: {', '.join(missing)}")
            evidence_id = entry.get("id")
            if evidence_id in seen_ids:
                errors.append(f"Duplicate evidence ID: {evidence_id}")
            seen_ids.add(evidence_id)
            source = entry.get("source")
            if source and not (root / source).is_file():
                errors.append(f"Evidence entry {evidence_id or index} references missing source: {source}")
    figures = root / "experiments/figures"
    if figures.is_dir() and any(figures.iterdir()):
        if not any(path.suffix.lower() in {".pdf", ".eps", ".svg"} for path in figures.iterdir()):
            errors.append("Figures exist but no vector figure is present")
        if not any(path.suffix.lower() == ".png" for path in figures.iterdir()):
            errors.append("Figures exist but no PNG preview is present")
    if require_docx:
        delivery = root / "delivery"
        if not delivery.is_dir() or not any(delivery.glob("*.docx")):
            errors.append("No filled DOCX found in delivery/")
        if not any(path.is_file() for path in delivery.rglob("*.png")) and not any(delivery.glob("*.pdf")):
            errors.append("No rendered DOCX preview found in delivery/")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_dir")
    parser.add_argument("--stage", choices=("plan", "results", "final"), default="final")
    parser.add_argument("--require-docx", action="store_true")
    args = parser.parse_args()
    root = Path(args.case_dir).expanduser().resolve(strict=True)
    errors: list[str] = []
    audit_plan(root, errors)
    if args.stage in {"results", "final"}:
        audit_results(root, errors)
    if args.stage == "final":
        audit_final(root, args.require_docx, errors)
    if errors:
        print("AUDIT FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"AUDIT PASSED: {args.stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
