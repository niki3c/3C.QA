"""
Iterates though 3 invalid passwords then closes
the browser, if there are no failures
Three browsers are tested
"""
import os
from playwright.sync_api import sync_playwright, expect
from common_functions import unique_credentials, display_initial_page
from dotenv import load_dotenv
load_dotenv()

def test_login_check_for_weak_pw(playwright):
    # Get credentials
    valid_username = os.getenv("STAGE_MANAGER_TESTING_USERNAME")
    valid_password = os.getenv("STAGE_MANAGER_TESTING_PW")
    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"
    # test it in all 3 browsers
    # browser_types = ['chromium', 'firefox', 'webkit']
    # email, fullname, userpass = unique_credentials()
    # for browser_type in browser_types:
    page, browser, context, stage_manager_url = display_initial_page(playwright, os.getenv("BROWSER"),
                                                                     headless_mode, 'login', 500)

    # Verify it is displayed
    expect(page.get_by_text("Log in to your account")).to_be_visible()
    page.locator("#login-app input[type=\"text\"]").fill(valid_username)
    # Define the modified passwords in a dictionary with descriptions
    password_variations = {
        "Password without special symbols": "".join([char for char in valid_password if char.isalnum()]),
        "Password without uppercase letters": valid_password.lower(),
        "Password with less than 12 characters": valid_password[:11]
    }
    pw_field_selector = 'input[type="password"]'
    # Loop through each password variation and enter it into the field
    for description, password in password_variations.items():
        page.locator("#login-app input[type=\"text\"]").fill(valid_username)
        page.fill(pw_field_selector, password)
        # Attempt to log in with the invalid pw
        page.get_by_label("tc-button").nth(2).click()
        # Check for the error message
        expect(page.get_by_role("list")).to_contain_text("Invalid email or password. Please try again")
        page.reload()

    # Clean up
    context.close()
    browser.close()


# with sync_playwright() as pw:
#     login_check_for_weak_pw(pw)

