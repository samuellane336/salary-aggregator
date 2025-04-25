
INSERT INTO Company (name, industry, size, hq_location)
VALUES ('TechCorp', 'Technology', '500-1000', 'San Francisco, CA');

INSERT INTO JobPosting (title, company_id, location, salary_min, salary_max, salary_type, source, date_posted, job_url, description)
VALUES ('Software Engineer', 1, 'Remote', 90000, 130000, 'yearly', 'Indeed', CURRENT_DATE, 'https://example.com/job1', 'Build and maintain web applications.');
