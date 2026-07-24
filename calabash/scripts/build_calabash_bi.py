#!/usr/bin/env python3
"""Build a reproducible Calabash BI summary and desktop-friendly HTML dashboard."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

RESOLVED_CLAIM_STATES = {"SUPPORTED", "DECIDED"}
CLOSED_QUESTION_STATES = {"ANSWERED", "RETIRED", "SUPERSEDED"}
CLOSED_SIGNAL_STATES = {"DISMISSED", "AMENDED", "RESOLVED", "SUPERSEDED"}
STALE_TRACE_STATES = {"STALE", "INVALID", "SUPERSEDED"}
HIGH_SEVERITIES = {"HIGH", "CRITICAL"}
GENERATED_BI_PATHS = {
    "bi/summary.json",
    "bi/dashboard.html",
    "bi/compact.html",
    "bi/runtime/state.json",
    "bi/bootstrap.json",
}


def _read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: {exc}") from exc
    return rows


def _glob_json(folder: Path) -> list[dict[str, Any]]:
    if not folder.exists():
        return []
    return [_read_json(p, {}) for p in sorted(folder.glob("*.json"))]


def _percent(numerator: int, denominator: int) -> float:
    return round((numerator / denominator * 100.0), 1) if denominator else 100.0


def _is_overdue(raw: str | None) -> bool:
    if not raw:
        return False
    try:
        due = date.fromisoformat(raw[:10])
    except ValueError:
        return False
    return due < datetime.now(timezone.utc).date()


def _theme_rows(theme_map: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for theme in theme_map.get("themes", []):
        claims = theme.get("claims", [])
        required = [c for c in claims if c.get("required", False)]
        resolved = [c for c in required if c.get("status") in RESOLVED_CLAIM_STATES]
        blocked = [c for c in required if c.get("status") == "BLOCKED"]
        monitoring = [c for c in claims if c.get("status") == "MONITORING"]
        rows.append(
            {
                "theme_id": theme.get("theme_id", ""),
                "title": theme.get("title", ""),
                "status": theme.get("status", "OPEN"),
                "criticality": theme.get("criticality", "MEDIUM"),
                "required": len(required),
                "resolved": len(resolved),
                "blocked": len(blocked),
                "monitoring": len(monitoring),
                "completeness": _percent(len(resolved), len(required)),
            }
        )
    return rows


def _governed_files(croot: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(croot.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(croot).as_posix()
        if rel in GENERATED_BI_PATHS or rel.startswith("bi/runtime/"):
            continue
        files.append(path)
    return files


def compute_state_hash(project: str | Path) -> tuple[str, int]:
    project_root = Path(project).resolve()
    croot = project_root / ".calabash"
    digest = hashlib.sha256()
    files = _governed_files(croot)
    for path in files:
        rel = path.relative_to(croot).as_posix().encode("utf-8")
        digest.update(len(rel).to_bytes(4, "big"))
        digest.update(rel)
        data = path.read_bytes()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return f"sha256:{digest.hexdigest()}", len(files)


def source_fingerprint(project: str | Path) -> str:
    """Return the current governed Calabash source fingerprint."""
    return compute_state_hash(project)[0]


def _git_state(project_root: Path) -> dict[str, Any]:
    def run(*args: str) -> str | None:
        try:
            result = subprocess.run(
                ["git", "-C", str(project_root), *args],
                check=True,
                text=True,
                capture_output=True,
                timeout=5,
            )
            return result.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return None

    head = run("rev-parse", "HEAD")
    branch = run("rev-parse", "--abbrev-ref", "HEAD")
    status = run("status", "--porcelain", "--", ".calabash")
    return {
        "head": head,
        "branch": branch,
        "calabash_dirty": bool(status),
        "changed_paths": status.splitlines() if status else [],
    }


def _derive_changes(
    decisions: list[dict[str, Any]],
    amendments: list[dict[str, Any]],
    reviews: list[dict[str, Any]],
    ui_signals: list[dict[str, Any]],
    workflow_signals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Fallback for 2.1 projects without an explicit semantic change feed."""
    rows: list[dict[str, Any]] = []
    for d in decisions:
        rows.append(
            {
                "event_id": f"DERIVED-{d.get('decision_id', 'DECISION')}",
                "timestamp": d.get("timestamp", ""),
                "change_type": "OWNER_DECISION",
                "summary": d.get("normalized_claim", "Owner decision"),
                "reason": "Derived from the decision ledger",
                "affected_parts": d.get("affected_parts", []),
                "impact": d.get("impact", []),
                "status": d.get("decision_status", "ACCEPTED"),
                "git_commit": d.get("git_commit"),
                "actor": d.get("actor", "Owner"),
                "derived": True,
            }
        )
    for a in amendments:
        rows.append(
            {
                "event_id": f"DERIVED-{a.get('amendment_id', 'AMENDMENT')}",
                "timestamp": a.get("created_at", ""),
                "change_type": "AMENDMENT",
                "summary": a.get("summary", "Calabash amendment"),
                "reason": a.get("reason", "Derived from amendment record"),
                "affected_parts": a.get("affected_parts", []),
                "impact": a.get("impact", []),
                "status": a.get("status", "PROVISIONAL"),
                "git_commit": a.get("git_commit"),
                "actor": a.get("created_by", "Calabash Builder"),
                "derived": True,
            }
        )
    for r in reviews:
        rows.append(
            {
                "event_id": f"DERIVED-{r.get('review_id', 'REVIEW')}",
                "timestamp": r.get("reviewed_at", ""),
                "change_type": "REVIEW",
                "summary": f"Review verdict: {r.get('verdict', 'UNKNOWN')}",
                "reason": r.get("trigger", "Review"),
                "affected_parts": r.get("scope", []),
                "impact": r.get("actions", []),
                "status": "ACCEPTED",
                "git_commit": r.get("git_commit"),
                "actor": "Calabash Reviewer",
                "derived": True,
            }
        )
    for signal, kind in [(x, "UI_SIGNAL") for x in ui_signals] + [
        (x, "WORKFLOW_SIGNAL") for x in workflow_signals
    ]:
        rows.append(
            {
                "event_id": f"DERIVED-{signal.get('signal_id', kind)}",
                "timestamp": signal.get("observed_at", ""),
                "change_type": kind,
                "summary": signal.get("summary", kind),
                "reason": "Derived from living-track observation",
                "affected_parts": signal.get("affected_parts", []),
                "impact": signal.get("impact", []),
                "status": "PROVISIONAL" if signal.get("status") not in CLOSED_SIGNAL_STATES else "RESOLVED",
                "git_commit": signal.get("git_commit"),
                "actor": signal.get("observed_by", "Observer"),
                "derived": True,
            }
        )
    return rows


