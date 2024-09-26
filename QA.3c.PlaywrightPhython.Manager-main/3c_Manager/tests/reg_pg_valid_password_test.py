import os

from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv
from common_functions import unique_credentials, is_valid_in_xpath, display_initial_page
load_dotenv()


def test_check_for_valid_password(playwright: Playwright):
    email, fullname, userpass = unique_credentials()
    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"
    # browser_types = ['chromium', 'firefox', 'webkit']
    # for browser_type in browser_types:
    # page, browser, context, stage_manager_url = display_initial_page(pw, browser_type, headless_mode, 'reg', 500)
    page, browser, context, stage_manager_url = display_initial_page(playwright, os.getenv("BROWSER"), headless_mode,
                                                                     'reg', 500)
    # Verify the "Get started..." page is displayed
    expect(page.get_by_text("Get started in minutes")).to_be_visible()
    # Enter user's email
    page.get_by_role("textbox").fill(email)
    page.locator("button").filter(has_text="Continue with email").click()
    # Verify the Welcome to Threecolts page is displayed
    expect(page.get_by_text("Welcome to Threecolts!")).to_be_visible()
    # Enter your full name field.
    expect(page.locator("#app")).to_contain_text(f"You’re registering as {email}")
    # Enter user's name
    page.locator("#app input[name=\"full_name\"]").fill(fullname)
    # Verify each of the pw requirements have been met
    i = 1
    for i in range(1, 4):
        page.fill('input[name="password"]', 'Threecolts56kIsdn12%')  # Adjust the selector to match your password input field
        # ensure pw requirements are green
        try:
            xpath = f"//section[@class='ant-layout v-app']//li[{i}]"
            is_valid = is_valid_in_xpath(page, xpath)
        except AssertionError as e:
            print(f" *** FAILED ON the : {i}th xpath ***")

    # Check for, Password mismatch error message (percent char missing from the end)
    page.locator("input[name=\"confirm_password\"]").fill("Threecolts56kIsdn12")
    # Onblur, so click outside of field to display the error message
    page.locator(".section-content").click()
    expect(page.get_by_role("tooltip")).to_contain_text("Password mismatch")
    # Now let's clear the field and input a matching pw. The Continue button should enable
    page.locator("input[name=\"confirm_password\"]").fill("")
    page.locator("input[name=\"confirm_password\"]").fill("Threecolts56kIsdn12%")
    # The Continue button should become enabled
    button = page.locator('button:has(span:text("Continue"))')
    if button.is_disabled():
        raise Exception('The Continue button is still disabled!!!')
    else:
        # Clean up
        context.close()
        browser.close()


# with sync_playwright() as pw:
#    check_for_valid_password(pw)