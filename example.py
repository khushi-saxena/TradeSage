#!/usr/bin/env python3
"""
TradeSage Example Script
Demonstrates how to use TradeSage programmatically
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradesage.utils import load_data
from tradesage.strategy import SMACrossover
from tradesage.backtester import Backtester
import matplotlib.pyplot as plt

def main():
    """Example of using TradeSage programmatically"""
    
    print("🚀 TradeSage Example - Programmatic Usage")
    print("=" * 50)
    
    # 1. Load data
    print("📊 Loading Apple stock data...")
    data = load_data('data/AAPL_5y.csv')
    print(f"   Loaded {len(data)} days of data")
    print(f"   Date range: {data.index[0].date()} to {data.index[-1].date()}")
    print(f"   Price range: ${data['Close'].min():.2f} - ${data['Close'].max():.2f}")
    
    # 2. Create strategy
    print("\n📈 Creating SMA Crossover strategy...")
    strategy = SMACrossover(short_window=20, long_window=100)
    print(f"   Short MA: {strategy.short} days")
    print(f"   Long MA: {strategy.long} days")
    
    # 3. Run backtest
    print("\n🔄 Running backtest...")
    backtester = Backtester(data, strategy, initial_capital=100000)
    results = backtester.run()
    
    # 4. Display results
    print("\n📊 Backtest Results:")
    print("-" * 30)
    for metric, value in results.items():
        print(f"   {metric}: {value:.4f}")
    
    # 5. Create custom plot
    print("\n📈 Creating custom visualization...")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Price and moving averages
    ax1.plot(data.index, data['Close'], label='AAPL Price', alpha=0.7)
    ax1.plot(data.index, data['Close'].rolling(strategy.short).mean(), 
             label=f'{strategy.short}-day MA', alpha=0.8)
    ax1.plot(data.index, data['Close'].rolling(strategy.long).mean(), 
             label=f'{strategy.long}-day MA', alpha=0.8)
    ax1.set_title('AAPL Price with Moving Averages')
    ax1.set_ylabel('Price ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Equity curve
    equity_curve = backtester.equity
    ax2.plot(equity_curve.index, equity_curve.values, label='Portfolio Value', linewidth=2)
    ax2.set_title('Portfolio Equity Curve')
    ax2.set_ylabel('Portfolio Value ($)')
    ax2.set_xlabel('Date')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/example_analysis.png', dpi=300, bbox_inches='tight')
    print("   Saved to: plots/example_analysis.png")
    
    # 6. Strategy analysis
    print("\n🔍 Strategy Analysis:")
    print("-" * 30)
    
    # Calculate some additional metrics
    total_return = results['Cumulative Return']
    sharpe_ratio = results['Sharpe Ratio']
    max_drawdown = results['Max Drawdown']
    total_trades = results['Total Trades']
    
    print(f"   Strategy Performance:")
    print(f"     • Total Return: {total_return:.2%}")
    print(f"     • Annualized Return: {total_return * (252/len(data)):.2%}")
    print(f"     • Sharpe Ratio: {sharpe_ratio:.3f}")
    print(f"     • Max Drawdown: {max_drawdown:.2%}")
    print(f"     • Total Trades: {int(total_trades)}")
    
    # Performance interpretation
    print(f"\n   Performance Assessment:")
    if total_return > 0:
        print(f"     ✅ Strategy generated positive returns")
    else:
        print(f"     ❌ Strategy generated negative returns")
    
    if sharpe_ratio > 1.0:
        print(f"     ✅ Good risk-adjusted returns (Sharpe > 1.0)")
    elif sharpe_ratio > 0.5:
        print(f"     ⚠️  Moderate risk-adjusted returns")
    else:
        print(f"     ❌ Poor risk-adjusted returns")
    
    if abs(max_drawdown) < 0.2:
        print(f"     ✅ Acceptable drawdown (< 20%)")
    else:
        print(f"     ⚠️  High drawdown risk (> 20%)")
    
    print(f"\n🎯 Example completed successfully!")
    print(f"   Check 'plots/example_analysis.png' for detailed charts")

if __name__ == "__main__":
    main()
