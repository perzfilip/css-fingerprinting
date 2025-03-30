import base64
import json
import sqlite3
import uuid
from pprint import pprint

import jwt
from itsdangerous import URLSafeTimedSerializer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

DB_PATH = "../instance/database.db"



def save_to_db(session_id, attribute_name, attribute_value):
    # connect to the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # insert the data into the database
    c.execute('INSERT INTO css_attribute (session_id, attribute, value, source) VALUES (?, ?, ?, ?)',
              (session_id, attribute_name, attribute_value, 'browserstack'))

    # commit the changes
    conn.commit()

    # close the connection
    conn.close()

def decode_flask_session_cookie(cookie_value):
    # Flask cookies are in the format: "<base64_payload>.<signature>"
    try:
        encoded_data = cookie_value.split(".")[0]
        decoded_bytes = base64.urlsafe_b64decode(encoded_data + "==")
        json_session = json.loads(decoded_bytes.decode("utf-8"))
        return str(uuid.UUID(json_session['session_id'][' u']))
    except Exception as e:
        return f"Error decoding cookie: {e}"


options = ChromeOptions()
options.set_capability('sessionName', 'BStack Local Test')

# The webdriver management will be handled by the browserstack-sdk
# so this will be overridden and tests will run browserstack -
# without any changes to the test files!
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options)

try:
    driver.get('http://localhost:5000')
    page_title = driver.title


    # check if local connected successfully
    if 'CSS Fingerprinting' in page_title:
        # mark test as passed if Local website is accessible
        # collect data about the device from browserstack
        device_info = driver.execute_script('browserstack_executor: {"action": "getSessionDetails"}')
        device_info = json.loads(device_info)
        try:
            window_size = driver.get_window_size()
        except Exception as e:
            window_size = {'height': None, 'width': None}

        # todo wait for the whole page to load so a little bit of timeout is needed
        # get session_id from cookie
        session_id = decode_flask_session_cookie(driver.get_cookie('session')['value'])

        # print the device information
        # print(f"============\nsession_id: {session_id}\n============")
        # print(f"============\nwindow_size: {window_size}\n============")
        # print(f"============\nbrowser_version: {driver.capabilities}\n============")
        # pprint(device_info)

        # save device information to a database
        save_to_db(session_id, 'browser', device_info['browser'] if device_info['browser'] is not None else 'unknown')
        save_to_db(session_id, 'browser_version', device_info['browser_version'] if device_info['browser_version'] is not None else 'unknown')
        save_to_db(session_id, 'os', device_info['os'] if device_info['os'] is not None else 'unknown')
        save_to_db(session_id, 'os_version', device_info['os_version'] if device_info['os_version'] is not None else 'unknown')
        save_to_db(session_id, 'browser', device_info['browser'] if device_info['browser'] is not None else 'unknown')
        save_to_db(session_id, 'real_height', window_size['height'] if window_size['height'] is not None else 'unknown')
        save_to_db(session_id, 'real_width', window_size['width'] if window_size['width'] is not None else 'unknown')

        # set the status of the test as passed
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Local Test ran successfully"}}')
    else:
        # mark test as failed if Local website is not accessible
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Local test setup failed"}}')
except Exception as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')

# Stop the driver
driver.quit()
