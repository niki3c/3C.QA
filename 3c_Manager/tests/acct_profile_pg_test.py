"""
click on username->settings to display the My Profile page
Run test in all 3 browsers
"""
import os
from playwright.sync_api import Playwright, sync_playwright, expect
from common_functions import display_initial_page
from dotenv import load_dotenv
load_dotenv()

def test_display_org_pg(playwright):
    valid_username = os.getenv("STAGE_MANAGER_TESTING_USERNAME")
    valid_password = os.getenv("STAGE_MANAGER_TESTING_PW")

    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"

    # Initialize page and browser
    page, browser, context, stage_manager_url = display_initial_page(
        playwright, os.getenv("BROWSER"), headless_mode, 'login', 500)
    page.locator("#login-app input[type=\"text\"]").fill(valid_username)
    page.locator("input[type=\"password\"]").fill(valid_password)
    # Click the Continue button
    page.get_by_label("tc-button").nth(2).click()
    # Click username in upper right corner of page
    page.click("body > div:nth-child(1) > section:nth-child(1) > header:nth-child(1) > div:nth-child(1) > " 
               "div:nth-child(1) > div:nth-child(2) > button:nth-child(4) > span:nth-child(2)")
    page.locator("#threecolts_top_navbar").get_by_role("link", name="My Profile").click()
    expect(page.get_by_role("main")).to_contain_text("My Profile")

    # ---------------------
    context.close()
    browser.close()
