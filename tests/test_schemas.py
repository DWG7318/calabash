from pathlib import Path
import json
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'calabash'
EX = SKILL / 'examples/living-project/.calabash'


def validate(data_path, schema_name):
    data = json.loads(data_path.read_text())
    schema = json.loads((SKILL / 'contracts' / schema_name).read_text())
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data))
    assert not errors, [e.message for e in errors]


def validate_jsonl(data_path, schema_name):
    schema = json.loads((SKILL / 'contracts' / schema_name).read_text())
    for line in data_path.read_text().splitlines():
        if line.strip():
            errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(json.loads(line)))
            assert not errors, [e.message for e in errors]


def test_core_examples():
    validate(EX / 'baseline/manifest.json', 'project-calabash-baseline.schema.json')
    validate(EX / 'sources/register.json', 'source-register.schema.json')
    validate(EX / 'themes/map.json', 'theme-map.schema.json')
    validate(EX / 'bi/config.json', 'bi-config.schema.json')
    validate(EX / 'bi/bootstrap.json', 'bi-bootstrap.schema.json')
    validate(EX / 'sources/preparation-pass.json', 'source-preparation-pass.schema.json')
    validate(EX / 'baseline/freeze.json', 'baseline-freeze.schema.json')


def test_questions():
    for path in (EX / 'questions').glob('*.json'):
        validate(path, 'question-card.schema.json')


def test_observations_reviews_amendments_and_traces():
    for path in (EX / 'observations/ui').glob('*.json'):
        validate(path, 'observation.schema.json')
    for path in (EX / 'observations/workflow').glob('*.json'):
        validate(path, 'observation.schema.json')
    for path in (EX / 'reviews').glob('*.json'):
        validate(path, 'review-record.schema.json')
    for path in (EX / 'amendments').glob('*.json'):
        validate(path, 'amendment-record.schema.json')
    for path in (EX / 'traces/go').glob('*.json'):
        validate(path, 'go-calabash-trace.schema.json')
    for path in (EX / 'traces/edge').glob('*.json'):
        validate(path, 'edge-authority-trace.schema.json')


def test_ledgers():
    validate_jsonl(EX / 'decisions/ledger.jsonl', 'decision-event.schema.json')
    validate_jsonl(EX / 'bi/change-feed.jsonl', 'bi-change-event.schema.json')
