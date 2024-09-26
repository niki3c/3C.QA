"""
Attempts to log in to 3c Manager with invalid credentials
Eventually logs in with valid credentials
"""
import os
from playwright.sync_api import sync_playwright, expect
from common_functions import sign_out_of_manager, is_button_disabled, display_initial_page
from dotenv import load_dotenv
load_dotenv()

def test_verify_credentials(playwright):
    valid_username = os.getenv("STAGE_MANAGER_TESTING_USERNAME")
    valid_password = os.getenv("STAGE_MANAGER_TESTING_PW")
    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"
    # Create invalid credentials
    invalid_user = "Ringo Star"
    invalid_pw = "WithALittleHelpFromMyFriends"
    # Test all three browsers
    # browser_types = ['chromium', 'firefox', 'webkit']
    # for browser_type in browser_types:
    page, browser, context, stage_manager_url = display_initial_page(playwright, os.getenv("BROWSER"),
                                                                     headless_mode, 'login', 500)
    # Verify we are on the correct page
    expect(page.get_by_text("Log in to your account")).to_be_visible()
    invalid_username_invalid_pw(page, invalid_user, invalid_pw)
    page.reload()
    empty_username_valid_pw(page, valid_password)
    page.reload()
    valid_username_empty_pw(page, valid_username)
    page.reload()
    invalid_username_valid_pw(page, valid_password)
    page.reload()
    valid_username_empty_pw(page, valid_username)
    page.reload()
    valid_username_valid_pw(page, valid_username, valid_password)

    # Cleanup
    context.close()
    browser.close()

def invalid_username_invalid_pw(page, username, password):
    page.locator("#login-app input[type=\"text\"]").fill(username)
    page.locator("input[type=\"password\"]").fill(password)
    # Click the Login button, do we get the error message
    page.get_by_label("tc-button").nth(2).click()
    expect(page.get_by_role("list")).to_contain_text("Invalid email or password. Please try again", timeout=500)

def valid_username_valid_pw(page, valid_username, valid_password):
    page.locator("#login-app input[type=\"text\"]").fill(valid_username)
    page.locator("input[type=\"password\"]").fill(valid_password)
    # Click the Continue button
    page.get_by_label("tc-button").nth(2).click()
    # Verify that we are on the Products page
    expect(page.locator("#presentation-layout")).to_contain_text("Products")
    # Sign out
    sign_out_of_manager(page, valid_username)

def empty_username_valid_pw(page, valid_pw): ####
    # Clear the field
    page.locator("#login-app input[type=\"text\"]").fill("")
    page.locator("input[type=\"password\"]").fill(valid_pw)
    # The continue button should not be enabled
    state = is_button_disabled(page, '[aria-label="tc-button"] >> nth=2')
    if state:
        pass  # It is supposed to disabled so do nothing
    else:
        raise Exception('The Continue button is ENABLED!!!')

def valid_username_empty_pw(page, valid_user): ####
    page.locator("#login-app input[type=\"text\"]").fill(valid_user)
    page.locator("#login-app input[type=\"password\"]").fill("")
    # The continue button should not be enabled
    state = is_button_disabled(page, '[aria-label="tc-button"] >> nth=2')
    if state:
        pass  # It is supposed to disabled so do nothing
    else:
        raise Exception('The Continue button is ENABLED!!!')

def invalid_username_valid_pw(page, valid_pw): ####
    page.locator("#login-app input[type=\"text\"]").fill("HumpyDumpty12%")
    page.locator("#login-app input[type=\"password\"]").fill(valid_pw)
    # Click the Login button, do we get the error message
    page.get_by_label("tc-button").nth(2).click()
    expect(page.get_by_role("list")).to_contain_text("Invalid email or password. Please try again", timeout=500)

def valid_username_invalid_pw(page, valid_user): ####
    page.locator("#login-app input[type=\"text\"]").fill(valid_user)
    page.locator("#login-app input[type=\"password\"]").fill("Threecolts")

    expect(page.get_by_role("list")).to_contain_text("Invalid email or password. Please try again")

# with sync_playwright() as pw:
#     verify_credentials(pw)