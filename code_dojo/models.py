import reflex as rx
import sqlmodel
from enum import Enum

class Category(rx.Model, table=True):
    name: str = sqlmodel.Field(index=True)
    description: str = ""
    subcategories: list["SubCategory"] = sqlmodel.Relationship(back_populates="category", cascade_delete=True)

class SubCategory(rx.Model, table=True):
    name: str = sqlmodel.Field(index=True)
    category_id: int | None = sqlmodel.Field(default=None, foreign_key="category.id")
    category: Category | None = sqlmodel.Relationship(back_populates="subcategories")
    challenges: list["Challenge"] = sqlmodel.Relationship(back_populates="subcategory", cascade_delete=True)

class Challenge(rx.Model, table=True):
    prompt: str
    solution_source: str
    difficulty: int
    sub_category_id: int | None = sqlmodel.Field(default=None, foreign_key="subcategory.id")
    subcategory: SubCategory | None = sqlmodel.Relationship(back_populates="challenges")
