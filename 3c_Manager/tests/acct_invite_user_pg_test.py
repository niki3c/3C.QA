"""
click on username->settings to display the Invite User page
Run test in all 3 browsers
"""
import os

from playwright.sync_api import Playwright, sync_playwright, expect
from common_functions import display_initial_page, login_to_manager
from dotenv import load_dotenv
load_dotenv()

def test_display_org_pg(playwright):
    valid_username = os.getenv("STAGE_MANAGER_TESTING_USERNAME")
    valid_password = os.getenv("STAGE_MANAGER_TESTING_PW")

    # Convert the returned string to a boolean
    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "True").strip().lower() == "true"

    # Initialize page and browser
    page, browser, context, stage_manager_url = display_initial_page(
        playwright, os.getenv("BROWSER"), headless_mode, 'login', 500)

    login_to_manager(page, valid_username, valid_password)
    # Click on Users, in the left menu
    page.get_by_role("link", name="Users").click()
    # Click the Invite User button
    page.get_by_label("false").click()
    # Verify the correct page is displayed
    expect(page.locator("#presentation-layout")).to_contain_text("Invite User")


    # ---------------------
    context.close()
    browser.close()

# with sync_playwright() as pw:
#     test_display_org_pg(pw)
