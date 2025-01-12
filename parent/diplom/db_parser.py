
import schedule
import time
from parent.diplom.parser import fetch_source_text_from_db


def run_scheduler():
    while True:
        print("schedule job")
        schedule.run_pending()
        time.sleep(5)
        try:
          fetch_source_text_from_db()
        except Exception:
          print("Connection error trying again")

if __name__ == '__main__':
    print("Scheduler is running. Press Ctrl+C to exit.")
    run_scheduler()