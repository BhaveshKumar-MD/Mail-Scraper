from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import time

def extract_ids_with_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    all_ids = []
    
    try:
        for page in range(9, 10):  # Iterate through 25 pages
            url = f"https://freida.ama-assn.org/search/list?spec=42736&page={page}"
            print(f"Processing page {page}: {url}")
            driver.get(url)
            time.sleep(3)  # Wait for JavaScript to load
            
             # Get page content
            page_source = driver.page_source
            # Updated regex to include letters and numbers
            matches = re.findall(r'ID:\s*([A-Za-z0-9]+)', page_source)
            
            if matches:
                all_ids.extend(matches)
                print(f"Found {len(matches)} IDs on page {page}")
            else:
                print(f"No IDs found on page {page}. Check page structure.")
                
    finally:
        driver.quit()
    
    # Save to file
    with open('Family Medicine9_ids.txt', 'w') as f:
        for pid in all_ids:
            f.write(f"{pid}\n")
    
    print(f"\nSaved {len(all_ids)} IDs to Family Medicine9_ids.txt")

if __name__ == "__main__":
    extract_ids_with_selenium()