#!/usr/bin/env python3
"""Run the persistent compact Calabash BI desktop surface."""
from __future__ import annotations

import argparse
import json
import os
import time
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

from build_calabash_bi import build_summary, source_fingerprint, write_outputs


def _read_config(project: Path) -> dict:
    path = project / ".calabash/bi/config.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _write_runtime(project: Path, status: str, mode: str, fingerprint: str | None, error: str | None = None) -> None:
    path = project / ".calabash/bi/runtime/state.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": status,
        "mode": mode,
        "pid": os.getpid(),
        "last_refresh_at": datetime.now(timezone.utc).isoformat(),
        "source_fingerprint": fingerprint,
        "error": error,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _compact_lines(summary: dict) -> tuple[str, str, str, list[str], str]:
    baseline = summary.get("baseline", {})
    definition = summary.get("current_definition", {})
    product = definition.get("product_architecture", {})
    ontology = definition.get("ontology", {})
    git = summary.get("git", {})
    identity = (
        f"{summary.get('overall_status')} · {baseline.get('mode','DRAFT')} "
        f"v{baseline.get('version','—')} · {git.get('branch') or 'no-git'}"
    )
    purpose = definition.get("grandpa", {}).get("purpose", "Definition not yet established")
    product_text = (
        f"Roles: {' · '.join(map(str, product.get('roles', []))) or '—'}\n"
        f"Journey: {' → '.join(map(str, product.get('journeys', []))) or '—'}\n"
        f"Ontology: {' · '.join(map(str, ontology.get('concepts', []))) or '—'}"
    )
    latest = [
        f"{x.get('timestamp','')} · {x.get('change_type','')} · {x.get('status','')}\n{x.get('summary','')}"
        for x in summary.get("changes", {}).get("recent", [])
    ]
    q = summary.get("questions", {})
    lt = summary.get("living_tracks", {})
    review = summary.get("review", {})
    attention = (
        f"{q.get('blocking',0)} blocking · {lt.get('ui_open',0)} UI drift · "
        f"{lt.get('workflow_open',0)} Workflow drift · review {review.get('next_review_due') or '—'}"
    )
    return identity, purpose, product_text, latest, attention


def _browser_loop(project: Path, interval: int, open_once: bool = True) -> int:
    compact = project / ".calabash/bi/compact.html"
    last = None
    if open_once:
        write_outputs(project)
        webbrowser.open(compact.as_uri())
    try:
        while True:
            current = source_fingerprint(project)
            if current != last:
                try:
                    write_outputs(project)
                    _write_runtime(project, "CALABASH_BI_LIVE", "BROWSER_COMPACT", current)
                    last = current
                except Exception as exc:
                    _write_runtime(project, "CALABASH_BI_ERROR", "BROWSER_COMPACT", current, str(exc))
            time.sleep(interval)
    except KeyboardInterrupt:
        _write_runtime(project, "CALABASH_BI_STOPPED", "BROWSER_COMPACT", last)
        return 0


