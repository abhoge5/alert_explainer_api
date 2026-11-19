# Alert Explainer API

A FastAPI service for storing alerts and generating deterministic, rule-based explanations from each alert's severity, metric value, and threshold. The service uses a local SQLite database and does not call an external language model API.

## Project Structure

```text
.
|-- database.py          # SQLite engine, SQLAlchemy base, and DB session dependency
|-- main.py              # FastAPI application and root health endpoint
|-- models.py            # SQLAlchemy Alert model
|-- schemas.py           # Pydantic request and response schemas
|-- requirements.txt     # Application dependencies
|-- routers/
|   `-- alerts.py        # Alert and explanation endpoints
|-- services/
|   `-- explainer.py     # Rule-based explanation generation
|-- test_alerts.py       # API tests
`-- docs/
	`-- adr/             # Architecture Decision Records
```

The SQLite database is stored in `alerts.db` in the working directory and is created when the application starts.

## Alert Fields

All fields below are returned for a stored alert. When creating an alert, send the five required fields that do not have a generated value.

| Field | Type | Details |
| --- | --- | --- |
| `id` | integer | Generated database identifier. |
| `title` | string | Alert title. |
| `severity` | string | One of `critical`, `warning`, or `info`. |
| `source` | string | Alert source. |
| `metric_name` | string | Name of the measured metric. |
| `metric_value` | number | Current metric value. |
| `threshold` | number | Comparison threshold. |
| `created_at` | date-time | Generated creation timestamp. |

## Endpoints

| Method | Path | Status codes | Description |
| --- | --- | --- | --- |
| `GET` | `/` | `200` | Health check. |
| `POST` | `/alerts/` | `201`, `422` | Create an alert; `422` indicates invalid input. |
| `GET` | `/alerts/` | `200` | List alerts ordered by ID. |
| `GET` | `/alerts/{alert_id}` | `200`, `404`, `422` | Get an alert; `404` if it does not exist, `422` if the ID is not an integer. |
| `POST` | `/alerts/{alert_id}/explain` | `200`, `404`, `422` | Generate an explanation; `404` if the alert does not exist, `422` if the ID is not an integer. |

FastAPI's interactive API documentation is available at `http://127.0.0.1:8000/docs` while the service is running.

## Install and Run on Windows

In PowerShell, from the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. If PowerShell blocks activation of the virtual environment, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` and then activate it again.

## Run Tests

The test tools are not listed in `requirements.txt`. With the virtual environment active, install them and run the test suite from the project directory:

```powershell
python -m pip install pytest httpx
python -m pytest -v
```

## Architecture Decision Records

- [0001: Rule-Based Explanations](docs/adr/0001-rule-based-explanations.md)
- [0002: Human Approval for Alert Summaries](docs/adr/0002-human-approval-for-alert-summaries.md)
