import time
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from services.google_drive import list_files

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', minutes=15)
def scheduled_sync():
    print("Syncing data with QuickBooks and other services...")

@scheduler.scheduled_job('interval', minutes=30)
def sync_drive():
    files = list_files()
    with open('drive_cache.json', 'w') as f:
        json.dump(files, f)

if __name__ == "__main__":
    scheduler.start()
