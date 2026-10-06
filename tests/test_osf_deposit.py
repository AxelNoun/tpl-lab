"""Frozen prereg hashes must match git at 0a5e794. No network."""

import subprocess

from tpl.io.osf_deposit import (
    FROZEN_COMMIT,
    FROZEN_SHA256,
    manifest,
    snapshot,
    upload,
)
import pytest


def _frozen_commit_available():
    """True if FROZEN_COMMIT is in the git repository of the current directory.

    osf_deposit reads the frozen files with `git show` from the current
    directory, so the check runs there too. It is false in a shallow clone
    (CI checkout at depth 1), in a release zip/tarball (no .git), or when git
    is not installed.
    """
    try:
        subprocess.run(
            ["git", "cat-file", "-e", f"{FROZEN_COMMIT}^{{commit}}"],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return False
    return True


# Skip rather than fail: the hashes cannot be checked without the commit, and a
# missing commit says nothing about whether they match. Run from a full clone
# (`git fetch --unshallow` in a shallow one) to exercise these tests.
requires_frozen_commit = pytest.mark.skipif(
    not _frozen_commit_available(),
    reason=(
        f"frozen commit {FROZEN_COMMIT[:7]} (prereg-v1) is not in this checkout "
        "(shallow clone or release archive); clone the full history to run"
    ),
)


@requires_frozen_commit
def test_snapshot_matches_pinned_hashes():
    snap = snapshot()
    assert set(snap) == set(FROZEN_SHA256)
    for path, rec in snap.items():
        assert rec["sha256"] == FROZEN_SHA256[path]
        assert rec["nbytes"] == len(rec["bytes"])


@requires_frozen_commit
def test_manifest_points_at_the_freeze_not_head():
    man = manifest()
    assert man["commit"] == FROZEN_COMMIT
    assert man["tag"] == "prereg-v1"
    assert "0a5e794" in man["github"]


def test_upload_refuses_an_empty_token():
    with pytest.raises(ValueError, match="OSF_TOKEN"):
        upload("")


@requires_frozen_commit
def test_write_bundle_matches_git(tmp_path):
    from tpl.io.osf_deposit import write_bundle

    meta = write_bundle(tmp_path)
    assert (tmp_path / "manifest.json").is_file()
    assert (tmp_path / "PREREGISTRATION.md").is_file()
    assert meta["commit"].startswith("0a5e794")
