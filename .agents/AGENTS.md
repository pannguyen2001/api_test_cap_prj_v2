# AGENTS.md

Compact guidance for AI sessions in this repo. Every line is something an
agent would likely miss without help.

**Goal:** This repo is an **API Testing Framework** (Python + Pytest) for the
capstone `datn-be` backend — not a security scanner or cyber tool.

## Read first
- `RULE.md` is the authoritative behavior contract for the AI in this repo.
  Its core sections (§1–§6: truth-over-comfort, no unauthorized actions,
  no hardcoded secrets, quality/style, AI role/response modes) are
  non-negotiable and apply to every session.
- `./skills/python.md` holds the Python + Pytest domain rules for this repo —
  follow it for all code work (RULE.md §8).
- `README.md` is the authoritative project guide: features, setup, folder
  structure, and run commands.
- Action gate: propose changes/commands first, then wait for explicit approval.
  Never run commands or edit files on the assumption it is wanted (RULE.md §1/§6).

## Repo state
- **Repo Context:** API Automation stack built on **Pytest**, driving a real
  backend (`BASE_URL` from `.env`).
- **Current Goal:** Data-driven functional/integration tests for REST endpoints
  (happy, edge, boundary) plus reusable framework layers.
- **Primary Stack:** Python **3.14**, `pytest`, `requests` (synchronous),
  `pandas`, `openpyxl` + `python-calamine` (Excel), `allure-pytest`,
  `pytest-html`, `pytest-xdist`, `loguru`, `python-dotenv`, `pytz`.
- **Tooling:** `uv` for env/deps; **Ruff** for lint + format; Git + GitHub
  Actions (`.github/workflows/ci.yaml`).
- **Status:** Working framework — `apis/`, `common/`, `process_responses/`,
  `case_setup/`, `configs/`, `helpers/`, `testcases/`, `data/` are all present.
- **Not used here (do not introduce silently):** `httpx`, `pytest-asyncio`,
  `factory_boy`/`faker`, `respx`/`responses`, FastAPI, MongoDB/`pymongo`,
  Docker. The stack is synchronous `requests` + Excel-driven cases.

## Architecture (layered — respect boundaries)
- `apis/` — thin endpoint wrappers returning raw `requests.Response`.
- `common/` — `Client` (session, headers/token, retry adapter, login/logout) and
  `User` (client + response processors).
- `process_responses/` — business-level calls that `validate_response()` and
  return parsed JSON.
- `case_setup/` — per-module fixtures building `pre_data` (ids, names).
- `configs/` — `.env` loading, enums (`ROLE`, `APIMETHOD`, `FILETYPE`).
- `helpers/` — `load_data`, `run_case`, assertion helpers, `retry`, `logger`,
  placeholder replacement.
- `testcases/` — `test_*.py` + shared `conftest.py` fixtures
  (`admin`/`student`/`teacher`). Orchestrate only; no direct HTTP.
- `data/` — Excel test cases + JSON request-body templates.

## Conventions (verified from RULE.md + ./skills/python.md)
- Secrets/credentials/URLs live in `.env` via `configs/constants.py`, never
  hardcoded, never committed (§1/§6).
- Python style: PEP8 + Google docstrings, formatted/linted with Ruff.
- Tests: data-driven from `data/test_cases/*.xlsx`, filtered to `status == "Done"`,
  parametrized by `case_no`, delegated to `helpers.run_case.run_case`; per-module
  markers registered in `pytest.ini`. Target the 80% highest-value cases — happy,
  edge, boundary — no duplication, no flaky tests; follow the test pyramid (§2).
- New endpoint = a method in `apis/` **and** a matching method in
  `process_responses/`; reuse `helpers/` before writing new code.
- Response mode depends on request: **review** = analyze trade-offs before fixing;
  **debug** = give the fix immediately, then explain (§4).
