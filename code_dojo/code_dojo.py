import reflex as rx
from .models import Challenge, Category
import random
import sqlmodel

class State(rx.State):
    code: str = ""
    result: str = ""
    current_challenge: Challenge | None = None
    selected_category: str | None = None

    def set_category(self, category: str):
        self.selected_category = category
        self.load_challenge()

    def load_challenge(self):
        with rx.session() as session:
            query = sqlmodel.select(Challenge)
            if self.selected_category:
                query = query.where(Challenge.category == self.selected_category)
            
            challenges = session.exec(query).all()
            if challenges:
                self.current_challenge = random.choice(challenges)
                self.code = ""  # Reset code on new challenge
                self.result = "" # Reset result
            else:
                self.current_challenge = None

    def check_solution(self):
        """Validates the user solution."""
        if not self.code:
             self.result = "❌ No code entered."
             return
        
        # Mock validation
        self.result = f"🔍 Validating...\nReceived: {self.code[:20]}..."

    def set_code(self, code: str):
        self.code = code

def sidebar() -> rx.Component:
    return rx.vstack(
        rx.heading("Categories", size="5", color="white", mb="4"),
        rx.foreach(
            list(Category),
            lambda category: rx.button(
                category,
                on_click=lambda: State.set_category(category),
                width="100%",
                variant="ghost",
                color_scheme="gray",
                justify_content="start",
            )
        ),
        width="20%",
        height="100vh",
        bg="gray.900",
        padding="2em",
        align_items="start",
    )

def index() -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.container(
            rx.color_mode.button(position="top-right"),
            rx.vstack(
                rx.heading("CodeDojo", size="9"),
                rx.text(
                    rx.cond(
                        State.current_challenge,
                        State.current_challenge.prompt,
                        "Select a category to start training."
                    ),
                    mb="2", 
                    color="gray.500"
                ),
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
                    disabled=~State.current_challenge,
                ),
                spacing="5",
                justify="center",
                min_height="85vh",
                align="center",
                width="100%", 
                margin="0 auto",
            ),
            padding="2em",
            width="80%",
        ),
        width="100%",
        spacing="0",
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
