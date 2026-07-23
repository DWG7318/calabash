from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_version_consistency():
    version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    assert version == '2.2.0'
    assert '2.2.0' in (ROOT / 'README.md').read_text(encoding='utf-8')
    assert '2.2.0' in (ROOT / 'calabash/SKILL.md').read_text(encoding='utf-8')


def test_minimum_exact_definition():
    text = (ROOT / 'calabash/SKILL.md').read_text(encoding='utf-8')
    assert 'Grandpa\n→ Product Architecture\n→ Ontology' in text


def test_dynamic_not_fixed_questionnaire():
    text = (ROOT / 'calabash/SKILL.md').read_text(encoding='utf-8')
    assert 'No fixed questionnaire' in text
    assert 'question count' in text


def test_living_tracks_git_and_mandatory_desktop_bi():
    text = (ROOT / 'calabash/SKILL.md').read_text(encoding='utf-8')
    for token in [
        'UI Reality Track',
        'Core Workflow Reality Track',
        'Git Governance',
        'CALABASH_BI_BOOTSTRAP_PASS',
        'BI_VISIBILITY_DEGRADED',
        'BI_CHANGE_EVENT',
        'Current definition',
        'Latest changes',
    ]:
        assert token in text


def test_loop_names():
    text = (ROOT / 'calabash/references/loop-method-integration.md').read_text(encoding='utf-8')
    assert 'SLK' in text and 'CLK' in text and 'GLK' in text
    assert 'MSLK` is the legacy name' in text


def test_markdown_under_1000_lines():
    for path in ROOT.rglob('*.md'):
        assert len(path.read_text(encoding='utf-8').splitlines()) <= 1000, path


def test_all_json_parses():
    for path in ROOT.rglob('*.json'):
        json.loads(path.read_text(encoding='utf-8'))
