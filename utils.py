import pandas as pd
import random

def format_financial_data(data):
    """
    Format financial data for display.
    
    Args:
        data (dict): Raw financial data
        
    Returns:
        dict: Formatted financial data
    """
    formatted = {}
    
    # Currency formatting helper function
    def format_currency(value, currency="$"):
        if value == 'N/A' or value is None:
            return 'N/A'
        
        if isinstance(value, (int, float)):
            if value >= 1_000_000_000:
                return f"{currency}{value/1_000_000_000:.2f}B"
            elif value >= 1_000_000:
                return f"{currency}{value/1_000_000:.2f}M"
            elif value >= 1_000:
                return f"{currency}{value/1_000:.2f}K"
            else:
                return f"{currency}{value:.2f}"
        return value
    
    # Percentage formatting helper function
    def format_percentage(value):
        if value == 'N/A' or value is None:
            return 'N/A'
        
        if isinstance(value, (int, float)):
            return f"{value*100:.2f}%" if value < 1 else f"{value:.2f}%"
        return value
    
    # Format each metric appropriately
    currency = data.get('currency', 'USD')
    currency_symbol = "$" if currency == "USD" else currency + " "
    
    formatted["Company"] = data.get('longName', 'N/A')
    formatted["Current Price"] = format_currency(data.get('currentPrice', 'N/A'), currency_symbol)
    formatted["Previous Close"] = format_currency(data.get('previousClose', 'N/A'), currency_symbol)
    formatted["Open"] = format_currency(data.get('open', 'N/A'), currency_symbol)
    formatted["Day High"] = format_currency(data.get('dayHigh', 'N/A'), currency_symbol)
    formatted["Day Low"] = format_currency(data.get('dayLow', 'N/A'), currency_symbol)
    formatted["Market Cap"] = format_currency(data.get('marketCap', 'N/A'), currency_symbol)
    formatted["P/E Ratio"] = data.get('peRatio', 'N/A')
    formatted["EPS"] = format_currency(data.get('eps', 'N/A'), currency_symbol)
    formatted["Dividend Yield"] = format_percentage(data.get('dividendYield', 'N/A'))
    formatted["Beta"] = data.get('beta', 'N/A')
    formatted["52-Week High"] = format_currency(data.get('52WeekHigh', 'N/A'), currency_symbol)
    formatted["52-Week Low"] = format_currency(data.get('52WeekLow', 'N/A'), currency_symbol)
    formatted["Target Price"] = format_currency(data.get('targetMeanPrice', 'N/A'), currency_symbol)
    formatted["Volume"] = data.get('volume', 'N/A')
    if formatted["Volume"] != 'N/A' and isinstance(formatted["Volume"], (int, float)):
        formatted["Volume"] = f"{formatted['Volume']:,}"
    formatted["Avg. Volume"] = data.get('averageVolume', 'N/A')
    if formatted["Avg. Volume"] != 'N/A' and isinstance(formatted["Avg. Volume"], (int, float)):
        formatted["Avg. Volume"] = f"{formatted['Avg. Volume']:,}"
    formatted["Sector"] = data.get('sector', 'N/A')
    formatted["Industry"] = data.get('industry', 'N/A')
    
    return formatted

def convert_df_to_csv(df):
    """
    Convert dataframe to CSV for download.
    
    Args:
        df (pandas.DataFrame): Dataframe to convert
        
    Returns:
        str: CSV data
    """
    return df.to_csv(index=False).encode('utf-8')

def get_random_image(image_list):
    """
    Return a random image URL from the provided list.
    
    Args:
        image_list (list): List of image URLs
        
    Returns:
        str: Random image URL
    """
    return random.choice(image_list)
