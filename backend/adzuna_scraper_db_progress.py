
import os
import csv
import requests
import psycopg2
import time
import random
import json
from datetime import datetime

def connect_db():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )

def load_progress_from_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT last_completed_index FROM ScrapeProgress WHERE source = 'adzuna'")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else 0

def save_progress_to_db(index):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ScrapeProgress (source, last_completed_index)
        VALUES ('adzuna', %s)
        ON CONFLICT (source) DO UPDATE
        SET last_completed_index = EXCLUDED.last_completed_index
    """, (index,))
    conn.commit()
    cur.close()
    conn.close()

def normalize_salary(min_salary, max_salary, contract_time):
    if min_salary is None:
        min_salary = 0
    if max_salary is None:
        max_salary = 0
    if contract_time == "month":
        min_salary *= 12
        max_salary *= 12
    elif contract_time == "week":
        min_salary *= 52
        max_salary *= 52
    elif contract_time == "day":
        min_salary *= 260
        max_salary *= 260
    elif contract_time == "hour":
        min_salary *= 2080
        max_salary *= 2080
    return min_salary, max_salary

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except:
        return None

def fetch_jobs(title, location, page=1):
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"
    params = {
        "app_id": os.environ['ADZUNA_APP_ID'],
        "app_key": os.environ['ADZUNA_APP_KEY'],
        "results_per_page": 50,
        "what": title,
        "where": location,
        "sort_by": "date",
        "max_days_old": 30
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code} for {title} in {location}")
        return None

def save_jobs(jobs):
    conn = connect_db()
    cur = conn.cursor()
    inserted_count = 0
    for job in jobs:
        try:
            if job.get('salary_is_predicted') == "1":
                continue
            salary_min, salary_max = normalize_salary(
                job.get('salary_min'),
                job.get('salary_max'),
                job.get('contract_time')
            )
            if salary_min == 0 and salary_max == 0:
                continue
            cur.execute("""
                INSERT INTO JobPosting 
                (adzuna_id, title, company_name, location, category, salary_min, salary_max,
                 contract_type, salary_interval, description, date_posted, job_url, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (adzuna_id) DO NOTHING
            """, (
                job.get('adref'),
                job.get('title'),
                job.get('company', {}).get('display_name'),
                job.get('location', {}).get('display_name'),
                job.get('category', {}).get('label'),
                salary_min,
                salary_max,
                job.get('contract_type'),
                job.get('contract_time'),
                job.get('description'),
                format_date(job.get('created')),
                job.get('redirect_url'),
                "adzuna"
            ))
            if cur.rowcount == 1:
                inserted_count += 1
        except Exception as e:
            print(f"Error inserting job: {e}")
            continue
    conn.commit()
    cur.close()
    conn.close()
    return inserted_count

def run_scraper():
    calls_made = 0
    start_idx = load_progress_from_db()

    with open('master_query_list.csv', newline='', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        for idx, row in enumerate(reader):
            if idx < start_idx:
                continue
            if calls_made >= 250:
                print("Reached 250 API calls. Stopping.")
                return
            title = row['job_title']
            location = row['city']
            print(f"Scraping: {title} in {location}")
            data = fetch_jobs(title, location)
            calls_made += 1
            if data and data.get('results'):
                results = data['results']
                if len(results) < 10:
                    print("Few results. Trying US-wide.")
                    data_us = fetch_jobs(title, "")
                    calls_made += 1
                    if data_us and data_us.get('results'):
                        results += data_us['results']
                count = save_jobs(results)
                print(f"Inserted {count} jobs.")
            save_progress_to_db(idx + 1)
            time.sleep(random.uniform(2.5, 3.5))

        print("✅ Scraping complete. Resetting scrape index to 0 for next run.")
        save_progress_to_db(0)

if __name__ == "__main__":
    run_scraper()
