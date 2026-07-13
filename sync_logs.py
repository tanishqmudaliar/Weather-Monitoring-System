import hashlib
import os
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

PYTHONANYWHERE_USERNAME = os.getenv("PYTHONANYWHERE_USERNAME")

PROJECT = Path(f"/home/{PYTHONANYWHERE_USERNAME}/Weather-Monitoring-System")
LOG = PROJECT / ".github/logs/deployment.log"
HASH_FILE = PROJECT / ".github/logs/.deployment.hash"

if not LOG.exists():
    raise SystemExit(0)

current_hash = hashlib.sha256(LOG.read_bytes()).hexdigest()

old_hash = ""
if HASH_FILE.exists():
    old_hash = HASH_FILE.read_text().strip()

# Nothing changed
if current_hash == old_hash:
    raise SystemExit(0)

subprocess.run(
    ["git", "add", ".github/logs/deployment.log"],
    cwd=PROJECT,
    check=True
)

commit = subprocess.run(
    [
        "git",
        "commit",
        "-m",
        f"[LOGS] {datetime.now():%Y-%m-%d %H:%M:%S}"
    ],
    cwd=PROJECT
)

if commit.returncode == 0:
    subprocess.run(
        ["git", "push", "origin", "master"],
        cwd=PROJECT,
        check=True
    )

HASH_FILE.write_text(current_hash)