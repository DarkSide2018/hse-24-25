import schedule
import time
from parent.diplom.parser import fetch_links_with_phrase

def run_scheduler():
    while True:
        print("schedule job")
        schedule.run_pending()
        time.sleep(5)
        url_welcome_page = f'https://www.cbr.ru/dkp/cal_mp/#t8'
        phrase = "пресс-релиза"
        fetch_links_with_phrase(url_welcome_page, phrase)

# Start the scheduler
if __name__ == '__main__':
    print("Scheduler is running. Press Ctrl+C to exit.")
    run_scheduler()