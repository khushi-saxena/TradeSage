import pandas as pd

class SMACrossover:
    def __init__(self, short_window: int = 50, long_window: int = 200):
        if short_window >= long_window:
            raise ValueError("short_window must be < long_window")
        self.short = short_window
        self.long = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Returns DataFrame with columns:
          - 'signal': +1 for long, 0 for flat
          - 'positions': diff of signal (entry/exit)
        """
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['Close']
        signals['short_ma'] = data['Close'].rolling(window=self.short, min_periods=1).mean()
        signals['long_ma']  = data['Close'].rolling(window=self.long, min_periods=1).mean()
        signals['signal']   = 0
        signals.loc[signals['short_ma'] > signals['long_ma'], 'signal'] = 1
        signals['positions'] = signals['signal'].diff().fillna(0)
        return signals
