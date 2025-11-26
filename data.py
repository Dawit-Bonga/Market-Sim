import pandas as pd 
import yfinance as yf

def get_price_data(tickers, start='2018-01-01', end='2025-11-01'):
    data = yf.download(tickers, start=start,end=end, auto_adjust=True)
    
    
    if isinstance(tickers, str):
        if 'Close' in data.columns:
            data = data[['Close']]
    else:
        if 'Close' in data.columns:
            data = data['Close']
    # if isinstance(data, pd.Series):
    #     data = data.to_frame()

    data = data.dropna(how="all")
    
    return data
    
    