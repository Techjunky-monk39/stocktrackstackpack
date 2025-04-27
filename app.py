import streamlit as st
from urllib.parse import parse_qs

# Handle query parameters for navigation
query_params = st.query_params  # Updated from st.experimental_get_query_params
page = query_params.get("page", ["main"])[0]
section = query_params.get("section", [None])[0]

# Navigation bar for logged-in users
def render_navigation():
    """Render a navigation bar for logged-in users."""
    if st.session_state.get("is_logged_in", False):
        st.markdown("""
        <style>
        .nav-bar {
            display: flex;
            justify-content: space-around;
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 5px;
        }
        .nav-bar a {
            text-decoration: none;
            color: #0068c9;
            font-weight: bold;
        }
        .nav-bar a:hover {
            text-decoration: underline;
        }
        </style>
        <div class="nav-bar">
            <a href="?page=main">Home</a>
            <a href="?page=api_update">API Profile</a>
            <a href="?page=wallet">Wallet</a>
            <a href="?page=stats">Stats</a>
            <a href="?page=add_payment">Add Payment</a>
            <a href="?page=add_crypto">Add Crypto</a>
        </div>
        """, unsafe_allow_html=True)

if page == "api_update":
    import api_update
    import health_checks
    render_navigation()  # Add navigation bar
    st.experimental_set_query_params(page="api_update")  # Reverted to experimental method
    if section == "openai":
        st.markdown("### Update OpenAI API Key")
        st.markdown(health_checks.check_openai_api(), unsafe_allow_html=True)
    elif section == "codegpt":
        st.markdown("### Update CodeGPT API Key")
        st.markdown(health_checks.check_codegpt_api(), unsafe_allow_html=True)
    # Simplified handling of 'main' attribute
    if callable(getattr(api_update, "main", None)):
        api_update.main()  # Call the API update page logic
    else:
        st.error("The 'main' function is missing or not callable in the 'api_update' module.")
elif page == "wallet":
    st.title("Wallet Page")
    render_navigation()  # Add navigation bar
    st.write("Wallet functionality coming soon.")
elif page == "stats":
    st.title("Stats Page")
    render_navigation()  # Add navigation bar
    st.write("Stats functionality coming soon.")
elif page == "add_payment":
    st.title("Add Payment Page")
    render_navigation()  # Add navigation bar
    st.write("Add payment functionality coming soon.")
elif page == "add_crypto":
    st.title("Add Crypto Page")
    render_navigation()  # Add navigation bar
    st.write("Add crypto functionality coming soon.")
