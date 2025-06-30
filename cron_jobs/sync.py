import time
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', minutes=15)
def scheduled_sync():
    print("Syncing data with QuickBooks and other services...")

if __name__ == "__main__":
    scheduler.start()
