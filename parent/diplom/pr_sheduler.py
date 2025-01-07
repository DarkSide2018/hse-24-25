import schedule
import time
from parent.diplom.parser import fetch_cbr_api


def run_scheduler():
    while True:
        print("schedule job")
        schedule.run_pending()
        time.sleep(5)
        url = f'https://www.cbr.ru/news/eventandpress/?page=0&IsEng=false&type=4&dateFrom=2024-12-01T00:00:00&dateTo=2024-12-31T00:00:00&Tid=0&vol=&phrase=&_={time.time()}'
        fetch_cbr_api(url)

# Start the scheduler
if __name__ == '__main__':
    print("Scheduler is running. Press Ctrl+C to exit.")
    run_scheduler()