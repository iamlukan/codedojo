import reflex as rx
from code_dojo.models import Challenge, Category, SubCategory
from sqlmodel import Session, create_engine, select
import os
import json

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
            cat_name = item['category']
            
            # 1. Get or Create Category
            category = session.exec(select(Category).where(Category.name == cat_name)).first()
            if not category:
                category = Category(name=cat_name, description=f"{cat_name} challenges")
                session.add(category)
                session.commit()
                session.refresh(category)
                print(f"Created Category: {cat_name}")

            # 2. Get or Create SubCategory (Defaulting to 'General' for migrated items)
            # In a real scenario, JSON might have subcategory field.
            subcat_name = item.get('subcategory', 'General')
            subcategory = session.exec(
                select(SubCategory)
                .where(SubCategory.name == subcat_name)
                .where(SubCategory.category_id == category.id)
            ).first()
            
            if not subcategory:
                subcategory = SubCategory(name=subcat_name, category_id=category.id)
                session.add(subcategory)
                session.commit()
                session.refresh(subcategory)
                print(f"Created SubCategory: {subcat_name} in {cat_name}")

            # 3. Create Challenge
            existing = session.exec(
                select(Challenge).where(Challenge.prompt == item['prompt'])
            ).first()
            
            if existing:
                continue
            
            challenge = Challenge(
                sub_category_id=subcategory.id,
                prompt=item['prompt'],
                solution_source=item['solution_source'],
                difficulty=item['difficulty']
            )
            session.add(challenge)
            new_count += 1
            print(f"Adding: [{cat_name}/{subcat_name}] {item['prompt'][:30]}...")

        session.commit()
        print(f"\nSeeding complete! {new_count} new questions imported.")

if __name__ == "__main__":
    seed()
