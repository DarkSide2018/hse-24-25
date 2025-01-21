import json
from time import sleep, time

import requests
from bs4 import BeautifulSoup
import re
from parent.diplom.service import insert_press_release, extract_date, insert_only_source_text, \
    select_only_sources_where_key_rate_is_null, select_releases_where_text_is_null, select_nearest_key_rate_by_date, \
    select_release_where_html_exists, insert_text_by_id

base_url="https://www.cbr.ru"

def fetch_cbr_api(url):
    content = requests.get(url).text
    data = json.loads(content)
    for doc in data:
        doc_html = doc['doc_htm']
        date_update = doc['dateupdate']
        html = base_url + '/press/pr/?file=' + doc_html
        print("url",html)
        insert_only_source_text(html,date_update)

def fetch_only_change_releases():
    texts = select_release_where_html_exists()
    print("texts count", len(texts))
    for t in texts:
        soup = BeautifulSoup(t[1], 'html.parser')
        landing_text = (soup
                        .find('div', class_='landing-text')
                        .get_text(strip=True)
                        .replace("При использовании материала ссылка на Пресс-службу Банка России обязательна.",""))
        insert_text_by_id(t[0],landing_text)
    return ""
def fetch_source_text_from_db():
    sources = select_releases_where_text_is_null()
    print("sources count", len(sources))
    for s in sources:
        response = requests.get(s, verify=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.find('div', class_='landing-text').get_text(strip=True)
        release_date = extract_date(text)
        key_rate = select_nearest_key_rate_by_date(release_date)
        if len(key_rate) == 0:
            key_rate =[(5.5,)]
        landing_text = (soup
                          .find('div', class_='landing-text')
                          .get_text(strip=True)
                          .replace("При использовании материала ссылка на Пресс-службу Банка России обязательна.",""))
        insert_press_release(landing_text,key_rate[0][0],s,release_date)
    return ""

def fetch_links_with_phrase(url, phrase):
    try:
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



