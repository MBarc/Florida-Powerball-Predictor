# 🎰 Florida Powerball Predictor 🎰

An automated Powerball number prediction system that analyzes historical lottery data to generate predictions and sends notifications when jackpots exceed $1 billion.

## Features

- **Historical Data Collection**: Scrapes 10+ years of Powerball results from official website
- **Frequency-Based Predictions**: Generates number predictions based on historical frequency patterns
- **Smart Notifications**: Automatically sends push notifications via IFTTT when jackpots exceed $1B
- **Automated Monitoring**: Checks current jackpot amounts and triggers predictions accordingly

## System Flow

```mermaid
flowchart TD
    A[GitHub Actions Trigger<br/>9:00 AM on Drawing Days<br/>Mon/Wed/Sat] --> B[Check Current Jackpot]
    B --> C{Jackpot > $1 Billion?}
    C -->|No| D[End - No Action Taken]
    C -->|Yes| E[Scrape Historical Data<br/>Past 10 Years of Results]
    E --> F[Analyze Number <br/>Frequencies<br/> of White Balls & Powerball]
    F --> G[Generate Prediction<br/>Based on Historical Patterns]
    G --> H[Send to IFTTT Webhook<br/>POST Request with Prediction]
    H --> I[IFTTT Applet Triggered]
    I --> J[Push Notification Sent<br/>to Mobile Device]
    
    style A fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style C fill:#FF9800,stroke:#F57C00,stroke-width:2px,color:#fff
    style D fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style J fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
```

## How It Works

1. **Data Collection** (`dataGatherer.py`): Uses Selenium to scrape historical Powerball results
2. **Prediction Engine** (`predictNumbers.py`): Analyzes number frequencies to generate predictions
3. **Jackpot Monitoring** (`main.py`): Checks current jackpot and triggers system when threshold is met
4. **Notifications** (`notifier.py`): Sends predictions via IFTTT webhooks

## Installation

### Prerequisites
- Python 3.7+
- Chrome browser
- ChromeDriver

### Setup
```bash
git clone https://github.com/yourusername/powerball-predictor.git
cd powerball-predictor
pip install -r requirements.txt
```

### Required Dependencies
```
pandas
selenium
beautifulsoup4
requests
numpy
```

## Configuration

### IFTTT Setup
1. Create an IFTTT account and set up a webhook trigger
2. Replace the webhook URL in `notifier.py` with your own IFTTT webhook URL
3. Configure your preferred notification method (email, SMS, etc.) in IFTTT

### ChromeDriver
Ensure ChromeDriver is installed and accessible in your PATH, or update the driver path in `dataGatherer.py`.

## Usage

### Run the complete system:
```bash
python main.py
```

### Individual components:

**Collect historical data:**
```bash
python dataGatherer.py
```

**Generate predictions (requires data):**
```bash
python predictNumbers.py
```

**Test notifications:**
```bash
python notifier.py
```

## Example Output

```
Current Jackpot: $1.40 Billion
Jackpot exceeds $1B, generating prediction...
Clicked 'Load More' button. . .
Gathering more data. . .
Reached 10 years of data: 2014-12-15 00:00:00
White balls: [12, 23, 44, 57, 61] Powerball: 18
IFTTT notification sent successfully!
```

## Technical Details

### Data Collection Strategy
- Scrapes official Powerball website for maximum accuracy
- Collects 10+ years of historical results automatically
- Handles dynamic loading with Selenium automation

### Prediction Algorithm
- Analyzes frequency patterns of white balls (1-69) and Powerball numbers (1-26)
- Uses weighted random sampling based on historical occurrence rates
- **Note**: This is for entertainment purposes only - lottery numbers are random!

### Notification System
- Integrates with IFTTT for flexible notification options
- Only triggers when jackpots exceed $1 billion threshold
- Customizable message format and delivery methods

## Project Structure

```
powerball-predictor/
├── main.py              # Main orchestration script
├── dataGatherer.py      # Web scraping and data collection
├── predictNumbers.py    # Prediction algorithm
├── notifier.py          # IFTTT notification system
└── README.md           # This file
```

## Limitations & Disclaimers

⚠️ **Important**: This project is for educational and entertainment purposes only. Lottery numbers are random, and past results do not influence future drawings. This system cannot predict actual winning numbers.

- Requires stable internet connection for web scraping
- ChromeDriver compatibility needed for Selenium
- Rate limiting may affect data collection speed
- IFTTT webhook has usage limits

## Future Enhancements

- [ ] Add support for other lottery games (Mega Millions, etc.)
- [ ] Implement more sophisticated ML models (neural networks, regression)
- [ ] Add data visualization dashboard
- [ ] Create Slack/Discord notification options
- [ ] Add historical prediction accuracy tracking
- [ ] Implement database storage for long-term data retention

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Official Powerball website for providing historical data
- IFTTT for notification services
- Selenium and BeautifulSoup communities for web scraping tools

---

**Disclaimer**: Gambling can be addictive. Please play responsibly and within your means. This tool is for entertainment and educational purposes only.
