

import schedule
import time
from parent.diplom.parser import fetch_only_change_releases


def run_scheduler():
    while True:
        print("schedule job")
        schedule.run_pending()
        time.sleep(5)
        try:
          fetch_only_change_releases()
        except Exception:
          print("Connection error trying again")

if __name__ == '__main__':
    print("Scheduler is running. Press Ctrl+C to exit.")
    run_scheduler()