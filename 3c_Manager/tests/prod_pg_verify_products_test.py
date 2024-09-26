"""
Verifies the Products page is loaded and that each product panel
has an image.
Also verifies that the user's email address is located in the
upper right and to the left of the user's name
"""
import os

from playwright.sync_api import sync_playwright, expect

from common_functions import display_initial_page
from dotenv import load_dotenv
load_dotenv()



def is_image_displayed(page, img_selector):
    # Wait for the image to appear in the DOM
    try:
        page.wait_for_selector(img_selector, timeout=5000)  # Wait up to 5 seconds
    except:
        # If the image does not appear within the timeout, return False
        return False

    # Check if the image is displayed by evaluating its naturalWidth property
    image_displayed = page.evaluate(f'''
        () => {{
            const img = document.querySelector('{img_selector}');
            return img && img.complete && img.naturalWidth > 0;
        }}
    ''')
    return image_displayed


def test_verify_products_are_listed(playwright):
    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"
    # Test all three browsers
    # browser_types = ['chromium', 'firefox', 'webkit']
    # for browser_type in browser_types:
    page, browser, context, stage_manager_url = display_initial_page(playwright, os.getenv("BROWSER"),
                                                                     headless_mode, 'login', 500)
    valid_username = os.getenv("STAGE_MANAGER_TESTING_USERNAME")
    valid_password = os.getenv("STAGE_MANAGER_TESTING_PW")
    # Verify we are on the correct page
    expect(page.get_by_text("Log in to your account")).to_be_visible()
    # Enter username and pw
    page.locator("#login-app input[type=\"text\"]").fill(valid_username)
    page.locator("input[type=\"password\"]").fill(valid_password)
    # Click the Continue button
    page.get_by_label("tc-button").nth(2).click()
    # Verify that we are on the Products page
    expect(page.locator("#presentation-layout")).to_contain_text("Products")
    # Wait for page to completely load
    page.wait_for_load_state('load')
    """
    First, let's ensure that the user's email address is located in the upper
    right and to the left of the user's name        
    """
    expect(page.locator("#threecolts_top_navbar")).to_contain_text(valid_username)
    # Verify if the image is displayed
    if not is_image_displayed(page, 'img[alt="PrinceletSQL"]'):
        print('PrinceletSLQ is not displayed - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="Bindwise Test"]'):
        print('Bindwise is not displayed - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="ChannelReply Stage"]'):
        print('ChannelReply is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="RefundSniper"]'):
        print('RefundSniper is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="OldStreetMedia"]'):
        print('OldStreetMedia is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="SellerBench"]'):  #######
        print('SellerBench is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="HotShp"]'):
        print('HotShp is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="Tactical Arbitrage-dev4"]'):
        print('Tactical Arbitrage-dev4 is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="Tactical Arbitrage-dev6"]'):
        print('Tactical Arbitrage-dev6 is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="SellerRunning"]'):
        print('SellerRunning is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="ChannelReply Sandbox"]'):
        print('ChannelReply Sandbox is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="Bindwise Local"]'):
        print('Bindwise Local is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="Onsite Support"]'):
        print('Onsite Support is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="FeedbackWhiz Profit Analytics"]'):
        print('FeedbackWhiz Profit Analytics is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="FeedbackWhiz Email"]'):
        print('FeedbackWhiz Email is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="FeedbackWhiz Alerts"]'):
        print('FeedbackWhiz Alerts is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="SmartRepricer"]'): #########
         print('SmartRepricer is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="ScoutIQ Stage"]'):
        print('ScoutIQ Stage is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="SellerRunning"]'):
        print('SellerRunning2 is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="ExportYourStore"]'):
        print('ExportYourStore is not displayed  - ' + os.getenv("BROWSER"))
    if not is_image_displayed(page, 'img[alt="DimeTyd"]'):
        print('DimeTyd is not displayed  - ' + os.getenv("BROWSER"))


    # Clean up
    context.close()
    browser.close()

# with sync_playwright() as pw:
#      test_verify_products_are_listed(pw)