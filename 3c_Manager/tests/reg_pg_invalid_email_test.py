"""
1. Navigates to https://dev1-manager.threecolts.com/v2/register
2. Enters a properly formatted email address
3. Iterates though invalid characters and inject them into the
Local Part of the email address while ensuring that an error
message is displayed.
4. Does the same thing for the Domain Part of the email address
"""
import os
from playwright.sync_api import sync_playwright, expect
from common_functions import unique_credentials, display_initial_page
from dotenv import load_dotenv
load_dotenv()

def test_check_for_invalid_email(playwright):
    """
    Iterates through invalid chars that are injected into the email address
    and verifies that an error message is displayed.
    """
    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"
    invalid_local_part_characters = [' ','<','>','(',')',":", ';', '@','£','¿']
    invalid_domain_part_characters = ['!','#','$','%','&',"'",'*','+','/','=','?','^','_','{','}','|','~']
    # test it in all 3 browsers
    # browser_types = ['chromium', 'firefox', 'webkit']
    # for browser_type in browser_types:
    page, browser, context, stage_manager_url = display_initial_page(playwright, os.getenv("BROWSER"),
                                                                     headless_mode, 'reg', 500)
    # used for testing
    myemail = 'anybody@mydomain.com'
    # Verify we're on the correct page
    expect(page.get_by_text("Get started in minutes")).to_be_visible()
    # Iterate through the invalid characters
    char: str
    for char in invalid_local_part_characters:
        try:
            invalid_email = myemail[:3] + char + myemail[3:]
            page.locator("#app input[type=\"text\"]").fill(invalid_email)
            # need to click outside the field since the error message is
            # presented on blur
            page.locator(".section-content").click()
            # Now check for error message
            expect(page.get_by_role("tooltip")).to_contain_text("Please enter a valid email")

        except AssertionError as e:
            print(f" ERROR: {e} *** FAILED ON Char: {char} ***")

    # Iterate through the invalid characters
    for char in invalid_domain_part_characters:
        try:
            invalid_email = myemail[:10] + char + myemail[10:]
            page.locator("#app input[type=\"text\"]").fill(invalid_email)
            # need to click outside the field since the error message is
            # presented on blur
            page.locator(".section-content").click()
            # Now check for error message
            expect(page.get_by_role("tooltip")).to_contain_text("Please enter a valid email")

        except AssertionError as e:
            print(f" ERROR: {e} *** FAILED ON Char: {char} ***")

    # Clean up
    context.close()
    browser.close()


# with sync_playwright() as pw:
#    check_for_invalid_email(pw)