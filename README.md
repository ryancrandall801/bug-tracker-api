# Bug Tracker API

[![Python Tests](https://github.com/ryancrandall801/bug-tracker-api/actions/workflows/python-tests.yml/badge.svg)](https://github.com/ryancrandall801/bug-tracker-api/actions)

A small REST API built with FastAPI and pytest to practice API design and automated API testing.

This project implements a simple bug tracking service with full CRUD functionality and automated tests.

The goal of the project is to better understand:

REST API design

HTTP methods and status codes

request validation

idempotency

API test automation with pytest

backend project structure

Tech Stack

Python

FastAPI

Pydantic

Uvicorn

pytest

FastAPI TestClient

Project Structure
bug-tracker-api
│
├── app
│   ├── main.py          # FastAPI app entry point
│   ├── models.py        # Pydantic request/response schemas
│   └── routes
│       └── bugs.py      # Bug API endpoints
│
├── tests
│   ├── test_health.py   # Health endpoint tests
│   └── test_bugs.py     # API tests for bug endpoints
│
├── requirements.txt
├── README.md
└── .gitignore
Running the API

Activate the virtual environment:

.venv\Scripts\Activate.ps1

Run the server:

uvicorn app.main:app --reload

Open the API documentation:

http://127.0.0.1:8000/docs

FastAPI automatically generates Swagger UI for testing endpoints.

Running Tests

Run the automated API tests:

python -m pytest

Tests use FastAPI TestClient to simulate HTTP requests against the API.

Data Storage

This project currently uses an in-memory datastore.

bugs_db = []

Data is stored in a Python list while the server is running.

Important implications:

data resets when the server restarts

no external database is required

simplifies development and testing

In a real production service this would likely be replaced with:

PostgreSQL

MySQL

MongoDB

Implemented API Endpoints
Create Bug
POST /bugs

Example request:

{
  "title": "Login button not working",
  "description": "Clicking login does nothing",
  "priority": "high"
}

Response:

201 Created
Get All Bugs
GET /bugs

Returns a list of bugs.

Get Bug by ID
GET /bugs/{id}

Example:

GET /bugs/1

Possible responses:

200 OK

404 Not Found

Update Bug
PATCH /bugs/{id}

Allows partial updates.

Example request:

{
  "status": "resolved"
}

FastAPI automatically validates request fields.

Delete Bug
DELETE /bugs/{id}

Possible responses:

204 No Content — bug deleted

404 Not Found — bug does not exist

Idempotency

The DELETE endpoint is idempotent but not safe.

Example behavior:

DELETE /bugs/1 → 204
DELETE /bugs/1 → 404

The system state remains unchanged after the first deletion.

Testing Strategy

Tests verify:

successful API operations

validation failures

missing resources

correct HTTP status codes

idempotent behavior

Example scenarios tested:

test_create_bug_success
test_create_bug_missing_title
test_get_bug_by_id_returns_correct_bug
test_patch_bug_updates_status
test_delete_bug_success
test_delete_bug_is_idempotent

Each test resets the in-memory datastore to ensure test isolation.

Future Improvements

Potential enhancements:

filtering bugs (GET /bugs?status=open)

pagination

authentication / authorization

database integration

CI pipeline for automated tests

rate limiting

Purpose of This Project

This project is designed to:

practice API testing concepts

demonstrate backend development fundamentals

build a portfolio project for SDET / backend engineering roles

Quick Refresher When Returning to the Project

If you open this project later, the main flow is:

Run the server with uvicorn

Open /docs

Create a bug using POST /bugs

Retrieve bugs using GET /bugs

Run tests with pytest

The API currently stores bugs in memory inside bugs_db.