def _current_definition(baseline: dict[str, Any]) -> dict[str, Any]:
    architecture = baseline.get("product_architecture", {})
    ontology = baseline.get("ontology", {})
    full_layers = baseline.get("full_layers", {})
    return {
        "grandpa": baseline.get("grandpa", {}),
        "product_architecture": {
            "roles": architecture.get("roles", []),
            "entry_points": architecture.get("entry_points", architecture.get("entries", [])),
            "journeys": architecture.get("journeys", []),
            "modules": architecture.get("modules", []),
            "outcomes": architecture.get("outcomes", []),
        },
        "ontology": {
            "concepts": ontology.get("concepts", []),
            "relationships": ontology.get("relationships", []),
            "states": ontology.get("states", []),
            "open_conflicts": ontology.get("open_conflicts", []),
        },
        "full_layers": full_layers,
        "known_gaps": baseline.get("known_gaps", []),
        "upgrade_triggers": baseline.get("upgrade_triggers", []),
    }


def build_summary(project: str | Path) -> dict[str, Any]:
    """Build a machine-readable BI summary for a project-local .calabash tree."""
    project_root = Path(project).resolve()
    croot = project_root / ".calabash"
    if not croot.exists():
        raise FileNotFoundError(f"missing Calabash control tree: {croot}")

    baseline = _read_json(croot / "baseline/manifest.json", {})
    config = _read_json(croot / "bi/config.json", {})
    bootstrap = _read_json(croot / "bi/bootstrap.json", {})
    source_register = _read_json(croot / "sources/register.json", {"sources": []})
    contradictions_data = _read_json(croot / "sources/contradictions.json", {"contradictions": []})
    theme_map = _read_json(croot / "themes/map.json", {"themes": []})
    questions = _glob_json(croot / "questions")
    decisions = _read_jsonl(croot / "decisions/ledger.jsonl")
    amendments = _glob_json(croot / "amendments")
    baseline_history = _read_jsonl(croot / "baseline/history.jsonl")
    ui_signals = _glob_json(croot / "observations/ui")
    workflow_signals = _glob_json(croot / "observations/workflow")
    reviews = _glob_json(croot / "reviews")
    go_traces = _glob_json(croot / "traces/go")
    edge_traces = _glob_json(croot / "traces/edge")
    explicit_changes = _read_jsonl(croot / "bi/change-feed.jsonl")

    themes = _theme_rows(theme_map)
    required_claims = sum(t["required"] for t in themes)
    resolved_required = sum(t["resolved"] for t in themes)
    blocked_required = sum(t["blocked"] for t in themes)
    monitoring_claims = sum(t["monitoring"] for t in themes)

    sources = source_register.get("sources", [])
    verified_sources = sum(1 for s in sources if s.get("verified") is True)
    stale_sources = sum(1 for s in sources if s.get("freshness_status") == "STALE")

    open_questions = [q for q in questions if q.get("status") not in CLOSED_QUESTION_STATES]
    theme_by_id = {t.get("theme_id"): t for t in theme_map.get("themes", [])}
    blocking_questions = sum(
        1 for q in open_questions if theme_by_id.get(q.get("theme_id"), {}).get("blocking") is True
    )

    contradictions = contradictions_data.get("contradictions", [])
    open_contradictions = sum(
        1 for c in contradictions if c.get("status") not in {"RESOLVED", "DISMISSED", "SUPERSEDED"}
    )

    open_ui = [s for s in ui_signals if s.get("status") not in CLOSED_SIGNAL_STATES]
    open_workflow = [s for s in workflow_signals if s.get("status") not in CLOSED_SIGNAL_STATES]

    latest_review = max(reviews, key=lambda r: r.get("reviewed_at", ""), default={})
    next_review_due = (
        latest_review.get("next_review_due")
        or baseline.get("review_policy", {}).get("next_review_due")
        or ""
    )
    overdue = _is_overdue(next_review_due)

    go_stale = sum(1 for t in go_traces if t.get("status") in STALE_TRACE_STATES)
    edge_stale = sum(1 for t in edge_traces if t.get("status") in STALE_TRACE_STATES)

    changes = explicit_changes or _derive_changes(decisions, amendments, reviews, ui_signals, workflow_signals)
    changes = sorted(changes, key=lambda x: x.get("timestamp", ""), reverse=True)
    change_limit = int(config.get("desktop", {}).get("latest_change_count", 6))
    recent_changes = changes[:change_limit]

    state_hash, source_file_count = compute_state_hash(project_root)
    git_state = _git_state(project_root)

    if blocking_questions or blocked_required:
        overall_status = "BLOCKED"
    elif baseline.get("status") != "FROZEN":
        overall_status = "DRAFT"
    elif overdue:
        overall_status = "REVIEW_DUE"
    elif (
        open_contradictions
        or any(s.get("severity") in HIGH_SEVERITIES for s in open_ui + open_workflow)
        or go_stale
        or edge_stale
    ):
        overall_status = "AT_RISK"
    else:
        overall_status = "CURRENT"

    provisional_decisions = [
        d for d in decisions
        if d.get("decision_status") in {"PROVISIONAL", "EXPERIMENTAL"}
    ]
    pending_amendments = [
        a for a in amendments
        if a.get("status") not in {"ACCEPTED", "REJECTED", "SUPERSEDED"}
    ]

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "state_hash": state_hash,
        "source_file_count": source_file_count,
        "project_root": str(project_root),
        "project_name": config.get("project_name", baseline.get("baseline_id", project_root.name)),
        "overall_status": overall_status,
        "baseline": baseline,
        "current_definition": _current_definition(baseline),
        "bi": {
            "bootstrap_status": bootstrap.get("status"),
            "presentation_mode": bootstrap.get("presentation_mode", config.get("desktop", {}).get("mode")),
            "start_with_project": config.get("desktop", {}).get("start_with_project", True),
            "refresh_seconds": config.get("desktop", {}).get("refresh_seconds", 5),
            "latest_change_count": change_limit,
            "local_only": True,
            "read_only": True,
        },
        "git": git_state,
        "working_state": {
            "git_dirty": git_state.get("calabash_dirty", False),
            "changed_paths": git_state.get("changed_paths", []),
            "provisional_decisions": len(provisional_decisions),
            "pending_amendments": len(pending_amendments),
            "open_ui_signals": len(open_ui),
            "open_workflow_signals": len(open_workflow),
            "authority_note": "Accepted baseline is authoritative; working changes remain non-authoritative until accepted and versioned.",
        },
        "completeness": {
            "required_claims": required_claims,
            "resolved_required_claims": resolved_required,
            "blocked_required_claims": blocked_required,
            "monitoring_claims": monitoring_claims,
            "percent": _percent(resolved_required, required_claims),
        },
        "sources": {
            "total": len(sources),
            "verified": verified_sources,
            "stale": stale_sources,
            "percent_verified": _percent(verified_sources, len(sources)),
        },
        "questions": {
            "total": len(questions),
            "open": len(open_questions),
            "blocking": blocking_questions,
            "answered": sum(1 for q in questions if q.get("status") == "ANSWERED"),
        },
        "decisions": {
            "total": len(decisions),
            "superseding": sum(1 for d in decisions if d.get("supersedes")),
            "provisional": sum(
                1 for d in decisions if d.get("decision_status") in {"PROVISIONAL", "EXPERIMENTAL"}
            ),
        },
        "contradictions": {"open": open_contradictions, "total": len(contradictions)},
        "living_tracks": {
            "ui_open": len(open_ui),
            "workflow_open": len(open_workflow),
            "ui_high": sum(1 for s in open_ui if s.get("severity") in HIGH_SEVERITIES),
            "workflow_high": sum(1 for s in open_workflow if s.get("severity") in HIGH_SEVERITIES),
        },
        "traces": {
            "go_total": len(go_traces),
            "go_stale": go_stale,
            "edge_total": len(edge_traces),
            "edge_stale": edge_stale,
        },
        "review": {
            "last_reviewed_at": latest_review.get("reviewed_at"),
            "next_review_due": next_review_due,
            "overdue": overdue,
            "count": len(reviews),
        },
        "amendments": {
            "total": len(amendments),
            "accepted": sum(1 for a in amendments if a.get("status") == "ACCEPTED"),
            "open": sum(1 for a in amendments if a.get("status") in {"PROPOSED", "REVIEWED"}),
            "records": sorted(amendments, key=lambda a: a.get("created_at", "")),
        },
        "changes": {
            "total": len(changes),
            "latest_at": recent_changes[0].get("timestamp") if recent_changes else None,
            "recent": recent_changes,
            "explicit_feed": bool(explicit_changes),
        },
        "baseline_history": baseline_history,
        "themes": themes,
        "open_questions": open_questions,
        "ui_signals": open_ui,
        "workflow_signals": open_workflow,
        "decision_timeline": sorted(decisions, key=lambda d: d.get("timestamp", ""), reverse=True),
    }
    return summary


