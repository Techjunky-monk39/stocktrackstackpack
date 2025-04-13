import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta


def get_stock_data(ticker):
    """
    Fetch stock data for the given ticker.
    
    Args:
        ticker (str): Stock symbol
        
    Returns:
        tuple: (stock_info, stock_history)
    """
    try:
        # Create ticker object
        stock = yf.Ticker(ticker)
        
        # Get stock info
        info = stock.info
        
        # Get historical data
        history = stock.history(period="5y")
        
        if history.empty:
            return None, None
        
        # Extract relevant info
        stock_info = {
            'symbol': ticker,
            'longName': info.get('longName', 'N/A'),
            'currentPrice': info.get('currentPrice', info.get('regularMarketPrice', 'N/A')),
            'previousClose': info.get('previousClose', 'N/A'),
            'open': info.get('open', info.get('regularMarketOpen', 'N/A')),
            'dayHigh': info.get('dayHigh', info.get('regularMarketDayHigh', 'N/A')),
            'dayLow': info.get('dayLow', info.get('regularMarketDayLow', 'N/A')),
            'marketCap': info.get('marketCap', 'N/A'),
            'volume': info.get('volume', info.get('regularMarketVolume', 'N/A')),
            'averageVolume': info.get('averageVolume', 'N/A'),
            'peRatio': info.get('trailingPE', 'N/A'),
            'eps': info.get('trailingEps', 'N/A'),
            'dividendYield': info.get('dividendYield', 'N/A'),
            'beta': info.get('beta', 'N/A'),
            '52WeekHigh': info.get('fiftyTwoWeekHigh', 'N/A'),
            '52WeekLow': info.get('fiftyTwoWeekLow', 'N/A'),
            'targetMeanPrice': info.get('targetMeanPrice', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'website': info.get('website', 'N/A'),
            'currency': info.get('currency', 'USD'),
        }
        
        return stock_info, history
    
    except Exception as e:
        raise Exception(f"Error fetching stock data: {str(e)}")


def create_stock_chart(history, ticker, days=None):
    """
    Create an interactive stock price chart.
    
    Args:
        history (DataFrame): Historical stock data
        ticker (str): Stock symbol
        days (int, optional): Number of days to show. None for all data.
        
    Returns:
        plotly.graph_objects.Figure: Interactive chart
    """
    # Filter data if days is specified
    if days is not None:
        # Get the start date for filtering
        start_date = datetime.now() - timedelta(days=days)
        
        # Handle timezone-aware datetime index by converting to the same timezone format
        if history.index.tzinfo is not None:
            # Convert start_date to UTC or make it timezone-aware to match the dataframe's timezone
            from pandas import Timestamp
            start_date = Timestamp(start_date).tz_localize('UTC').tz_convert(history.index.tzinfo)
        
        # Now filter the data
        history = history[history.index >= start_date]
    
    # Create figure
    fig = go.Figure()
    
    # Add candlestick chart
    fig.add_trace(go.Candlestick(
        x=history.index,
        open=history['Open'],
        high=history['High'],
        low=history['Low'],
        close=history['Close'],
        name='Price'
    ))
    
    # Add moving averages
    if len(history) > 20:
        history['MA20'] = history['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(
            x=history.index,
            y=history['MA20'],
            line=dict(color='orange', width=1),
            name='20-day MA'
        ))
    
    if len(history) > 50:
        history['MA50'] = history['Close'].rolling(window=50).mean()
        fig.add_trace(go.Scatter(
            x=history.index,
            y=history['MA50'],
            line=dict(color='red', width=1),
            name='50-day MA'
        ))
    
    # Add volume as a bar chart in a separate subplot
    fig.add_trace(go.Bar(
        x=history.index,
        y=history['Volume'],
        marker_color='rgba(0, 0, 255, 0.3)',
        name='Volume',
        yaxis='y2'
    ))
    
    # Update layout
    fig.update_layout(
        title=f'{ticker} Stock Price Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        height=600,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    return fig
