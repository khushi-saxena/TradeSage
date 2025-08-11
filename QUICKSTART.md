# TradeSage Quick Start Guide 🚀

Get up and running with TradeSage in under 5 minutes!

## ⚡ Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Your First Backtest
```bash
python -m tradesage.main --data-file data/AAPL_5y.csv --short-ma 20 --long-ma 100 --initial-capital 100000
```

### 3. Check Results
- View performance metrics in the terminal
- Find your equity curve plot in `plots/backtest_result.png`

## 🎯 What Just Happened?

You just ran a **Simple Moving Average (SMA) Crossover** strategy on Apple stock data:

- **Strategy**: Buy when 20-day MA > 100-day MA, sell when 20-day MA < 100-day MA
- **Data**: 5 years of Apple stock prices
- **Capital**: $100,000 starting investment
- **Output**: Performance metrics + equity curve visualization

## 📊 Understanding Your Results

The output shows:
- **Cumulative Return**: Total profit/loss percentage
- **Sharpe Ratio**: Risk-adjusted performance (higher = better)
- **Max Drawdown**: Worst decline from peak (lower = better)
- **Total Trades**: Number of buy/sell signals

## 🔄 Try Different Settings

### More Aggressive (More Trades)
```bash
python -m tradesage.main --data-file data/AAPL_5y.csv --short-ma 10 --long-ma 50
```

### More Conservative (Fewer Trades)
```bash
python -m tradesage.main --data-file data/AAPL_5y.csv --short-ma 100 --long-ma 300
```

### Different Capital
```bash
python -m tradesage.main --data-file data/AAPL_5y.csv --initial-capital 50000
```

## 📈 Next Steps

1. **Experiment** with different MA periods
2. **Download new data** for other stocks using yfinance
3. **Open the Jupyter notebook** for interactive analysis
4. **Read the full README** for advanced features

## 🆘 Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Look at the troubleshooting section for common issues
- Verify your CSV data format matches the requirements

---

**That's it! You're now ready to explore algorithmic trading with TradeSage! 📈**
