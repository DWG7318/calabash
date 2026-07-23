#!/usr/bin/env python3
"""Validate a project-local Calabash tree against bundled JSON schemas."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator, FormatChecker

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from build_calabash_bi import compute_state_hash

SINGLE_FILES = {
    "baseline/manifest.json": "project-calabash-baseline.schema.json",
    "baseline/freeze.json": "baseline-freeze.schema.json",
    "sources/register.json": "source-register.schema.json",
    "sources/preparation-pass.json": "source-preparation-pass.schema.json",
    "themes/map.json": "theme-map.schema.json",
    "bi/config.json": "bi-config.schema.json",
    "bi/bootstrap.json": "bi-bootstrap.schema.json",
}

GLOB_FILES = {
    "questions/*.json": "question-card.schema.json",
    "observations/ui/*.json": "observation.schema.json",
    "observations/workflow/*.json": "observation.schema.json",
    "reviews/*.json": "review-record.schema.json",
    "amendments/*.json": "amendment-record.schema.json",
    "traces/go/*.json": "go-calabash-trace.schema.json",
    "traces/edge/*.json": "edge-authority-trace.schema.json",
}

JSONL_FILES = {
    "decisions/ledger.jsonl": "decision-event.schema.json",
    "bi/change-feed.jsonl": "bi-change-event.schema.json",
}


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _errors(instance, schema) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [e.message for e in sorted(validator.iter_errors(instance), key=lambda e: list(e.path))]


def _validate_json(path: Path, schema_path: Path) -> list[str]:
    return [f"{path}: {m}" for m in _errors(_load(path), _load(schema_path))]


def _validate_jsonl(path: Path, schema_path: Path) -> list[str]:
    schema = _load(schema_path)
    failures: list[str] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            failures.append(f"{path}:{line_no}: {exc}")
            continue
        failures.extend(f"{path}:{line_no}: {m}" for m in _errors(item, schema))
    return failures


def validate_project(project: str | Path, skill_root: str | Path) -> list[str]:
    project = Path(project).resolve()
    croot = project / ".calabash"
    schemas = Path(skill_root).resolve() / "contracts"
    failures: list[str] = []

    if not croot.exists():
        return [f"missing {croot}"]

    for rel in [
        "bi/summary.json",
        "bi/compact.html",
        "bi/dashboard.html",
        "bi/launch-calabash-bi.sh",
        "bi/launch-calabash-bi.command",
        "bi/launch-calabash-bi.ps1",
        "bi/launch-calabash-bi.cmd",
    ]:
        if not (croot / rel).exists():
            failures.append(f"missing {croot / rel}")

    for rel, schema_name in SINGLE_FILES.items():
        path = croot / rel
        if not path.exists():
            failures.append(f"missing {path}")
        else:
            failures.extend(_validate_json(path, schemas / schema_name))

    for pattern, schema_name in GLOB_FILES.items():
        for path in sorted(croot.glob(pattern)):
            failures.extend(_validate_json(path, schemas / schema_name))

    for rel, schema_name in JSONL_FILES.items():
        path = croot / rel
        if not path.exists():
            failures.append(f"missing {path}")
        else:
            failures.extend(_validate_jsonl(path, schemas / schema_name))

    # Parse append-only ledgers that currently have no dedicated schema.
    claims: list[dict] = []
    baseline_history: list[dict] = []
    for rel, sink in (("sources/claims.jsonl", claims), ("baseline/history.jsonl", baseline_history)):
        path = croot / rel
        if path.exists():
            for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    sink.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    failures.append(f"{path}:{line_no}: {exc}")

    # Cross-file reference checks.
    source_data = _load(croot / "sources/register.json") if (croot / "sources/register.json").exists() else {"sources": []}
    source_ids = {s.get("source_id") for s in source_data.get("sources", [])}
    question_rows = [_load(p) for p in sorted((croot / "questions").glob("*.json"))]
    question_ids = {q.get("question_id") for q in question_rows}
    decisions = []
    dpath = croot / "decisions/ledger.jsonl"
    if dpath.exists():
        for line in dpath.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    decisions.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    decision_ids = {d.get("decision_id") for d in decisions}

    for q in question_rows:
        missing = set(q.get("source_references", [])) - source_ids
        if missing:
            failures.append(f"question {q.get('question_id')} references missing sources: {sorted(missing)}")

    for d in decisions:
        if d.get("question_id") not in question_ids:
            failures.append(f"decision {d.get('decision_id')} references missing question {d.get('question_id')}")

    theme_path = croot / "themes/map.json"
    if theme_path.exists():
        for theme in _load(theme_path).get("themes", []):
            missing_q = set(theme.get("question_ids", [])) - question_ids
            if missing_q:
                failures.append(f"theme {theme.get('theme_id')} references missing questions: {sorted(missing_q)}")
            for claim in theme.get("claims", []):
                missing_s = set(claim.get("source_ids", [])) - source_ids
                missing_d = set(claim.get("decision_ids", [])) - decision_ids
                if missing_s:
                    failures.append(f"theme claim {claim.get('claim_id')} references missing sources: {sorted(missing_s)}")
                if missing_d:
                    failures.append(f"theme claim {claim.get('claim_id')} references missing decisions: {sorted(missing_d)}")

    baseline_path = croot / "baseline/manifest.json"
    if baseline_path.exists():
        baseline = _load(baseline_path)
        missing_sources = set(baseline.get("source_snapshot", [])) - source_ids
        if missing_sources:
            failures.append(f"baseline references missing sources: {sorted(missing_sources)}")
        head = baseline.get("decision_ledger_head")
        if head and head not in decision_ids:
            failures.append(f"baseline decision_ledger_head missing: {head}")

    summary_path = croot / "bi/summary.json"
    if summary_path.exists():
        summary = _load(summary_path)
        if not summary.get("state_hash"):
            failures.append("BI summary missing state_hash")
        if "current_definition" not in summary:
            failures.append("BI summary missing current_definition")
        if "changes" not in summary:
            failures.append("BI summary missing changes")
        current_hash, _ = compute_state_hash(project)
        if summary.get("state_hash") != current_hash:
            failures.append(f"BI summary stale: {summary.get('state_hash')} != {current_hash}")
        for rel in ("bi/compact.html", "bi/dashboard.html"):
            view_path = croot / rel
            if view_path.exists() and current_hash not in view_path.read_text(encoding="utf-8"):
                failures.append(f"BI view stale: {view_path}")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    failures = validate_project(args.project, args.skill_root)
    if failures:
        print("\n".join(failures))
        return 1
    print("CALABASH_PROJECT_VALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())
