import csv
import os
import logging
import time
import random
import requests
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

class NatureCrawler:
    """
    Nature Paper Crawler Tool
    Note: This tool is for academic research purposes only. 
    Please comply with Nature's terms of use and copyright regulations.
    """
    
    def __init__(self, download_path="./downloads", start_year=2010, max_articles=1000):
        self.download_path = download_path
        self.start_year = start_year
        self.max_articles = max_articles
        self.driver = None
        self.setup_logging()
        self.setup_download_directory()
    
    def setup_logging(self):
        """Setup logging system"""
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/nature_crawler.log', encoding='utf-8'),
                logging.StreamHandler()  # Also output to console
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_download_directory(self):
        """Create download directory"""
        os.makedirs(self.download_path, exist_ok=True)
        self.logger.info(f"Download directory set: {self.download_path}")
    
    def get_chrome_options(self):
        """Configure Chrome browser options"""
        chrome_options = Options()
        prefs = {
            "download.default_directory": os.path.abspath(self.download_path),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        # Optional: headless mode
        # chrome_options.add_argument("--headless")
        return chrome_options
    
    def initialize_driver(self):
        """Initialize WebDriver"""
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.get_chrome_options())
            self.driver.maximize_window()
            self.logger.info("Browser started successfully")
            return True
        except Exception as e:
            self.logger.error(f"Browser initialization failed: {e}")
            return False
    
    def navigate_to_nature(self, year):
        """Navigate to Nature search page"""
        search_url = (
            f"https://www.nature.com/search?"
            f"q=transmission%2Belectron%2Bmicroscopy&"
            f"article_type=research&"
            f"order=relevance&"
            f"date_range={year}-{year}"
        )
        
        try:
            self.driver.get(search_url)
            self.logger.info(f"Navigated to {year} search page")
            
            # Handle cookie consent popup
            self.handle_cookie_consent()
            return True
            
        except Exception as e:
            self.logger.error(f"Navigation failed: {e}")
            return False
    
    def handle_cookie_consent(self):
        """Handle cookie consent popup"""
        try:
            accept_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'accept')]"))
            )
            accept_button.click()
            self.logger.info("Cookie policy accepted")
        except:
            self.logger.info("No cookie consent popup found or already handled")
    
    def get_total_results(self):
        """Get total number of search results"""
        try:
            results_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-test='results-data'] > span:last-child"))
            )
            results_text = results_element.text
            results_number = int(results_text.split()[0])
            self.logger.info(f"Total search results: {results_number}")
            return results_number
        except Exception as e:
            self.logger.error(f"Cannot get total results: {e}")
            return 0
    
    def respectful_delay(self, min_delay=2, max_delay=4):
        """Add respectful delay to avoid overwhelming the server"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def download_pdf(self, pdf_url, file_name):
        """Download PDF file"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(pdf_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            file_path = os.path.join(self.download_path, file_name)
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            self.logger.info(f"PDF downloaded successfully: {file_name}")
            return True
            
        except requests.RequestException as e:
            self.logger.error(f"Download failed for {file_name}: {e}")
            return False
    
    def process_article(self, article_index, year, global_count):
        """Process a single article"""
        try:
            # Locate article link
            article_xpath = f"//*[@id='search-article-list']/div/ul/li[{article_index}]/div/article/div[1]/div[2]/h3/a"
            article = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, article_xpath))
            )
            
            # Open article in new tab
            ActionChains(self.driver).key_down(Keys.CONTROL).click(article).key_up(Keys.CONTROL).perform()
            
            # Switch to new tab
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            # Find and download PDF
            download_success = self.find_and_download_pdf(year, global_count)
            
            # Close current tab and return to main page
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            # Respectful delay
            self.respectful_delay()
            
            return download_success
            
        except Exception as e:
            self.logger.error(f"Error processing article {article_index}: {e}")
            # Ensure return to main window
            if len(self.driver.window_handles) > 1:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            return False
    
    def find_and_download_pdf(self, year, count):
        """Find and download PDF"""
        download_xpaths = [
            '//*[@id="entitlement-box-right-column"]/div/a',
            '//*[@id="content"]/aside/div[1]/div/a',
            '//a[contains(@href, ".pdf")]',
            '//a[contains(text(), "Download PDF")]'
        ]
        
        for xpath in download_xpaths:
            try:
                downloader = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                
                pdf_url = downloader.get_attribute("href")
                if pdf_url and pdf_url.endswith('.pdf'):
                    file_name = f"nature_{year}_{count:04d}.pdf"
                    return self.download_pdf(pdf_url, file_name)
                    
            except:
                continue
        
        self.logger.warning("No PDF download link found")
        return False
    
    def go_to_next_page(self):
        """Go to next page"""
        try:
            next_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@data-page='next']"))
            )
            next_button.click()
            self.logger.info("Switched to next page")
            self.respectful_delay()
            return True
        except:
            self.logger.info("No more pages available")
            return False
    
    def crawl_year(self, year):
        """Crawl articles for specified year"""
        if not self.navigate_to_nature(year):
            return False
        
        total_results = self.get_total_results()
        if total_results == 0:
            return False
        
        downloaded_count = 0
        processed_count = 0
        
        self.logger.info(f"Starting to crawl {year} data, total {total_results} articles")
        
        while downloaded_count < self.max_articles and processed_count < total_results:
            # Process articles on current page (usually 50 articles per page)
            for i in range(1, 51):  # 1-50
                if downloaded_count >= self.max_articles:
                    break
                
                processed_count += 1
                self.logger.info(f"Processing article {processed_count} of year {year}")
                
                success = self.process_article(i, year, downloaded_count + 1)
                if success:
                    downloaded_count += 1
                
                if processed_count >= total_results:
                    break
            
            # Try to go to next page
            if not self.go_to_next_page():
                break
        
        self.logger.info(f"Year {year} crawling completed, successfully downloaded {downloaded_count} articles")
        return True
    
    def run(self):
        """Main execution function"""
        if not self.initialize_driver():
            return False
        
        try:
            year = self.start_year
            while True:
                self.logger.info(f"Starting to process year {year}")
                success = self.crawl_year(year)
                
                if not success:
                    self.logger.info(f"Year {year} processing completed or error occurred")
                
                year += 1
                
                # Optional: set end year
                if year > 2024:  # For example, only process until 2024
                    break
                
        except KeyboardInterrupt:
            self.logger.info("Program interrupted by user")
        except Exception as e:
            self.logger.error(f"Program execution error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Nature Paper Crawler Tool')
    parser.add_argument('--year', type=int, default=2010, help='Starting year (default: 2021)')
    parser.add_argument('--max-articles', type=int, default=1000, help='Maximum articles per year (default: 1000)')
    parser.add_argument('--output-dir', default='./downloads', help='Download directory (default: ./downloads)')
    return parser.parse_args()


def main():
    """Main program entry point"""
    print("Nature Paper Crawler")
    print("=" * 50)
    print("This tool is for academic research purposes only.")
    print("Please ensure you comply with Nature's terms of use.")
    print("=" * 50)
    
    args = parse_arguments()
    
    print(f"Configuration:")
    print(f"  Starting year: {args.year}")
    print(f"  Max articles per year: {args.max_articles}")
    print(f"  Output directory: {args.output_dir}")
    print("=" * 50)
    
    crawler = NatureCrawler(
        download_path=args.output_dir,
        start_year=args.year,
        max_articles=args.max_articles
    )
    
    crawler.run()
    print("Program execution completed.")


if __name__ == "__main__":
    main()
