from time import sleep
import requests
from bs4 import BeautifulSoup
import re
from parent.diplom.service import insert_press_release, base_url, extract_date, insert_only_source_text, \
    select_only_sources_where_key_rate_is_null


def fetch_links_with_phrase(url, phrase):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.findAll('a')
        a_hrefs_welcome = [item.get('href') for item in links if phrase in item]
        for empty_href in a_hrefs_welcome:
            source_link = base_url + empty_href
            insert_only_source_text(source_link)

        a_hrefs_db = select_only_sources_where_key_rate_is_null()
        for href in a_hrefs_db:
            sleep(30)
            content = requests.get(href).text
            extracted_date = extract_date(content)
            if extracted_date:
                print("extracted_date :", extracted_date)
            soup_inner = BeautifulSoup(content, 'html.parser')
            referenceable = soup_inner.find('span', class_='referenceable')
            if referenceable:
              content_span = referenceable.get_text(strip=True)
              key_rate_pattern = re.search(r'(\d+[,\.]?\d*)%', content_span)
              percent_value = key_rate_pattern.group(1).replace(',', '.')
              print("content-span",content_span)
              print("percent_value",percent_value)
              insert_press_release(
                  content,
                  percent_value,
                  href,
                  extracted_date
              )
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

url_welcome_page = "/dkp/cal_mp/#t11"
phrase = "Пресс-релиз"

fetch_links_with_phrase(base_url+url_welcome_page, phrase)

