import time
import json
import os
import sys
from apscheduler.schedulers.blocking import BlockingScheduler

# Ensure the project root is on the Python path so that ``services`` can be
# imported when this script is executed directly.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.google_drive import list_files

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', minutes=15)
def scheduled_sync():
    print("Syncing data with QuickBooks and other services...")

@scheduler.scheduled_job('interval', minutes=30)
def sync_drive():
    """Sync Google Drive file list to a local cache file."""
    try:
        files = list_files()
    except FileNotFoundError as exc:
        # Provide a helpful message when credentials are missing
        print(f"Unable to sync Drive: {exc}")
        return

    cache_path = os.path.join(PROJECT_ROOT, 'drive_cache.json')
    with open(cache_path, 'w') as f:
        json.dump(files, f)

if __name__ == "__main__":
    scheduler.start()
