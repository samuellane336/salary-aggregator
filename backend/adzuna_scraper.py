import requests
import psycopg2
import time
from datetime import datetime
import os

# === CONFIG ===
APP_ID = "9a0a0f1a"
APP_KEY = "77da7d24800f5ceaafbda4e00f7da500"

DB_CONFIG = {
    'dbname': 'salary_db_njfw',
    'user': 'salary_db_njfw_user',
    'password': '5qONed3hlxpTP0n6afBI7ZoVUsnurlvb',
    'host': 'dpg-d05pdnbuibrs73fufs60-a.virginia-postgres.render.com',
    'port': 5432,
}

CALL_TRACKER_FILE = "call_tracker.txt"
DAILY_CALL_LIMIT = 250
MONTHLY_CALL_LIMIT = 2500
SLEEP_BETWEEN_CALLS = 3  # seconds

# Jobs and Locations
JOB_TITLES = [
    # 50 titles (5 per day)
    "software engineer", "marketing manager", "data analyst", "registered nurse", "project manager",
    "accountant", "graphic designer", "sales representative", "operations manager", "human resources specialist",
    "business analyst", "mechanical engineer", "customer support representative", "network administrator", "social media manager",
    "financial advisor", "civil engineer", "medical assistant", "quality assurance analyst", "supply chain manager",
    "electrical engineer", "paralegal", "nursing assistant", "product manager", "teacher",
    "construction manager", "software developer", "IT support specialist", "UX designer", "web developer",
    "pharmacist", "interior designer", "security guard", "systems analyst", "database administrator",
    "physical therapist", "copywriter", "training specialist", "chemist", "legal assistant",
    "dentist", "graphic illustrator", "HR coordinator", "environmental engineer", "project coordinator",
    "claims adjuster", "hardware engineer", "sales manager", "logistics coordinator", "content strategist"
]

LOCATIONS = [
    "California", "New York", "Texas", "Florida", "Illinois",
    "Washington", "Massachusetts", "Colorado", "Georgia", "North Carolina",
    "Michigan", "Ohio", "Arizona", "Pennsylvania", "Virginia",
    "Tennessee", "Indiana", "Missouri", "Maryland", "Wisconsin",
    "Minnesota", "South Carolina", "Alabama", "Louisiana", "Kentucky",
    "Oregon", "Oklahoma", "Connecticut", "Utah", "Iowa",
    "Nevada", "Arkansas", "Mississippi", "Kansas", "New Mexico",
    "Nebraska", "West Virginia", "Idaho", "Hawaii", "Maine",
    "New Hampshire", "Montana", "Rhode Island", "Delaware", "South Dakota",
    "North Dakota", "Alaska", "Vermont", "Wyoming"
]

# Connect to database
def connect_db():
    return psycopg2.connect(**DB_CONFIG)

# Fetch jobs from Adzuna
def fetch_jobs(job_title, location, page):
    base_url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": job_title,
        "where": location,
        "results_per_page": 50,
        "sort_by": "date",
        "salary_min": 1,
        "content-type": "application/json"
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None
    return response.json()

# Save jobs to database
def save_jobs(jobs):
    conn = connect_db()
    cur = conn.cursor()
    inserted_count = 0

    for job in jobs:
        if job.get("salary_is_predicted") == "1":
            continue  # Skip estimated salaries

        cur.execute("""
            INSERT INTO JobPosting (title, location, salary_min, salary_max, company_id, description, job_url, source, date_posted)
            VALUES (%s, %s, %s, %s, NULL, %s, %s, %s, CURRENT_DATE)
            ON CONFLICT DO NOTHING
        """, (
            job.get("title"),
            job.get("location", {}).get("display_name"),
            job.get("salary_min"),
            job.get("salary_max"),
            job.get("description"),
            job.get("redirect_url"),
            "Adzuna"
        ))
        inserted_count += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {inserted_count} jobs.")

# Track API calls
def update_call_tracker(calls_made_today):
    total_calls = 0
    if os.path.exists(CALL_TRACKER_FILE):
        with open(CALL_TRACKER_FILE, "r") as f:
            try:
                total_calls = int(f.read().strip())
            except ValueError:
                total_calls = 0

    total_calls += calls_made_today

    with open(CALL_TRACKER_FILE, "w") as f:
        f.write(str(total_calls))

    return total_calls

# Main scraping logic
def scrape_all():
    # Check total calls so far
    if os.path.exists(CALL_TRACKER_FILE):
        with open(CALL_TRACKER_FILE, "r") as f:
            try:
                total_calls = int(f.read().strip())
            except ValueError:
                total_calls = 0
    else:
        total_calls = 0

    if total_calls >= MONTHLY_CALL_LIMIT:
        print("Monthly API call limit reached (2500 calls). Pausing scraper until reset.")
        return

    today = datetime.utcnow().day
    day_index = (today % 10)  # 0-9
    today_job_titles = JOB_TITLES[day_index * 5: (day_index * 5) + 5]

    calls_made_today = 0

    for job_title in today_job_titles:
        for location in LOCATIONS:
            if calls_made_today >= DAILY_CALL_LIMIT:
                print("Daily API call limit reached (250 calls).")
                break

            print(f"Fetching: {job_title} in {location}")
            data = fetch_jobs(job_title, location, page=1)
            time.sleep(SLEEP_BETWEEN_CALLS)

            if data and "results" in data:
                save_jobs(data["results"])
                calls_made_today += 1

    total_calls_now = update_call_tracker(calls_made_today)

    print(f"Scraping complete. {calls_made_today} API calls today. Total this month: {total_calls_now} calls.")

if __name__ == "__main__":
    scrape_all()
