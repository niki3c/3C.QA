import os
from common_functions import display_initial_page
from playwright.sync_api import sync_playwright, expect
from dotenv import load_dotenv
import allure
from allure_commons.types import AttachmentType

load_dotenv()

def test_reset_password(playwright):
    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "true").strip().lower() == "true" 

    # Initialize page and browser
    page, browser, context, stage_manager_url = display_initial_page(
        playwright, os.getenv("BROWSER"), headless_mode, 'login', 500)

    # Enable tracing for additional debugging if needed
    context.tracing.start(screenshots=False, snapshots=True, sources=True)

    try:
        # Let's try this 3 times
        for i in range(3):
            # Verify we are on the correct page
            expect(page.get_by_text("Log in to your account")).to_be_visible()

            # Capture a screenshot and attach it to the Allure report
            # screenshot = page.screenshot(path=f"screenshot_login_step_{i}.png")
            # allure.attach.file(f"screenshot_login_step_{i}.png", name=f"Login Page Step {i}", attachment_type=AttachmentType.PNG)

            # Click the Reset Password link
            page.get_by_role("link", name="Reset password").click()

            # Verify we are on the correct page
            # expect(page.locator("#app")).to_contain_text("Enter your email to reset Password")

            # Capture another screenshot
            # screenshot = page.screenshot(path=f"screenshot_reset_password_step_{i}.png")
            # allure.attach.file(f"screenshot_reset_password_step_{i}.png", name=f"Reset Password Step {i}", attachment_type=AttachmentType.PNG)

            # Enter a bogus email address
            page.get_by_placeholder("Enter your email address").fill("asdfasdfasdf@ddd.com")

            # Click the submit button
            page.get_by_label("tc-button").click()

            # Capture a screenshot after submitting
            # screenshot = page.screenshot(path=f"screenshot_after_submit_{i}.png")
            # allure.attach.file(f"screenshot_after_submit_{i}.png", name=f"After Submit Step {i}", attachment_type=AttachmentType.PNG)

            # Now click the Back to Log in link
            page.locator("button").filter(has_text="Back to Log in").click()

            # See if we returned to the correct page, if so, we're done
            expect(page.get_by_text("Log in to your account")).to_be_visible()

            # Capture a final screenshot
            # screenshot = page.screenshot(path=f"screenshot_final_login_{i}.png")
            # allure.attach.file(f"screenshot_final_login_{i}.png", name=f"Final Login Step {i}", attachment_type=AttachmentType.PNG)

    finally:
        # Stop tracing and save the output
        context.tracing.stop(path="traces/trace.zip")

        # Cleanup
        context.close()
        browser.close()

