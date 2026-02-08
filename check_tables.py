from sqlalchemy import create_engine, text
import os

DB_URL = os.getenv("DATABASE_URL", "postgresql://reflex:password@localhost:5434/codedojo")

def check():
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result]
        print(f"Tables: {tables}")

if __name__ == "__main__":
    check()
