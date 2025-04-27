import streamlit as st
import database as db
import auth

def render_favorites_section(on_select_favorite=None):
    """
    Render the user's favorite stocks section.
    
    Args:
        on_select_favorite: Optional callback function when a favorite is selected
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Favorite Stocks")
    
    # Check if user is logged in
    if not auth.require_login():
        return
    
    user_id = auth.logged_in_user()
    
    # Get favorites from database
    favorites = db.get_favorite_stocks(user_id)
    
    if not favorites:
        st.sidebar.write("No favorite stocks yet. Add some!")
    else:
        # Display favorites with buttons
        for fav in favorites:
            col1, col2 = st.sidebar.columns([4, 1])
            
            # Stock ticker with button to select it
            with col1:
                if on_select_favorite and st.button(f"📊 {fav.ticker}", key=f"fav_{fav.id}"):
                    on_select_favorite(fav.ticker)
            
            # Remove button
            with col2:
                if st.button("❌", key=f"del_{fav.id}"):
                    db.remove_favorite_stock(user_id, fav.ticker)
                    st.rerun()
            
            # Display notes if any
            if fav.notes:
                st.sidebar.caption(fav.notes)
    
    # Add new favorite form
    with st.sidebar.expander("Add Favorite Stock"):
        with st.form(key="add_favorite"):
            ticker = st.text_input("Stock Symbol").upper()
            notes = st.text_area("Notes (optional)")
            submit = st.form_submit_button("Add to Favorites")
            
            if submit and ticker:
                success = db.add_favorite_stock(user_id, ticker, notes)
                if success:
                    st.success(f"Added {ticker} to favorites!")
                    st.rerun()
                else:
                    st.error(f"{ticker} is already in your favorites.")


def record_search(ticker, prevent_duplicates=False):
    """Record a stock search in the database."""
    if auth.require_login():
        user_id = auth.logged_in_user()
        if prevent_duplicates:
            recent_searches = db.get_recent_searches(user_id)
            if any(search.ticker.isnot(None) and search.ticker == ticker for search in recent_searches):  # Fixed conditional operand
                return
        db.add_search_history(user_id, ticker)


def render_recent_searches(on_select_search=None):
    """
    Render recent searches section.
    
    Args:
        on_select_search: Optional callback function when a search is selected
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Recent Searches")
    
    # Check if user is logged in
    if not auth.require_login():
        return
    
    user_id = auth.logged_in_user()
    
    # Get recent searches from database
    searches = db.get_recent_searches(user_id)
    
    if not searches:
        st.sidebar.write("No recent searches.")
    else:
        # Display recent searches as buttons
        for search in searches:
            if on_select_search and st.sidebar.button(f"🔍 {search.ticker}", key=f"search_{search.id}"):
                on_select_search(search.ticker)


def toggle_favorite_current_stock(ticker):
    """Toggle favorite status for current stock"""
    if not auth.require_login():
        return
    
    user_id = auth.logged_in_user()
    
    # Check if already in favorites
    favorites = db.get_favorite_stocks(user_id)
    is_favorite = False
    
    for fav in favorites:
        if fav.ticker == ticker:
            is_favorite = True
            break
    
    # Add or remove from favorites
    if is_favorite:
        db.remove_favorite_stock(user_id, ticker)
        return False
    else:
        db.add_favorite_stock(user_id, ticker)
        return True