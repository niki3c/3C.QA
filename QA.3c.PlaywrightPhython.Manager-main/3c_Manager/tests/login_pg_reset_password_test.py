import os
from common_functions import display_initial_page
from playwright.sync_api import sync_playwright, expect
from dotenv import load_dotenv
import pytest

load_dotenv()


def test_reset_password(playwright):
    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"
    # test it in all 3 browsers
    # browser_types = ['chromium', 'firefox', 'webkit']
    # for browser_type in browser_types:
    # Had to increase the delay to 500 because webkit is too slow
    # page, browser, context, stage_manager_url = display_initial_page(pw1, browser_type, headless_mode,'login', 500)
    page, browser, context, stage_manager_url = display_initial_page(playwright, os.getenv("BROWSER"), headless_mode, 'login',500)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    # Let's try this 3 times, quickly
    for i in range(3):
        # Verify we are on the correct page
        expect(page.get_by_text("Log in to your account")).to_be_visible()
        # Click the Reset Password link
        page.get_by_role("link", name="Reset password").click()
        #  Verify we are on the correct page
        expect(page.locator("#app")).to_contain_text("Enter your email to reset Password")
        # Enter a bogus email address
        page.get_by_placeholder("Enter your email address").fill("asdfasdfasdf@ddd.com")
        # click the submit button
        page.get_by_label("tc-button").click()
        # Now click the Back to Log in link
        page.locator("button").filter(has_text="Back to Log in").click()
        # See if we returned to the correct page, if so, we're done
        expect(page.get_by_text("Log in to your account")).to_be_visible()

    # Stop tracing and save the output
    context.tracing.stop(path="traces/trace.zip")
    # Cleanup
    context.close()
    browser.close()

# with sync_playwright() as pw:
#      test_reset_password(pw)
