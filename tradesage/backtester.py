import pandas as pd
import matplotlib.pyplot as plt
from .metrics import compute_returns, sharpe_ratio, max_drawdown
from .utils import save_plot
import os

class Backtester:
    def __init__(self, data: pd.DataFrame, strategy, initial_capital: float = 100000.0):
        self.data = data.copy()
        self.strategy = strategy
        self.initial_capital = initial_capital

    def run(self):
        # generate signals
        signals = self.strategy.generate_signals(self.data)
        # calculate returns and equity curve
        strat_ret = compute_returns(signals)
        equity = (1 + strat_ret).cumprod() * self.initial_capital
        # compute metrics
        stats = {
            'Cumulative Return': equity.iloc[-1] / self.initial_capital - 1,
            'Sharpe Ratio': sharpe_ratio(strat_ret),
            'Max Drawdown': max_drawdown(equity),
            'Total Trades': int(signals['positions'].abs().sum())
        }
        self.signals = signals
        self.returns = strat_ret
        self.equity = equity
        self.stats = stats
        return stats

    def plot_equity(self, output_path: str):
        fig, ax = plt.subplots()
        ax.plot(self.equity.index, self.equity.values)
        ax.set_title('Equity Curve')
        ax.set_xlabel('Date')
        ax.set_ylabel('Portfolio Value')
        save_plot(fig, output_path)
