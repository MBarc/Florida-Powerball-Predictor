<p align="center">
  <img src="pics/PowerballPredictorLogo.png" alt="Project Logo" width="500"/>
</p>

<h1 align="center">🎰 Florida Powerball Predictor 🎰</h1>

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

### Local Setup
```bash
git clone https://github.com/MBarc/Florida-Powerball-Predictor.git
cd Florida-Powerball-Predictor
pip install -r requirements.txt
cd src
python main.py
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
├── .github/
│   └── workflows/
│       └── run.yml    # GitHub Actions workflow for automated execution
├── src/
│   ├── main.py                    # Main orchestration script and entry point
│   ├── dataGatherer.py           # Web scraping module for historical Powerball data
│   ├── predictNumbers.py         # Prediction algorithm using frequency analysis
│   └── notifier.py              # IFTTT webhook notification system
├── requirements.txt              # Python dependencies
├── README.md                    # Project documentation
└── LICENSE                      # MIT license
```

## Limitations & Disclaimers

⚠️ **Important**: This project is for educational and entertainment purposes only.

- Requires stable internet connection for web scraping
- ChromeDriver compatibility needed for Selenium
- Rate limiting may affect data collection speed or may cause script to fail
- IFTTT webhook has usage limits

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
