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

def sharpe_ratio(returns: pd.Series, periods_per_year: int = 252, risk_free_rate: float = 0.0) -> float:
    """
    Annualized Sharpe ratio.
    
    Args:
        returns: Series of returns
        periods_per_year: Number of periods per year (252 for daily)
        risk_free_rate: Risk-free rate (default 0.0)
    
    Returns:
        Annualized Sharpe ratio
    """
    excess_returns = returns - risk_free_rate
    mean = excess_returns.mean() * periods_per_year
    std = excess_returns.std() * np.sqrt(periods_per_year)
    return mean / std if std != 0 else np.nan

def sortino_ratio(returns: pd.Series, periods_per_year: int = 252, risk_free_rate: float = 0.0) -> float:
    """
    Annualized Sortino ratio (downside risk-adjusted return).
    
    Args:
        returns: Series of returns
        periods_per_year: Number of periods per year (252 for daily)
        risk_free_rate: Risk-free rate (default 0.0)
    
    Returns:
        Annualized Sortino ratio
    """
    excess_returns = returns - risk_free_rate
    downside_returns = excess_returns[excess_returns < 0]
    downside_std = downside_returns.std() * np.sqrt(periods_per_year)
    mean = excess_returns.mean() * periods_per_year
    return mean / downside_std if downside_std != 0 else np.nan

def max_drawdown(equity: pd.Series) -> float:
    """
    Maximum drawdown of an equity curve.
    
    Args:
        equity: Series of portfolio values
    
    Returns:
        Maximum drawdown as a negative percentage
    """
    cum_max = equity.cummax()
    drawdown = (equity - cum_max) / cum_max
    return drawdown.min()

def calmar_ratio(returns: pd.Series, equity: pd.Series, periods_per_year: int = 252) -> float:
    """
    Calmar ratio: annualized return / maximum drawdown.
    
    Args:
        returns: Series of returns
        equity: Series of portfolio values
        periods_per_year: Number of periods per year (252 for daily)
    
    Returns:
        Calmar ratio
    """
    annualized_return = returns.mean() * periods_per_year
    max_dd = abs(max_drawdown(equity))
    return annualized_return / max_dd if max_dd != 0 else np.nan

def win_rate(signals: pd.DataFrame) -> float:
    """
    Calculate win rate of trades.
    
    Args:
        signals: DataFrame with 'positions' column indicating trade entries/exits
    
    Returns:
        Win rate as a percentage
    """
    positions = signals['positions']
    trades = positions[positions != 0]
    
    if len(trades) == 0:
        return 0.0
    
    # Calculate returns for each trade
    trade_returns = []
    in_position = False
    entry_price = 0
    
    for i, (date, row) in enumerate(signals.iterrows()):
        if row['positions'] == 1 and not in_position:  # Enter long position
            entry_price = row['price']
            in_position = True
        elif row['positions'] == -1 and in_position:  # Exit long position
            exit_price = row['price']
            trade_return = (exit_price - entry_price) / entry_price
            trade_returns.append(trade_return)
            in_position = False
    
    if len(trade_returns) == 0:
        return 0.0
    
    winning_trades = sum(1 for ret in trade_returns if ret > 0)
    return winning_trades / len(trade_returns)

def average_trade_return(signals: pd.DataFrame) -> float:
    """
    Calculate average return per trade.
    
    Args:
        signals: DataFrame with 'positions' and 'price' columns
    
    Returns:
        Average trade return
    """
    positions = signals['positions']
    trades = positions[positions != 0]
    
    if len(trades) == 0:
        return 0.0
    
    # Calculate returns for each trade
    trade_returns = []
    in_position = False
    entry_price = 0
    
    for i, (date, row) in enumerate(signals.iterrows()):
        if row['positions'] == 1 and not in_position:  # Enter long position
            entry_price = row['price']
            in_position = True
        elif row['positions'] == -1 and in_position:  # Exit long position
            exit_price = row['price']
            trade_return = (exit_price - entry_price) / entry_price
            trade_returns.append(trade_return)
            in_position = False
    
    return np.mean(trade_returns) if trade_returns else 0.0

def profit_factor(signals: pd.DataFrame) -> float:
    """
    Calculate profit factor (gross profit / gross loss).
    
    Args:
        signals: DataFrame with 'positions' and 'price' columns
    
    Returns:
        Profit factor
    """
    positions = signals['positions']
    trades = positions[positions != 0]
    
    if len(trades) == 0:
        return 0.0
    
    # Calculate returns for each trade
    trade_returns = []
    in_position = False
    entry_price = 0
    
    for i, (date, row) in enumerate(signals.iterrows()):
        if row['positions'] == 1 and not in_position:  # Enter long position
            entry_price = row['price']
            in_position = True
        elif row['positions'] == -1 and in_position:  # Exit long position
            exit_price = row['price']
            trade_return = (exit_price - entry_price) / entry_price
            trade_returns.append(trade_return)
            in_position = False
    
    if not trade_returns:
        return 0.0
    
    gross_profit = sum(ret for ret in trade_returns if ret > 0)
    gross_loss = abs(sum(ret for ret in trade_returns if ret < 0))
    
    return gross_profit / gross_loss if gross_loss != 0 else np.inf

def calculate_all_metrics(returns: pd.Series, equity: pd.Series, signals: pd.DataFrame) -> dict:
    """
    Calculate comprehensive performance metrics.
    
    Args:
        returns: Series of strategy returns
        equity: Series of portfolio values
        signals: DataFrame with strategy signals
    
    Returns:
        Dictionary containing all performance metrics
    """
    # Calculate cumulative return properly
    initial_value = equity.iloc[0] if len(equity) > 0 else 1.0
    final_value = equity.iloc[-1] if len(equity) > 0 else 1.0
    cumulative_return = (final_value / initial_value - 1) if initial_value != 0 else 0.0
    
    metrics = {
        'Cumulative Return': cumulative_return,
        'Sharpe Ratio': sharpe_ratio(returns),
        'Sortino Ratio': sortino_ratio(returns),
        'Max Drawdown': max_drawdown(equity),
        'Calmar Ratio': calmar_ratio(returns, equity),
        'Total Trades': int(signals['positions'].abs().sum()),
        'Win Rate': win_rate(signals),
        'Average Trade Return': average_trade_return(signals),
        'Profit Factor': profit_factor(signals),
        'Annualized Return': returns.mean() * 252,
        'Annualized Volatility': returns.std() * np.sqrt(252),
        'Best Trade': max([ret for ret in returns if ret > 0]) if any(returns > 0) else 0.0,
        'Worst Trade': min([ret for ret in returns if ret < 0]) if any(returns < 0) else 0.0
    }
    
    return metrics
