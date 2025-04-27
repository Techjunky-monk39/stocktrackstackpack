import os
import requests

def check_openai_api():
    """Checks if the OpenAI API is reachable and the API key is valid."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "[Warning: OPENAI_API_KEY not set](?page=api_update&section=openai)"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    try:
        response = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=5)
        response.raise_for_status()
        return "OpenAI API is working correctly."
    except requests.exceptions.RequestException as e:
        return f"[Error checking OpenAI API: {e}](?page=api_update&section=openai)"

def check_codegpt_api():
    """Checks if the CodeGPT API is reachable and the API key is valid."""
    api_key = os.environ.get("CODEGPT_API_KEY")
    api_url = os.environ.get("CODEGPT_HEALTH_CHECK_ENDPOINT", "https://example.com/health")

    if not api_key:
        return "[Warning: CODEGPT_API_KEY not set](?page=api_update&section=codegpt)"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    try:
        response = requests.get(api_url, headers=headers, timeout=5)
        response.raise_for_status()
        return "CodeGPT API is working correctly."
    except requests.exceptions.RequestException as e:
        return f"[Error checking CodeGPT API: {e}](?page=api_update&section=codegpt)"