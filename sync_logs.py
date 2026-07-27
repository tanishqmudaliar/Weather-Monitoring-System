import hashlib
import os
import subprocess
import fcntl
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PYTHONANYWHERE_USERNAME = os.getenv("PYTHONANYWHERE_USERNAME")

PROJECT = Path(f"/home/{PYTHONANYWHERE_USERNAME}/Weather-Monitoring-System")
# Live log the running app writes to continuously. Deliberately
# untracked (see .gitignore) so `git reset --hard` in the webhook
# handler can never touch it, no matter when this script runs
# relative to a deploy.
LOG = PROJECT / ".github/logs/deployment.log"
# Git-tracked snapshot this script owns exclusively - the app never
# writes to this path, so there's nothing for a deploy's reset to race
# against here either.
ARCHIVE = PROJECT / ".github/logs/deployment-history.log"
HASH_FILE = PROJECT / ".github/logs/.deployment.hash"
# Purely to avoid two git processes (this script and the webhook's
# fetch/reset) hitting the .git index lock at the same instant.
LOCK_FILE = PROJECT / ".git/deploy.lock"

# No deployment.log yet means the app hasn't logged anything on this
# machine (fresh clone, first boot) — nothing to sync, so exit quietly
# instead of erroring.
if not LOG.exists():
    raise SystemExit(0)

lock_fd = open(LOCK_FILE, "w")
fcntl.flock(lock_fd, fcntl.LOCK_EX)

try:
    # Hash the content rather than checking mtime/size: PythonAnywhere can
    # touch the file (reload, filesystem sync) without the content actually
    # changing, and mtime alone would trigger pointless commits.
    log_bytes = LOG.read_bytes()
    current_hash = hashlib.sha256(log_bytes).hexdigest()

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

    # Snapshot the live log's current content into the tracked archive
    # file. This is the only place ARCHIVE is ever written, so there's
    # no concurrent writer to race against.
    ARCHIVE.write_bytes(log_bytes)

    # check=True here on purpose: staging should never fail under normal
    # conditions, so treat it as fatal if it does rather than silently
    # continuing with a dirty/unstaged archive file.
    subprocess.run(
        ["git", "add", str(ARCHIVE.relative_to(PROJECT))],
        cwd=PROJECT,
        check=True
    )

    # No check=True: git commit exits non-zero when there's nothing staged
    # to commit (e.g. the archive already matched this content). That's
    # used as a signal below (skip the push) rather than treated as a
    # failure that should crash the script.
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
        push = subprocess.run(
            ["git", "push", "origin", "master"],
            cwd=PROJECT
        )
        # Only mark this content as synced once it's actually confirmed
        # on the remote - a failed push shouldn't be recorded as done,
        # or that log content would never be retried.
        if push.returncode == 0:
            HASH_FILE.write_text(current_hash)
finally:
    fcntl.flock(lock_fd, fcntl.LOCK_UN)
    lock_fd.close()