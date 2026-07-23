from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / 'calabash/scripts/bootstrap_calabash_bi.py'
RUNTIME = ROOT / 'calabash/scripts/run_calabash_bi_desktop.py'


def test_bootstrap_and_headless_runtime(tmp_path):
    project = tmp_path / 'project'
    project.mkdir()
    result = subprocess.run(
        [
            sys.executable,
            str(BOOTSTRAP),
            '--project',
            str(project),
            '--project-name',
            'Temporary Calabash',
            '--skill-root',
            str(ROOT / 'calabash'),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert 'CALABASH_BI_BOOTSTRAP_PASS' in result.stdout
    assert (project / '.calabash/bi/config.json').exists()
    assert (project / '.calabash/bi/bootstrap.json').exists()
    assert (project / '.calabash/bi/change-feed.jsonl').exists()
    assert (project / '.calabash/bi/compact.html').exists()
    assert (project / '.calabash/bi/dashboard.html').exists()
    assert (project / '.calabash/bi/launch-calabash-bi.sh').exists()

    config = json.loads((project / '.calabash/bi/config.json').read_text())
    assert config['desktop']['mode'] == 'COMPACT_WINDOW'
    assert config['desktop']['visibility_gate'] == 'REQUIRED_WHILE_ACTIVE'

    runtime = subprocess.run(
        [sys.executable, str(RUNTIME), '--project', str(project), '--headless-once'],
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(runtime.stdout)
    assert payload['status'] == 'CALABASH_BI_LIVE'
    assert (project / '.calabash/bi/runtime/state.json').exists()


def test_core_bootstrap_doctor_and_stale_detection(tmp_path):
    import importlib.util
    core_path = ROOT / 'calabash/scripts/calabash_bi_desktop.py'
    spec = importlib.util.spec_from_file_location('calabash_bi_desktop_core', core_path)
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)
    project = tmp_path / 'core-project'
    project.mkdir()
    result = core.bootstrap_project(project, 'Core Project', False, skill_root=ROOT / 'calabash')
    assert Path(result['compact']).exists()
    assert Path(result['dashboard']).exists()
    assert core.doctor_project(project) == []
    (project / '.calabash/themes').mkdir(parents=True, exist_ok=True)
    (project / '.calabash/themes/untracked-note.txt').write_text('semantic draft', encoding='utf-8')
    assert any('BI_SUMMARY_STALE' in item for item in core.doctor_project(project))


def test_semantic_change_write_through(tmp_path):
    project = tmp_path / 'change-project'
    project.mkdir()
    subprocess.run(
        [
            sys.executable,
            str(BOOTSTRAP),
            '--project',
            str(project),
            '--project-name',
            'Change Project',
            '--skill-root',
            str(ROOT / 'calabash'),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    recorder = ROOT / 'calabash/scripts/record_calabash_bi_change.py'
    subprocess.run(
        [
            sys.executable,
            str(recorder),
            '--project',
            str(project),
            '--type',
            'OWNER_DECISION',
            '--summary',
            'Owner selected guided first use.',
            '--reason',
            'Historical evidence left two materially different product outcomes.',
            '--status',
            'PROVISIONAL',
            '--part',
            'Product Architecture',
            '--record-id',
            'DEC-001',
            '--actor',
            'Owner',
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    lines = [json.loads(line) for line in (project / '.calabash/bi/change-feed.jsonl').read_text().splitlines() if line.strip()]
    assert lines[-1]['change_type'] == 'OWNER_DECISION'
    assert lines[-1]['status'] == 'PROVISIONAL'
    compact = (project / '.calabash/bi/compact.html').read_text(encoding='utf-8')
    assert 'Owner selected guided first use.' in compact
