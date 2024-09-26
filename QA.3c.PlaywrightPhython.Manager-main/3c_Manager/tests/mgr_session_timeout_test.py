import os
from playwright.sync_api import sync_playwright, expect
import re
import base64
import json
from datetime import datetime, timedelta, timezone
from common_functions import display_initial_page, delay, clear_specific_cookie
from dotenv import load_dotenv
load_dotenv()


def get_token_dev1_cookie(context):
    cookies = context.cookies()
    for cookie in cookies:
        if cookie['name'] == 'token_dev1':
            match = re.search(r'\.(.+)\.', cookie['value'])
            if match:
                return match.group(1)
            else:
                return cookie['value']
    return None

def decode_base64(encoded_string):
    try:
        encoded_string += '=' * ((4 - len(encoded_string) % 4) % 4)
        decoded_bytes = base64.urlsafe_b64decode(encoded_string)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        print(f"Error decoding: {e}")
        return None

def extract_exp_and_convert_to_local_time(decoded_value):
    try:
        payload = json.loads(decoded_value)
        if 'exp' in payload:
            exp_timestamp = payload['exp']
            exp_datetime = datetime.fromtimestamp(exp_timestamp, datetime.timezone.utc)
            local_time = exp_datetime.astimezone()
            return local_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        else:
            return "No 'exp' claim found in the token"
    except json.JSONDecodeError:
        return "Failed to parse JSON from decoded value"
    except Exception as e:
        return f"Error processing token: {e}"


def extract_exp_value(token):
    try:
        # Parse the JSON token
        token_dict = json.loads(token)

        # Retrieve the 'exp' value
        exp_value = token_dict.get("exp", None)
        return exp_value
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def epoch_to_datetime(epoch_time):
    """
    Convert epoch time to a human-readable date and time using datetime module.
    Return a string of date and time in the format 'YYYY-MM-DD HH:MM:SS'
    """
    dt_object = datetime.fromtimestamp(epoch_time)
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')


def convert_epoch_to_datetime_manual(epoch):
    # Convert epoch to a datetime object in UTC
    epoch_start = datetime(1970, 1, 1, tzinfo=timezone.utc)  # Set timezone to UTC
    future_date = epoch_start + timedelta(seconds=epoch)
    return future_date

def hours_until_future_date(epoch):
    # Convert the epoch to a datetime object with UTC timezone
    future_date = convert_epoch_to_datetime_manual(epoch)

    # Get the current UTC time
    current_utc_time = datetime.now(timezone.utc)

    # Calculate the time difference
    time_difference = future_date - current_utc_time

    # Calculate the total hours in the difference
    hours_in_future = time_difference.total_seconds() / 3600  # Convert seconds to hours

    # Return the int hours if in the future; otherwise, 0
    return max(int(hours_in_future), 0)

def test_verify_session_timeout(playwright):
    """
    Launches browser, navigates to website, retrieves cookies, and stores specific ones.
    Extracts and prints the part between periods from the specified token.
    """
    valid_username = os.getenv("STAGE_MANAGER_TESTING_USERNAME")
    valid_password = os.getenv("STAGE_MANAGER_TESTING_PW")

    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"
    page, browser, context, stage_manager_url = display_initial_page(playwright, os.getenv("BROWSER"),
                                                                     headless_mode, 'login', 500)
    page.locator("#login-app input[type=\"text\"]").fill(valid_username)
    page.locator("input[type=\"password\"]").fill(valid_password)

    # Click the Continue button
    page.get_by_label("tc-button").nth(2).click()

    # wait for the Products page to display
    expect(page.locator("#presentation-layout")).to_contain_text("Products")

    # Gets the cookie value that is between the periods "."
    token_value = get_token_dev1_cookie(context)

    if token_value:
        print(f"The extracted portion of token_dev1 cookie is: {token_value}")

        # Decodes to human-readable form
        decoded_value = decode_base64(token_value)
        if decoded_value:
            # print(f"Decoded token value: {decoded_value}")

            # Gets the encoded datetime (1726263194)
            exp_value = extract_exp_value(decoded_value)
            # print(f"'exp' value: {exp_value}")

            # Converts it to readable hours (i.e 11.99)
            hrs_remaining = hours_until_future_date(exp_value)
            # print(f"The session expires {hrs_remaining:.2f} hours from now!")

            # Check that there are at least 11 hrs remaining because as soon as
            # the cookie is created, it starts counting down from 12 hrs and could
            # be a value of 11.999 or less
            if hrs_remaining < 11:
                raise ValueError(f" ({hrs_remaining}) is less than 11.")

            # Clear the specific 'token_dev1' cookie
            clear_specific_cookie(context, "token_dev1")
        else:
            raise Exception("Failed to decode token value!")
    else:
        raise Exception("token_dev1 token not found!")

    # ---------------------
    context.close()
    browser.close()


# with sync_playwright() as pw:
#     verify_session_timeout(pw)
