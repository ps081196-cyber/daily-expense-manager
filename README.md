# Daily Expense Manager — Practice Project

A simple Streamlit application for recording and reviewing daily expenses.

## Features

- Add expenses with date, category, description, amount, and payment method
- View total expenses, today's spending, and transaction count
- View category-wise and day-wise spending charts
- Delete individual transactions or clear the current session
- Download expense data as CSV

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud

1. Put `app.py`, `requirements.txt`, and `README.md` in a GitHub repository.
2. In Streamlit Community Cloud, create a new app from the repository.
3. Select `app.py` as the entry point and deploy.

## Hugging Face Spaces

1. Create a new Space and choose Streamlit if available for your Space configuration, or use the supported Docker/Streamlit configuration required by Hugging Face at deployment time.
2. Upload the project files to the Space repository.
3. Ensure the Space launches `streamlit run app.py` when using a Docker-based configuration.

## Storage note

This practice version stores data in Streamlit session state, so entries are not permanent and may reset when a session or deployment restarts. A production version should use a persistent database such as SQLite (where supported), PostgreSQL, or Supabase.
