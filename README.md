# BrowserPilot — Python Browser Automation Framework

A submission-ready learning project demonstrating browser automation with **Python, Playwright, logging, screenshots, exception handling, and automated tests**. The demo site is included locally, so the core task does not depend on a public website or network connection.

## Features

- Opens a browser with Playwright Chromium.
- Automates a login form using accessible labels and role-based locators.
- Checks successful and unsuccessful login flows.
- Captures a full-page screenshot.
- Writes logs to the console and `artifacts/logs/automation.log`.
- Handles Playwright timeouts and browser errors with useful messages.
- Includes five automated pytest test cases.
- Uses a local HTML page and demo-only credentials; do not use real account passwords.

## Project structure

```text
BrowserPilot/
├── artifacts/
│   ├── logs/                  # Created when the script runs
│   └── screenshots/           # Screenshot output
├── demo_site/
│   └── index.html             # Local demo login page
├── src/
│   ├── __init__.py
│   └── browser_automation.py  # Automation implementation
├── tests/
│   ├── __init__.py
│   └── test_browser_automation.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer recommended
- pip
- Chromium browser installed through Playwright

## Setup (Windows PowerShell)

Open PowerShell in the extracted project folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
```

If PowerShell blocks activation, you can run the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

## Run the browser automation

From the project root:

```powershell
python -m src.browser_automation
```

Expected result: a browser opens in headless mode, fills the sample login form, submits it, and prints a report with `success: True`, the page title, the welcome message, and screenshot path.

The screenshot is saved as `artifacts/screenshots/login-success.png`. Logs are written to `artifacts/logs/automation.log`.

## Run automated tests

```powershell
python -m pytest -v
```

Expected test cases:

1. Page title is correct.
2. Valid credentials show the welcome message.
3. Invalid credentials show an error message.
4. Password field uses masked input.
5. Login button is visible.

All five tests should pass after dependencies and Chromium are installed.

## Error handling

The automation module:
- Logs the start and completion of the browser flow.
- Converts Playwright timeout and browser errors into readable `RuntimeError` messages while preserving the original cause.
- Closes the browser in a `finally` block.
- Raises a clear `FileNotFoundError` if the local demo page is missing.
- Raises a clear error if screenshot capture fails.

## Test case documentation

| ID | Scenario | Expected result |
|---|---|---|
| TC-01 | Open the demo page | Correct page title |
| TC-02 | Submit valid demo credentials | Welcome message is visible |
| TC-03 | Submit an invalid password | Login failure message is visible |
| TC-04 | Inspect password field | Input type is `password` |
| TC-05 | Inspect sign-in control | Button is visible |

## Submission checklist

- [ ] Install dependencies and Chromium.
- [ ] Run `python -m src.browser_automation`.
- [ ] Confirm `artifacts/screenshots/login-success.png` was created.
- [ ] Run `python -m pytest -v` and confirm all tests pass.
- [ ] Include this README and the complete project folder in your submission.

## Notes

This is an educational demo, not a production authentication system. The credentials are hard-coded only in the local sample page and its test flow. No real user data or external website is accessed.
