from time import sleep

import requests
from bs4 import BeautifulSoup
import re
from parent.diplom.service import insert_press_release, extract_date, insert_only_source_text, \
    select_only_sources_where_key_rate_is_null

base_url="https://www.cbr.ru"

def fetch_links_with_phrase(url, phrase):
    try:
        print("url",url)
        response = requests.get(url, verify=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.findAll('a')
        a_hrefs_welcome = [item.get('href') for item in links if phrase in item]
        for empty_href in a_hrefs_welcome:
            source_link = base_url + empty_href
            insert_only_source_text(source_link)

        a_hrefs_db = select_only_sources_where_key_rate_is_null()
        for href in a_hrefs_db:
            try:
              sleep(30)
              print("current_href",href)
              content = requests.get(href).text
              extracted_date = extract_date(content)
              soup_inner = BeautifulSoup(content, 'html.parser')
              referenceable = soup_inner.find('span', class_='referenceable')
              content_span = referenceable.get_text(strip=True)
              key_rate_pattern = re.search(r'(\d+[,\.]?\d*)%', content_span)
              if key_rate_pattern is not None:
                percent_value = key_rate_pattern.group(1).replace(',', '.')
                print("content-span",content_span)
                print("percent_value",percent_value)
                insert_press_release(
                    content,
                    percent_value,
                    href,
                    extracted_date
                )
                continue
              landing_text = soup_inner.find('div', class_='landing-text')
              match = re.search(r'до\s(\d{1,2},\d{1,2})%',landing_text.get_text(strip=True))
              if match:
                insert_press_release(
                    content,
                    match.group(1).replace(',', '.').replace('%', ''),
                    href,
                    extracted_date
                )
                continue
              match = re.search(r'на\sуровне\s(\d{1,2},\d{1,2})%',landing_text.get_text(strip=True))
              if match:
                  insert_press_release(
                      content,
                      match.group(1).replace(',', '.').replace('%', ''),
                      href,
                      extracted_date
                  )

            except Exception as e:
              print(f"An error occurred: {e} href: {href}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return



