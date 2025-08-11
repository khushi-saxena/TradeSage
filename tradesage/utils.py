import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data(csv_path: str) -> pd.DataFrame:
    """
    Load CSV into DataFrame, parse dates, set index.
    Expects at least 'Date' and 'Close' columns.
    """
    # Skip the first 2 rows which contain headers and metadata
    df = pd.read_csv(csv_path, skiprows=2)
    
    # Rename columns based on the CSV structure: Date, Close, High, Low, Open, Volume
    column_names = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    df.columns = column_names
    
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Set Date as index and sort
    df = df.set_index('Date').sort_index()
    
    return df

def save_plot(fig, filename: str):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fig.savefig(filename, bbox_inches='tight')
    plt.close(fig)
