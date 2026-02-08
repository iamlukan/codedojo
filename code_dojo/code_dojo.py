import reflex as rx
from .models import Challenge, Category
import random

class State(rx.State):
    code: str = ""
    result: str = ""
    current_challenge: Challenge | None = None

    def load_challenge(self):
        # Placeholder: Fetch a random challenge from DB
        # In a real app, this would query the DB.
        # For now, we rely on seeding and simple selection if DB is ready,
        # or just a mock if strictly following the step-by-step.
        # But since we are doing seeding next, let's try to fetch if possible,
        # or just wait for the user to trigger it.
        # Ideally, we load on mount.
        pass

    def check_solution(self):
        """Validates the user solution."""
        if not self.code:
             self.result = "❌ No code entered."
             return

        # Simple mock validation for now
        self.result = f"🔍 Validating...\nReceived: {self.code[:20]}..."
        # updated logic will come when we have full validation

    def set_code(self, code: str):
        self.code = code

def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("CodeDojo", size="9"),
            rx.text("Training Terminal", mb="2", color="gray.500"),
            rx.text_area(
                value=State.code,
                on_change=State.set_code,
                placeholder="> Enter your solution here...",
                bg="black",
                color="green.400",
                font_family="monospace",
                min_height="400px",
                width="100%",
                padding="1em",
                border_radius="md",
                _focus={"border_color": "green.500", "box_shadow": "0 0 0 1px green.500"},
            ),
            rx.text(State.result, color="yellow.400", white_space="pre-wrap"),
            rx.button(
                "Deploy / Test",
                color_scheme="green",
                size="3",
                width="100%",
                variant="surface",
                on_click=State.check_solution,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
            max_width="800px",
            margin="0 auto",
        ),
        padding="2em",
    )

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="large",
        accent_color="green",
    )
)
app.add_page(index)
