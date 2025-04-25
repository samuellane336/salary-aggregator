
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

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
    cur.execute("SELECT title, location, salary_min, salary_max FROM JobPosting")
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

if __name__ == "__main__":
    app.run(debug=True)
