import reflex as rx
import sqlmodel
from enum import Enum

class Category(str, Enum):
    CISCO = "Cisco"
    HP = "HP"
    PYTHON = "Python"
    SHELL = "Shell"
    DOCKER = "Docker"

class Challenge(rx.Model, table=True):
    category: Category
    prompt: str
    solution_hash: str
    difficulty: int
