import psycopg2
from psycopg2 import sql
from datetime import datetime
import re

DB_HOST = 'localhost'
DB_PORT=6000
DB_NAME = 'diplom_db'
DB_USER = 'myuser'
DB_PASSWORD = 'mypassword'


conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    port=DB_PORT,
    password=DB_PASSWORD
)

def select_nearest_key_rate_by_date(date):
    cursor = conn.cursor()
    cursor.execute("SET search_path to dip_schema;")
    conn.commit()
    cursor_select = conn.cursor()
    print("date",date)
    cursor_select.execute(sql.SQL("""select key_rate from press_release pr
                                  where release_date < %s and key_rate is not null order by release_date desc limit 1;
                                  """), (date,))
    result = cursor_select.fetchall()
    cursor_select.close()
    print("result",result)
    return result


def select_releases_where_text_is_null():
    cursor = conn.cursor()
    cursor.execute("SET search_path to dip_schema;")
    conn.commit()
    cursor_select = conn.cursor()
    cursor_select.execute(sql.SQL("select source_text from press_release pr where text is null"))
    res=[]
    result = cursor_select.fetchall()
    for row in result:
        res.append(row[0])
    print("text is null", res)
    cursor_select.close()
    return res

def select_only_sources_where_key_rate_is_null():
    cursor = conn.cursor()
    cursor.execute("SET search_path to dip_schema;")
    conn.commit()
    cursor_select = conn.cursor()
    cursor_select.execute(sql.SQL("select source_text from press_release pr where key_rate is null"))
    res=[]
    result = cursor_select.fetchall()
    for row in result:
        res.append(row[0])
    print("key_rate is null", res)
    cursor_select.close()
    return res

def insert_only_source_text(source_text,date_update):
    cursor = conn.cursor()
    cursor.execute("SET search_path to dip_schema;")
    conn.commit()
    cursor_exists = conn.cursor()
    cursor_exists.execute(sql.SQL("SELECT COUNT(*) FROM press_release WHERE source_text = %s"), [source_text])
    exists = cursor_exists.fetchone()[0]
    cursor_exists.close()
    if exists == 0:
        insert_query = sql.SQL("""
              INSERT INTO press_release (
              source_text,
              release_date
               )
              VALUES (%s,%s);
          """)
        cursor.execute(insert_query, (source_text,date_update))
        conn.commit()
        cursor.close()
        print("source_text inserted successfully.")

def insert_press_release(text, key_rate, source_text, release_date):
    cursor = conn.cursor()
    try:
        cursor.execute("SET search_path to dip_schema;")
        conn.commit()
        cursor_exists = conn.cursor()
        cursor_exists.execute(sql.SQL("SELECT COUNT(*) FROM press_release WHERE source_text = %s and key_rate is null"), [source_text])
        exists = cursor_exists.fetchone()[0]
        cursor_exists.close()
        if exists == 1:
          insert_query = sql.SQL("""
              update press_release set
              text = %s, 
              key_rate = %s, 
               release_date = %s where source_text = %s;
          """)
          cursor.execute(insert_query, (text, key_rate, release_date,source_text))
          conn.commit()
          print("Data inserted successfully.")
    except Exception as e:
        print("An error occurred while inserting data:", e)
    finally:
        cursor.close()

def extract_date(text):
    date_pattern = r'\b(\d{1,2})\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s+(\d{4})\b'
    match = re.search(date_pattern, text)
    if match:
        day, month, year = match.groups()
        month_mapping = {
            'января': 1,
            'февраля': 2,
            'марта': 3,
            'апреля': 4,
            'мая': 5,
            'июня': 6,
            'июля': 7,
            'августа': 8,
            'сентября': 9,
            'октября': 10,
            'ноября': 11,
            'декабря': 12
        }
        month_number = month_mapping[month]
        date_object = datetime(year=int(year), month=month_number, day=int(day))
        return date_object
    else:
        return None