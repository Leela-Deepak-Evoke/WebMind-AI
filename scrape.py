from bs4 import BeautifulSoup
import selenium.webdriver as webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import time


def scrape_website(website):

    print("Launching Chrome browser...")

    options = webdriver.ChromeOptions()

    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_argument(
        "user-agent=Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:

        driver.get(website)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Scroll page
        for _ in range(3):

            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            time.sleep(2)

        html = driver.page_source

        # Basic validation
        if len(html) < 1000:

            return ""

        return html

    except Exception as e:

        print(f"Scraping Error: {e}")

        return ""

    finally:

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

    # Remove unwanted elements
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
        "aside"
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

    # Remove duplicates
    unique_lines = list(
        dict.fromkeys(
            cleaned_content.splitlines()
        )
    )

    return "\n".join(unique_lines)