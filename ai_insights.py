import os
import requests

def get_codegpt_response(prompt, api_url):
    """
    Get response from CodeGPT agent.

    Args:
        prompt (str): The prompt to send to the agent
        api_url (str): The CodeGPT agent API URL
    """
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

def chat_about_stock(ticker, stock_data, user_message):
    """
    Chat about the stock based on user input using CodeGPT agent.
    """
    try:
        # Get CodeGPT API URL from environment
        api_url = os.environ.get("CODEGPT_API_URL")
        if not api_url:
            return "Error: CODEGPT_API_URL not set in environment variables"

        # Create context about the stock
        stock_context = f"""
        Stock: {ticker} ({stock_data.get('longName', 'N/A')})
        Current Price: ${stock_data.get('currentPrice', 'N/A')}
        Market Cap: ${stock_data.get('marketCap', 'N/A')}
        P/E Ratio: {stock_data.get('peRatio', 'N/A')}
        Industry: {stock_data.get('industry', 'N/A')}
        Sector: {stock_data.get('sector', 'N/A')}
        """

        # Prepare message for the agent
        prompt = f"Context about the stock:\n{stock_context}\n\nUser question: {user_message}"

        # Get response from CodeGPT agent
        return get_codegpt_response(prompt, api_url)

    except Exception as e:
        return f"Error chatting with AI: {str(e)}"