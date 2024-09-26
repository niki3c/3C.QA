"""
Verifies that the Terms and Conditions AND the Privacy Policy
pages are displayed when clicking on the links at the bottom
of the Registration page.
"""
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, expect
from common_functions import display_initial_page
load_dotenv()


def test_verify_terms_of_agreement(playwright):
    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"
    # test it in all 3 browsers
    # browser_types = ['chromium', 'firefox', 'webkit']
    # for browser_type in browser_types:
    page, browser, context, stage_manager_url = display_initial_page(playwright, os.getenv("BROWSER"),
                                                                     headless_mode,'reg', 500)
    with page.expect_popup() as page3_info:
        page.get_by_role("link", name="Terms").click()
    page3 = page3_info.value
    expect(page3.locator("body")).to_contain_text("Threecolts LLC Terms Of Use Agreement")
    page3.close()

    # ---------------------
    context.close()
    browser.close()


def test_verify_privacy_policy(playwright):
    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"
    # browser_types = ['chromium', 'firefox', 'webkit']
    # for browser_type in browser_types:
    page, browser, context, stage_manager_url = display_initial_page(playwright, os.getenv("BROWSER"),
                                                                     headless_mode,'reg', 500)
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Privacy Policy").click()
    page1 = page1_info.value
    expect(page1.locator("body")).to_contain_text("Threecolts LLC Privacy Policy")
    page1.close()

    # ---------------------
    context.close()
    browser.close()

# with sync_playwright() as pw:
#     test_verify_terms_of_agreement(pw)
#     test_verify_privacy_policy(pw)

