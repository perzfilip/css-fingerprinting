from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


def get_driver(browser="chrome"):
    """Returns a WebDriver instance based on the selected browser."""
    if browser.lower() == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)

    elif browser.lower() == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        # options.set_preference("pref.privacy.disable_button.tracking_protection_exceptions", True)
        return webdriver.Firefox(options=options)

    else:
        raise ValueError("Unsupported browser! Choose from 'chrome', 'firefox', or 'opera'.")


def measure_text_width(fonts, text, font_size=16, output_file="font_widths.csv", browser="chrome"):
    driver = get_driver(browser)

    results = []

    for font in fonts:
        html_content = f'''
        data:text/html,<html>
        <head>
            <style>
                .test-text {{
                    font-family: "{font}";
                    font-size: {font_size}px;
                    white-space: nowrap;
                }}
            </style>
        </head>
        <body>
            <span class="test-text" id="measure">{text}</span>
        </body>
        </html>
        '''

        driver.get(html_content)

        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "measure"))
            )
            width = element.size["width"]
            results.append((font, width))
            print(f"Font: {font}, Width: {width}px ({browser})")
        except Exception as e:
            print(f"Error measuring {font} in {browser}: {e}")
            results.append((font, "Error"))

    driver.quit()

    # Save results to CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Font", "Width (px)"])
        writer.writerows(results)

    print(f"Results saved to {output_file}")


if __name__ == '__main__':
    # Example usage
    font_list = [
        'sans-serif-thin',
        'ARNO PRO',
        'Agency FB',
        'Arabic Typesetting',
        'Arial Unicode MS',
        'AvantGarde Bk BT',
        'BankGothic Md BT',
        'Batang',
        'Bitstream Vera Sans Mono',
        'Calibri',
        'Century',
        'Century Gothic',
        'Clarendon',
        'EUROSTILE',
        'Franklin Gothic',
        'Futura Bk BT',
        'Futura Md BT',
        'GOTHAM',
        'Gill Sans',
        'HELV',
        'Haettenschweiler',
        'Helvetica Neue',
        'Humanst521 BT',
        'Leelawadee',
        'Letter Gothic',
        'Levenim MT',
        'Lucida Bright',
        'Lucida Sans',
        'Menlo',
        'MS Mincho',
        'MS Outlook',
        'MS Reference Specialty',
        'MS UI Gothic',
        'MT Extra',
        'MYRIAD PRO',
        'Marlett',
        'Meiryo UI',
        'Microsoft Uighur',
        'Minion Pro',
        'Monotype Corsiva',
        'PMingLiU',
        'Pristina',
        'SCRIPTINA',
        'Segoe UI Light',
        'Serifa',
        'SimHei',
        'Small Fonts',
        'Staccato222 BT',
        'TRAJAN PRO',
        'Univers CE 55 Medium',
        'Vrinda',
        'ZWAdobeF'
    ]
    sample_text = "mmmmmmmmmmlllllllllllllllllllllllllllllllllllllll"

    # Change 'chrome' to 'firefox' or 'opera' to test in other browsers
    measure_text_width(font_list, sample_text, output_file="firefox_without_sanserif.csv", browser="firefox")
