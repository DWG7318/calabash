#!/usr/bin/env python3
"""Bootstrap, diagnose, and serve the project-local Calabash Definition Window.

The service is deliberately local-only and read-only. Authoritative state remains
under .calabash/ and Git; this process only derives and presents BI outputs.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.parse
import webbrowser
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_calabash_bi import build_summary, compute_state_hash, write_outputs  # noqa: E402


DEFAULT_CONFIG: dict[str, Any] = {
    "project_name": "",
    "max_source_age_days": 180,
    "severity_weights": {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4},
    "desktop": {
        "enabled": True,
        "mode": "COMPACT_WINDOW",
        "host": "127.0.0.1",
        "port": 8765,
        "refresh_seconds": 5,
        "latest_change_count": 12,
        "start_with_project": True,
        "startup_policy": "PROJECT_START",
        "visibility_gate": "REQUIRED_WHILE_ACTIVE",
        "open_on_start": True,
        "prefer_app_window": True,
        "always_on_top": False,
        "window_width": 540,
        "window_height": 760,
        "install_desktop_shortcut": False,
        "headless_reason": None,
    },
    "full_dashboard": {
        "enabled": True,
        "output_path": ".calabash/bi/dashboard.html",
        "compact_output_path": ".calabash/bi/compact.html",
        "auto_rebuild": True,
        "auto_refresh_seconds": 10,
    },
    "commit_generated_assets": True,
}

CONTROL_DIRS = [
    "baseline",
    "sources",
    "themes",
    "questions",
    "decisions",
    "observations/ui",
    "observations/workflow",
    "reviews",
    "amendments",
    "traces/go",
    "traces/edge",
    "bi/runtime",
    "bi/snapshots",
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _deep_defaults(target: dict[str, Any], defaults: dict[str, Any]) -> dict[str, Any]:
    for key, value in defaults.items():
        if key not in target:
            target[key] = json.loads(json.dumps(value))
        elif isinstance(value, dict) and isinstance(target.get(key), dict):
            _deep_defaults(target[key], value)
    return target


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


def _ensure_tree(project: Path) -> None:
    croot = project / ".calabash"
    for rel in CONTROL_DIRS:
        (croot / rel).mkdir(parents=True, exist_ok=True)
    runtime_ignore = croot / "bi/runtime/.gitignore"
    if not runtime_ignore.exists():
        runtime_ignore.write_text("*\n!.gitignore\n", encoding="utf-8")


def _launcher_texts(project: Path, skill_root: Path) -> dict[str, str]:
    runner = skill_root / "scripts/run_calabash_bi_desktop.py"
    project_s = str(project)
    runner_s = str(runner)
    return {
        "launch-calabash-bi.sh": (
            "#!/usr/bin/env sh\n"
            f'exec "${{PYTHON:-python3}}" "{runner_s}" --project "{project_s}" "$@"\n'
        ),
        "launch-calabash-bi.command": (
            "#!/usr/bin/env sh\n"
            'cd "$(dirname "$0")"\n'
            f'exec "${{PYTHON:-python3}}" "{runner_s}" --project "{project_s}" "$@"\n'
        ),
        "launch-calabash-bi.ps1": (
            "$python = if ($env:PYTHON) { $env:PYTHON } else { 'python' }\n"
            f'& $python "{runner_s}" --project "{project_s}" @args\n'
            "exit $LASTEXITCODE\n"
        ),
        "launch-calabash-bi.cmd": (
            "@echo off\r\n"
            "if \"%PYTHON%\"==\"\" (set PYTHON=python)\r\n"
            f'\"%PYTHON%\" \"{runner_s}\" --project \"{project_s}\" %*\r\n'
        ),
    }


def _create_launchers(project: Path, skill_root: Path) -> list[Path]:
    folder = project / ".calabash/bi"
    folder.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for name, text in _launcher_texts(project, skill_root).items():
        path = folder / name
        path.write_text(text, encoding="utf-8", newline="")
        if path.suffix in {".sh", ".command"}:
            path.chmod(path.stat().st_mode | 0o111)
        paths.append(path)
    return paths


def _append_bootstrap_event(project: Path) -> None:
    feed = project / ".calabash/bi/change-feed.jsonl"
    if feed.exists() and feed.read_text(encoding="utf-8").strip():
        return
    now = datetime.now(timezone.utc)
    event = {
        "event_id": "CHG-" + now.strftime("%Y%m%d-%H%M%S-%f") + "-BOOTSTRAP",
        "timestamp": now.isoformat(),
        "change_type": "BOOTSTRAP",
        "summary": "Calabash desktop definition window initialized",
        "reason": "Current accepted definition and latest semantic changes must remain visible during project work",
        "status": "ACCEPTED",
        "affected_parts": ["Calabash BI"],
        "affected_artifacts": [
            "bi/config.json",
            "bi/bootstrap.json",
            "bi/change-feed.jsonl",
            "bi/compact.html",
            "bi/dashboard.html",
        ],
        "impact": ["Calabash state becomes continuously observable"],
        "before_refs": [],
        "after_refs": ["CALABASH_BI_BOOTSTRAP_PASS"],
        "source_refs": [],
        "decision_refs": [],
        "record_ids": [],
        "actor": "Calabash Builder",
        "git_commit": _git_head(project),
        "baseline_version": None,
        "baseline_from": None,
        "baseline_to": None,
    }
    feed.parent.mkdir(parents=True, exist_ok=True)
    feed.write_text(json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8")


def bootstrap_project(
    project: str | Path,
    project_name: str,
    headless: bool = False,
    *,
    skill_root: str | Path | None = None,
    port: int | None = None,
    refresh_seconds: int | None = None,
) -> dict[str, str]:
    """Create the BI control surface at project initiation.

    The function is idempotent for existing config and semantic data. Generated
    views, launchers, and the receipt are refreshed to match the current project.
    """
    project = Path(project).resolve()
    project.mkdir(parents=True, exist_ok=True)
    _ensure_tree(project)
    croot = project / ".calabash"
    bi = croot / "bi"
    skill_root_path = Path(skill_root).resolve() if skill_root else SCRIPT_DIR.parent

    config_path = bi / "config.json"
    config = _read_json(config_path, {}) or {}
    _deep_defaults(config, DEFAULT_CONFIG)
    config["project_name"] = project_name
    if port is not None:
        config["desktop"]["port"] = int(port)
    if refresh_seconds is not None:
        config["desktop"]["refresh_seconds"] = int(refresh_seconds)
    if headless:
        config["desktop"].update(
            {
                "mode": "HEADLESS_PUBLISHED",
                "startup_policy": "HEADLESS_PUBLISHED",
                "visibility_gate": "HEADLESS_PUBLISHED",
                "open_on_start": False,
                "headless_reason": config["desktop"].get("headless_reason")
                or "Desktop presentation is unavailable in this environment",
            }
        )
    _write_json(config_path, config)

    _append_bootstrap_event(project)
    launchers = _create_launchers(project, skill_root_path)

    # The receipt is excluded from the semantic state fingerprint, avoiding a
    # self-referential hash while keeping it as a durable governance record.
    outputs = write_outputs(project)
    summary = build_summary(project)
    receipt_path = bi / "bootstrap.json"
    receipt = {
        "bootstrap_id": "BI-BOOTSTRAP-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        "project_name": project_name,
        "project_root": str(project),
        "created_at": _utc_now(),
        "status": "CALABASH_BI_BOOTSTRAP_PASS",
        "presentation_mode": config["desktop"]["mode"],
        "config_path": str(config_path.relative_to(project)),
        "summary_path": str(outputs["summary"].relative_to(project)),
        "compact_path": str(outputs["compact"].relative_to(project)),
        "dashboard_path": str(outputs["dashboard"].relative_to(project)),
        "change_feed_path": str((bi / "change-feed.jsonl").relative_to(project)),
        "launchers": [str(path.relative_to(project)) for path in launchers],
        "local_only": True,
        "read_only": True,
        "refresh_seconds": int(config["desktop"]["refresh_seconds"]),
        "visibility_gate": config["desktop"]["visibility_gate"],
        "state_hash": summary["state_hash"],
        "headless_reason": config["desktop"].get("headless_reason"),
        "git_commit": _git_head(project),
    }
    _write_json(receipt_path, receipt)
    outputs = write_outputs(project)
    summary = build_summary(project)
    receipt["state_hash"] = summary["state_hash"]
    _write_json(receipt_path, receipt)
    write_outputs(project)

    return {
        "project": str(project),
        "config": str(config_path),
        "receipt": str(receipt_path),
        "summary": str(outputs["summary"]),
        "compact": str(outputs["compact"]),
        "dashboard": str(outputs["dashboard"]),
        "launcher": str(launchers[0]),
    }


def doctor_project(project: str | Path) -> list[str]:
    project = Path(project).resolve()
    bi = project / ".calabash/bi"
    failures: list[str] = []
    required = [
        "config.json",
        "bootstrap.json",
        "change-feed.jsonl",
        "summary.json",
        "compact.html",
        "dashboard.html",
        "launch-calabash-bi.sh",
        "launch-calabash-bi.command",
        "launch-calabash-bi.ps1",
        "launch-calabash-bi.cmd",
    ]
    for rel in required:
        if not (bi / rel).exists():
            failures.append(f"BI_REQUIRED_ARTIFACT_MISSING: {bi / rel}")
    if failures:
        return failures

    try:
        config = _read_json(bi / "config.json", {})
        receipt = _read_json(bi / "bootstrap.json", {})
        summary = _read_json(bi / "summary.json", {})
    except (OSError, json.JSONDecodeError) as exc:
        return [f"BI_RECORD_INVALID: {exc}"]

    desktop = config.get("desktop", {})
    if desktop.get("host") != "127.0.0.1":
        failures.append("BI_NETWORK_BOUNDARY_INVALID: host must be 127.0.0.1")
    if receipt.get("local_only") is not True or receipt.get("read_only") is not True:
        failures.append("BI_RECEIPT_BOUNDARY_INVALID: local_only/read_only must be true")
    if receipt.get("status") != "CALABASH_BI_BOOTSTRAP_PASS":
        failures.append("BI_BOOTSTRAP_RECEIPT_INVALID")

    current_hash, _ = compute_state_hash(project)
    if summary.get("state_hash") != current_hash:
        failures.append(
            f"BI_SUMMARY_STALE: summary={summary.get('state_hash')} current={current_hash}"
        )
    for name in ("compact.html", "dashboard.html"):
        text = (bi / name).read_text(encoding="utf-8")
        if current_hash not in text:
            failures.append(f"BI_VIEW_STALE: {name} does not contain current state hash")
    return failures


def _find_app_browser() -> str | None:
    candidates = [
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        "microsoft-edge",
        "microsoft-edge-stable",
        "chrome",
    ]
    for name in candidates:
        found = shutil.which(name)
        if found:
            return found
    platform_paths = [
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
        Path(os.environ.get("PROGRAMFILES", "")) / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Microsoft/Edge/Application/msedge.exe",
    ]
    for path in platform_paths:
        if path.is_file():
            return str(path)
    return None


def _open_definition_window(url: str, config: dict[str, Any]) -> None:
    desktop = config.get("desktop", {})
    if not desktop.get("open_on_start", True):
        return
    if desktop.get("prefer_app_window", True):
        browser = _find_app_browser()
        if browser:
            width = int(desktop.get("window_width", 540))
            height = int(desktop.get("window_height", 760))
            try:
                subprocess.Popen(
                    [browser, f"--app={url}", f"--window-size={width},{height}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return
            except OSError:
                pass
    webbrowser.open(url, new=1)


def _find_available_port(host: str, preferred: int) -> int:
    for port in range(preferred, preferred + 25):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
            except OSError:
                continue
            return port
    raise OSError(f"no available BI port in {preferred}-{preferred + 24}")


class _BIState:
    def __init__(self, project: Path, refresh_seconds: int):
        self.project = project
        self.bi = project / ".calabash/bi"
        self.refresh_seconds = refresh_seconds
        self.lock = threading.Lock()
        self.stop = threading.Event()
        self.last_hash: str | None = None
        self.last_error: str | None = None
        self.last_built_at: str | None = None

    def rebuild_if_needed(self, force: bool = False) -> None:
        with self.lock:
            try:
                current, _ = compute_state_hash(self.project)
                if force or current != self.last_hash:
                    write_outputs(self.project)
                    summary = _read_json(self.bi / "summary.json", {})
                    self.last_hash = summary.get("state_hash")
                    self.last_built_at = _utc_now()
                self.last_error = None
            except Exception as exc:  # keep service observable instead of dying silently
                self.last_error = f"{type(exc).__name__}: {exc}"
            self._write_health()

    def _write_health(self) -> None:
        health = {
            "status": "CURRENT" if not self.last_error else "ERROR",
            "project_root": str(self.project),
            "checked_at": _utc_now(),
            "state_hash": self.last_hash,
            "last_built_at": self.last_built_at,
            "error": self.last_error,
            "local_only": True,
            "read_only": True,
        }
        _write_json(self.bi / "runtime/health.json", health)

    def polling_loop(self) -> None:
        while not self.stop.wait(self.refresh_seconds):
            self.rebuild_if_needed()


class _Handler(BaseHTTPRequestHandler):
    state: _BIState

    def _send_bytes(self, payload: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self' 'unsafe-inline'; connect-src 'self'")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    def _send_file(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self._send_bytes(b"not found", "text/plain; charset=utf-8", HTTPStatus.NOT_FOUND)
            return
        self._send_bytes(path.read_bytes(), content_type)

    def do_GET(self) -> None:  # noqa: N802
        self.state.rebuild_if_needed()
        path = urllib.parse.urlparse(self.path).path
        if path in {"/", "/compact.html"}:
            self._send_file(self.state.bi / "compact.html", "text/html; charset=utf-8")
        elif path == "/dashboard.html":
            self._send_file(self.state.bi / "dashboard.html", "text/html; charset=utf-8")
        elif path == "/api/summary":
            self._send_file(self.state.bi / "summary.json", "application/json; charset=utf-8")
        elif path == "/api/health":
            self._send_file(self.state.bi / "runtime/health.json", "application/json; charset=utf-8")
        else:
            self._send_bytes(b"not found", "text/plain; charset=utf-8", HTTPStatus.NOT_FOUND)

    def do_HEAD(self) -> None:  # noqa: N802
        self.do_GET()

    def do_POST(self) -> None:  # noqa: N802
        self._send_bytes(b"read-only", "text/plain; charset=utf-8", HTTPStatus.METHOD_NOT_ALLOWED)

    def do_PUT(self) -> None:  # noqa: N802
        self.do_POST()

    def do_DELETE(self) -> None:  # noqa: N802
        self.do_POST()

    def log_message(self, fmt: str, *args: Any) -> None:
        if os.environ.get("CALABASH_BI_VERBOSE"):
            super().log_message(fmt, *args)


def headless_once(project: str | Path) -> dict[str, Any]:
    project = Path(project).resolve()
    write_outputs(project)
    summary = _read_json(project / ".calabash/bi/summary.json", {})
    payload = {
        "status": "CALABASH_BI_LIVE",
        "checked_at": _utc_now(),
        "state_hash": summary.get("state_hash"),
        "project_root": str(project),
        "local_only": True,
        "read_only": True,
    }
    _write_json(project / ".calabash/bi/runtime/state.json", payload)
    return payload


def serve_project(project: str | Path, *, no_open: bool = False) -> int:
    project = Path(project).resolve()
    failures = doctor_project(project)
    stale_only = all("STALE" in item for item in failures) if failures else False
    if failures and not stale_only:
        raise RuntimeError("; ".join(failures))
    if stale_only:
        write_outputs(project)

    config = _read_json(project / ".calabash/bi/config.json", {})
    desktop = config.get("desktop", {})
    host = desktop.get("host", "127.0.0.1")
    if host != "127.0.0.1":
        raise ValueError("Calabash BI must bind to 127.0.0.1")
    port = _find_available_port(host, int(desktop.get("port", 8765)))
    refresh = int(desktop.get("refresh_seconds", 5))
    state = _BIState(project, refresh)
    state.rebuild_if_needed(force=True)

    handler = type("CalabashBIHandler", (_Handler,), {"state": state})
    server = ThreadingHTTPServer((host, port), handler)
    server.daemon_threads = True
    poller = threading.Thread(target=state.polling_loop, name="calabash-bi-refresh", daemon=True)
    poller.start()

    compact_url = f"http://{host}:{port}/"
    dashboard_url = f"http://{host}:{port}/dashboard.html"
    runtime = {
        "status": "RUNNING",
        "started_at": _utc_now(),
        "host": host,
        "port": port,
        "compact_url": compact_url,
        "dashboard_url": dashboard_url,
        "pid": os.getpid(),
        "local_only": True,
        "read_only": True,
    }
    _write_json(project / ".calabash/bi/runtime/server.json", runtime)
    if not no_open:
        _open_definition_window(compact_url, config)
    print(f"CALABASH_BI_RUNNING {compact_url}")
    print(f"FULL_DASHBOARD {dashboard_url}")
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        state.stop.set()
        server.server_close()
        runtime.update({"status": "STOPPED", "stopped_at": _utc_now()})
        _write_json(project / ".calabash/bi/runtime/server.json", runtime)
    return 0


def install_shortcut(project: str | Path, target: str | Path | None = None) -> Path:
    project = Path(project).resolve()
    launcher = project / ".calabash/bi/launch-calabash-bi.sh"
    if not launcher.exists():
        raise FileNotFoundError("bootstrap BI before installing a shortcut")
    if target is None:
        desktop = Path.home() / "Desktop"
        target_path = desktop / f"Calabash BI - {project.name}.desktop"
    else:
        target_path = Path(target).expanduser().resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        "[Desktop Entry]\n"
        "Type=Application\n"
        f"Name=Calabash BI - {project.name}\n"
        f"Exec={launcher}\n"
        "Terminal=false\n"
        "Categories=Development;ProjectManagement;\n"
    )
    target_path.write_text(text, encoding="utf-8")
    target_path.chmod(target_path.stat().st_mode | 0o111)
    return target_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_boot = sub.add_parser("bootstrap")
    p_boot.add_argument("--project", required=True)
    p_boot.add_argument("--project-name", required=True)
    p_boot.add_argument("--headless", action="store_true")
    p_boot.add_argument("--skill-root")
    p_boot.add_argument("--port", type=int)
    p_boot.add_argument("--refresh-seconds", type=int)

    p_build = sub.add_parser("build")
    p_build.add_argument("--project", required=True)

    p_doctor = sub.add_parser("doctor")
    p_doctor.add_argument("--project", required=True)

    p_serve = sub.add_parser("serve")
    p_serve.add_argument("--project", required=True)
    p_serve.add_argument("--no-open", action="store_true")
    p_serve.add_argument("--headless-once", action="store_true")

    p_shortcut = sub.add_parser("install-shortcut")
    p_shortcut.add_argument("--project", required=True)
    p_shortcut.add_argument("--target")

    args = parser.parse_args()
    try:
        if args.command == "bootstrap":
            result = bootstrap_project(
                args.project,
                args.project_name,
                args.headless,
                skill_root=args.skill_root,
                port=args.port,
                refresh_seconds=args.refresh_seconds,
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print("CALABASH_BI_BOOTSTRAP_PASS")
            return 0
        if args.command == "build":
            paths = write_outputs(args.project)
            print(json.dumps({k: str(v) for k, v in paths.items()}, indent=2))
            return 0
        if args.command == "doctor":
            failures = doctor_project(args.project)
            if failures:
                print("\n".join(failures))
                return 1
            print("CALABASH_BI_CURRENT")
            return 0
        if args.command == "serve":
            if args.headless_once:
                print(json.dumps(headless_once(args.project), ensure_ascii=False))
                return 0
            return serve_project(args.project, no_open=args.no_open)
        if args.command == "install-shortcut":
            path = install_shortcut(args.project, args.target)
            print(path)
            return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"CALABASH_BI_BLOCKED: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
