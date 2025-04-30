
import psycopg2
import os

# Load DB credentials from environment
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def reset_progress():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ScrapeProgress (source, last_completed_index)
        VALUES ('adzuna', 0)
        ON CONFLICT (source) DO UPDATE
        SET last_completed_index = 0
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Scrape progress reset to 0.")

if __name__ == "__main__":
    reset_progress()