def _tk_loop(project: Path, config: dict) -> int:
    try:
        import tkinter as tk
        from tkinter import ttk
    except Exception:
        return _browser_loop(project, int(config.get("desktop", {}).get("refresh_seconds", 5)))

    desktop = config.get("desktop", {})
    interval = int(desktop.get("refresh_seconds", 5))
    width = int(desktop.get("window_width", 540))
    height = int(desktop.get("window_height", 760))
    last = {"fingerprint": None}

    try:
        root = tk.Tk()
    except Exception:
        return _browser_loop(project, interval)
    root.title(f"Calabash BI — {config.get('project_name', project.name)}")
    root.geometry(f"{width}x{height}")
    with_topmost = bool(desktop.get("always_on_top", False))
    if with_topmost:
        root.attributes("-topmost", True)

    outer = ttk.Frame(root, padding=14)
    outer.pack(fill="both", expand=True)
    ttk.Label(outer, text=f"Calabash — {config.get('project_name', project.name)}", font=("TkDefaultFont", 15, "bold")).pack(anchor="w")
    identity_var = tk.StringVar(); ttk.Label(outer, textvariable=identity_var).pack(anchor="w", pady=(2, 10))
    ttk.Label(outer, text="GRANDPA", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
    purpose_var = tk.StringVar(); ttk.Label(outer, textvariable=purpose_var, wraplength=width-40, justify="left").pack(anchor="w", pady=(2, 10))
    ttk.Label(outer, text="PRODUCT", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
    product_var = tk.StringVar(); ttk.Label(outer, textvariable=product_var, wraplength=width-40, justify="left").pack(anchor="w", pady=(2, 10))
    ttk.Label(outer, text="LATEST CHANGES", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
    changes_box = tk.Text(outer, height=15, wrap="word", state="disabled", relief="flat", background=root.cget("bg"))
    changes_box.pack(fill="both", expand=True, pady=(2, 10))
    ttk.Label(outer, text="ATTENTION", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
    attention_var = tk.StringVar(); ttk.Label(outer, textvariable=attention_var, wraplength=width-40, justify="left").pack(anchor="w", pady=(2, 8))
    freshness_var = tk.StringVar(); ttk.Label(outer, textvariable=freshness_var).pack(anchor="w")
    buttons = ttk.Frame(outer); buttons.pack(fill="x", pady=(10, 0))

    def open_full() -> None:
        webbrowser.open((project / ".calabash/bi/dashboard.html").as_uri())

    def render(force: bool = False) -> None:
        current = source_fingerprint(project)
        if force or current != last["fingerprint"]:
            try:
                write_outputs(project)
                summary = build_summary(project)
                identity, purpose, product, latest, attention = _compact_lines(summary)
                identity_var.set(identity); purpose_var.set(purpose); product_var.set(product); attention_var.set(attention)
                changes_box.configure(state="normal"); changes_box.delete("1.0", "end")
                changes_box.insert("1.0", "\n\n".join(latest) if latest else "No changes recorded yet")
                changes_box.configure(state="disabled")
                freshness_var.set(f"Updated {summary.get('generated_at')} · CALABASH_BI_LIVE")
                last["fingerprint"] = current
                _write_runtime(project, "CALABASH_BI_LIVE", "COMPACT_WINDOW", current)
            except Exception as exc:
                freshness_var.set(f"CALABASH_BI_ERROR · {exc}")
                _write_runtime(project, "CALABASH_BI_ERROR", "COMPACT_WINDOW", current, str(exc))
        root.after(interval * 1000, render)

    ttk.Button(buttons, text="Refresh", command=lambda: render(True)).pack(side="left")
    ttk.Button(buttons, text="Open Full BI", command=open_full).pack(side="right")

    def close() -> None:
        _write_runtime(project, "CALABASH_BI_STOPPED", "COMPACT_WINDOW", last["fingerprint"])
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", close)
    render(True)
    root.mainloop()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--headless-once", action="store_true")
    args = parser.parse_args()
    project = Path(args.project).resolve()
    config = _read_config(project)
    interval = int(config.get("desktop", {}).get("refresh_seconds", 5))
    if args.headless_once:
        outputs = write_outputs(project)
        summary = build_summary(project)
        _write_runtime(project, "CALABASH_BI_LIVE", "HEADLESS_ONCE", summary.get("state_hash"))
        print(json.dumps({
            "status": "CALABASH_BI_LIVE",
            "project_name": summary.get("project_name"),
            "overall_status": summary.get("overall_status"),
            "state_hash": summary.get("state_hash"),
            "outputs": {k: str(v) for k, v in outputs.items()},
        }, indent=2, ensure_ascii=False))
        return 0
    if args.headless:
        return _browser_loop(project, interval, open_once=False)
    mode = config.get("desktop", {}).get("mode")
    if args.browser or mode == "BROWSER_COMPACT":
        return _browser_loop(project, interval)
    if mode == "HEADLESS_PUBLISHED":
        return _browser_loop(project, interval, open_once=False)
    return _tk_loop(project, config)


if __name__ == "__main__":
    raise SystemExit(main())
