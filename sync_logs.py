import hashlib
import os
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PYTHONANYWHERE_USERNAME = os.getenv("PYTHONANYWHERE_USERNAME")

PROJECT = Path(f"/home/{PYTHONANYWHERE_USERNAME}/Weather-Monitoring-System")
LOG = PROJECT / ".github/logs/deployment.log"
HASH_FILE = PROJECT / ".github/logs/.deployment.hash"

# No deployment.log yet means the app hasn't logged anything on this
# machine (fresh clone, first boot) — nothing to sync, so exit quietly
# instead of erroring.
if not LOG.exists():
    raise SystemExit(0)

# Hash the content rather than checking mtime/size: PythonAnywhere can
# touch the file (reload, filesystem sync) without the content actually
# changing, and mtime alone would trigger pointless commits.
current_hash = hashlib.sha256(LOG.read_bytes()).hexdigest()

# No hash file yet = first run on this machine. old_hash stays "",
# which never matches a real sha256 digest, so the first run always
# falls through and commits whatever log content currently exists.
old_hash = ""
if HASH_FILE.exists():
    old_hash = HASH_FILE.read_text().strip()

# Nothing changed since the last sync — skip straight to exit so we
# never create an empty commit.
if current_hash == old_hash:
    raise SystemExit(0)

# check=True here on purpose: staging should never fail under normal
# conditions, so treat it as fatal if it does rather than silently
# continuing with a dirty/unstaged log file.
subprocess.run(
    ["git", "add", ".github/logs/deployment.log"],
    cwd=PROJECT,
    check=True
)

# No check=True: git commit exits non-zero when there's nothing staged
# to commit. That's used as a signal below (skip the push) rather than
# treated as a failure that should crash the script.
commit = subprocess.run(
    [
        "git",
        "commit",
        "-m",
        f"[LOGS] {datetime.now():%Y-%m-%d %H:%M:%S}"
    ],
    cwd=PROJECT
)

# Only push if a commit was actually created, so we're never pushing
# when there's nothing new for the remote.
if commit.returncode == 0:
    subprocess.run(
        ["git", "push", "origin", "master"],
        cwd=PROJECT,
        check=True
    )

# Written unconditionally after the block above — including when the
# commit step failed for a reason other than "nothing to commit" (e.g.
# git identity not configured). In that case this run's log content
# is marked as synced even though it never made it to the remote, and
# won't be retried on the next run.
HASH_FILE.write_text(current_hash)