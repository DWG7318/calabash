from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "calabash/scripts/validate_calabash_project.py"
spec = importlib.util.spec_from_file_location("calabash_validator", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_example_cross_file_invariants():
    failures = mod.validate_project(
        ROOT / "calabash/examples/living-project",
        ROOT / "calabash",
    )
    assert failures == []
