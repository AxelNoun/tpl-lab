"""Frozen prereg hashes must match git at 0a5e794. No network."""

from tpl.io.osf_deposit import (
    FROZEN_COMMIT,
    FROZEN_SHA256,
    manifest,
    snapshot,
    upload,
)
import pytest


def test_snapshot_matches_pinned_hashes():
    snap = snapshot()
    assert set(snap) == set(FROZEN_SHA256)
    for path, rec in snap.items():
        assert rec["sha256"] == FROZEN_SHA256[path]
        assert rec["nbytes"] == len(rec["bytes"])


def test_manifest_points_at_the_freeze_not_head():
    man = manifest()
    assert man["commit"] == FROZEN_COMMIT
    assert man["tag"] == "prereg-v1"
    assert "0a5e794" in man["github"]


def test_upload_refuses_an_empty_token():
    with pytest.raises(ValueError, match="OSF_TOKEN"):
        upload("")


def test_write_bundle_matches_git(tmp_path):
    from tpl.io.osf_deposit import write_bundle

    meta = write_bundle(tmp_path)
    assert (tmp_path / "manifest.json").is_file()
    assert (tmp_path / "PREREGISTRATION.md").is_file()
    assert meta["commit"].startswith("0a5e794")
