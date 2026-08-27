"""OSF deposit of the frozen prereg-v1 commit. No thresholds are read here.

    python -m tpl.io.osf_deposit --manifest
    python -m tpl.io.osf_deposit --upload   # needs OSF_TOKEN

The files are taken from git commit FROZEN_COMMIT, never from the working
tree: PREREGISTRATION.md was later annotated with IBL/Claar notes.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

FROZEN_COMMIT = "0a5e794477c788f174f623465177b0ffee08c880"
FROZEN_TAG = "prereg-v1"
GITHUB_TREE = f"https://github.com/AxelNoun/tpl-lab/tree/{FROZEN_COMMIT}"
OSF_NODES = "https://api.osf.io/v2/nodes/"

# Paths as they existed at the freeze. Do not add post-tag files.
FROZEN_PATHS = (
    "PREREGISTRATION.md",
    "configs/prereg_v1.json",
    "src/tpl/analysis/run_id.py",
    "CLAUDE.md",
)

# sha256 of `git show FROZEN_COMMIT:path` — pin so a retag cannot silently drift.
FROZEN_SHA256 = {
    "PREREGISTRATION.md": "5758c0a0c8b5b4925b060a170a6c7d53ff940e649480dd2b292fb11d3779de8b",
    "configs/prereg_v1.json": "15cf7f2d0f0fe9c06b0b32b23ff6b9371bf80f334b7fffa8cf4c7119760bbd2a",
    "src/tpl/analysis/run_id.py": "a1f98e46c8426feaa648f4ccc9c01ba783b120f9d202c85464802bb64afee735",
    "CLAUDE.md": "59bb6b5cab6948554bb403539586942846698dea4c733b45186ee7cc66a3ee0e",
}


def _git_show(path, commit=FROZEN_COMMIT):
    return subprocess.check_output(["git", "show", f"{commit}:{path}"])


def snapshot(commit=FROZEN_COMMIT):
    """Bytes and sha256 of each frozen path, as stored in git."""
    out = {}
    for path in FROZEN_PATHS:
        raw = _git_show(path, commit=commit)
        digest = hashlib.sha256(raw).hexdigest()
        expected = FROZEN_SHA256[path]
        if digest != expected:
            raise ValueError(
                f"{path} at {commit} has sha256 {digest}, expected {expected}"
            )
        out[path] = {"sha256": digest, "nbytes": len(raw), "bytes": raw}
    return out


def manifest(commit=FROZEN_COMMIT):
    snap = snapshot(commit=commit)
    return {
        "tag": FROZEN_TAG,
        "commit": commit,
        "github": GITHUB_TREE,
        "note": (
            "This is the analysis plan frozen BEFORE real-data contact. "
            "Later commits annotate results; they are not the prereg."
        ),
        "files": {
            path: {"sha256": rec["sha256"], "nbytes": rec["nbytes"]}
            for path, rec in snap.items()
        },
    }


def write_bundle(dest, commit=FROZEN_COMMIT):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    snap = snapshot(commit=commit)
    meta = manifest(commit=commit)
    (dest / "manifest.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    for path, rec in snap.items():
        target = dest / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(rec["bytes"])
    return meta


def _request(
    url, token, method="GET", data=None, content_type="application/vnd.api+json"
):
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if data is not None:
        req.add_header("Content-Type", content_type)
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read()
        if not body:
            return {}
        return json.loads(body.decode("utf-8"))


def upload(token, commit=FROZEN_COMMIT):
    """Create a public OSF project and upload the frozen files.

    Returns the OSF HTML URL. Requires a personal access token with
    `osf.full_write` (https://osf.io/settings/tokens).
    """
    if not token:
        raise ValueError("OSF_TOKEN is empty")
    snap = snapshot(commit=commit)
    payload = json.dumps(
        {
            "data": {
                "type": "nodes",
                "attributes": {
                    "title": "TPL-Lab prereg-v1 (frozen analysis plan)",
                    "category": "project",
                    "description": (
                        f"Git tag {FROZEN_TAG} = commit {commit}. "
                        "TwoNN + named-S6 geometry of cortical spike-count vectors. "
                        "Plan frozen 20 Aug 2026, before real-data contact. "
                        f"Canonical copy: {GITHUB_TREE}"
                    ),
                    "public": True,
                },
            }
        }
    ).encode("utf-8")
    created = _request(OSF_NODES, token, method="POST", data=payload)
    node_id = created["data"]["id"]
    html = created["data"]["links"]["html"]
    files_link = created["data"]["relationships"]["files"]["links"]["related"]["href"]
    listing = _request(files_link, token)
    upload_url = listing["data"][0]["links"]["upload"]
    for path, rec in snap.items():
        name = path.replace("/", "__")
        dest = f"{upload_url}?kind=file&name={name}"
        _request(
            dest,
            token,
            method="PUT",
            data=rec["bytes"],
            content_type="application/octet-stream",
        )
    man = json.dumps(manifest(commit=commit), indent=2).encode("utf-8")
    _request(
        f"{upload_url}?kind=file&name=manifest.json",
        token,
        method="PUT",
        data=man,
        content_type="application/octet-stream",
    )
    return {"id": node_id, "html": html}


def main(argv=None):
    p = argparse.ArgumentParser(description="OSF deposit of prereg-v1")
    p.add_argument("--manifest", action="store_true")
    p.add_argument("--bundle", help="write frozen files to this directory")
    p.add_argument("--upload", action="store_true", help="needs OSF_TOKEN")
    p.add_argument("--seed", type=int, default=0)
    a = p.parse_args(argv)
    print(f"[seed={a.seed}] frozen {FROZEN_TAG} {FROZEN_COMMIT}")
    if a.manifest or not (a.bundle or a.upload):
        print(json.dumps(manifest(), indent=2))
    if a.bundle:
        meta = write_bundle(a.bundle)
        print(f"wrote bundle {a.bundle} ({len(meta['files'])} files)")
    if a.upload:
        token = os.environ.get("OSF_TOKEN", "").strip()
        if not token:
            print(
                "OSF_TOKEN missing. Create one at https://osf.io/settings/tokens "
                "(osf.full_write), then:  $env:OSF_TOKEN='...'; "
                "python -m tpl.io.osf_deposit --upload",
                file=sys.stderr,
            )
            return 2
        try:
            info = upload(token)
        except urllib.error.HTTPError as e:
            print(f"OSF HTTP {e.code}: {e.read()[:500]!r}", file=sys.stderr)
            return 1
        print(f"OSF project {info['html']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
