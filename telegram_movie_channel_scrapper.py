import time
import pyperclip
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def setup_driver():
    """Set up and return the Chrome WebDriver in debugger mode."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
    chromedriver_path = "/usr/bin/chromedriver"  # Update path if needed
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    logging.info("Chrome WebDriver connected in debugger mode.")
    return driver
def search_movie():
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    # Open Telegram Web
    driver.get("https://web.telegram.org/a/")
    logging.info("Opened Telegram Web.")
    # Click on the search bar
    search_bar = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']")))
    search_bar.click()
    logging.info("Clicked on the Telegram search bar.")
    time.sleep(2)
    # Click on "Channels" tab
    channels_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[.='Channels']")))
    channels_tab.click()
    logging.info("Clicked on the 'Channels' tab.")
    time.sleep(2)
    # Ask user for the movie name
    movie_name = input("Enter the movie name to search: ").strip()
    if movie_name:
        # Copy movie name to clipboard
        pyperclip.copy(movie_name)
        time.sleep(1)  # Allow clipboard update
        # Click on the search bar before pasting
        search_bar.click()
        time.sleep(1)
        # Paste movie name using pyperclip
        search_bar.send_keys(pyperclip.paste())
        logging.info(f"Pasted movie name: {movie_name}")
        time.sleep(3)  # Wait for search results to load
        # Click "Show more" once (if available)
        try:
            show_more = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#"]')))
            show_more.click()
            logging.info("Clicked on 'Show more' once.")
            time.sleep(3)  # Allow new results to load
        except:
            logging.info("No 'Show more' button found. Proceeding with existing results.")
        # Collect all search results
        search_results = driver.find_elements(By.XPATH, "//div[@class='search-section']//div[@class='ListItem chat-item-clickable search-result']")
        logging.info(f"Total search results found: {len(search_results)}")
        # Print all results
        for index, result in enumerate(search_results, start=1):
            try:
                text = result.text.strip()
                logging.info(f"{index}. {text}")
            except:
                logging.warning(f"Could not retrieve text for result {index}")
    else:
        logging.warning("No movie name entered. Exiting script.")
    time.sleep(2)
if __name__ == "__main__":
    search_movie()