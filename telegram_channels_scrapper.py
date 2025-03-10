import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """Set up and return the Chrome WebDriver."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
    chromedriver_path = "/usr/bin/chromedriver"
    service = Service(chromedriver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def scroll_up(driver):
    """Scrolls up to load older messages."""
    driver.execute_script("window.scrollBy(0, -500);")
    time.sleep(2)

def scrape_telegram_channel(driver, telegram_url, messages_to_extract=3):
    """
    Scrape messages from a given Telegram channel URL.
    """
    driver.get("about:blank")
    time.sleep(1)
    driver.get(telegram_url)
    time.sleep(5)
    copied_data = []
    attempts = 0
    while len(copied_data) < messages_to_extract and attempts < 15:
        try:
            messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message")]')
            if len(messages) < messages_to_extract:
                scroll_up(driver)
                attempts += 1
                continue
            for message in messages[:messages_to_extract]:
                actions = ActionChains(driver)
                actions.context_click(message).perform()
                time.sleep(2)
                try:
                    copy_link_option = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '(//div[@role="menuitem" and contains(@class, "MenuItem compact")][4])[2]'))
                    )
                    driver.execute_script("arguments[0].click();", copy_link_option)
                    time.sleep(2)
                    message_link = pyperclip.paste()
                except Exception:
                    message_link = "N/A"
                try:
                    actions.context_click(message).perform()
                    time.sleep(2)
                    copy_text_option = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '(//div[@role="menuitem" and contains(@class, "MenuItem compact")][3])[3]'))
                    )
                    driver.execute_script("arguments[0].click();", copy_text_option)
                    time.sleep(2)
                    message_text = pyperclip.paste()
                except Exception:
                    message_text = "N/A"
                if message_link != "N/A" or message_text != "N/A":
                    copied_data.append((message_link, message_text))
                    print(f"Message {len(copied_data)}: Link = {message_link}, Text = {message_text}")
                if len(copied_data) >= messages_to_extract:
                    break
        except Exception as e:
            print(f"Error: {e}")
            scroll_up(driver)
            attempts += 1
    return copied_data

def save_data_to_file(all_channel_data, output_file="telegram_messages.txt"):
    """Save extracted messages to a file."""
    with open(output_file, "w", encoding="utf-8") as f:
        for url, data in all_channel_data.items():
            f.write(f"\nChannel URL: {url}\n")
            for idx, (link, text) in enumerate(data, 1):
                f.write(f"{idx}. Link: {link} | Text: {text}\n")
                print(f"{idx}. Link: {link} | Text: {text}")
    print(f"\nAll copied data has been saved to {output_file}")

def main():
    telegram_urls = [
        "https://web.telegram.org/a/#-1001901401132",
        "https://web.telegram.org/a/#-1002206623452",
        "https://web.telegram.org/a/#-1002163603910"
    ]
    driver = setup_driver()
    all_channel_data = {}
    try:
        for index, url in enumerate(telegram_urls, 1):
            print(f"\n--- Scraping Channel {index}: {url} ---")
            channel_data = scrape_telegram_channel(driver, url)
            all_channel_data[url] = channel_data
            time.sleep(2)
        print("\n--- Comprehensive Scraping Results ---")
        save_data_to_file(all_channel_data)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
