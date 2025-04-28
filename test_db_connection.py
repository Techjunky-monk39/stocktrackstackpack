from sqlalchemy import create_engine
import logging

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="db_errors.log",  # Log database errors to a file
    filemode="a"
)

DATABASE_URL = "postgresql://neondb_owner:npg_1FxlXMTZz4jP@ep-soft-cloud-a6nb6ez7-pooler.us-west-2.aws.neon.tech/neondb?sslmode=require"

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("Database connection successful!")
    connection.close()
except Exception as e:
    logging.error(f"Database connection failed: {e}", exc_info=True)
    print(f"Database connection failed: {e}")
