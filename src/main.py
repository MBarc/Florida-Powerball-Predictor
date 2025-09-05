import requests
from bs4 import BeautifulSoup
from dataGatherer import fetch_and_parse_powerball
from predictNumbers import predict_numbers
from notifier import send_notification

def fetch_current_jackpot():
    """
    Fetches the current Powerball jackpot estimate from the Powerball website HTML.
    Returns jackpot as a string (e.g., "$1.40 Billion").
    """
    url = "https://www.powerball.com/api/v1/estimates/powerball"
    resp = requests.get(url)
    print(resp.status_code)

    print(resp.txt)

    soup = BeautifulSoup(resp.text, 'html.parser')
    span = soup.find('span', class_='game-jackpot-number')
    if span:
        jackpot_str = span.get_text(strip=True)
        return jackpot_str
    else:
        raise ValueError("Jackpot value not found on the page.")

if __name__ == "__main__":
    jackpot = fetch_current_jackpot()
    print(f"Current Jackpot: ${jackpot}")

    if "billion" in jackpot.lower():
        print("Jackpot exceeds $1B, generating prediction...")

        # Getting historical data
        data = fetch_and_parse_powerball()

        # Generate predicted numbers based off historical data
        whites, powerball = predict_numbers(data)

        whites = sorted([int(w) for w in whites])

        # Build message
        message = f"White balls: {whites} Powerball: {powerball}"
        print(message)

        # Send notification
        send_notification(message)
    else:
        print("Jackpot below $1B, no notification sent.")
