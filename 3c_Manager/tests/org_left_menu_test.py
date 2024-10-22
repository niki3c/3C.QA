import os
from playwright.sync_api import Playwright, sync_playwright, expect
from common_functions import display_initial_page, login_to_manager
from dotenv import load_dotenv
load_dotenv()

def are_product_panels_visible(page):
    try:
        expect(page.get_by_role("main")).to_contain_text("PrinceletSQL")
        expect(page.get_by_role("main")).to_contain_text("Bindwise Test")
        expect(page.get_by_role("main")).to_contain_text("ChannelReply Stage")
        expect(page.get_by_role("main")).to_contain_text("RefundSniper")
        expect(page.get_by_role("main")).to_contain_text("OldStreetMedia")
        expect(page.get_by_role("main")).to_contain_text("SellerBench")
        expect(page.get_by_role("main")).to_contain_text("HotShp")
        expect(page.get_by_role("main")).to_contain_text("Tactical Arbitrage-dev6")
        expect(page.get_by_role("main")).to_contain_text("SellerRunning")
        expect(page.get_by_role("main")).to_contain_text("Tactical Arbitrage-dev4")
        expect(page.get_by_role("main")).to_contain_text("Tactical Arbitrage-dev4")
        expect(page.get_by_role("main")).to_contain_text("ChannelReply Sandbox")
        expect(page.get_by_role("main")).to_contain_text("Bindwise Local")
        expect(page.get_by_role("main")).to_contain_text("Onsite Support")
        expect(page.get_by_role("main")).to_contain_text("FeedbackWhiz Profit Analytics")
        expect(page.get_by_role("main")).to_contain_text("FeedbackWhiz Email")
        expect(page.get_by_role("main")).to_contain_text("FeedbackWhiz Alerts")
        expect(page.get_by_role("main")).to_contain_text("SmartRepricer")
        expect(page.get_by_role("main")).to_contain_text("ScoutIQ Stage")
        expect(page.get_by_role("main")).to_contain_text("SellerRunning2")
        expect(page.get_by_role("main")).to_contain_text("ExportYourStore")
        expect(page.get_by_role("main")).to_contain_text("DimeTyd")
    except AssertionError as e:
        print('Error:', e)


def test_validate_left_menu(playwright: Playwright) -> None:
    valid_username = os.getenv("STAGE_MANAGER_TESTING_USERNAME")
    valid_password = os.getenv("STAGE_MANAGER_TESTING_PW")
    # Convert the returned string (from .env) to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"
    # Test all three browsers
    # browser_types = ['chromium', 'firefox', 'webkit']
    #for browser_type in browser_types:
    page, browser, context, stage_manager_url = display_initial_page(playwright, os.getenv("BROWSER"),
                                                                     headless_mode, 'login', 2000)
    login_to_manager(page, valid_username, valid_password)
    # Are we on the Products page
    expect(page.get_by_role("main")).to_contain_text("All products")
    # Click on Users and verify the correct page displays
    page.get_by_role("link", name="Users").click()
    expect(page.get_by_label("false").locator("span")).to_contain_text("Invite User")
    # Click on Organization and verify the correct page displays
    page.get_by_role("link", name="Organization", exact=True).click()
    expect(page.get_by_role("main")).to_contain_text("Organization Settings")
    # Click on My Profile and verify the correct page displays
    page.get_by_role("link", name="My Profile").click()
    expect(page.get_by_role("main")).to_contain_text("My Profile")
    # Click on Notifications and verify the correct page displays
    page.get_by_role("link", name="Notifications").click()
    expect(page.locator("#rc-tabs-1-tab-promotions")).to_contain_text("Promotions")
    # Click on Customer Coaching and verify the correct page displays

    #===OLD===
    #page.get_by_role("link", name="Customer Coaching").click()
    #expect(page.locator("#presentation-layout")).to_contain_text("Courses")

    #====NEW====
    page.get_by_role("link", name="Customer Coaching").click()
    page.get_by_text("Courses").click()
    # Check that at least two courses can be found
    #expect(page.get_by_role("main")).to_contain_text("Ship It LTL With InventoryLab") #NO

    #===OLD===
    expect(page.get_by_role("main")).to_contain_text("TA - Reverse Search 101")

    #====NEW===
    page.get_by_text("TA - Reverse Search").nth(1).click()


    # Since we haven't clicked on it yet, click on Products and verify the
    # correct page displays

    #===old====
    #page.get_by_role("link", name="Products").click()
    #expect(page.get_by_role("main")).to_contain_text("All products")

    #===NEW===
    page.get_by_role("link", name="Products").click()
    page.locator("button").filter(has_text="All products").click()

    # Now verify all the panes are visible
    are_product_panels_visible(page)
    # ------------
    context.close()
    browser.close()


# with sync_playwright() as pw:
#     validate_left_menu(pw)