def _escape(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def _list_text(values: Any) -> str:
    if isinstance(values, dict):
        return "; ".join(f"{k}: {v}" for k, v in values.items())
    if isinstance(values, list):
        return "; ".join(str(v) for v in values) if values else "—"
    return str(values) if values not in (None, "") else "—"


def _object_lines(value: Any) -> str:
    if not isinstance(value, dict) or not value:
        return "<p class='muted'>—</p>"
    rows = []
    for key, item in value.items():
        rows.append(f"<div class='kv'><span>{_escape(key.replace('_',' ').title())}</span><strong>{_escape(_list_text(item))}</strong></div>")
    return "".join(rows)


def build_html(summary: dict[str, Any]) -> str:
    b = summary.get("baseline", {})
    definition = summary.get("current_definition", {})
    c = summary.get("completeness", {})
    q = summary.get("questions", {})
    co = summary.get("contradictions", {})
    lt = summary.get("living_tracks", {})
    tr = summary.get("traces", {})
    rv = summary.get("review", {})
    changes = summary.get("changes", {}).get("recent", [])
    refresh_seconds = float(summary.get("bi", {}).get("refresh_seconds", 3))

    change_cards = "".join(
        f"""
        <article class='change'>
          <div class='change-head'><span class='type'>{_escape(x.get('change_type'))}</span><time>{_escape(x.get('timestamp'))}</time></div>
          <h4>{_escape(x.get('summary'))}</h4>
          <p>{_escape(x.get('reason'))}</p>
          <div class='tags'>{''.join(f"<span>{_escape(v)}</span>" for v in x.get('affected_parts', []))}</div>
          <details><summary>Impact and provenance</summary>
            <p><b>Impact:</b> {_escape(_list_text(x.get('impact', [])))}</p>
            <p><b>Status:</b> {_escape(x.get('status'))} · <b>Commit:</b> {_escape(x.get('git_commit') or 'pending')}</p>
            <p><b>Actor:</b> {_escape(x.get('actor'))}</p>
          </details>
        </article>"""
        for x in changes
    ) or "<p class='muted'>No semantic changes recorded yet.</p>"

    question_rows = "".join(
        f"<tr><td>{_escape(x.get('question_id'))}</td><td>{_escape(x.get('decision_claim'))}</td><td>{_escape(_list_text(x.get('recommended_option_ids', [])))}</td><td>{_escape(x.get('recommendation_confidence'))}</td></tr>"
        for x in summary.get("open_questions", [])
    ) or "<tr><td colspan='4'>No open Owner decisions</td></tr>"

    theme_rows = "".join(
        f"<tr><td>{_escape(x.get('theme_id'))}</td><td>{_escape(x.get('title'))}</td><td>{_escape(x.get('status'))}</td><td>{x.get('resolved',0)}/{x.get('required',0)}</td><td>{x.get('completeness',0)}%</td></tr>"
        for x in summary.get("themes", [])
    ) or "<tr><td colspan='5'>No themes</td></tr>"

    def signal_rows(rows: list[dict[str, Any]]) -> str:
        return "".join(
            f"<tr><td>{_escape(x.get('signal_id'))}</td><td>{_escape(x.get('severity'))}</td><td>{_escape(x.get('summary'))}</td><td>{_escape(_list_text(x.get('affected_parts', [])))}</td></tr>"
            for x in rows
        ) or "<tr><td colspan='4'>No open signals</td></tr>"

    full_layers = definition.get("full_layers", {})
    full_layer_html = _object_lines(full_layers) if full_layers else "<p class='muted'>Minimum Calabash — Full layers not frozen.</p>"

    return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<meta name='calabash-state-hash' content='{_escape(summary.get('state_hash'))}'>
<title>Calabash Definition Window — {_escape(summary.get('project_name'))}</title>
<style>
:root{{--bg:#f4f6f9;--panel:#fff;--ink:#1b2430;--muted:#697386;--line:#e4e8ef;--accent:#315efb;--danger:#b42318;--warn:#b54708;--ok:#027a48}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:13px/1.45 system-ui,-apple-system,Segoe UI,sans-serif}}
.top{{position:sticky;top:0;z-index:5;background:#101828;color:#fff;padding:12px 18px;box-shadow:0 2px 8px #0002}}
.top-row{{display:flex;gap:12px;align-items:center;flex-wrap:wrap}}h1{{font-size:17px;margin:0;flex:1}}.pill{{border:1px solid #ffffff35;border-radius:999px;padding:4px 8px;font-weight:700}}
.now{{display:grid;grid-template-columns:repeat(7,minmax(110px,1fr));gap:8px;margin-top:10px}}.metric{{background:#ffffff12;border-radius:8px;padding:7px 9px}}.metric b{{display:block;font-size:15px}}.metric span{{font-size:11px;color:#d0d5dd}}
.layout{{display:grid;grid-template-columns:minmax(320px,1.15fr) minmax(300px,.85fr);gap:14px;padding:14px}}
.panel{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px;box-shadow:0 1px 3px #1018280a}}h2{{font-size:15px;margin:0 0 12px}}h3{{font-size:13px;margin:14px 0 6px}}h4{{font-size:13px;margin:5px 0}}.muted{{color:var(--muted)}}
.definition-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}}.section{{border:1px solid var(--line);border-radius:9px;padding:10px}}.section.wide{{grid-column:1/-1}}
.kv{{display:grid;grid-template-columns:115px 1fr;gap:8px;padding:5px 0;border-bottom:1px dashed var(--line)}}.kv:last-child{{border:0}}.kv span{{color:var(--muted)}}
.changes{{display:flex;flex-direction:column;gap:8px;max-height:68vh;overflow:auto;padding-right:3px}}.change{{border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:9px;padding:9px;background:#fbfcfe}}.change-head{{display:flex;justify-content:space-between;gap:8px;color:var(--muted);font-size:11px}}.type{{font-weight:800;color:var(--accent)}}.change p{{margin:4px 0}}.tags{{display:flex;gap:5px;flex-wrap:wrap}}.tags span{{background:#eef2ff;padding:2px 6px;border-radius:999px;font-size:10px}}
.details{{grid-column:1/-1;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:7px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}th{{font-size:11px;color:var(--muted)}}details summary{{cursor:pointer;color:var(--accent)}}
.connection{{display:flex;align-items:center;gap:5px}}.dot{{width:8px;height:8px;border-radius:50%;background:#12b76a}}.dot.bad{{background:#f04438}}
footer{{padding:8px 16px 18px;color:var(--muted);font-size:11px}}
@media(max-width:900px){{.now{{grid-template-columns:repeat(3,1fr)}}.layout{{grid-template-columns:1fr}}.details{{grid-template-columns:1fr}}}}
@media(max-width:520px){{.now{{grid-template-columns:repeat(2,1fr)}}.definition-grid{{grid-template-columns:1fr}}.section.wide{{grid-column:auto}}}}
</style></head><body>
<header class='top'><div class='top-row'><h1>Calabash Definition Window — {_escape(summary.get('project_name'))}</h1><span class='pill'>{_escape(summary.get('overall_status'))}</span><span class='connection'><i id='dot' class='dot'></i><span id='connection'>current</span></span></div>
<div class='now'>
<div class='metric'><span>Baseline</span><b>{_escape(b.get('mode'))} v{_escape(b.get('version'))}</b></div>
<div class='metric'><span>Completeness</span><b>{c.get('percent',0)}%</b></div>
<div class='metric'><span>Blocking</span><b>{q.get('blocking',0)+c.get('blocked_required_claims',0)}</b></div>
<div class='metric'><span>Contradictions</span><b>{co.get('open',0)}</b></div>
<div class='metric'><span>UI / Workflow</span><b>{lt.get('ui_open',0)} / {lt.get('workflow_open',0)}</b></div>
<div class='metric'><span>Stale traces</span><b>{tr.get('go_stale',0)+tr.get('edge_stale',0)}</b></div>
<div class='metric'><span>Next review</span><b>{_escape(rv.get('next_review_due') or '—')}</b></div>
</div></header>
<main class='layout'>
<section class='panel'><h2>Current definition</h2><div class='definition-grid'>
<div class='section wide'><h3>Grandpa</h3>{_object_lines(definition.get('grandpa',{}))}</div>
<div class='section'><h3>Product Architecture</h3>{_object_lines(definition.get('product_architecture',{}))}</div>
<div class='section'><h3>Ontology</h3>{_object_lines(definition.get('ontology',{}))}</div>
<div class='section'><h3>Full Calabash coverage</h3>{full_layer_html}</div>
<div class='section'><h3>Known gaps and upgrade triggers</h3><p><b>Gaps:</b> {_escape(_list_text(definition.get('known_gaps',[])))}</p><p><b>Triggers:</b> {_escape(_list_text(definition.get('upgrade_triggers',[])))}</p></div>
</div></section>
<section class='panel'><h2>Latest changes</h2><div class='changes'>{change_cards}</div></section>
<div class='details'>
<section class='panel'><h2>Open Owner decisions</h2><table><thead><tr><th>ID</th><th>Decision</th><th>AI recommendation</th><th>Confidence</th></tr></thead><tbody>{question_rows}</tbody></table></section>
<section class='panel'><h2>Theme completeness</h2><table><thead><tr><th>ID</th><th>Theme</th><th>Status</th><th>Resolved</th><th>%</th></tr></thead><tbody>{theme_rows}</tbody></table></section>
<section class='panel'><h2>UI Reality</h2><table><thead><tr><th>ID</th><th>Severity</th><th>Finding</th><th>Affected</th></tr></thead><tbody>{signal_rows(summary.get('ui_signals', []))}</tbody></table></section>
<section class='panel'><h2>Core Workflow Reality</h2><table><thead><tr><th>ID</th><th>Severity</th><th>Finding</th><th>Affected</th></tr></thead><tbody>{signal_rows(summary.get('workflow_signals', []))}</tbody></table></section>
</div></main>
<footer>State {_escape(summary.get('state_hash'))} · generated {_escape(summary.get('generated_at'))} · Git {_escape(summary.get('git',{}).get('head') or 'unavailable')}</footer>
<script>
const initialHash={json.dumps(summary.get('state_hash'))};
const refreshMs={int(refresh_seconds*1000)};
async function refreshCheck(){{
  const dot=document.getElementById('dot'), label=document.getElementById('connection');
  if(location.protocol==='file:'){{label.textContent='static';setTimeout(()=>location.reload(),refreshMs);return;}}
  try{{const r=await fetch('/api/summary?ts='+Date.now(),{{cache:'no-store'}});if(!r.ok)throw new Error('status');const s=await r.json();dot.classList.remove('bad');label.textContent='current';if(s.state_hash!==initialHash)location.reload();}}
  catch(e){{dot.classList.add('bad');label.textContent='disconnected';}}
  setTimeout(refreshCheck,refreshMs);
}}
setTimeout(refreshCheck,refreshMs);
</script></body></html>"""


def build_compact_html(summary: dict[str, Any]) -> str:
    """Build the lightweight browser fallback for the persistent desktop view."""
    definition = summary.get("current_definition", {})
    product = definition.get("product_architecture", {})
    ontology = definition.get("ontology", {})
    b = summary.get("baseline", {})
    changes = summary.get("changes", {}).get("recent", [])
    cards = "".join(
        "<article class='change'>"
        f"<div class='meta'>{_escape(x.get('timestamp'))} · {_escape(x.get('change_type'))} · {_escape(x.get('status'))}</div>"
        f"<strong>{_escape(x.get('summary'))}</strong>"
        f"<p>{_escape(_list_text(x.get('affected_parts', [])))}</p>"
        "</article>"
        for x in changes
    ) or "<p class='muted'>No semantic changes recorded yet.</p>"
    q = summary.get("questions", {})
    lt = summary.get("living_tracks", {})
    rv = summary.get("review", {})
    git = summary.get("git", {})
    return f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<meta http-equiv='refresh' content='{int(summary.get('bi',{}).get('refresh_seconds',5))}'>
<title>Calabash Compact — {_escape(summary.get('project_name'))}</title><style>
body{{font:13px/1.45 system-ui,-apple-system,Segoe UI,sans-serif;margin:0;background:#f4f6f9;color:#1b2430}}header{{position:sticky;top:0;background:#101828;color:#fff;padding:14px 16px}}main{{padding:12px}}
.pill{{display:inline-block;border:1px solid #ffffff45;border-radius:999px;padding:3px 8px;margin-right:6px}}.card,.change{{background:#fff;border:1px solid #e4e8ef;border-radius:10px;padding:11px;margin-bottom:9px}}h1{{font-size:17px;margin:0 0 7px}}h2{{font-size:13px;margin:16px 0 7px}}p{{margin:5px 0}}.meta,.muted{{color:#697386;font-size:11px}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}.metric b{{font-size:20px;display:block}}
</style></head><body><header><h1>Calabash · {_escape(summary.get('project_name'))}</h1>
<span class='pill'>{_escape(summary.get('overall_status'))}</span><span class='pill'>{_escape(b.get('mode','DRAFT'))} v{_escape(b.get('version','—'))}</span>
<div class='meta' style='color:#d0d5dd;margin-top:6px'>{_escape(git.get('branch') or 'no-git')} · {_escape(git.get('head') or 'no-head')}</div></header><main>
<div class='grid'><section class='card metric'><b>{summary.get('completeness',{}).get('percent',0)}%</b>definition</section><section class='card metric'><b>{q.get('blocking',0)}</b>blocking</section><section class='card metric'><b>{lt.get('ui_open',0)}</b>UI signals</section><section class='card metric'><b>{lt.get('workflow_open',0)}</b>Workflow signals</section></div>
<h2>Current accepted definition</h2><section class='card'><strong>Grandpa</strong><p>{_escape(definition.get('grandpa',{}).get('purpose','Definition not yet established'))}</p>
<strong>Roles</strong><p>{_escape(_list_text(product.get('roles',[])))}</p><strong>Journey</strong><p>{_escape(' → '.join(map(str,product.get('journeys',[]))) or '—')}</p>
<strong>Ontology</strong><p>{_escape(_list_text(ontology.get('concepts',[])))}</p><strong>Known gaps</strong><p>{_escape(_list_text(definition.get('known_gaps',[])))}</p></section>
<h2>Latest semantic changes</h2>{cards}<h2>Working state</h2><section class='card'><p>Git draft: {_escape('yes' if summary.get('working_state',{}).get('git_dirty') else 'no')} · Provisional decisions: {summary.get('working_state',{}).get('provisional_decisions',0)} · Pending amendments: {summary.get('working_state',{}).get('pending_amendments',0)}</p><p class='muted'>Draft and observed changes are not part of the accepted baseline until versioned.</p></section><h2>Attention</h2><section class='card'><p>Open Owner decisions: {q.get('open',0)} · Next review: {_escape(rv.get('next_review_due') or '—')}</p></section>
<p class='muted'>State {_escape(summary.get('state_hash'))} · generated {_escape(summary.get('generated_at'))} · read-only</p></main></body></html>"""


def write_outputs(project: str | Path, summary: dict[str, Any] | None = None) -> dict[str, Path]:
    project_root = Path(project).resolve()
    summary = summary or build_summary(project_root)
    bi = project_root / ".calabash/bi"
    summary_path = bi / "summary.json"
    compact_path = bi / "compact.html"
    dashboard_path = bi / "dashboard.html"
    bi.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    compact_path.write_text(build_compact_html(summary), encoding="utf-8")
    dashboard_path.write_text(build_html(summary), encoding="utf-8")
    return {"summary": summary_path, "compact": compact_path, "dashboard": dashboard_path}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Project root containing .calabash/")
    parser.add_argument("--output", help="Full HTML output path; defaults to .calabash/bi/dashboard.html")
    parser.add_argument("--summary", help="JSON summary path; defaults to .calabash/bi/summary.json")
    parser.add_argument("--compact", help="Compact HTML output path; defaults to .calabash/bi/compact.html")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    summary = build_summary(project)
    if args.output or args.summary or args.compact:
        summary_path = Path(args.summary).resolve() if args.summary else project / ".calabash/bi/summary.json"
        output_path = Path(args.output).resolve() if args.output else project / ".calabash/bi/dashboard.html"
        compact_path = Path(args.compact).resolve() if args.compact else project / ".calabash/bi/compact.html"
        for path in (summary_path, output_path, compact_path):
            path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        output_path.write_text(build_html(summary), encoding="utf-8")
        compact_path.write_text(build_compact_html(summary), encoding="utf-8")
        paths = {"summary": summary_path, "compact": compact_path, "dashboard": output_path}
    else:
        paths = write_outputs(project, summary)
    for label, path in paths.items():
        print(f"Wrote {label}: {path}")
    print(f"State {summary['state_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
