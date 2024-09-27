"""
Login then click on Customer Coaching tab
Exercise the filters
"""
import os
from playwright.sync_api import Playwright, sync_playwright, expect
from common_functions import display_initial_page
from dotenv import load_dotenv
load_dotenv()

def filter_the_products(pg):
    pg.locator(".ant-select-selection-overflow").click()
    pg.get_by_title("SellerRunning", exact=True).locator("div").click()
    pg.get_by_title("SmartRepricer", exact=True).locator("div").click()
    pg.get_by_title("InventoryLab", exact=True).locator("div").click()


def test_display_cust_coaching_pg(playwright):
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

    # Click on Customer Coaching, in the left menu
    page.get_by_role("link", name="Customer Coaching").click()

    # Filter the available products
    filter_the_products(page)

    # Clear the filters by click the Clear button
    page.locator("button").filter(has_text="Clear").click()

    # ---------------------
    context.close()
    browser.close()
