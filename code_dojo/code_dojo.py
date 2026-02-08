import reflex as rx
from .models import Challenge

def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("CodeDojo", size="9"),
            rx.text("Training Terminal", mb="2", color="gray.500"),
            rx.text_area(
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
            rx.button(
                "Deploy / Test",
                color_scheme="green",
                size="3",
                width="100%",
                variant="surface",
                # Setup pending logic for validation
                on_click=rx.console_log("Validating solution...") 
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
