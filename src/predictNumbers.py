import pandas as pd
import numpy as np


def predict_numbers(df):
    """
    Expects a DataFrame with columns:
        'date', 'day_of_week', 'week_number', 'numbers', 'powerball', 'powerplay'
    'numbers' should be a string of 5 space-separated white ball numbers.
    'powerball' should be a string or int representing the Powerball number.
    """
    # Split white balls into separate columns
    white_balls = df['numbers'].str.split(' ', expand=True).astype(int)
    white_balls.columns = [f'white_{i+1}' for i in range(5)]
    # Ensure powerball is int
    powerball_col = df['powerball'].astype(int)
    df_ml = pd.concat([white_balls, powerball_col], axis=1)
    df_ml.columns = [f'white_{i+1}' for i in range(5)] + ['powerball']

    # Frequencies
    all_white = df_ml[[f'white_{i+1}' for i in range(5)]].values.flatten()
    white_counts = pd.Series(all_white).value_counts(normalize=True)
    powerball_counts = df_ml['powerball'].value_counts(normalize=True)

    # Sample prediction
    predicted_whites = np.random.choice(
        white_counts.index, size=5, replace=False, p=white_counts.values
    )
    predicted_powerball = np.random.choice(
        powerball_counts.index, p=powerball_counts.values
    )

    return sorted(predicted_whites), int(predicted_powerball)
