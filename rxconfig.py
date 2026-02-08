import reflex as rx
import os

config = rx.Config(
    app_name="code_dojo",
    db_url=os.getenv("DATABASE_URL", "postgresql://reflex:password@db:5432/codedojo"),
)
