# Overview
A web app to track prop firm trading accounts and trades.
This project is built with FastAPI, PostgreSQL and Docker, designed as a personal learning project to improve backend development skills, including REST APIs, database management and deployment methodologies.

# Features
  - User authentication (login/logout)
  - Add and manage trading accounts
  - Log trades with key details (symbol, size, entry/exit, PnL)
  - View multiple metrics and dashboards
  - REST API endpoints for frontend integration

# Tech Stack
  - Programming Languages: Python & MQL5 (if needed)
  - Backend: FastAPI
  - Database: PostgreSQL
  - Containerization: Docker
  - Version Control: Git + GitHub

# Project Structure
trading_account_tracker/
├─ app/
│  ├─ main.py          # FastAPI entrypoint
│  ├─ models.py        # SQLAlchemy models
│  ├─ schemas.py       # Pydantic schemas
│  ├─ crud.py          # Database operations
│  ├─ api/
│  │   └─ accounts.py  # Example router
├─ tests/              # Unit tests
├─ requirements.txt    # Python dependencies
├─ Dockerfile          # Optional Docker setup
├─ .gitignore
└─ README.md


# Future Improvements
  - Connect to MT5 API for automated trade import
  - Add frontend dashboard (Using React.js)

# Notes
  - Free hosting or database services will sleep when inactive. Suitable for developemnt/testing purposes.