"""
Tests the logic when entering a weak password.
"""
import os
import re
from playwright.sync_api import sync_playwright, expect
from common_functions import unique_credentials, is_valid_in_xpath, display_initial_page
from dotenv import load_dotenv
import allure
from allure_commons.types import AttachmentType

load_dotenv()


def test_reg_check_for_weak_pw(playwright):
    email, fullname, userpass = unique_credentials()

    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"

    page, browser, context, stage_manager_url = display_initial_page(playwright, os.getenv("BROWSER"),
                                                                     headless_mode, 'reg', 500)

    # Enable tracing for additional debugging if needed
    context.tracing.start(screenshots=False, snapshots=True, sources=True)

    # go straight to the account page to check for weak passwords
    page.goto(stage_manager_url + 'account')

    # Verify it is displayed
    expect(page.get_by_text("Welcome to Threecolts!")).to_be_visible()

    # Capture a screenshot and attach it to the Allure report
    screenshot = page.screenshot(path=f"screenshot_login_step.png")
    allure.attach.file(f"screenshot_login_step.png", name=f"Login Page Step",
                       attachment_type=AttachmentType.PNG)

    # Enter user's Full Name
    page.locator("#app input[name=\"full_name\"]").fill(fullname)

    # Click the eye icon so we can see the password
    page.locator("form").filter(has_text="You’re registering as").locator("path").first.click()

    # Now for the pw Confirmation field
    page.locator("form").filter(has_text="You’re registering as").locator("path").nth(1).click()
    """ pw validity check
    THREECOLTS     fails all
    THREECOLTs     passes the, 1 lowercase check
    THREECOLTs5    passes previous and 1 numeric check
    THREECOLTs5%   passes previous and 1 special char check
    THREECOLTs56k% passes all 
    """
    passwords = ['THREECOLTS', 'THREECOLTs','THREECOLTs5','THREECOLTs5%','THREECOLTs56k%']
    for password in passwords:
        page.fill('input[name="password"]', password)
        i=1
        for i in range(1,5):

            # check each of the requirements
            try:
                xpath = f"//section[@class='ant-layout v-app']//li[{i}]"
                is_valid = is_valid_in_xpath(page, xpath)
                if not is_valid:
                    print(password +':' + ' is Not Valid')
                else:
                    print(password +':' + ' is Valid')
            except AssertionError as e:
                print(f" *** FAILED ON the : {i}th xpath ***")

    # Enter the valid pw and continue
    page.locator("input[name=\"confirm_password\"]").fill("THREECOLTs56k%")
    expect(page.locator("div").filter(has_text=re.compile(r"^Password$")).get_by_role("textbox")).to_be_visible()

    # The Continue button should become enabled
    button = page.locator('button:has(span:text("Continue"))')
    if button.is_disabled():
        raise Exception('The Continue button is still disabled!!!')
    else:

        # Clean up
        context.close()
        browser.close()
