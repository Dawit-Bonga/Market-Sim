from data import get_price_data
from backtest import backtest_portfolio, compute_metrics
import argparse
from plot import plot_equity_curves, plot_drawdown, plot_monthly_returns, create_all_charts

def main():
    # tickers = ["AAPL", "OPEN", "TSLA", "SPY"]
    # start = "2020-01-01"
    # end = "2025-01-01"
    
    parser = argparse.ArgumentParser(
        description="Backtest a portfolio of stocks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
        Examples:
  python app_cli.py --tickers AAPL TSLA --start 2020-01-01 --end 2024-01-01
  python app_cli.py --tickers AAPL OPEN TSLA SPY --start 2020-01-01 --end 2025-01-01 --initial 50000
        '''
    )
    
    parser.add_argument(
        '--tickers',
        nargs='+',
        default=["AAPL", "OPEN", "TSLA", "SPY"],
        help="Stock ticker symbols"
    )
    
    parser.add_argument(
        '--start',
        type=str,
        default='2020-01-01',
        help="Start Date is in YYYY-MM-DD format"
    )
    
    parser.add_argument(
        '--end',
        type=str,
        default='2025-01-01',
        help="End Date is in YYYY-MM-DD format"
    )
    
    parser.add_argument(
        '--initial',
        type=float,
        default=10000.0,
        help='Initial investment amount (default: 10000)'
    )
    
    parser.add_argument(
        '--plot',
        action='store_true',
        help='Display visualization charts'
    )
    
    parser.add_argument(
        '--save-charts',
        action='store_true',
        help='Save charts to files'
    )
    
    
    args = parser.parse_args()
    
    tickers = args.tickers
    start = args.start
    end = args.end
    initial_amount = args.initial
    
    
    
    
    
    prices = get_price_data(tickers, start, end)
    
    spy_prices = get_price_data(['SPY'], start, end)
    
    n = len(tickers)
    
    weights = [1 / n] * n
    
    equity_curve, port_returns = backtest_portfolio(prices, weights, initial_amount)
    
    metrics = compute_metrics(equity_curve, port_returns)
    
    spy_equity_curve, spy_returns = backtest_portfolio(spy_prices, [1.0], initial_amount)
    
    spy_metrics = compute_metrics(spy_equity_curve, spy_returns)
    
    # print("Portfolio:", tickers)
    # print(f"Initial Amount: ${intial_amount:,.2f}")
    # print(f"Final Value: ${equity_curve.iloc[-1]:,.2f}")
    # print("\nMetrics:")
    # for k,v in metrics.items():
    #    print(f"{k}: {v:.4f}")
    
    print("=" * 70)
    print(f"Backtest Period: {start} to {end}")
    print(f"Initial Investment: ${initial_amount:,.2f}")
    print("=" * 70)
    print(f"\nPortfolio Tickers: {', '.join(tickers)}")
    print(f"Benchmark: SPY (S&P 500)")
    print("\n" + "=" * 70)
    print(f"{'Metric':<25} {'Portfolio':<20} {'SPY':<20}")
    print("=" * 70)
    
    # Format and display each metric side-by-side
    for metric in ['total_return', 'annual_return', 'annual_vol', 'sharpe', 'max_drawdown']:
        portfolio_val = metrics[metric]
        spy_val = spy_metrics[metric]
        
        # Format as percentage for returns and drawdown
        if metric in ['total_return', 'annual_return', 'max_drawdown']:
            portfolio_str = f"{portfolio_val:.2%}"
            spy_str = f"{spy_val:.2%}"
        # Format as decimal for volatility
        elif metric == 'annual_vol':
            portfolio_str = f"{portfolio_val:.2%}"
            spy_str = f"{spy_val:.2%}"
        # Format as decimal for sharpe
        else:
            portfolio_str = f"{portfolio_val:.4f}"
            spy_str = f"{spy_val:.4f}"
        
        # Add indicator if portfolio outperforms
        indicator = "✓" if portfolio_val > spy_val else " " if metric != 'max_drawdown' else ("✓" if portfolio_val > spy_val else " ")
        
        print(f"{metric.replace('_', ' ').title():<25} {portfolio_str:<20} {spy_str:<20}")
    
    print("=" * 70)
    print(f"\nFinal Values:")
    print(f"Portfolio: ${equity_curve.iloc[-1]:,.2f}")
    print(f"SPY:       ${spy_equity_curve.iloc[-1]:,.2f}")
    
    # Calculate outperformance
    portfolio_final = equity_curve.iloc[-1]
    spy_final = spy_equity_curve.iloc[-1]
    outperformance = portfolio_final - spy_final
    outperformance_pct = (portfolio_final / spy_final - 1) * 100
    
    print(f"\nOutperformance: ${outperformance:,.2f} ({outperformance_pct:+.2f}%)")
    
    if args.plot or args.save_charts:
        print("\n" + "=" * 70)
        print("Generating visualizations...")
        print("=" * 70)
        
        if args.save_charts:
            create_all_charts(equity_curve, spy_equity_curve, port_returns, spy_returns, tickers, start, end)
        else:
            plot_equity_curves(equity_curve, spy_equity_curve, tickers, start, end)
            plot_drawdown(equity_curve, spy_equity_curve)
            plot_monthly_returns(port_returns, spy_returns)
            


if __name__ == "__main__":
    main()