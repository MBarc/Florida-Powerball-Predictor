import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import tempfile

def fetch_and_parse_powerball():
    # --- Selenium setup ---
    options = Options()
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

    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")
    
    print(f"🔧 Using temp directory: {temp_dir}")
    
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.powerball.com/previous-results?gc=powerball")

    ten_years_ago = datetime.today() - timedelta(days=365*10)

    # Click "Load More" until we have 10 years of data
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        date_elements = soup.select(".card-title")
        if not date_elements:
            break
        last_date_text = date_elements[-1].get_text(strip=True)
        try:
            last_date_obj = datetime.strptime(last_date_text, "%a, %b %d, %Y")
        except ValueError:
            break
        if last_date_obj < ten_years_ago:
            print(f"Reached 10 years of data: {last_date_obj}")
            break
        try:
            load_more = driver.find_element(By.ID, "loadMore")
            driver.execute_script("arguments[0].click();", load_more)
            print("Clicked 'Load More' button. . .")
            print("Gathering more data. . .")
            time.sleep(1)
        except:
            break

    # Final parse
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")

    records = []

    for card in soup.select("a.card"):
        # Date
        date_text = card.select_one("h5.card-title").get_text(strip=True)
        date_obj = datetime.strptime(date_text, "%a, %b %d, %Y")
        if date_obj < ten_years_ago:
            continue

        # Numbers
        balls = card.select("div.form-control.item-powerball")
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

    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError("There was an error fetching Powerball data! Were you rate limited?")

    return df

if __name__ == "__main__":
    fetch_and_parse_powerball()


