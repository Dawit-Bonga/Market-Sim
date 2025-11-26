import numpy as np
import pandas as pd

def compute_returns(prices: pd.DataFrame):
    returns = prices.pct_change().dropna()
    return returns

def backtest_portfolio(prices, weights, initial_amount: float = 10_000):
    results = compute_returns(prices)
    
    w = np.array(weights, dtype=float)
    w = w / w.sum()
    
    port_returns = (results * w).sum(axis=1)
    
    equity_curve = (1 + port_returns).cumprod() * initial_amount
    
    return equity_curve, port_returns


def compute_metrics(equity_curve, port_returns, risk_free_rate: float = 0.0):
    total_returns = equity_curve.iloc[-1] / equity_curve.iloc[0] - 1  #last minus first
    
    daily_mean_return = port_returns.mean()
    daily_vol = port_returns.std()
    annual_return = daily_mean_return * 252
    annual_vol = daily_vol * np.sqrt(252)
    
    sharpe = (annual_return - risk_free_rate) / annual_vol if annual_vol != 0 else np.nan
    
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1
    max_drawdown = drawdown.min()
    
    return {
        "total_return": total_returns,
        "annual_return": annual_return,
        "annual_vol": annual_vol,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
    }
    
    
    
    
    