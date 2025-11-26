# Market Simulator - Portfolio Backtesting Tool

A Python tool for backtesting investment portfolios and comparing their performance against benchmarks like the S&P 500 (SPY).

## Overview

This project allows you to:

- Download historical stock price data for any tickers
- Backtest a portfolio with custom weights
- Calculate key performance metrics (returns, volatility, Sharpe ratio, max drawdown)
- Compare portfolio performance (future: visualization and SPY comparison)

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

Currently, the portfolio is hardcoded in `app_cli.py`. Run:

```bash
python app_cli.py
```

This will backtest a portfolio of AAPL, OPEN, TSLA, and SPY from 2020-01-01 to 2025-01-01.

## Project Structure

- `data.py`: Handles downloading and processing stock price data
- `backtest.py`: Contains backtesting logic and metric calculations
- `app_cli.py`: Main entry point for running backtests

## Next Steps

See the development roadmap below for planned improvements.

## Requirements

- Python 3.8+
- pandas
- numpy
- yfinance
