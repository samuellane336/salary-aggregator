
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "🚀 Your backend is live!"


def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 5432)
    )

@app.route("/jobs", methods=["GET"])
def get_jobs():
    conn = get_db_connection()
    cur = conn.cursor()

    location = request.args.get("location")
    title = request.args.get("title")

    query = "SELECT title, location, salary_min, salary_max FROM JobPosting WHERE TRUE"
    params = []

    if location:
        query += " AND location ILIKE %s"
        params.append(f"%{location}%")
    if title:
        query += " AND title ILIKE %s"
        params.append(f"%{title}%")

    cur.execute(query, params)
    jobs = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(jobs)

@app.route("/jobs/median", methods=["GET"])
def get_median_salary():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY (salary_min + salary_max)/2) FROM JobPosting")
    median = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify({"median_salary": median})

@app.route("/autocomplete/job", methods=["GET"])
def autocomplete_job():
    query = request.args.get("query", "").strip().lower()
    if not query:
        return jsonify([])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT title FROM JobPosting
        WHERE LOWER(title) LIKE %s
        ORDER BY title
        LIMIT 10
    """, (f"%{query}%",))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([row[0] for row in results])


@app.route("/autocomplete/location", methods=["GET"])
def autocomplete_location():
    query = request.args.get("query", "").strip().lower()
    if not query:
        return jsonify([])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT location FROM JobPosting
        WHERE LOWER(location) LIKE %s
        ORDER BY location
        LIMIT 10
    """, (f"%{query}%",))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([row[0] for row in results])

if __name__ == "__main__":
   import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=True)