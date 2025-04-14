import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import stock_analysis
import ai_insights
import utils
import auth
import user_data
import database as db

# Set page config
st.set_page_config(
    page_title="StockSense: AI-Powered Financial Insights",
    page_icon="📈",
    layout="wide"
)

# Show login form in sidebar
auth.login_form()

# Header
st.title("📊 StockSense: AI-Powered Financial Analysis")
st.markdown("""
Get real-time stock data, interactive charts, and AI-powered insights for your investments.
Enter a stock symbol (e.g., AAPL, MSFT, GOOGL) below to begin your analysis.
""")

# Display a random stock market image
stock_images = [
    "https://images.unsplash.com/photo-1526628953301-3e589a6a8b74",  # Stephen Dawson
    "https://images.unsplash.com/photo-1542744173-05336fcc7ad4",  # Campaign Creators
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71",  # Luke Chesser
    "https://images.unsplash.com/photo-1488459716781-31db52582fe9",  # Jacopo Maiarelli
    "https://images.unsplash.com/photo-1444653614773-995cb1ef9efa",  # Adeolu Eletu
    "https://images.unsplash.com/photo-1563986768711-b3bde3dc821e",  # Austin Distel
    "https://images.unsplash.com/photo-1556155092-490a1ba16284",  # Austin Distel
    "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40",  # Scott Graham
]

# Initialize session state variables if they don't exist
if "ticker" not in st.session_state:
    st.session_state.ticker = ""
if "last_update_time" not in st.session_state:
    st.session_state.last_update_time = None
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False
if "refresh_interval" not in st.session_state:
    st.session_state.refresh_interval = 60  # Default refresh interval in seconds
if "data" not in st.session_state:
    st.session_state.data = None
if "history" not in st.session_state:
    st.session_state.history = None
if "ai_insights" not in st.session_state:
    st.session_state.ai_insights = None
if "error" not in st.session_state:
    st.session_state.error = None
if "is_loading_data" not in st.session_state:
    st.session_state.is_loading_data = False
if "is_loading_insights" not in st.session_state:
    st.session_state.is_loading_insights = False
if "is_favorite" not in st.session_state:
    st.session_state.is_favorite = False

# Function to fetch and update data
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
                user_data.record_search(ticker)
                
                # Check if stock is in favorites
                user_id = auth.logged_in_user()
                favorites = db.get_favorite_stocks(user_id)
                st.session_state.is_favorite = any(fav.ticker == ticker for fav in favorites)
        else:
            st.session_state.error = f"Invalid stock symbol: {ticker}"
    except Exception as e:
        st.session_state.error = f"Error fetching data: {str(e)}"
    
    st.session_state.is_loading_data = False

# Define callback for favorite stock selection
def select_favorite_stock(ticker):
    """Handle favorite stock selection"""
    st.session_state.ticker = ticker
    update_data(ticker)
    st.rerun()

# Define callback for recent search selection
def select_recent_search(ticker):
    """Handle recent search selection"""
    st.session_state.ticker = ticker
    update_data(ticker)
    st.rerun()

# Render sidebar components if user is logged in
if st.session_state.get("is_logged_in", False):
    user_data.render_favorites_section(on_select_favorite=select_favorite_stock)
    user_data.render_recent_searches(on_select_search=select_recent_search)

# Stock symbol input
col1, col2 = st.columns([3, 1])
with col1:
    ticker_input = st.text_input(
        "Enter Stock Symbol (e.g., AAPL, MSFT, GOOGL)",
        value=st.session_state.ticker,
        key="ticker_input"
    )
with col2:
    submit_button = st.button("Analyze Stock", use_container_width=True)

# Auto-refresh settings
refresh_col1, refresh_col2 = st.columns([1, 3])
with refresh_col1:
    auto_refresh = st.checkbox("Auto-refresh data", value=st.session_state.auto_refresh)
with refresh_col2:
    if auto_refresh:
        refresh_interval = st.slider(
            "Refresh interval (seconds)", 
            min_value=30, 
            max_value=300, 
            value=st.session_state.refresh_interval,
            step=30
        )
        st.session_state.refresh_interval = refresh_interval
    st.session_state.auto_refresh = auto_refresh

# Function to fetch and update data
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
                user_data.record_search(ticker)
                
                # Check if stock is in favorites
                user_id = auth.logged_in_user()
                favorites = db.get_favorite_stocks(user_id)
                st.session_state.is_favorite = any(fav.ticker == ticker for fav in favorites)
        else:
            st.session_state.error = f"Invalid stock symbol: {ticker}"
    except Exception as e:
        st.session_state.error = f"Error fetching data: {str(e)}"
    
    st.session_state.is_loading_data = False

# Function to get AI insights
def get_ai_insights(ticker, stock_data):
    st.session_state.is_loading_insights = True
    
    try:
        # Get AI insights
        insights = ai_insights.generate_stock_insights(ticker, stock_data)
        st.session_state.ai_insights = insights
    except Exception as e:
        st.session_state.ai_insights = f"Error generating AI insights: {str(e)}"
    
    st.session_state.is_loading_insights = False

# Process the submitted stock symbol
if submit_button and ticker_input:
    update_data(ticker_input)
    # Clear any previous AI insights when a new stock is requested
    st.session_state.ai_insights = None

# Auto-refresh logic
if st.session_state.auto_refresh and st.session_state.ticker:
    if (st.session_state.last_update_time is None or 
        (datetime.now() - st.session_state.last_update_time).total_seconds() >= st.session_state.refresh_interval):
        update_data(st.session_state.ticker)
        st.rerun()

# Display error message if any
if st.session_state.error:
    st.error(st.session_state.error)
    # Display a random stock image when there's an error
    st.image(utils.get_random_image(stock_images), use_column_width=True)

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
        recent_history.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        
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
        st.subheader("AI-Powered Financial Insights")
        
        # AI analysis section
        if st.session_state.ai_insights is None:
            if st.button("Generate AI Insights"):
                get_ai_insights(st.session_state.ticker, st.session_state.data)
                st.rerun()
            
            if st.session_state.is_loading_insights:
                st.info("Generating AI insights... This may take a moment.")
        else:
            # Display AI insights
            if isinstance(st.session_state.ai_insights, str) and st.session_state.ai_insights.startswith("Error"):
                st.error(st.session_state.ai_insights)
            else:
                st.write(st.session_state.ai_insights)
                
                if st.button("Refresh AI Insights"):
                    get_ai_insights(st.session_state.ticker, st.session_state.data)
                    st.rerun()

# Display disclaimer
st.markdown("---")
st.caption("""
**Disclaimer**: This application provides financial data for informational purposes only. It is not intended to provide investment advice. 
Market data may be delayed. The AI-powered insights are generated using algorithms and should not be considered as financial advice. 
Always conduct your own research before making investment decisions.
""")
