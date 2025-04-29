
import os
import csv
import requests
import psycopg2
import time
import random
from datetime import datetime

# Validate master_query_list.csv before running
def validate_master_query_list():
    try:
        with open('master_query_list.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            first_row = next(reader)
            if 'job_title' not in first_row or 'city' not in first_row:
                print("❌ Error: master_query_list.csv must have 'job_title' and 'city' headers.")
                exit(1)
            else:
                print("✅ master_query_list.csv validated successfully.")
    except Exception as e:
        print(f"❌ Error reading master_query_list.csv: {e}")
        exit(1)

# Load environment variables
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
ADZUNA_APP_ID = os.environ.get('ADZUNA_APP_ID')
ADZUNA_APP_KEY = os.environ.get('ADZUNA_APP_KEY')

# Database connection
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Save a batch of jobs into database
def save_jobs(jobs):
    conn = connect_db()
    cur = conn.cursor()
    for job in jobs:
        try:
            if job.get('salary_is_predicted') == "1":
                continue

            salary_min, salary_max = normalize_salary(
                job.get('salary_min'),
                job.get('salary_max'),
                job.get('contract_time')
            )

            cur.execute("""
                INSERT INTO JobPosting 
                (adzuna_id, title, company_name, location, category, salary_min, salary_max, 
                 contract_time, salary_type, description, date_posted, job_url, source)
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
                job.get('contract_time'),
                job.get('contract_type'),
                job.get('description'),
                format_date(job.get('created')),
                job.get('redirect_url'),
                "adzuna"
            ))
        except Exception as e:
            print(f"⚠️ Error inserting job: {e}")
            continue

    conn.commit()
    cur.close()
    conn.close()

# Normalize salaries to annual
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

# Format ISO date
def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except:
        return None

# Fetch jobs from Adzuna API
def fetch_jobs(title, location, page=1):
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 50,
        "what": title,
        "where": location,
        "sort_by": "date",
        "max_days_old": 30,  # Updated to 30 days
        "content-type": "application/json"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"⚠️ Error {response.status_code} for {title} in {location}")
        return None

# Save scraper progress
def save_progress(index):
    with open('progress.txt', 'w') as f:
        f.write(str(index))

# Load scraper progress
def load_progress():
    if os.path.exists('progress.txt'):
        with open('progress.txt', 'r') as f:
            return int(f.read())
    return 0

# Main scraping function
def run_scraper():
    calls_made = 0
    start_idx = load_progress()

    with open('master_query_list.csv', newline='', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))

        for idx, row in enumerate(reader):
            if idx < start_idx:
                continue

            if calls_made >= 25:  # Reduced limit for testing
                print("✅ Reached safe test limit of 25 API calls. Stopping.")
                return

            title = row['job_title']
            location = row['city']

            print(f"🔎 Scraping: {title} in {location}")
            data = fetch_jobs(title, location)
            calls_made += 1

            if data and data.get('results'):
                results = data['results']
                if len(results) < 10:
                    print(f"🌎 Few results for {title} in {location}. Broadening search.")
                    data_us = fetch_jobs(title, "")
                    calls_made += 1
                    if data_us and data_us.get('results'):
                        results += data_us['results']

                save_jobs(results)

            save_progress(idx + 1)
            time.sleep(random.uniform(2.5, 3.5))

if __name__ == "__main__":
    validate_master_query_list()
    run_scraper()
