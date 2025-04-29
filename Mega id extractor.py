from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time

# Configuration
MAX_RETRIES = 3
PAGE_LOAD_DELAY = 3
SPECIALTIES_FILE = "Specialties trial.txt"  # Text file containing specialty data

def load_specialties():
    specialties = []
    try:
        with open(SPECIALTIES_FILE) as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    spec, name = line.split(maxsplit=1)
                    specialties.append({
                        "spec": spec,
                        "name": name.replace('_', ' ')  # Convert underscores back to spaces
                    })
        print(f"Loaded {len(specialties)} specialties from {SPECIALTIES_FILE}")
        return specialties
    except FileNotFoundError:
        print(f"Error: {SPECIALTIES_FILE} not found.")
        print("Create a text file with format: SPEC_NUMBER SPECIALTY_NAME (space-separated)")
        exit()
    except Exception as e:
        print(f"Error reading {SPECIALTIES_FILE}: {str(e)}")
        exit()

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return webdriver.Chrome(options=chrome_options)

def scrape_specialty(driver, spec_code, specialty_name):
    print(f"\n{'='*40}\nScraping {specialty_name} (SPEC: {spec_code})\n{'='*40}")
    all_ids = []
    page = 1
    
    while True:
        url = f"https://freida.ama-assn.org/search/list?spec={spec_code}&page={page}"
        print(f"Processing page {page}: {url}")
        
        for attempt in range(MAX_RETRIES):
            try:
                driver.get(url)
                time.sleep(PAGE_LOAD_DELAY)
                page_source = driver.page_source
                break
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    print(f"Failed to load page {page} after {MAX_RETRIES} attempts")
                    return all_ids
                print(f"Retrying page {page}... ({attempt+1}/{MAX_RETRIES})")
                time.sleep(2)

        # Modified regex pattern to include letters
        matches = re.findall(r'ID: ([A-Za-z0-9]+)', page_source)  # Changed from \d+ to [A-Za-z0-9]+
        
        if matches:
            all_ids.extend(matches)
            print(f"Found {len(matches)} IDs on page {page}")
            page += 1
        else:
            if page == 1:
                print("No IDs found on first page. Check specialty code.")
            else:
                print("Reached end of pages")
            break

    return all_ids

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
import os  # Added for path handling

# ... [keep previous configuration and functions unchanged until save_ids()] ...

def save_ids(specialty_name, ids):
    if not ids:
        print(f"No IDs found for {specialty_name}. Skipping file creation.")
        return
    
    # Sanitize filename and ensure it stays in current directory
    sanitized_name = re.sub(r'[\\/*?:"<>| ]', "_", specialty_name)
    filename = f"{sanitized_name}_program_ids.txt"
    
    # Write to current directory (no subfolders)
    with open(filename, 'w') as f:
        f.write('\n'.join(ids))
    print(f"\nSaved {len(ids)} IDs to {filename}")

# ... [rest of the code remains unchanged] ...
def main():
    specialties = load_specialties()
    driver = setup_driver()
    
    try:
        for specialty in specialties:
            ids = scrape_specialty(driver, specialty["spec"], specialty["name"])
            save_ids(specialty["name"], ids)
            
    finally:
        driver.quit()
        print("\nBrowser closed. Scraping completed!")

if __name__ == "__main__":
    main()