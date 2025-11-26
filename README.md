# Market Simulator - Portfolio Backtesting Tool

A Python tool for backtesting investment portfolios and comparing their performance against benchmarks like the S&P 500 (SPY).

## Overview

This project allows you to:

- Download historical stock price data for any tickers
- Backtest a portfolio with equal weights (custom weights support coming soon)
- Calculate key performance metrics (returns, volatility, Sharpe ratio, max drawdown)
- Compare portfolio performance against SPY with visual dashboards

## Features

- **Data Collection**: Fetches historical price data using Yahoo Finance API
- **Portfolio Backtesting**: Simulates portfolio performance with equal or custom weights
- **Performance Metrics**: Calculates:
  - Total return
  - Annualized return
  - Annualized volatility
  - Sharpe ratio
  - Maximum drawdown

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Streamlit dashboard (recommended)

Run an interactive dashboard with charts, data tables, and download options:

```bash
streamlit run app_streamlit.py
```

Use the sidebar to pick tickers, change the time range, adjust the initial investment, and toggle SPY benchmarking or monthly return charts.

### Command-line interface

The CLI mirrors the dashboard logic for quick scripted runs:

```bash
python app_cli.py --tickers AAPL OPEN TSLA SPY --start 2020-01-01 --end 2025-01-01 --initial 25000 --plot
```

Use `python app_cli.py --help` to discover all available flags.

## Project Structure

- `data.py`: Handles downloading and processing stock price data
- `backtest.py`: Contains backtesting logic and metric calculations
- `plot.py`: Matplotlib helpers for CLI plots
- `app_cli.py`: Command-line entry point
- `app_streamlit.py`: Interactive dashboard entry point

## Next Steps

See the development roadmap below for planned improvements.

## Requirements

- Python 3.8+
- pandas
- numpy
- yfinance
