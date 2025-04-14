
import os
import requests
from openai import OpenAI

def get_codegpt_response(prompt, api_url):
    """Get response from CodeGPT agent."""
    if not api_url:
        return "Error: CodeGPT API URL not configured"
    
    try:
        headers = {
            'X-API-Key': 'sk-c2b77e4d-d6a5-4469-90b1-d382a9c1389a',
            'User-Agent': 'bc1d_vs'
        }
        response = requests.post(api_url, json={"prompt": prompt}, headers=headers)
        if response.status_code == 200:
            return response.json().get('response', '')
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error connecting to CodeGPT agent: {str(e)}"

def get_openai_response(prompt):
    """Get response from OpenAI."""
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a knowledgeable financial analyst assistant. Provide concise, accurate responses about stocks and markets."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to OpenAI: {str(e)}"

def chat_about_stock(ticker, stock_data, user_message, ai_provider="codegpt"):
    """
    Chat about the stock based on user input using specified AI provider.
    
    Args:
        ticker: Stock symbol
        stock_data: Stock information
        user_message: User's question
        ai_provider: Either "codegpt" or "openai"
    """
    try:
        stock_context = f"""
        Stock: {ticker} ({stock_data.get('longName', 'N/A')})
        Current Price: ${stock_data.get('currentPrice', 'N/A')}
        Market Cap: ${stock_data.get('marketCap', 'N/A')}
        P/E Ratio: {stock_data.get('peRatio', 'N/A')}
        Industry: {stock_data.get('industry', 'N/A')}
        Sector: {stock_data.get('sector', 'N/A')}
        """
        
        prompt = f"Context about the stock:\n{stock_context}\n\nUser question: {user_message}"
        
        if ai_provider == "openai":
            return get_openai_response(prompt)
        else:
            api_url = os.environ.get("CODEGPT_API_URL")
            return get_codegpt_response(prompt, api_url)

    except Exception as e:
        return f"Error chatting with AI: {str(e)}"
