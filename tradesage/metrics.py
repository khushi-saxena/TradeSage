import numpy as np
import pandas as pd

def compute_returns(signals: pd.DataFrame) -> pd.Series:
    """
    Compute strategy returns based on positions and price changes.
    """
    returns = signals['price'].pct_change().fillna(0)
    # shift signal so that today's signal applies to tomorrow's return
    strategy_returns = returns * signals['signal'].shift(1)
    return strategy_returns

def sharpe_ratio(returns: pd.Series, periods_per_year: int = 252) -> float:
    """
    Annualized Sharpe ratio, assuming risk-free=0.
    """
    mean = returns.mean() * periods_per_year
    std = returns.std() * np.sqrt(periods_per_year)
    return mean / std if std != 0 else np.nan

def max_drawdown(equity: pd.Series) -> float:
    """
    Max drawdown of an equity curve.
    """
    cum_max = equity.cummax()
    drawdown = (equity - cum_max) / cum_max
    return drawdown.min()
