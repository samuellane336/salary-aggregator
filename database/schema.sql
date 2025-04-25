
CREATE TABLE Company (
    company_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    size VARCHAR(50),
    hq_location VARCHAR(255)
);

CREATE TABLE JobPosting (
    job_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company_id INTEGER REFERENCES Company(company_id),
    location VARCHAR(255),
    salary_min INTEGER,
    salary_max INTEGER,
    salary_type VARCHAR(50),
    source VARCHAR(100),
    date_posted DATE,
    job_url TEXT,
    description TEXT
);
