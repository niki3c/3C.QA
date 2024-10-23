"""
Uses a unique username and password to sign up a new user.
"""
import os

from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv

from common_functions import display_initial_page, unique_credentials

load_dotenv()

def test_valid_signup(playwright) -> None:
    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"
    # test it in all 3 browsers
    # browser_types = ['chromium', 'firefox', 'webkit']
    # for browser_type in browser_types:
    email, fullname, userpass = unique_credentials()
    page, browser, context, stage_manager_url = display_initial_page(playwright, os.getenv("BROWSER"),
                                                                     headless_mode, 'login', 500)
    page.get_by_role("link", name="Sign up").click()
    # Verify the "Get started..." page is displayed
    expect(page.get_by_text("Get started in minutes")).to_be_visible()
    # Enter user's email
    page.get_by_role("textbox").fill("testNiki111@yopmail.com")
    page.locator("button").filter(has_text="Continue with email").click()
    # Verify the Welcome to Threecolts page is displayed
    expect(page.get_by_text("Welcome to Threecolts!")).to_be_visible()
    # Verify that the correct email is displayed above the
    # Enter your full name field.
    expect(page.locator("#app")).to_contain_text(f"You’re registering as {email}")
    # Enter user's name
    page.locator("#app input[name=\"full_name\"]").fill('Niki Test')
    # enter user's pw and confirm
    page.locator("input[name=\"password\"]").fill('testNiki111@yopmail.com')
    # Confirm pw
    page.locator("input[name=\"confirm_password\"]").fill('testNiki111@yopmail.com')
    # Click the Continue button
    page.get_by_label("tc-button").click()
    # Click the Skip button
    #====NEW===
    page.locator("button").filter(has_text="Skip").wait_for(state="visible", timeout=10000)
    #page.locator("button").filter(has_text="Skip").click()
    # Verify that we are on the Products page
    
    #====ERROR HERE=====
    expect(page.locator("#presentation-layout")).to_contain_text("Products")
    # Sign out
    page.get_by_role("button", name=fullname).click()
    page.locator("a").filter(has_text="Sign Out").click()
    # Clean up
    context.close()
    browser.close()


# with sync_playwright() as pw:
#     test_valid_signup(pw)
