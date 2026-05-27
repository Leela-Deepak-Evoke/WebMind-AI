from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

import time


def create_driver():

    chrome_options = Options()

    # REQUIRED FOR STREAMLIT CLOUD
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    # Performance & Stability
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-popup-blocking")

    # Prevent automation detection
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    # User Agent
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    # IMPORTANT:
    # DO NOT USE webdriver-manager IN STREAMLIT CLOUD

    driver = webdriver.Chrome(
        options=chrome_options
    )

    return driver


def scrape_website(website):

    driver = None

    try:

        print("Launching Chrome browser...")

        driver = create_driver()

        driver.set_page_load_timeout(30)

        driver.get(website)

        # Wait until page body loads
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )

        # Scroll page slowly
        for _ in range(3):

            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            time.sleep(2)

        html = driver.page_source

        # Basic validation
        if not html or len(html) < 1000:

            print("Page content too small.")

            return ""

        return html

    except TimeoutException:

        print("Page load timeout.")

        return ""

    except WebDriverException as e:

        print(f"WebDriver Error: {e}")

        return ""

    except Exception as e:

        print(f"Unexpected Error: {e}")

        return ""

    finally:

        if driver:

            driver.quit()


def extract_body_content(html_content):

    if not html_content:

        return ""

    soup = BeautifulSoup(
        html_content,
        "html.parser"
    )

    body_content = soup.body

    if body_content:

        return str(body_content)

    return ""


def clean_body_content(body_content):

    if not body_content:

        return ""

    soup = BeautifulSoup(
        body_content,
        "html.parser"
    )

    # Remove unwanted tags
    for tag in soup([
        "script",
        "style",
        "noscript",
        "iframe",
        "svg",
        "img",
        "footer",
        "header",
        "nav",
        "aside",
        "form",
        "button"
    ]):

        tag.extract()

    cleaned_content = soup.get_text(
        separator="\n"
    )

    # Remove blank lines
    cleaned_content = "\n".join(
        line.strip()
        for line in cleaned_content.splitlines()
        if line.strip()
    )

    # Remove duplicate lines
    unique_lines = list(
        dict.fromkeys(
            cleaned_content.splitlines()
        )
    )

    final_content = "\n".join(unique_lines)

    return final_content