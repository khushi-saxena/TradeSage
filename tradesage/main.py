import argparse
from .utils import load_data
from .strategy import SMACrossover
from .backtester import Backtester

def parse_args():
    parser = argparse.ArgumentParser(description="Run SMA Crossover backtest")
    parser.add_argument('--data-file', type=str, required=True,
                        help='Path to CSV file with Date and Close columns')
    parser.add_argument('--short-ma', type=int, default=50, help='Short moving average window')
    parser.add_argument('--long-ma',  type=int, default=200, help='Long moving average window')
    parser.add_argument('--initial-capital', type=float, default=100000.0,
                        help='Starting portfolio value')
    parser.add_argument('--output-plot', type=str, default='plots/backtest_result.png',
                        help='Where to save the equity curve')
    return parser.parse_args()

def main():
    args = parse_args()
    # load price data
    data = load_data(args.data_file)
    # setup strategy & backtester
    strat = SMACrossover(short_window=args.short_ma, long_window=args.long_ma)
    bt = Backtester(data, strat, initial_capital=args.initial_capital)
    # run
    stats = bt.run()
    # report comprehensive results
    print("=" * 60)
    print("📊 TRADESAGE BACKTEST RESULTS")
    print("=" * 60)
    
    # Core Performance Metrics
    print("\n🎯 CORE PERFORMANCE METRICS:")
    print("-" * 40)
    print(f"  Cumulative Return:     {stats['Cumulative Return']:.2%}")
    print(f"  Annualized Return:     {stats['Annualized Return']:.2%}")
    print(f"  Annualized Volatility: {stats['Annualized Volatility']:.2%}")
    print(f"  Sharpe Ratio:          {stats['Sharpe Ratio']:.3f}")
    print(f"  Sortino Ratio:         {stats['Sortino Ratio']:.3f}")
    print(f"  Calmar Ratio:          {stats['Calmar Ratio']:.3f}")
    
    # Risk Metrics
    print("\n⚠️  RISK METRICS:")
    print("-" * 40)
    print(f"  Maximum Drawdown:      {stats['Max Drawdown']:.2%}")
    print(f"  Best Trade:            {stats['Best Trade']:.2%}")
    print(f"  Worst Trade:           {stats['Worst Trade']:.2%}")
    
    # Trading Statistics
    print("\n📈 TRADING STATISTICS:")
    print("-" * 40)
    print(f"  Total Trades:          {stats['Total Trades']}")
    print(f"  Win Rate:              {stats['Win Rate']:.2%}")
    print(f"  Average Trade Return:  {stats['Average Trade Return']:.2%}")
    print(f"  Profit Factor:         {stats['Profit Factor']:.2f}")
    
    print("\n" + "=" * 60)
    # plot equity
    bt.plot_equity(args.output_plot)
    print(f"Equity curve saved to {args.output_plot}")

if __name__ == "__main__":
    main()
