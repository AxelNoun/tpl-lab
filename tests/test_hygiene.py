"""Repo hygiene regressions — files CLAUDE.md cites must exist."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_license_exists():
    assert (ROOT / "LICENSE").is_file()


def test_onboarding_resources_exists():
    assert (ROOT / "docs" / "onboarding" / "RESSOURCES.md").is_file()


def test_package_version():
    import tpl

    assert tpl.__version__ == "0.1.0"
