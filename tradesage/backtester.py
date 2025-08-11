import pandas as pd
import matplotlib.pyplot as plt
from .metrics import compute_returns, calculate_all_metrics
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
        # Fill NaN values with 0 for the first period
        strat_ret = strat_ret.fillna(0)
        equity = (1 + strat_ret).cumprod() * self.initial_capital
        # compute comprehensive metrics
        stats = calculate_all_metrics(strat_ret, equity, signals)
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
