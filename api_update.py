import streamlit as st
import os

def save_api_key(key_name, key_value):
    """Save or update the API key in the environment file."""
    if not key_value.strip():
        st.error(f"{key_name} cannot be empty.")
        return

    try:
        # Read existing .env content
        env_path = ".env"
        if os.path.exists(env_path):
            with open(env_path, "r") as env_file:
                lines = env_file.readlines()
        else:
            lines = []

        # Update or append the key
        updated = False
        with open(env_path, "w") as env_file:
            for line in lines:
                if line.startswith(f"{key_name}="):
                    env_file.write(f"{key_name}={key_value}\n")
                    updated = True
                else:
                    env_file.write(line)
            if not updated:
                env_file.write(f"{key_name}={key_value}\n")

        st.success(f"{key_name} updated successfully!")
    except FileNotFoundError:
        st.error(f"Error: The .env file could not be found.")
    except PermissionError:
        st.error(f"Error: Permission denied while accessing the .env file.")
    except Exception as e:
        st.error(f"Failed to update {key_name}: {e}")

st.title("🔑 API Key Management")

st.subheader("Update OpenAI API Key")
openai_key = st.text_input("Enter OpenAI API Key", type="password")
if st.button("Update OpenAI API Key"):
    save_api_key("OPENAI_API_KEY", openai_key)

st.subheader("Update CodeGPT API Key")
codegpt_key = st.text_input("Enter CodeGPT API Key", type="password")
if st.button("Update CodeGPT API Key"):
    save_api_key("CODEGPT_API_KEY", codegpt_key)

st.subheader("Update Gemini API Key (Future Integration)")
gemini_key = st.text_input("Enter Gemini API Key", type="password")
if st.button("Update Gemini API Key"):
    save_api_key("GEMINI_API_KEY", gemini_key)
