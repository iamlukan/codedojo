import reflex as rx
from code_dojo.models import Challenge, Category
from sqlmodel import Session, create_engine, select
import os

# Ensure this matches your rxconfig or docker-compose env
DB_URL = os.getenv("DATABASE_URL", "postgresql://reflex:password@localhost:5434/codedojo")

def seed():
    engine = create_engine(DB_URL)
    
    with Session(engine) as session:
        # Check if we already have data
        existing = session.exec(select(Challenge)).first()
        if existing:
            print("Database already populated.")
            return

        print("Seeding database...")
        challenges = [
            Challenge(
                category=Category.CISCO, 
                prompt="Configure the hostname to 'Router1'.", 
                solution_hash="hostname Router1", 
                difficulty=1
            ),
            Challenge(
                category=Category.PYTHON, 
                prompt="Print 'Hello, CodeDojo!' to the console.", 
                solution_hash="print('Hello, CodeDojo!')", 
                difficulty=1
            ),
            Challenge(
                category=Category.SHELL, 
                prompt="List all files in the current directory including hidden ones.", 
                solution_hash="ls -la", 
                difficulty=2
            ),
            Challenge(
                category=Category.DOCKER, 
                prompt="Run a hello-world container.", 
                solution_hash="docker run hello-world", 
                difficulty=1
            )
        ]
        
        for ch in challenges:
            session.add(ch)
            print(f"Added: [{ch.category}] {ch.prompt}")
        
        session.commit()
        print("Seeding complete!")

if __name__ == "__main__":
    seed()
