import requests
import psycopg2
import os
from datetime import date

def connect_db():
    return psycopg2.connect(
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=5432
    )

# === CONFIG ===
APP_ID = os.environ.get('ADZUNA_APP_ID')
APP_KEY = os.environ.get('ADZUNA_APP_KEY')
BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"

# 5 popular jobs in California
job_titles = [
    "Software Engineer",
    "Data Analyst",
    "Project Manager",
    "Registered Nurse",
    "Marketing Manager"
]
states = ["California"]

# Adzuna API call limits
DAILY_CALL_LIMIT = 250

def fetch_jobs(job_title, location, page=1):
    params = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'results_per_page': 50,
        'what': job_title,
        'where': location        
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching jobs for {job_title} in {location}: {e}")
        return None

def save_jobs(jobs):
    conn = connect_db()
    cur = conn.cursor()
    inserted_count = 0

    for job in jobs:
        if job.get("salary_is_predicted") == "1":
            continue  # Skip estimated salaries

        try:
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
        except Exception as e:
            print(f"Error inserting job: {job.get('title')} - Error: {e}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {inserted_count} jobs into the database.")

def scrape_all():
    calls_made_today = 0

    for job_title in job_titles:
        for location in states:
            if calls_made_today >= DAILY_CALL_LIMIT:
                print("Reached daily API call limit. Stopping scrape.")
                return

            data = fetch_jobs(job_title, location, page=1)
            if data and "results" in data:
                print(f"Pulled {len(data['results'])} jobs for {job_title} in {location}")
                save_jobs(data["results"])
                calls_made_today += 1

if __name__ == "__main__":
    scrape_all()
