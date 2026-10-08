# Bulk Certificate Generator API

A Python-based REST API for generating certificates in bulk for multiple recipients.

The system accepts a single bulk certificate generation request, validates recipient data, processes certificates in the background, stores job information in a relational SQLite database, generates PDF certificates using ReportLab, tracks job progress, handles individual failures, and allows generated certificates to be retrieved through an API endpoint.

---

## Features

- Bulk certificate generation
- REST API using FastAPI
- SQLite relational database
- Recipient data validation using Pydantic
- PDF certificate generation using ReportLab
- Background job processing
- Job status tracking
- Job progress tracking
- Individual certificate status tracking
- Individual failure handling
- Certificate PDF retrieval
- Automated tests using Pytest
- Interactive Swagger API documentation

---

## Technology Stack

- Python 3
- FastAPI
- SQLite
- Pydantic
- ReportLab
- Pytest
- HTTPX
- Uvicorn

---

## Project Structure

```text
bulk-certificate-generator/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── jobs.py
│   │   └── certificates.py
│   │
│   └── services/
│       ├── __init__.py
│       └── certificate_generator.py
│
├── templates/
│   └── certificate_template.py
│
├── generated/
│
├── tests/
│   ├── __init__.py
│   ├── test_jobs.py
│   ├── test_validation.py
│   ├── test_generation.py
│   ├── test_status.py
│   ├── test_failure.py
│   └── test_retrieval.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── run.py