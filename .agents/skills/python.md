---
name: python
description: Python + Pytest conventions for the API testing framework in this repo
disable-model-invocation: false
---

# Python & Pytest Skill — API Testing Framework

You are an expert in **Python API automation testing** with **Pytest**, `requests`,
`pandas`, `allure-pytest`, and `loguru`. This skill supplements `RULE.md` for all
Python work in this repo (see `RULE.md` §8). Read `README.md` for the full project
guide before proposing structural changes.

## Core Principles

- Concise, technical responses with runnable, copy-pasteable Python examples.
- Follow **PEP8**, use **Google-style docstrings**, and format/lint with **Ruff**
  (`ruff check .` and `ruff format .` — the same commands the CI runs).
- Add type hints to every function signature (`from typing import Dict, List, ...`);
  all existing modules already annotate. Prefer built-in generics (`list`, `dict`)
  only when the file already uses them — otherwise stay consistent with the file.
- Keep pure, stateless utilities in `helpers/`; use classes only for stateful
  components (`Client`, `User`, `AccountResponse`, `RoleProcessResponse`), matching
  the current design. Reuse existing helpers before writing new ones.
- Descriptive names with auxiliary verbs (`is_valid`, `has_token`); `snake_case` for
  files and directories (`account_apis.py`, `setup_test_case.py`).
- Never hardcode secrets, tokens, or environment-specific values — read them from
  `.env` through `configs/constants.py` (`RULE.md` §1/§6). Never commit `.env`.

## Layered Architecture (respect these boundaries)

| Layer | Directory | Responsibility |
| --- | --- | --- |
| Endpoint wrappers | `apis/` | Thin, one method per endpoint, returns a raw `requests.Response`. No assertions, no business logic. |
| HTTP client / session | `common/client.py`, `common/user.py` | Session, headers/token, retry-adapter, `login()`/`logout()`, role/email state. |
| Response processing | `process_responses/` | Business-level calls that `validate_response()` and return parsed JSON (e.g. `create_new_account_with_check`). |
| Per-module fixtures | `case_setup/` | Pytest fixtures that build `pre_data` (ids, names) for a module. |
| Config | `configs/` | `.env` loading, enums (`ROLE`, `APIMETHOD`, `FILETYPE`), constants. |
| Reusable utilities | `helpers/` | `load_data`, `run_case`, assertion helpers, `retry`, `logger`, placeholder replacement. |
| Tests | `testcases/` | `test_*.py` + `conftest.py` fixtures. Orchestrate, do not re-implement HTTP. |

Rule of thumb: a new endpoint = a method in `apis/` **and** a method in the matching
`process_responses/` class. Do not call `requests` directly from `testcases/`.

## Pytest Conventions

- Test files are named `test_*.py` under `testcases/`; test paths/markers live in
  `pytest.ini` (`testpaths = testcases`).
- Tests are **data-driven**: load an Excel case file with `helpers.load_data.load_data`,
  filter to `status == "Done"`, then `@pytest.mark.parametrize` over the rows with
  `ids=[i["case_no"] for i in cases]` and delegate to `helpers.run_case.run_case`.
- Register a marker per module in `pytest.ini` (`role`, `account`, ...) and apply it
  plus the matching `case_setup` fixture. Session-scoped fixtures (`admin`,
  `student`, `teacher`) live in `testcases/conftest.py`.
- Assertions for data-driven cases go through `helpers/run_case.py` helpers
  (`assert_status_code`, `assert_key_value`, `assert_data_value`,
  `assert_error_response`) so failures are logged and recorded consistently.
  Use plain `assert` only in genuine unit tests.
- Target the 80% highest-value cases — happy path, edge, boundary — no duplication,
  no flaky tests; follow the test pyramid (`RULE.md` §2).

## Test Data & Placeholders

- Case definitions live in `data/test_cases/*.xlsx`; request templates live in
  `data/request_body_template/*.json`. Columns include `status`, `case_no`,
  `description`, `role`, `method`, `api`, `request_body`, `expected_result`.
- Inject dynamic values with the existing placeholder syntax resolved by
  `helpers/replace_data_by_setup_values.py`:
  - `{some_key}` — replaced from the fixture `pre_data` dict.
  - `{random_string(n)}` — random string of length `n`.
  - `{datetime(%Y-%m-%d %H:%M:%S,<hours_delta>)}` — timestamp with offset.
- Prefer `pandas` for tabular case handling (already the standard) and `openpyxl` /
  `python-calamine` engines for Excel. Keep generated data deterministic where a
  test asserts on it.

## HTTP & Error Handling

- Use the shared `Client` (`common/client.py`) — it owns the `requests.Session`,
  auth header, and the mounted retry adapter. Do not create ad-hoc sessions.
- Pass parsed JSON via `validate_response()` rather than calling `res.json()`
  everywhere; it centralises the `status_code >= 400` guard.
- Guard clauses first, early returns for invalid input, happy path last; keep the
  existing style.
- Raise/log through the project wrappers: `logger_wrapper` (log + `pytest.exit` on
  unexpected exception), `retry(...)` for transient network calls, and `loguru`
  structured context (`module`, `function`, parameters) instead of `print`.
- Logs and Allure reports must be detailed enough to diagnose a failure from the
  output alone (`RULE.md` §2).

## Logging & Reporting

- Import the shared logger from `helpers.logger` (configures `loguru` sinks to
  stdout and the daily file under `LOG_FOLDER`). Never use `print` in library code.
- Use `logger.info/success/warning/error` with the existing `{:=^50}` banner style
  for phase boundaries.
- Reports: `allure-pytest` (primary), `pytest-html`, and `pytest-xdist` for parallel
  runs. Failed cases are also written to `REPORT_FOLDER/failed_cases/*.txt` via
  `helpers/record_failed_case.py`.

## Dependencies

- Keep `requirements.txt` and `pyproject.toml` in sync; install with
  `uv pip install -r requirements.txt` (uv is the project/CI tool).
- Current stack: `requests`, `pytest`, `pytest-html`, `pytest-xdist`,
  `allure-pytest`, `loguru`, `pandas`, `openpyxl`, `python-calamine`, `pytz`,
  `python-dotenv`.
- This project is **synchronous** (`requests`), with no async test layer. Do not
  introduce `httpx`, `pytest-asyncio`, `factory_boy`, `respx`, or a DB driver
  without an explicit team decision — prefer the existing helpers.

## Run Commands

```powershell
uv sync                                     # create env + install deps (uv.lock)
uv run python main.py                       # run via main.py entrypoint
uv run pytest -m <mark>                     # by module marker (role/account/...)
uv run pytest testcases/<test_file_name>.py # a single file
uv run ruff check .; uv run ruff format .   # lint & format (same as CI)
uv run pytest --alluredir=allure-results --clean-alluredir
allure generate allure-results -o allure-report --clean
allure serve allure-results
```
