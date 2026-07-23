#!/usr/bin/env python3
"""Append one semantic Calabash change event and refresh the BI views."""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from build_calabash_bi import write_outputs

CHANGE_TYPES = [
    "BOOTSTRAP", "BI", "SOURCE", "THEME", "QUESTION", "OWNER_DECISION",
    "BASELINE", "AMENDMENT", "UI_SIGNAL", "WORKFLOW_SIGNAL", "REVIEW",
    "TRACE", "LOOP_ADOPTION", "RUNTIME",
]
STATUSES = [
    "DRAFT", "OBSERVED", "PROVISIONAL", "EXPERIMENTAL", "ACCEPTED",
    "BLOCKED", "SUPERSEDED", "REJECTED", "RESOLVED",
]


def _git_head(project: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(project), "rev-parse", "HEAD"],
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def append_change(
    project: str | Path,
    change_type: str,
    summary: str,
    reason: str,
    affected_parts: list[str],
    affected_artifacts: list[str],
    impact: list[str],
    record_ids: list[str],
    status: str,
    actor: str | None,
    git_commit: str | None = None,
) -> dict:
    project = Path(project).resolve()
    feed = project / ".calabash/bi/change-feed.jsonl"
    feed.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    event = {
        "event_id": "CHG-" + now.strftime("%Y%m%d-%H%M%S-%f"),
        "timestamp": now.isoformat(),
        "change_type": change_type,
        "summary": summary,
        "reason": reason,
        "status": status,
        "affected_parts": affected_parts,
        "affected_artifacts": affected_artifacts,
        "impact": impact,
        "before_refs": [],
        "after_refs": record_ids,
        "source_refs": [],
        "decision_refs": [],
        "record_ids": record_ids,
        "actor": actor,
        "git_commit": git_commit or _git_head(project),
        "baseline_version": None,
        "baseline_from": None,
        "baseline_to": None,
    }
    with feed.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    write_outputs(project)
    return event


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--type", required=True, dest="change_type", choices=CHANGE_TYPES)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--status", choices=STATUSES, default="ACCEPTED")
    parser.add_argument("--part", action="append", default=[])
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--impact", action="append", default=[])
    parser.add_argument("--record-id", action="append", default=[])
    parser.add_argument("--actor")
    parser.add_argument("--git-commit")
    args = parser.parse_args()
    event = append_change(
        args.project,
        args.change_type,
        args.summary,
        args.reason,
        args.part,
        args.artifact,
        args.impact,
        args.record_id,
        args.status,
        args.actor,
        args.git_commit,
    )
    print(json.dumps(event, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
