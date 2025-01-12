import schedule
import time
from parent.diplom.parser import fetch_cbr_api


def run_scheduler():
    while True:
        print("schedule job")
        schedule.run_pending()
        time.sleep(5)
        for i in range(1,13):
          print("current i:", i)
          # Here unfortunately, you will have to change dates with your hands, because i am lazy.
          url = f'https://www.cbr.ru/news/eventandpress/?page=0&IsEng=false&type=4&dateFrom=2014-{i:02}-01T00:00:00&dateTo=2014-{i:02}-31T00:00:00&Tid=0&vol=&phrase=&_={time.time()}'
          fetch_cbr_api(url)


if __name__ == '__main__':
    print("Scheduler is running. Press Ctrl+C to exit.")
    run_scheduler()