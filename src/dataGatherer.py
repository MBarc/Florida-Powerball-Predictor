import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import tempfile
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def fetch_and_parse_powerball():
    logger.info("Starting Powerball data collection...")
    
    # --- Selenium setup ---
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins") 
    options.add_argument("--disable-images")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")
    
    logger.info("Initializing Chrome webdriver...")
    try:
        driver = webdriver.Chrome(options=options)
        logger.info("Chrome webdriver initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Chrome webdriver: {e}")
        raise
    
    try:
        logger.info("Navigating to Powerball website...")
        driver.get("https://www.powerball.com/previous-results?gc=powerball")
        logger.info("Page loaded successfully")
        
        # Wait for initial content to load
        wait = WebDriverWait(driver, 30)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-title")))
            logger.info("Initial lottery cards found on page")
        except TimeoutException:
            logger.error("Timeout waiting for initial content to load")
            raise
        
        ten_years_ago = datetime.today() - timedelta(days=365*10)
        logger.info(f"Target date for data collection: {ten_years_ago.strftime('%Y-%m-%d')}")
        
        load_more_clicks = 0
        max_clicks = 50
        
        # Click "Load More" until we have 10 years of data
        logger.info("Starting data collection loop...")
        while load_more_clicks < max_clicks:
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            date_elements = soup.select(".card-title")
            
            if not date_elements:
                logger.warning("No date elements found on page, breaking loop")
                break
                
            last_date_text = date_elements[-1].get_text(strip=True)
            logger.debug(f"Last date found on page: {last_date_text}")
            
            try:
                last_date_obj = datetime.strptime(last_date_text, "%a, %b %d, %Y")
            except ValueError as e:
                logger.error(f"Could not parse date '{last_date_text}': {e}")
                break
                
            if last_date_obj < ten_years_ago:
                logger.info(f"Reached 10 years of data: {last_date_obj}")
                break
                
            try:
                load_more = wait.until(EC.element_to_be_clickable((By.ID, "loadMore")))
                driver.execute_script("arguments[0].click();", load_more)
                load_more_clicks += 1
                logger.info(f"Clicked 'Load More' button ({load_more_clicks}/{max_clicks})")
                time.sleep(2)  # Wait for new content to load
                
            except (TimeoutException, NoSuchElementException):
                logger.warning("Load More button not found or not clickable, ending collection")
                break
            except Exception as e:
                logger.error(f"Error clicking Load More button: {e}")
                break
        
        logger.info("Data collection loop completed, parsing final results...")
        
    except Exception as e:
        logger.error(f"Error during data collection: {e}")
        raise
    finally:
        # Final parse
        html = driver.page_source
        driver.quit()
        logger.info("Chrome webdriver closed")
    
    logger.info("Parsing HTML content...")
    soup = BeautifulSoup(html, "html.parser")
    records = []
    cards = soup.select("a.card")
    logger.info(f"Found {len(cards)} lottery result cards")
    
    skipped_count = 0
    processed_count = 0
    
    for i, card in enumerate(cards):
        try:
            # Date
            date_elem = card.select_one("h5.card-title")
            if not date_elem:
                logger.debug(f"Card {i}: No date element found, skipping")
                skipped_count += 1
                continue
                
            date_text = date_elem.get_text(strip=True)
            date_obj = datetime.strptime(date_text, "%a, %b %d, %Y")
            
            if date_obj < ten_years_ago:
                continue
            
            # Numbers
            balls = card.select("div.form-control.item-powerball")
            if len(balls) < 6:
                logger.debug(f"Card {i} ({date_text}): Incomplete ball data ({len(balls)} balls), skipping")
                skipped_count += 1
                continue
                
            numbers = [b.get_text(strip=True) for b in balls[:5]]
            powerball = balls[5].get_text(strip=True) if len(balls) > 5 else ""
            
            # Power Play
            pp_elem = card.select_one("span.power-play .multiplier")
            powerplay = pp_elem.get_text(strip=True) if pp_elem else ""
            
            week_num = date_obj.isocalendar()[1]
            
            records.append({
                "date": date_obj.strftime("%Y-%m-%d"),
                "day_of_week": date_obj.strftime("%a"),
                "week_number": week_num,
                "numbers": " ".join(numbers),
                "powerball": powerball,
                "powerplay": powerplay
            })
            
            processed_count += 1
            
            # Log first few records for verification
            if processed_count <= 5:
                logger.info(f"Sample record {processed_count}: {date_text} -> Numbers: {numbers}, Powerball: {powerball}")
                
        except Exception as e:
            logger.error(f"Error parsing card {i}: {e}")
            skipped_count += 1
            continue
    
    logger.info(f"Parsing completed: {processed_count} records processed, {skipped_count} cards skipped")
    
    df = pd.DataFrame(records)
    
    if df.empty:
        logger.error("No data collected! DataFrame is empty")
        raise ValueError("There was an error fetching Powerball data! Were you rate limited?")
    
    date_range = f"{df['date'].min()} to {df['date'].max()}"
    logger.info(f"Successfully collected {len(df)} records spanning {date_range}")
    
    return df

if __name__ == "__main__":
    try:
        data = fetch_and_parse_powerball()
        logger.info(f"Data collection completed successfully: {len(data)} total records")
    except Exception as e:
        logger.error(f"Data collection failed: {e}")
        raise
