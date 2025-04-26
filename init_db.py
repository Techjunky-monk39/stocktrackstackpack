import os
from database import Base, engine

def initialize_database():
    """Initialize the database schema."""
    print("Initializing database...")
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")

if __name__ == "__main__":
    # Ensure DATABASE_URL is set
    if not os.environ.get("DATABASE_URL"):
        raise ValueError("DATABASE_URL environment variable is not set. Please configure it before running this script.")

    initialize_database()