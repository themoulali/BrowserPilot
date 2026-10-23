"""Reusable Playwright browser automation with logging and safe error handling."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from playwright.sync_api import (
    Browser,
    Error as PlaywrightError,
    Page,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
SCREENSHOT_DIR = ARTIFACTS_DIR / "screenshots"
LOG_DIR = ARTIFACTS_DIR / "logs"
DEMO_PAGE = PROJECT_ROOT / "demo_site" / "index.html"


def configure_logging(log_file: Path | None = None) -> logging.Logger:
    """Configure console and file logging; repeated calls do not duplicate handlers."""
    destination = log_file or (LOG_DIR / "automation.log")
    destination.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("browserpilot")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        file_handler = logging.FileHandler(destination, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(console)
        logger.addHandler(file_handler)
    return logger


def capture_screenshot(page: Page, name: str = "page.png") -> Path:
    """Save a full-page screenshot and return its path."""
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    target = SCREENSHOT_DIR / name
    try:
        page.screenshot(path=str(target), full_page=True)
    except (PlaywrightError, OSError) as exc:
        configure_logging().exception("Could not save screenshot to %s", target)
        raise RuntimeError(f"Screenshot capture failed: {target}") from exc
    configure_logging().info("Screenshot saved: %s", target)
    return target


def run_login_demo(
    username: str = "student",
    password: str = "Playwright123!",
    headless: bool = True,
) -> dict[str, Any]:
    """Run the included offline login demo and return a small execution report."""
    logger = configure_logging()
    screenshot_path: Path | None = None
    result: dict[str, Any] = {
        "success": False,
        "page_title": None,
        "welcome_message": None,
        "screenshot": None,
    }

    if not DEMO_PAGE.exists():
        raise FileNotFoundError(f"Demo HTML page was not found: {DEMO_PAGE}")

    logger.info("Starting Playwright login demo")
    try:
        with sync_playwright() as playwright:
            browser: Browser = playwright.chromium.launch(headless=headless)
            try:
                page = browser.new_page(viewport={"width": 1280, "height": 800})
                page.set_default_timeout(5000)
                page.goto(DEMO_PAGE.resolve().as_uri(), wait_until="load")
                result["page_title"] = page.title()
                logger.info("Opened demo page: %s", result["page_title"])

                page.get_by_label("Username").fill(username)
                page.get_by_label("Password").fill(password)
                page.get_by_role("button", name="Sign in").click()

                message = page.locator("#status-message")
                message.wait_for(state="visible")
                result["welcome_message"] = message.inner_text()
                result["success"] = "Welcome" in result["welcome_message"]
                screenshot_path = capture_screenshot(page, "login-success.png")
                result["screenshot"] = str(screenshot_path)
                logger.info("Login flow finished; success=%s", result["success"])
                return result
            finally:
                browser.close()
                logger.info("Browser closed")
    except PlaywrightTimeoutError as exc:
        logger.exception("Timed out while automating the login demo")
        raise RuntimeError("Automation timed out. Check selectors and browser setup.") from exc
    except PlaywrightError as exc:
        logger.exception("Playwright browser automation failed")
        raise RuntimeError("Playwright could not complete the browser task.") from exc
    except Exception:
        logger.exception("Unexpected error during browser automation")
        raise


if __name__ == "__main__":
    report = run_login_demo()
    print("\nAutomation report")
    for key, value in report.items():
        print(f"{key}: {value}")
