import requests
import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException


# ---------------- REQUEST HEADERS ----------------

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


# ---------------- CREATE SELENIUM DRIVER ----------------

def create_driver():

    chrome_options = Options()

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    chrome_options.add_argument("--window-size=1920,1080")

    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        options=chrome_options
    )

    return driver


# ---------------- MAIN SCRAPER ----------------

def scrape_website(website):

    # ---------------- FIX URL ----------------

    if not website.startswith("http"):

        website = "https://" + website

    # ---------------- TRY NORMAL REQUEST FIRST ----------------

    try:

        response = requests.get(
            website,
            headers=HEADERS,
            timeout=20
        )

        if response.status_code == 200:

            html = response.text

            if len(html) > 1000:

                print("Scraped using requests")

                return html

    except Exception as e:

        print(f"Requests scraping failed: {e}")

    # ---------------- FALLBACK TO SELENIUM ----------------

    driver = None

    try:

        print("Launching Selenium browser...")

        driver = create_driver()

        driver.set_page_load_timeout(30)

        driver.get(website)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )

        # Scroll slowly
        for _ in range(3):

            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            time.sleep(2)

        html = driver.page_source

        if html and len(html) > 1000:

            print("Scraped using Selenium")

            return html

        return ""

    except TimeoutException:

        print("Timeout while loading website")

        return ""

    except WebDriverException as e:

        print(f"Selenium WebDriver Error: {e}")

        return ""

    except Exception as e:

        print(f"Unexpected Selenium Error: {e}")

        return ""

    finally:

        if driver:

            driver.quit()


# ---------------- EXTRACT BODY ----------------

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


# ---------------- CLEAN CONTENT ----------------

def clean_body_content(body_content):

    if not body_content:

        return ""

    soup = BeautifulSoup(
        body_content,
        "html.parser"
    )

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

    cleaned_content = "\n".join(
        line.strip()
        for line in cleaned_content.splitlines()
        if line.strip()
    )

    unique_lines = list(
        dict.fromkeys(
            cleaned_content.splitlines()
        )
    )

    final_content = "\n".join(unique_lines)

    return final_content