import os
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Get database URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create declarative base
Base = declarative_base()

# Define models
class User(Base):
    """User model to store user information and preferences"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    searches = relationship("SearchHistory", back_populates="user")
    favorites = relationship("FavoriteStock", back_populates="user")
    
    def __repr__(self):
        return f"<User(username='{self.username}')>"


class SearchHistory(Base):
    """Search history model to track user stock searches"""
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ticker = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="searches")
    
    def __repr__(self):
        return f"<SearchHistory(ticker='{self.ticker}')>"


class FavoriteStock(Base):
    """Favorite stock model to store user's favorite stocks"""
    __tablename__ = "favorite_stocks"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ticker = Column(String(10), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String(255), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="favorites")
    
    def __repr__(self):
        return f"<FavoriteStock(ticker='{self.ticker}')>"


class StockPrediction(Base):
    """Stock prediction model to store historical predictions"""
    __tablename__ = "stock_predictions"
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String(10), nullable=False)
    prediction_date = Column(DateTime, default=datetime.utcnow)
    target_date = Column(DateTime, nullable=False)
    predicted_price = Column(Float, nullable=False)
    actual_price = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)
    
    def __repr__(self):
        return f"<StockPrediction(ticker='{self.ticker}', target_date='{self.target_date}')>"


# Create all tables in the database
Base.metadata.create_all(engine)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

# Streamlit session state management for database
def get_or_create_user(username):
    """Get or create a user with the given username"""
    db = get_db()
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        user = User(username=username, last_login=datetime.utcnow())
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update last login time
        user.last_login = datetime.utcnow()
        db.commit()
        
    return user


def add_search_history(user_id, ticker):
    """Add a new search history entry"""
    db = get_db()
    search = SearchHistory(user_id=user_id, ticker=ticker)
    db.add(search)
    db.commit()


def get_recent_searches(user_id, limit=5):
    """Get recent searches for a user"""
    db = get_db()
    return db.query(SearchHistory).filter(
        SearchHistory.user_id == user_id
    ).order_by(
        SearchHistory.timestamp.desc()
    ).limit(limit).all()


def add_favorite_stock(user_id, ticker, notes=None):
    """Add a stock to favorites"""
    db = get_db()
    
    # Check if already in favorites
    existing = db.query(FavoriteStock).filter(
        FavoriteStock.user_id == user_id,
        FavoriteStock.ticker == ticker
    ).first()
    
    if not existing:
        favorite = FavoriteStock(user_id=user_id, ticker=ticker, notes=notes)
        db.add(favorite)
        db.commit()
        return True
    
    return False


def remove_favorite_stock(user_id, ticker):
    """Remove a stock from favorites"""
    db = get_db()
    favorite = db.query(FavoriteStock).filter(
        FavoriteStock.user_id == user_id,
        FavoriteStock.ticker == ticker
    ).first()
    
    if favorite:
        db.delete(favorite)
        db.commit()
        return True
    
    return False


def get_favorite_stocks(user_id):
    """Get all favorite stocks for a user"""
    db = get_db()
    return db.query(FavoriteStock).filter(
        FavoriteStock.user_id == user_id
    ).order_by(
        FavoriteStock.added_at.desc()
    ).all()


def add_stock_prediction(ticker, target_date, predicted_price):
    """Add a new stock price prediction"""
    db = get_db()
    prediction = StockPrediction(
        ticker=ticker,
        target_date=target_date,
        predicted_price=predicted_price
    )
    db.add(prediction)
    db.commit()
    return prediction.id


def update_prediction_accuracy(prediction_id, actual_price):
    """Update a prediction with the actual price and calculate accuracy"""
    db = get_db()
    prediction = db.query(StockPrediction).filter(
        StockPrediction.id == prediction_id
    ).first()
    
    if prediction:
        prediction.actual_price = actual_price
        
        # Calculate accuracy as percentage difference
        if prediction.predicted_price > 0:
            diff = abs(prediction.predicted_price - actual_price)
            prediction.accuracy = 100 - ((diff / prediction.predicted_price) * 100)
        
        db.commit()
        return True
    
    return False


def get_recent_predictions(ticker=None, limit=10):
    """Get recent predictions, optionally filtered by ticker"""
    db = get_db()
    query = db.query(StockPrediction)
    
    if ticker:
        query = query.filter(StockPrediction.ticker == ticker)
    
    return query.order_by(StockPrediction.prediction_date.desc()).limit(limit).all()