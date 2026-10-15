# API Testing Framework — Capstone Project

- **Created by:** Pham Anh Nhat
- **Version:** 1.0.0
- **Status:** In progress
- **Stack:** Python 3.14 · Pytest · requests · pandas · Allure

An end-to-end **API automation testing framework** that validates a real backend
(request/response cycles, status codes, headers, and JSON payloads). Tests are
**data-driven from Excel**, run with **Pytest**, and produce rich **Allure**
reports. It is built to be easy to extend: adding a new endpoint or a new test
case is a small, localized change.

---

## Table of contents

1. [Overview](#i-overview)
2. [Key features](#ii-key-features)
3. [Tech stack](#iii-tech-stack)
4. [Project structure](#iv-project-structure)
5. [How it works](#v-how-it-works)
6. [Getting started](#vi-getting-started-5-minutes)
7. [Configuration](#vii-configuration)
8. [Running tests](#viii-running-tests)
9. [Test data & placeholders](#ix-test-data--placeholders)
10. [Adding a new module / test case](#x-adding-a-new-module--test-case)
11. [Reports & logs](#xi-reports--logs)
12. [CI / CD](#xii-ci--cd)
13. [Code quality](#xiii-code-quality)
14. [Troubleshooting](#xiv-troubleshooting)
15. [Related projects](#xv-related-projects)

---

## I. Overview

This repository contains a custom API testing tool built with Python to automate
validation of backend services. It verifies request–response cycles, status codes,
and data payloads so system functionality stays aligned with the technical design.
By combining Python, Pytest, and Pandas, it provides a structured approach to
functional and data-driven API testing.

The framework drives a live backend (a URL from `.env`), logs in as multiple roles
(admin / student / teacher), and runs parameterized test cases loaded from Excel
files.

---

## II. Key features

- **Request/Response validation** — status codes, response keys, and JSON body values.
- **Data-driven testing** — test cases live in Excel; Pandas injects each row into a request.
- **Reusable, layered architecture** — endpoint wrappers, response processors, and helpers.
- **Role-based sessions** — session-scoped login fixtures for admin, student, and teacher.
- **Dynamic test data** — placeholders for random strings, datetimes, and pre-data ids.
- **Detailed observability** — loguru logs to console + daily file; failed cases dumped to disk.
- **Rich reporting** — Allure (primary) and pytest-html, with parallel execution via pytest-xdist.
- **CI/CD ready** — GitHub Actions for lint + tests (CI) and scheduled regression + Allure publish (CD).

---

## III. Tech stack

| Category | Package / tool | Version |
| --- | --- | --- |
| Language | Python | 3.14 (`.python-version`, `pyproject.toml` `>=3.14`) |
| Test runner | pytest | 9.1.1 |
| HTTP client | requests | 2.34.2 |
| Data | pandas / openpyxl / python-calamine | 3.0.5 / 3.1.5 / 0.8.2 |
| Reporting | allure-pytest / pytest-html | 2.16.0 / 4.2.0 |
| Parallelism | pytest-xdist | 3.8.0 |
| Logging | loguru | 0.7.3 |
| Config | python-dotenv / pytz | 1.2.3 / 2026.3.post1 |
| Tooling | uv (env + deps), Ruff (lint + format) | — |

> This framework is **synchronous** (`requests`). It intentionally does **not**
> use `httpx`, `pytest-asyncio`, `factory_boy`, or a database driver.

---

## IV. Project structure

```
api_test_cap_prj_v2/
├── .github/workflows/
│   ├── ci.yaml                 # Lint + test + image build on PR/push
│   └── cd.yaml                 # Build/push image + regression + Allure → GitHub Pages
├── apis/                       # Thin endpoint wrappers (return raw requests.Response)
│   ├── account_apis.py
│   └── role_apis.py
├── case_setup/                 # Per-module fixtures that build `pre_data` (ids, names)
│   ├── account_case_setup.py
│   └── role_case_setup.py
├── common/                     # Core runtime objects
│   ├── client.py               # Session, headers/token, retry adapter, login/logout
│   ├── user.py                 # Client + response processors (per role)
│   └── common_setup.py         # Loads predata + client info for fixtures
├── configs/                    # Configuration
│   ├── constants.py            # .env loading, enums (ROLE, APIMETHOD, FILETYPE)
│   └── user_info.json          # Test accounts per role (committed; test users only)
├── data/
│   ├── request_body_template/  # JSON templates used to build predata
│   └── test_cases/             # Excel test-case files (one per module)
├── helpers/                    # Reusable utilities (see table below)
├── process_responses/          # Business-level response handling (validate + parse JSON)
│   ├── account_process_response.py
│   └── role_process_responses.py
├── testcases/                  # Pytest tests + shared fixtures
│   ├── conftest.py             # admin / student / teacher session fixtures
│   ├── test_account.py
│   └── test_role.py
├── logs/                       # Daily log files (gitignored)
├── reports/                    # Failed-case reports (gitignored)
├── main.py                     # Convenience entrypoint
├── pytest.ini                  # testpaths, markers, addopts
├── pyproject.toml              # Dependencies + uv/ruff config
├── requirements.txt            # Flat dependency list (mirrors pyproject)
├── Dockerfile                  # Test-runner image (framework + dependencies)
├── .dockerignore               # Keeps secrets/caches out of the image
└── README.md
```

**Helpers** (`helpers/`):

| Helper | Purpose |
| --- | --- |
| `load_data.py` | Load JSON / text / CSV / Excel into dicts/lists. |
| `run_case.py` | Execute a data-driven case and assert status/keys/values. |
| `setup_test_case.py` | Prepare a case DataFrame and substitute pre-data. |
| `validate_response.py` | Raise on `status_code >= 400`; return parsed JSON. |
| `retry.py` | Decorator to retry transient calls. |
| `logger.py` / `logger_wrapper.py` | Loguru sinks + error-catching wrapper. |
| `time_execution_wrapper.py` | Log function execution time. |
| `record_failed_case.py` | Append a failed case to `reports/failed_cases/*.txt`. |
| `replace_data_by_setup_values.py` / `replace_string_by_dict_value.py` | Resolve placeholders. |
| `random_string.py` / `random_number_string.py` | Generate random test values. |
| `save_data.py`, `dict_to_str.py` | Output helpers. |

---

## V. How it works

```
 testcases/test_account.py
        │  loads Excel cases, filters status == "Done"
        ▼
 helpers.run_case.run_case()          ← the engine
        │  setup_test_case()  → substitute pre-data placeholders
        │  for each row:
        │     pick user by role (admin/student/teacher fixture)
        │     call user.client.<method>(api, request_body)
        ▼
 common.client.Client  ──►  requests session (+ auth header, retry adapter)
        │
        ▼
 HTTP request to BASE_URL
        │
        ▼
 assert_status_code / assert_key_value / assert_data_value
        │  on failure → log + record_failed_case + pytest.fail
        ▼
 Allure results  →  reports / GitHub Pages
```

- **`conftest.py`** builds one logged-in `User` per role for the whole session.
- **`case_setup/<module>_case_setup.py`** prepares prerequisite data (e.g. role and
  account ids) once per session and returns a `pre_data` dict.
- **Excel placeholders** like `{student_role_id}` are replaced from `pre_data`
  before the request is sent.

---

## VI. Getting started (5 minutes)

### Prerequisites

- **Python 3.14**
- **[uv](https://docs.astral.sh/uv/)** — install once with `pip install uv`
- **[Allure CLI](https://allurereport.org/docs/install/)** — only needed to view reports
  (`npm install -g allure-commandline`, or `scoop install allure` on Windows)

### Steps

```powershell
# 1. Install uv once (skip if already installed)
pip install uv

# 2. Create the virtual env and install all dependencies (reads pyproject.toml + uv.lock)
uv sync

# 3. (Optional) activate the venv — `uv run` works without activating
.venv/Scripts/Activate.ps1        # Windows PowerShell
# source .venv/bin/activate       # Linux / macOS

# 4. Verify the python version
uv run python --version           # -> Python 3.14.x

# 5. Configure .env (see next section) — already present at repo root

# 6. Run the test suite
uv run pytest
```

> On Windows, if activation is blocked run once:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`

### VS Code tips

- Use the bundled **Excel viewer** for `data/test_cases/*.xlsx` (already mapped in `.vscode/settings.json`).
- Select the `.venv` interpreter so imports resolve.

---

## VII. Configuration

### `.env` (repo root, gitignored)

```dotenv
LOG_FOLDER = ./logs
REPORT_FOLDER = ./reports
BASE_URL = https://your-backend-url
TEST_CASE_FILE_PATH = ./data/test_cases/account_test_cases.xlsx
```

| Key | Meaning |
| --- | --- |
| `LOG_FOLDER` | Directory for daily log files. |
| `REPORT_FOLDER` | Directory for reports and `failed_cases/`. |
| `BASE_URL` | Backend base URL the tests run against. |
| `TEST_CASE_FILE_PATH` | Default Excel case file (used by tooling/entrypoints). |

> `configs/constants.py` loads `.env` with `python-dotenv`. **Real environment
> variables always win** (dotenv does not override), so CI can inject `BASE_URL`
> without editing files. Never commit `.env` or real credentials.

### Test accounts — `configs/user_info.json`

```json
{
  "admin":   { "email": "test_user_01@gmail.com", "password": "***" },
  "student": { "email": "test_user_07@gmail.com", "password": "***" },
  "teacher": { "email": "test_user_02@gmail.com", "password": "***" }
}
```

### Markers — `pytest.ini`

Registered markers: `role`, `account`, `student`, `teacher`. Add a new marker
here whenever you add a module (Pytest warns about unknown markers).

---

## VIII. Running tests

```powershell
# Everything
uv run pytest

# By marker
uv run pytest -m account
uv run pytest -m role

# A single file
uv run pytest testcases/test_account.py

# Parallel (pytest-xdist)
uv run pytest -n auto

# Via the convenience entrypoint (defaults to the account marker)
uv run python main.py
```

### Allure report

```powershell
uv run pytest --alluredir=allure-results --clean-alluredir
allure generate allure-results -o allure-report --clean
allure serve allure-results
```

### Run with Docker

Build the test-runner image (framework + dependencies baked in):

```powershell
docker build -t api-test-cap-prj-v2:local .
```

Run the suite inside the container. `BASE_URL` is passed at runtime (env vars win
over `.env`), and Allure results + failed-case reports are written back via mounts:

```powershell
# all tests
docker run --rm `
  -e BASE_URL=https://datn-be-steel.vercel.app `
  -v ${PWD}/allure-results:/app/allure-results `
  -v ${PWD}/reports:/app/reports `
  api-test-cap-prj-v2:local

# by marker (args are passed straight to pytest)
docker run --rm -e BASE_URL=... api-test-cap-prj-v2:local -m account

# a single file, with an Allure results dir
docker run --rm -e BASE_URL=... `
  -v ${PWD}/allure-results:/app/allure-results `
  api-test-cap-prj-v2:local testcases/test_account.py --alluredir=allure-results
```

> The image does **not** contain `.env` (see `.dockerignore`), so always pass
> `BASE_URL` (and optionally `LOG_FOLDER`/`REPORT_FOLDER`) as `-e` variables.

---

## IX. Test data & placeholders

### Excel case files — `data/test_cases/*.xlsx`

One row per test case. Required columns:

| Column | Description |
| --- | --- |
| `case_no` | Unique case id (used as the Pytest param id). |
| `description` | Human-readable description. |
| `status` | Only rows with `Done` are executed. |
| `role` | Which session to use: `admin` / `student` / `teacher`. |
| `method` | HTTP method: `GET` / `POST` / `PUT` / `PATCH` / `DELETE`. |
| `api` | Endpoint path (e.g. `/api/roles/{role_01_id}`). |
| `request_body` | JSON body (or `null`). |
| `expected_result` | JSON like `{"status_code": 200, "name": "..."}`. |

Columns `result`, `detail`, `datetime`, `actual_result` are added at runtime.

### Placeholders

Resolved by `helpers/replace_data_by_setup_values.py` before the request:

| Placeholder | Resolves to |
| --- | --- |
| `{some_key}` / `{[some_key]}` | Value from the fixture `pre_data` dict. |
| `{random_string(n)}` | Random string of length `n`. |
| `{datetime(%Y-%m-%d,0)}` | Timestamp with format + hour offset. |

### Request-body templates — `data/request_body_template/*.json`

Define reusable `predata` payloads and the list of records to `need_clear`
(cleaned up before each run so tests are repeatable).

---

## X. Adding a new module / test case

### Add a new endpoint (e.g. `course`)

1. **Wrapper** — `apis/course_apis.py`: one method per endpoint, returns a `Response`
   (mirror `apis/role_apis.py`).
2. **Processor** — `process_responses/course_process_response.py`: call the wrapper,
   pass through `validate_response()`, return parsed JSON (mirror
   `role_process_responses.py`). Export it from `process_responses/__init__.py`.
3. **Wire into `User`** — expose the processor on `common/user.py`.
4. **Templates** — add `data/request_body_template/course_request_body_template.json`.
5. **Cases** — add `data/test_cases/course_test_cases.xlsx` with the columns above.
6. **Fixture** — `case_setup/course_case_setup.py` builds `pre_data` (mirror
   `role_case_setup.py`).
7. **Test** — `testcases/test_course.py` (mirror `test_role.py`).
8. **Marker** — register `course` in `pytest.ini`.

### Add a single test case

Add a row to the relevant Excel file with `status = "Done"`, fill
`method` / `api` / `request_body` / `expected_result`, and run
`uv run pytest -m <module>`.

> Keep changes **localized** — never call `requests` directly from `testcases/`;
> go through the `Client` so auth, retries, and logging stay consistent.

---

## XI. Reports & logs

| Output | Location | Notes |
| --- | --- | --- |
| Console + file logs | stdout / `logs/<date>.log` | loguru, with function + line context. |
| Allure results | `allure-results/` | Feed to `allure generate` / `allure serve`. |
| Failed cases | `reports/failed_cases/fail_case_<timestamp>.txt` | One block per failed case with details. |
| pytest-html | per `--html=` flag | Self-contained HTML report. |

---

## XII. CI / CD

### CI — `.github/workflows/ci.yaml`

Runs on pull requests to `main` and `staging`, and on pushes to `main`:

1. Install `uv` (Python from `.python-version`).
2. `uv sync --dev`.
3. `uv run ruff check .` + `uv run ruff format --check .`.
4. `uv run pytest` (with coverage) — uploads reports on failure.
5. **Build the Docker test-runner image** (no push) to validate the `Dockerfile`.

### CD — `.github/workflows/cd.yaml`

Runs **nightly**, on **push to `main` / version tags**, and **manually** (choose
environment + marker):

1. **Build & push** the test-runner image to GitHub Container Registry
   (`ghcr.io/<owner>/<repo>`), tagged `latest`, `<branch>`, `<sha>`, and SemVer on tags.
2. Log in to GHCR (same job flow) and **run the regression inside the container**
   (`docker run`) against the resolved `BASE_URL`.
3. Generate the Allure report from the mounted `allure-results/`.
4. Publish it to the **`gh-pages`** branch.

**One-time setup:**
- Set **Settings → Pages → Source = "Deploy from a branch", branch `gh-pages` / root**.
- The GHCR package is published from this workflow using `GITHUB_TOKEN` (`packages: write`).
- Optional repo **Variables**: `STAGING_BASE_URL`, `PROD_BASE_URL`.

The report is served at `https://<owner>.github.io/<repo>/`; the image at
`ghcr.io/<owner>/<repo>:latest`.

---

## XIII. Code quality

```powershell
uv run ruff check .      # lint
uv run ruff format .     # format
```

Follow **PEP8** and **Google-style docstrings** (see `.agents/skills/python.md`).

---

## XIV. Troubleshooting

| Symptom | Cause / fix |
| --- | --- |
| `TypeError` on `os.path.join(None, ...)` at import | `.env` missing or `LOG_FOLDER`/`REPORT_FOLDER` not set. Create `.env` (section VII) or export those env vars. |
| `pytest: command not found` | Run via `uv run pytest`, or activate the venv first. |
| `ModuleNotFoundError` | Run `uv sync` (or `uv pip install -r requirements.txt`). |
| `PytestUnknownMarkWarning` | Register the new marker in `pytest.ini`. |
| Login fails / `401` | Check `BASE_URL` and the accounts in `configs/user_info.json`. |
| `allure: command not found` | Install the Allure CLI (`npm install -g allure-commandline`). |
| Docker build fails on the lockfile / "package" | Run `uv lock --dev` and rebuild, or ensure `[tool.uv] package = false` is present. |
| Tests mutate data / flaky | Add the created names to `need_clear` in the module template so runs are repeatable. |

---

## XV. Related projects

- **Capstone project** (cloned, used for testing):
  - FE: https://github.com/pannguyen2001/datn-fe
  - BE: https://github.com/pannguyen2001/datn-be
  - App: https://datn-fe-sooty.vercel.app
- **Generate data tool** (auto-generate correct data into the DB):
  - https://github.com/pannguyen2001/gen_data_tool
- **API testing (v1):** https://github.com/pannguyen2001/api_test_cap_prj/
- **API testing (v2, Pytest + Allure):** https://github.com/pannguyen2001/api_test_cap_prj_v2
- **UI testing (Selenium):** upcoming
