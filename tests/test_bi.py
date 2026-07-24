from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'calabash/scripts/build_calabash_bi.py'
spec = importlib.util.spec_from_file_location('calabash_bi', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_summary_and_desktop_html():
    project = ROOT / 'calabash/examples/living-project'
    summary = mod.build_summary(project)
    assert summary['project_name'] == 'Demo Living Calabash'
    assert summary['completeness']['required_claims'] == 3
    assert summary['completeness']['resolved_required_claims'] == 2
    assert summary['questions']['open'] == 1
    assert summary['living_tracks']['ui_open'] == 1
    assert summary['living_tracks']['workflow_open'] == 1
    assert summary['amendments']['total'] == 1
    assert len(summary['baseline_history']) == 3
    assert summary['changes']['explicit_feed'] is True
    assert summary['changes']['total'] >= 6
    assert summary['changes']['recent'][0]['change_type'] == 'BOOTSTRAP'
    assert summary['state_hash'].startswith('sha256:')
    assert 'current_definition' in summary

    dashboard = mod.build_html(summary)
    assert 'Calabash Definition Window' in dashboard
    assert 'Current definition' in dashboard
    assert 'Latest changes' in dashboard
    assert 'UI Reality' in dashboard
    assert '/api/summary' in dashboard
    assert summary['state_hash'] in dashboard


def test_state_hash_ignores_generated_outputs(tmp_path):
    project = ROOT / 'calabash/examples/living-project'
    first, count = mod.compute_state_hash(project)
    summary_path = project / '.calabash/bi/summary.json'
    original = summary_path.read_text(encoding='utf-8')
    try:
        summary_path.write_text(json.dumps({'temporary': True}), encoding='utf-8')
        second, count2 = mod.compute_state_hash(project)
    finally:
        summary_path.write_text(original, encoding='utf-8')
    assert first == second
    assert count == count2
