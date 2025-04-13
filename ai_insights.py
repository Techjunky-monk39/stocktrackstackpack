import os
from openai import OpenAI

# The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# Do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

def get_openai_client():
    """
    Initialize and return the OpenAI client.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables. Please set OPENAI_API_KEY.")
    return OpenAI(api_key=api_key)

def generate_stock_insights(ticker, stock_data):
    """
    Generate AI-powered insights for the given stock.
    
    Args:
        ticker (str): Stock symbol
        stock_data (dict): Stock information
        
    Returns:
        str: AI-generated insights
    """
    try:
        client = get_openai_client()
        
        # Create a simplified version of stock data
        data_for_ai = {
            "symbol": ticker,
            "company_name": stock_data.get('longName', 'N/A'),
            "current_price": stock_data.get('currentPrice', 'N/A'),
            "previous_close": stock_data.get('previousClose', 'N/A'),
            "market_cap": stock_data.get('marketCap', 'N/A'),
            "pe_ratio": stock_data.get('peRatio', 'N/A'),
            "eps": stock_data.get('eps', 'N/A'),
            "dividend_yield": stock_data.get('dividendYield', 'N/A'),
            "52_week_high": stock_data.get('52WeekHigh', 'N/A'),
            "52_week_low": stock_data.get('52WeekLow', 'N/A'),
            "analyst_target_price": stock_data.get('targetMeanPrice', 'N/A'),
            "sector": stock_data.get('sector', 'N/A'),
            "industry": stock_data.get('industry', 'N/A'),
        }
        
        # Prepare prompt for the AI
        prompt = f"""
        Provide a detailed financial analysis for {ticker} ({data_for_ai['company_name']}) based on the following data:
        
        Current Price: {data_for_ai['current_price']}
        Previous Close: {data_for_ai['previous_close']}
        Market Cap: {data_for_ai['market_cap']}
        P/E Ratio: {data_for_ai['pe_ratio']}
        EPS: {data_for_ai['eps']}
        Dividend Yield: {data_for_ai['dividend_yield']}
        52-Week Range: {data_for_ai['52_week_low']} - {data_for_ai['52_week_high']}
        Analyst Target Price: {data_for_ai['analyst_target_price']}
        Sector: {data_for_ai['sector']}
        Industry: {data_for_ai['industry']}
        
        Please include:
        1. Brief company overview
        2. Analysis of current valuation
        3. Key financial strengths and weaknesses
        4. Industry comparison
        5. Potential catalysts and risks
        6. Overall investment perspective
        
        Format your response in a clean, easy-to-read structure with headers for each section.
        """
        
        # Get response from OpenAI
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a professional financial analyst providing detailed insights on stocks. Your analysis should be informed, balanced, and educational."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error generating AI insights: {str(e)}"
