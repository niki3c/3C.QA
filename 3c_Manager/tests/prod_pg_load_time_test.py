"""
Measure the time it takes to display the Products page,
starting at login.
"""
import os
import time

from playwright.sync_api import sync_playwright, expect
from common_functions import display_initial_page
from dotenv import load_dotenv
load_dotenv()

def test_product_pg_load_time(playwright):
    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"
    # Test all three browsers
    # browser_types = ['chromium', 'firefox', 'webkit']
    # for browser_type in browser_types:
    start_time = time.time()
    valid_username = os.getenv("STAGE_MANAGER_TESTING_USERNAME")
    page, browser, context, stage_manager_url = display_initial_page(playwright, os.getenv("BROWSER"),
                                                                     headless_mode, 'login', 500)
    valid_password = os.getenv("STAGE_MANAGER_TESTING_PW")
    # Verify we are on the correct page
    expect(page.get_by_text("Log in to your account")).to_be_visible()
    # Enter username and pw
    page.locator("#login-app input[type=\"text\"]").fill(valid_username)
    page.locator("input[type=\"password\"]").fill(valid_password)
    # Click the Continue button
    page.get_by_label("tc-button").nth(2).click()
    # Verify that we are on the Products page
    expect(page.locator("#presentation-layout")).to_contain_text("Products")
    # Wait for page to completely load
    page.wait_for_load_state('load')
    end_time = time.time()
    total_load_time = (end_time - start_time) * 1000
    print(f"Page load time for {os.getenv("BROWSER")}: {total_load_time:.2f} ms")

    # Clean up
    context.close()
    browser.close()



# with sync_playwright() as pw:
#     test_product_pg_load_time(pw)