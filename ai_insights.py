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

def chat_about_stock(ticker, stock_data, user_message):
    """
    Chat about the stock based on user input.
    
    Args:
        ticker (str): Stock symbol
        stock_data (dict): Stock information
        user_message (str): User's question or prompt
        
    Returns:
        str: AI response
    """
    try:
        client = get_openai_client()
        
        # Create context about the stock
        stock_context = f"""
        Stock: {ticker} ({stock_data.get('longName', 'N/A')})
        Current Price: ${stock_data.get('currentPrice', 'N/A')}
        Market Cap: ${stock_data.get('marketCap', 'N/A')}
        P/E Ratio: {stock_data.get('peRatio', 'N/A')}
        Industry: {stock_data.get('industry', 'N/A')}
        Sector: {stock_data.get('sector', 'N/A')}
        """
        
        # Prepare message for the AI
        system_prompt = """You are a knowledgeable financial analyst assistant. 
        Provide concise, accurate responses about stocks, comparing them with competitors,
        and analyzing investment opportunities. Use data to support your points."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context about the stock:\n{stock_context}\n\nUser question: {user_message}"}
        ]
        
        # Get response from OpenAI
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error chatting with AI: {str(e)}"
