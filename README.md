
# Salary Aggregator Website

A full-stack app to search job postings and view aggregated salary data.

## 🚀 Local Setup

### Backend (Flask)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DB_NAME=...
export DB_USER=...
export DB_PASSWORD=...
export DB_HOST=...
python app.py
```

### Frontend
```bash
cd frontend
open index.html (or serve with any static file server)
```

### Database
- Load schema and sample data:
```bash
psql -U your_user -d your_db -f database/schema.sql
psql -U your_user -d your_db -f database/sample_data.sql
```

## 🌐 Deploy on Render

1. Upload to GitHub
2. Use Render's web service setup
3. Add environment variables in Render dashboard:
   - DB_NAME
   - DB_USER
   - DB_PASSWORD
   - DB_HOST

## 🔁 Updating the Live Site

```bash
# Make your changes locally
git add .
git commit -m "Update feature"
git push

# Render will auto-deploy
```

---
