from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from markdownify import markdownify as md
import os
import time
import traceback

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1920,1080')
    return webdriver.Chrome(options=options)

def save_markdown(content, filename):
    os.makedirs('baritone_docs', exist_ok=True)
    with open(f'baritone_docs/{filename}.md', 'w', encoding='utf-8') as f:
        f.write(content)

def convert_to_markdown(html_content):
    return md(html_content)

def crawl_page(driver, visited_urls, url_queue):
    while url_queue:
        current_url = url_queue.pop(0)
        if current_url in visited_urls:
            print(f"Skipping already processed URL: {current_url}")
            continue

        try:
            print(f"\nProcessing: {current_url}")
            driver.get(current_url)
            time.sleep(2)

            # Initialize header_content as an empty string
            header_content = ""

            # Attempt to extract header
            try:
                header = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'header'))
                )
                header_content = convert_to_markdown(header.get_attribute('innerHTML'))
            except Exception as header_exception:
                print(f"Header extraction timed out for {current_url}: {str(header_exception)}")

            # Extract content
            content = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'contentContainer'))
            )

            # Convert content to Markdown
            markdown_content = header_content + "\n\n" + convert_to_markdown(content.get_attribute('innerHTML'))

            # Generate filename from URL
            filename = current_url.split('.com')[1].replace('/', '.') 
            filename = filename.replace('.html', '') 
            filename = filename.lstrip('.')
            
            # Save to file
            save_markdown(markdown_content, filename)
            print(f"Saved markdown file: {filename}")
            visited_urls.add(current_url)

            # Extract links from contentContainer
            links = content.find_elements(By.TAG_NAME, 'a')
            for link in links:
                href = link.get_attribute('href')
                if href and 'baritone.leijurv.com' in href and href not in visited_urls and '#' not in href:  # Ensure it's a valid link
                    url_queue.append(href)

        except Exception as e:
            print(f"\nERROR processing {current_url}: {str(e)}")
            traceback.print_exc()
            continue

def main():
    driver = setup_driver()
    try:
        print("Starting crawler...")
        entry_points = [
            'https://baritone.leijurv.com/overview-summary.html',
            'https://baritone.leijurv.com/index-all.html',
            'https://baritone.leijurv.com/overview-tree.html'
        ]
        visited_urls = set()
        url_queue = entry_points[:]  # Initialize the queue with all entry points

        # Start crawling
        crawl_page(driver, visited_urls, url_queue)
        print("\nCrawling completed!")
        print(f"Total pages processed: {len(visited_urls)}")

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()
