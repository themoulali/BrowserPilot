"""Automated tests for the included offline login demo."""
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEMO_PAGE = PROJECT_ROOT / "demo_site" / "index.html"


@pytest.fixture()
def page():
    """Launch a fresh Chromium page for each test and always close it."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        browser_page = browser.new_page(viewport={"width": 1280, "height": 800})
        browser_page.set_default_timeout(5000)
        browser_page.goto(DEMO_PAGE.resolve().as_uri(), wait_until="load")
        yield browser_page
        browser.close()


def test_page_title_is_correct(page):
    assert page.title() == "BrowserPilot | Automation Demo"


def test_successful_login_shows_welcome_message(page):
    page.get_by_label("Username").fill("student")
    page.get_by_label("Password").fill("Playwright123!")
    page.get_by_role("button", name="Sign in").click()

    message = page.get_by_role("status")
    assert message.is_visible()
    assert message.inner_text() == "Welcome, student! Login successful."


def test_invalid_login_shows_error_message(page):
    page.get_by_label("Username").fill("student")
    page.get_by_label("Password").fill("wrong-password")
    page.get_by_role("button", name="Sign in").click()

    message = page.get_by_role("status")
    assert message.is_visible()
    assert message.inner_text() == "Login failed. Check your username and password."


def test_password_input_is_masked(page):
    assert page.get_by_label("Password").get_attribute("type") == "password"


def test_login_button_is_available(page):
    assert page.get_by_role("button", name="Sign in").is_visible()
