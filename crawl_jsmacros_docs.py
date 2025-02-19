from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import os
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1920,1080')
    return webdriver.Chrome(options=options)

def convert_to_markdown(html_content):
    return md(html_content, heading_style="ATX")

def save_markdown(content, filename):
    os.makedirs('output', exist_ok=True)
    with open(f'output/{filename}.md', 'w', encoding='utf-8') as f:
        f.write(content)

def is_valid_link(href):
    if not href:
        return False
    if 'https://' in href or 'http://' in href:
        return False
    if href.startswith('#'):
        return False
    return True

def clean_filename(text):
    # First, handle the case of complex class names with generics
    if '<' in text:
        text = text.split('<')[0].strip()
    
    # Replace invalid filename characters with space
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        text = text.replace(char, ' ')
    
    # Clean up multiple spaces and trim
    text = ' '.join(text.split())
    return text.strip().replace(' ', '_').lower()

def crawl_page(driver, processed_urls, url_queue):
    while url_queue:
        current_url = url_queue.pop(0)
        if current_url in processed_urls:
            print(f"Skipping already processed URL: {current_url}")
            continue

        try:
            print(f"\nProcessing: {current_url}")
            # Click the link instead of navigating directly
            link_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'a[href*="{current_url}"]'))
            )
            link_element.click()
            print("Link clicked successfully")
            time.sleep(2)  # Wait 2 seconds after each click

            # Get the page content
            main_content = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "mainContent"))
            )
            
            # Get the h2 title for filename
            soup = BeautifulSoup(main_content.get_attribute('innerHTML'), 'html.parser')
            h2_title = soup.find('h2')
            if h2_title and h2_title.text:
                filename = clean_filename(h2_title.text)
            else:
                # Fallback to URL-based filename if no h2 found
                filename = clean_filename(current_url.replace('.html', ''))
            
            # Convert to markdown and save
            markdown_content = convert_to_markdown(main_content.get_attribute('innerHTML'))
            save_markdown(markdown_content, filename)
            print(f"Saved markdown file: {filename}.md")
            processed_urls.add(current_url)

        except Exception as e:
            print(f"\nERROR processing {current_url}:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            continue

def main():
    driver = setup_driver()
    try:
        print("Starting crawler...")
        # Start with the initial page
        print("Loading initial page...")
        driver.get('https://jsmacros.wagyourtail.xyz/?general.html')
        print("Waiting 15 seconds for initial load...")
        time.sleep(15)  # Wait 15 seconds for initial load

        processed_urls = set()
        url_queue = []

        # Get sidebar links
        print("Getting sidebar links...")
        sidebar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sideNav"))
        )
        soup = BeautifulSoup(sidebar.get_attribute('innerHTML'), 'html.parser')
        initial_links = [link.get('href') for link in soup.find_all('a') 
                        if link.get('href') and is_valid_link(link.get('href'))]
        url_queue.extend(initial_links)
        print(f"Found {len(initial_links)} links in sidebar")

        # Start crawling
        print("\nStarting main crawl process...")
        crawl_page(driver, processed_urls, url_queue)
        print("\nCrawling completed!")
        print(f"Total pages processed: {len(processed_urls)}")

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()
