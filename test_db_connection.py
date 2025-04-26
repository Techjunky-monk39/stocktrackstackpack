from sqlalchemy import create_engine

DATABASE_URL = "postgresql://neondb_owner:npg_1FxlXMTZz4jP@ep-soft-cloud-a6nb6ez7-pooler.us-west-2.aws.neon.tech/neondb?sslmode=require"

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("Database connection successful!")
    connection.close()
except Exception as e:
    print(f"Database connection failed: {e}")
