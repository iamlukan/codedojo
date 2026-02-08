from sqlalchemy import create_engine, text
import os

DB_URL = os.getenv("DATABASE_URL", "postgresql://reflex:password@localhost:5434/codedojo")

def cleanup():
    print(f"Connecting to {DB_URL}...")
    engine = create_engine(DB_URL)
    with engine.begin() as conn:
        print("Dropping objects...")
        conn.execute(text("DROP TABLE IF EXISTS challenge CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))
        conn.execute(text("DROP TYPE IF EXISTS category CASCADE;"))
    print("Cleanup complete.")

if __name__ == "__main__":
    cleanup()
