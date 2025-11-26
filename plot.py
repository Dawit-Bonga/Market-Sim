import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime

def plot_equity_curves(portfolio_curve, spy_curve, tickers, start_date, end_date, save_path=None):
    """
    Plot portfolio equity curve vs SPY benchmark.
    
    Args:
        portfolio_curve: pandas Series with portfolio equity curve
        spy_curve: pandas Series with SPY equity curve
        tickers: list of ticker symbols
        start_date: start date string
        end_date: end date string
        save_path: optional path to save the figure
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot both curves
    ax.plot(portfolio_curve.index, portfolio_curve.values, 
            label=f'Portfolio ({", ".join(tickers)})', 
            linewidth=2, color='#2E86AB')
    ax.plot(spy_curve.index, spy_curve.values, 
            label='SPY (S&P 500)', 
            linewidth=2, color='#A23B72', linestyle='--')
    
    # Formatting
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Portfolio Value ($)', fontsize=12, fontweight='bold')
    ax.set_title(f'Portfolio vs SPY Performance\n{start_date} to {end_date}', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='best', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    
    # Format y-axis as currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved to {save_path}")
    
    plt.show()


def plot_drawdown(portfolio_curve, spy_curve, save_path=None):
    """
    Plot drawdown chart comparing portfolio and SPY.
    
    Args:
        portfolio_curve: pandas Series with portfolio equity curve
        spy_curve: pandas Series with SPY equity curve
        save_path: optional path to save the figure
    """
    # Calculate drawdowns
    portfolio_running_max = portfolio_curve.cummax()
    portfolio_drawdown = (portfolio_curve / portfolio_running_max - 1) * 100
    
    spy_running_max = spy_curve.cummax()
    spy_drawdown = (spy_curve / spy_running_max - 1) * 100
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Fill area under drawdown curves
    ax.fill_between(portfolio_drawdown.index, portfolio_drawdown.values, 0, 
                    alpha=0.3, color='#2E86AB', label='Portfolio Drawdown')
    ax.fill_between(spy_drawdown.index, spy_drawdown.values, 0, 
                    alpha=0.3, color='#A23B72', label='SPY Drawdown')
    
    # Plot drawdown lines
    ax.plot(portfolio_drawdown.index, portfolio_drawdown.values, 
            linewidth=1.5, color='#2E86AB')
    ax.plot(spy_drawdown.index, spy_drawdown.values, 
            linewidth=1.5, color='#A23B72', linestyle='--')
    
    # Formatting
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Drawdown (%)', fontsize=12, fontweight='bold')
    ax.set_title('Portfolio vs SPY Drawdown Analysis', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    
    # Set y-axis to show negative percentages
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1f}%'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Drawdown chart saved to {save_path}")
    
    plt.show()


def plot_monthly_returns(portfolio_returns, spy_returns, save_path=None):
    """
    Plot monthly returns comparison as bar chart.
    
    Args:
        portfolio_returns: pandas Series with portfolio daily returns
        spy_returns: pandas Series with SPY daily returns
        save_path: optional path to save the figure
    """
    # Convert to monthly returns
    portfolio_monthly = (1 + portfolio_returns).resample('M').prod() - 1
    spy_monthly = (1 + spy_returns).resample('M').prod() - 1
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x = np.arange(len(portfolio_monthly))
    width = 0.35
    
    # Create bars
    bars1 = ax.bar(x - width/2, portfolio_monthly.values * 100, width, 
                   label='Portfolio', color='#2E86AB', alpha=0.8)
    bars2 = ax.bar(x + width/2, spy_monthly.values * 100, width, 
                   label='SPY', color='#A23B72', alpha=0.8)
    
    # Formatting
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Monthly Return (%)', fontsize=12, fontweight='bold')
    ax.set_title('Monthly Returns: Portfolio vs SPY', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels([d.strftime('%Y-%m') for d in portfolio_monthly.index], 
                       rotation=45, ha='right')
    ax.legend(fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # Color bars based on positive/negative
    for bar in bars1:
        bar.set_color('#2E86AB' if bar.get_height() >= 0 else '#E63946')
    for bar in bars2:
        bar.set_color('#A23B72' if bar.get_height() >= 0 else '#E63946')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Monthly returns chart saved to {save_path}")
    
    plt.show()


def create_all_charts(portfolio_curve, spy_curve, portfolio_returns, spy_returns, 
                      tickers, start_date, end_date, output_dir='charts'):
    """
    Create all visualization charts and save them.
    
    Args:
        portfolio_curve: pandas Series with portfolio equity curve
        spy_curve: pandas Series with SPY equity curve
        portfolio_returns: pandas Series with portfolio daily returns
        spy_returns: pandas Series with SPY daily returns
        tickers: list of ticker symbols
        start_date: start date string
        end_date: end date string
        output_dir: directory to save charts
    """
    import os
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filenames
    ticker_str = '_'.join(tickers[:3])  # Use first 3 tickers for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    equity_path = os.path.join(output_dir, f'equity_curve_{ticker_str}_{timestamp}.png')
    drawdown_path = os.path.join(output_dir, f'drawdown_{ticker_str}_{timestamp}.png')
    monthly_path = os.path.join(output_dir, f'monthly_returns_{ticker_str}_{timestamp}.png')
    
    # Create and save charts
    plot_equity_curves(portfolio_curve, spy_curve, tickers, start_date, end_date, equity_path)
    plot_drawdown(portfolio_curve, spy_curve, drawdown_path)
    plot_monthly_returns(portfolio_returns, spy_returns, monthly_path)
    
    print(f"\nAll charts saved to '{output_dir}' directory")