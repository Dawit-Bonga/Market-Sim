from data import get_price_data
from backtest import backtest_portfolio, compute_metrics

def main():
    tickers = ["AAPL", "OPEN", "TSLA", "SPY"]
    start = "2020-01-01"
    end = "2025-01-01"
    
    prices = get_price_data(tickers, start, end)
    
    n = len(tickers)
    
    weights = [1 / n] * n
    
    equity_curve, port_returns = backtest_portfolio(prices, weights)
    
    metrics = compute_metrics(equity_curve, port_returns)
    
    print("Portfolio:", tickers)
    for k,v in metrics.items():
       print(f"{k}: {v:.4f}")


if __name__ == "__main__":
    main()