else:
    import health_checks
    import pandas as pd
    import time
    from datetime import datetime, timedelta
    import stock_analysis
    import ai_insights
    import utils
    import auth
    import user_data
    import database as db
    import logging

    # Configure logging to capture errors and ensure the GUI remains functional
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Set page config
        st.set_page_config(
            page_title="StockSense: AI-Powered Financial Insights",
            page_icon="📈",
            layout="wide"
        )

        # Show login form in sidebar
        if not auth.login_form():
            st.stop()

        # Render navigation bar
        render_navigation()

        # Record session start time
        if "session_start_time" not in st.session_state:
            st.session_state.session_start_time = datetime.now()
            db.record_session_time(auth.logged_in_user(), st.session_state.session_start_time)

        # Header
        st.title("📊 StockSense: AI-Powered Financial Analysis")
        st.markdown("""
        Get real-time stock data, interactive charts, and AI-powered insights for your investments.
        Enter a stock symbol (e.g., AAPL, MSFT, GOOGL) below to begin your analysis.
        """)

        # Function to fetch and update data with auto-correction
        def update_data(ticker):
            st.session_state.ticker = ticker.upper()
            st.session_state.is_loading_data = True

            try:
                # Fetch stock data
                stock_info, stock_data = stock_analysis.get_stock_data(ticker)

                if stock_info and stock_data is not None:
                    st.session_state.data = stock_info
                    st.session_state.history = stock_data
                    st.session_state.last_update_time = datetime.now()
                    st.session_state.error = None

                    # Record the search in database if user is logged in
                    if st.session_state.get("is_logged_in", False):
                        user_data.record_search(stock_info.get("symbol", ticker), prevent_duplicates=True)

                        # Check if stock is in favorites
                        user_id = auth.logged_in_user()
                        favorites = db.get_favorite_stocks(user_id)
                        st.session_state.is_favorite = any(fav.ticker == stock_info.get("symbol", ticker) for fav in favorites)
                else:
                    st.session_state.error = None  # Remove error message
            except Exception as e:
                st.session_state.error = None  # Remove error message

            st.session_state.is_loading_data = False

        # Stock symbol input
        col1, col2 = st.columns([3, 1])
        with col1:
            ticker_input = st.text_input(
                "Enter Stock/Crypto Symbol (e.g., AAPL, MSFT, BTC-USD)",
                value=st.session_state.ticker,
                key="ticker_input"
            )
        with col2:
            submit_button = st.button("Analyze Stock", use_container_width=True)

        # Process the submitted stock symbol
        if submit_button:
            if ticker_input:
                update_data(ticker_input.strip().upper())
                # Clear any previous AI insights when a new stock is requested
                st.session_state.ai_insights = None
                st.rerun()
            else:
                st.error("Please enter a stock symbol")

        # Auto-refresh logic
        if st.session_state.auto_refresh and st.session_state.ticker:
            if (st.session_state.last_update_time is None or 
                (datetime.now() - st.session_state.last_update_time).total_seconds() >= st.session_state.refresh_interval):
                update_data(st.session_state.ticker)
                st.rerun()

        # Define a placeholder list of stock images
        stock_images = ["/workspaces/stocktrackstackpack/attached_assets/image_1744634579171.png"]

        # Display error message if any
        if st.session_state.error:
            st.error(st.session_state.error)
            # Display a random stock image when there's an error
            st.image(utils.get_random_image(stock_images), use_container_width=True)

        # If we have data to show
        if st.session_state.data is not None and st.session_state.history is not None:
            # Display last update time
            if st.session_state.last_update_time:
                st.caption(f"Last updated: {st.session_state.last_update_time.strftime('%Y-%m-%d %H:%M:%S')}")

            # Current price and basic info
            current_price = st.session_state.data.get('currentPrice', 'N/A')
            prev_close = st.session_state.data.get('previousClose', 'N/A')

            if current_price != 'N/A' and prev_close != 'N/A':
                price_change = current_price - prev_close
                price_change_pct = (price_change / prev_close) * 100
                price_color = "green" if price_change >= 0 else "red"
                change_symbol = "▲" if price_change >= 0 else "▼"
            else:
                price_change = 'N/A'
                price_change_pct = 'N/A'
                price_color = "black"
                change_symbol = ""

            # Display the current price and change
            price_col, change_col, fav_col = st.columns([1, 1, 1])
            with price_col:
                st.metric(
                    label=f"{st.session_state.ticker} Current Price",
                    value=f"${current_price:.2f}" if isinstance(current_price, (int, float)) else current_price
                )

            with change_col:
                if isinstance(price_change, (int, float)) and isinstance(price_change_pct, (int, float)):
                    st.metric(
                        label="Change",
                        value=f"${price_change:.2f}",
                        delta=f"{price_change_pct:.2f}%"
                    )

            # Add to favorites button if user is logged in
            with fav_col:
                if st.session_state.get("is_logged_in", False):
                    if st.session_state.is_favorite:
                        if st.button("❤️ Remove from Favorites"):
                            user_data.toggle_favorite_current_stock(st.session_state.ticker)
                            st.session_state.is_favorite = False
                            st.rerun()
                    else:
                        if st.button("🤍 Add to Favorites"):
                            user_data.toggle_favorite_current_stock(st.session_state.ticker)
                            st.session_state.is_favorite = True
                            st.rerun()
                else:
                    st.info("Login to add favorites")

            # Display tabs for different sections
            tab1, tab2, tab3 = st.tabs(["📈 Price Chart", "📊 Financial Data", "🤖 AI Insights"])

            with tab1:
                st.subheader(f"{st.session_state.ticker} Stock Price History")

                # Time period selector
                time_periods = {
                    "1M": 30,
                    "3M": 90,
                    "6M": 180,
                    "1Y": 365,
                    "5Y": 1825,
                    "Max": None
                }

                selected_period = st.select_slider(
                    "Select Time Period",
                    options=list(time_periods.keys()),
                    value="6M"
                )

                # Create and display interactive chart
                fig = stock_analysis.create_stock_chart(
                    st.session_state.history, 
                    st.session_state.ticker,
                    days=time_periods[selected_period]
                )
                st.plotly_chart(fig, use_container_width=True)

            with tab2:
                st.subheader("Key Financial Data")

                # Format and display key financial metrics
                financial_data = utils.format_financial_data(st.session_state.data)

                # Split into columns for better display
                col1, col2, col3 = st.columns(3)

                metrics = list(financial_data.items())
                metrics_per_col = len(metrics) // 3 + (1 if len(metrics) % 3 > 0 else 0)

                for i, (label, value) in enumerate(metrics):
                    col_idx = i // metrics_per_col
                    if col_idx == 0:
                        with col1:
                            st.metric(label, value)
                    elif col_idx == 1:
                        with col2:
                            st.metric(label, value)
                    else:
                        with col3:
                            st.metric(label, value)

                # Create a table of the data for download
                st.subheader("Detailed Financial Data")

                # Convert to dataframe for display
                df_data = pd.DataFrame({
                    "Metric": list(financial_data.keys()),
                    "Value": list(financial_data.values())
                })

                st.dataframe(df_data, use_container_width=True)

                # Download button for CSV
                csv = utils.convert_df_to_csv(df_data)
                st.download_button(
                    label="Download Data as CSV",
                    data=csv,
                    file_name=f"{st.session_state.ticker}_financial_data.csv",
                    mime="text/csv",
                )

                # Historical data table (recent)
                st.subheader("Recent Price History")
                recent_history = st.session_state.history.tail(10).reset_index()
                # Ensure we only select the columns we want to display
                recent_history = recent_history[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

                # Format the dataframe
                recent_history['Date'] = recent_history['Date'].dt.strftime('%Y-%m-%d')
                for col in ['Open', 'High', 'Low', 'Close']:
                    recent_history[col] = recent_history[col].round(2)

                st.dataframe(recent_history, use_container_width=True)

                # Download button for historical data CSV
                hist_csv = utils.convert_df_to_csv(recent_history)
                st.download_button(
                    label="Download Historical Data as CSV",
                    data=hist_csv,
                    file_name=f"{st.session_state.ticker}_historical_data.csv",
                    mime="text/csv",
                )

            with tab3:
                st.subheader("Chat with AI about " + st.session_state.ticker)

                # Initialize chat history if not exists
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []

                # Display chat history
                for message in st.session_state.chat_history:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])

                # Run health checks for AI providers
                openai_status = health_checks.check_openai_api()
                codegpt_status = health_checks.check_codegpt_api()

                # Display health check results in the sidebar
                with st.sidebar:
                    st.subheader("API Health Status")
                    st.sidebar.markdown(openai_status, unsafe_allow_html=True)
                    st.sidebar.markdown(codegpt_status, unsafe_allow_html=True)

                # AI provider selection
                available_providers = []
                if "working" in openai_status.lower():
                    available_providers.append("openai")
                if "working" in codegpt_status.lower():
                    available_providers.append("codegpt")

                if not available_providers:
                    st.error("No AI providers are currently available. Please try again later.")
                else:
                    ai_provider = st.selectbox(
                        "Choose AI Provider",
                        available_providers,
                        key="ai_provider"
                    )

                    # Chat input
                    user_message = st.chat_input("Ask about this stock, compare with others, or get investment advice...")

                    if user_message:
                        # Display user message
                        with st.chat_message("user"):
                            st.write(user_message)

                        # Get AI response
                        with st.chat_message("assistant"):
                            with st.spinner("Thinking..."):
                                response = ai_insights.chat_about_stock(
                                    st.session_state.ticker,
                                    st.session_state.data,
                                    user_message,
                                    ai_provider
                                )
                                st.write(response)

                        # Store in chat history
                        st.session_state.chat_history.append({"role": "user", "content": user_message})
                        st.session_state.chat_history.append({"role": "assistant", "content": response})

        # Display disclaimer
        st.markdown("---")
        st.caption("""
        **Disclaimer**: This application provides financial data for informational purposes only. It is not intended to provide investment advice. 
        Market data may be delayed. The AI-powered insights are generated using algorithms and should not be considered as financial advice. 
        Always conduct your own research before making investment decisions.
        """)

        # Ensure Streamlit runs on 0.0.0.0 and port 5000
        if __name__ == "__main__":
            import os
            os.system("streamlit run app.py --server.port=5000 --server.address=0.0.0.0")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        st.error("An unexpected error occurred. Please try again later.")

# Define a placeholder list of stock images
stock_images = ["/workspaces/stocktrackstackpack/attached_assets/image_1744634579171.png"]