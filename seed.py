import reflex as rx
from code_dojo.models import Challenge, Category
from sqlmodel import Session, create_engine, select
import os
import json

# Ensure this matches your rxconfig or docker-compose env
DB_URL = os.getenv("DATABASE_URL", "postgresql://reflex:password@localhost:5434/codedojo")

def seed():
    json_file = "challenges.json"
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found.")
        return

    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    print(f"Loaded {len(data)} challenges from JSON.")

    engine = create_engine(DB_URL)
    
    with Session(engine) as session:
        new_count = 0
        for item in data:
            # Check for existing challenge by prompt
            existing = session.exec(
                select(Challenge).where(Challenge.prompt == item['prompt'])
            ).first()
            
            if existing:
                print(f"Skipping duplicate: {item['prompt'][:30]}...")
                continue
            
            try:
                # Convert string category to Enum
                category_enum = Category(item['category'])
                
                challenge = Challenge(
                    category=category_enum,
                    prompt=item['prompt'],
                    solution_source=item['solution_source'],
                    difficulty=item['difficulty']
                )
                session.add(challenge)
                new_count += 1
                print(f"Adding: [{category_enum.value}] {item['prompt'][:30]}...")
            except ValueError:
                print(f"Error: Invalid category '{item['category']}' for prompt '{item['prompt']}'")
                continue

        session.commit()
        print(f"\nSeeding complete! {new_count} new questions imported.")

if __name__ == "__main__":
    seed()
