import asyncio
import json
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import PyPDF2
import openpyxl

# Helper function to get a simplified page name from the URL
def get_page_name(url):
    parsed_url = urlparse(url)
    return parsed_url.path.strip('/').replace('/', '_') or 'home'

async def scrape_page(page, base_url, url, visited_urls, scraped_data):
    if url in visited_urls:
        return
    visited_urls.add(url)
    
    try:
        await page.goto(url)
        print(f"Scraping: {url}")
        
        # Wait until the page is fully loaded before accessing its content
        await page.wait_for_load_state('networkidle')  # Wait for network to be idle
        
        # Remove unwanted elements like <script>, <style>, and invisible elements
        await page.eval_on_selector_all('script, style, [hidden]', 'elements => elements.forEach(el => el.remove())')
        
        # Get the useful text content of the page (without HTML tags)
        page_text = await page.text_content('body')  # Get text content from the body tag
        page_name = get_page_name(url)  # Simplified page name
        
        # Store the text content in the dictionary
        soup = BeautifulSoup(page_text, 'html.parser')
    
        # Extract the text and clean it
        cleaned_text = soup.get_text(separator=' ', strip=True)

        if "404" not in cleaned_text:
            scraped_data[page_name] = cleaned_text  # Stripping extra whitespace
        
        # Interact with dropdowns or dynamic elements that might contain links
        dropdown_selectors = [
            'button[aria-haspopup="true"]',
            'div.dropdown',
            '.menu-item-has-children > a',
        ]
        
        for selector in dropdown_selectors:
            try:
                dropdown_elements = await page.query_selector_all(selector)
                for dropdown in dropdown_elements:
                    try:
                        await dropdown.hover()  # Hover to reveal dropdown
                        await page.wait_for_timeout(500)
                        await dropdown.click()  # Or click to reveal links
                        await page.wait_for_timeout(1000)
                    except Exception as e:
                        print(f"Failed to interact with dropdown {selector}: {e}")
            except Exception as e:
                print(f"Dropdown selector {selector} not found: {e}")
        
        # Get all links from the page
        links = await page.eval_on_selector_all('a', 'elements => elements.map(el => el.href)')
        
        # Parse base URL
        parsed_base_url = urlparse(base_url)
        
        # Recursively visit and scrape subpages that belong to the same base domain
        for link in links:
            parsed_link = urlparse(link)
            
            # Check if the link matches the base domain
            if parsed_link.netloc == parsed_base_url.netloc and link not in visited_urls:
                await scrape_page(page, base_url, link, visited_urls, scraped_data)
    
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

async def scrape_main(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        visited_urls = set()
        scraped_data = {}  # Dictionary to store page content
        
        # Start scraping from the main page
        await scrape_page(page, url, url, visited_urls, scraped_data)
        
        await browser.close()

        return scraped_data

def parse_pdf(file):
    with open(file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        data_text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            data_text = data_text + f"\n{text}"

        return data_text
    
def parse_pdf_page(file, page_num):
    with open(file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        data_text = ""

        page = reader.pages[page_num]
        text = page.extract_text()
        data_text = data_text + f"\n{text}"
        
        return data_text

def parse_vendors(file_path):
    # Load the workbook
    workbook = openpyxl.load_workbook(file_path)

    # Select the active worksheet
    sheet = workbook.active

    # Initialize a list to hold the column data
    data = []

    # Iterate through the rows and get the first two columns
    for row in sheet.iter_rows(min_row=2, max_col=2, values_only=True):
        details = {"name" : row[0], "website": row[1]}
        data.append(details)

    return data

