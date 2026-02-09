import reflex as rx
from .models import Challenge, Category, SubCategory
import random
import sqlmodel
from sqlalchemy.orm import selectinload

class State(rx.State):
    code: str = ""
    result: str = ""
    current_challenge: Challenge | None = None
    
    # Categories state
    categories: list[Category] = []
    selected_subcategory_id: int | None = None
    
    # Admin Modal state
    is_admin_open: bool = False
    new_category_name: str = ""
    # Store pending new subcategory names per category_id
    new_subcategory_names: dict[int, str] = {} 
    
    def set_sub_input(self, cat_id: int, value: str):
        self.new_subcategory_names[cat_id] = value

    def load_categories(self):
        with rx.session() as session:
            # Re-fetch categories to ensure UI sync
            self.categories = session.exec(
                sqlmodel.select(Category).options(selectinload(Category.subcategories))
            ).all()
            # Initialize dict for inputs if needed, though default dict handles updates nicely

    def set_subcategory(self, subcategory_id: int):
        self.selected_subcategory_id = subcategory_id
        self.load_challenge()

    def load_challenge(self):
        with rx.session() as session:
            query = sqlmodel.select(Challenge)
            if self.selected_subcategory_id:
                query = query.where(Challenge.sub_category_id == self.selected_subcategory_id)
            
            challenges = session.exec(query).all()
            if challenges:
                self.current_challenge = random.choice(challenges)
                self.code = ""
                self.result = ""
            else:
                self.current_challenge = None
                self.result = "No challenges found in this subcategory."

    def check_solution(self):
        if not self.code:
             self.result = "❌ No code entered."
             return
        
        if not self.current_challenge:
            self.result = "❌ No active challenge."
            return

        # Simple string comparison (strip for safety)
        if self.code.strip() == self.current_challenge.solution_source.strip():
            self.result = "✅ Correct! Well done."
        else:
            self.result = f"❌ Incorrect.\nExpected:\n{self.current_challenge.solution_source}\n\nReceived:\n{self.code}"

    def set_code(self, code: str):
        self.code = code

    # CRUD
    def toggle_admin(self):
        self.is_admin_open = not self.is_admin_open
        if self.is_admin_open:
            self.load_categories()

    def add_category(self):
        with rx.session() as session:
            session.add(Category(name=self.new_category_name))
            session.commit()
        self.new_category_name = ""
        self.load_categories()

    def delete_category(self, id: int):
        with rx.session() as session:
            cat = session.get(Category, id)
            if cat:
                session.delete(cat)
                session.commit()
        self.load_categories()
        
    def add_subcategory(self, category_id: int):
        # Get name from dict, default to empty
        name = self.new_subcategory_names.get(category_id, "").strip()
        if not name:
            return

        with rx.session() as session:
            session.add(SubCategory(name=name, category_id=category_id))
            session.commit()
        
        # Clear input for this category
        self.new_subcategory_names[category_id] = ""
        self.load_categories()
    
    def delete_subcategory(self, id: int):
        with rx.session() as session:
            sub = session.get(SubCategory, id)
            if sub:
                session.delete(sub)
                session.commit()
        self.load_categories()

def sidebar() -> rx.Component:
    return rx.vstack(
        rx.heading("Categories", size="5", color="white", mb="4"),
        rx.accordion.root(
            rx.foreach(
                State.categories,
                lambda cat: rx.accordion.item(
                    rx.accordion.header(rx.text(cat.name, color="white")),
                    rx.accordion.content(
                        rx.vstack(
                            rx.foreach(
                                cat.subcategories,
                                lambda sub: rx.button(
                                    sub.name,
                                    on_click=lambda: State.set_subcategory(sub.id),
                                    variant="ghost",
                                    size="1",
                                    width="100%",
                                    justify_content="start"
                                )
                            )
                        )
                    ),
                    value=cat.name
                )
            ),
            width="100%",
            type="multiple",
        ),
        rx.spacer(),
        rx.button(
            rx.icon("settings"),
            "Manage",
            on_click=State.toggle_admin,
            variant="soft",
            color_scheme="gray",
            width="100%"
        ),
        width="20%",
        height="100vh",
        bg="gray.900",
        padding="2em",
        align_items="start",
    )

def admin_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Manage Categories"),
            rx.dialog.description("Add or remove categories and subcategories."),
            rx.flex(
                rx.input(
                    placeholder="New Category Name",
                    value=State.new_category_name,
                    on_change=State.set_new_category_name
                ),
                rx.button("Add", on_click=State.add_category),
                spacing="2"
            ),
            rx.separator(margin_y="4"),
            rx.scroll_area(
                rx.vstack(
                    rx.foreach(
                        State.categories,
                        lambda cat: rx.vstack(
                            rx.hstack(
                                rx.text(cat.name, weight="bold"),
                                rx.button("X", on_click=lambda: State.delete_category(cat.id), color_scheme="red", size="1"),
                                justify="between",
                                width="100%"
                            ),
                            rx.flex(
                                rx.input(
                                    placeholder="New SubCategory", 
                                    # Properly bind per-category input
                                    value=State.new_subcategory_names[cat.id],
                                    on_change=lambda val: State.set_sub_input(cat.id, val),
                                    size="1"
                                ),
                                rx.button("+", on_click=lambda: State.add_subcategory(cat.id), size="1", variant="outline"),
                                spacing="2",
                                width="100%"
                            ),
                            rx.vstack(
                                rx.foreach(
                                    cat.subcategories,
                                    lambda sub: rx.hstack(
                                        rx.text(f"- {sub.name}", size="1"),
                                        rx.button("x", on_click=lambda: State.delete_subcategory(sub.id), size="1", variant="ghost", color_scheme="red"),
                                        spacing="1",
                                        align="center"
                                    )
                                ),
                                padding_left="1em",
                                width="100%"
                            ),
                            padding="0.5em",
                            border="1px solid gray",
                            border_radius="md",
                            width="100%"
                        )
                    ),
                    spacing="2"
                ),
                height="300px"
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Close", on_click=State.toggle_admin)
                ),
                justify="end",
                margin_top="4"
            )
        ),
        open=State.is_admin_open,
        on_open_change=State.toggle_admin,
    )

def index() -> rx.Component:
    return rx.hstack(
        admin_modal(),
        sidebar(),
        rx.container(
            rx.color_mode.button(position="top-right"),
            rx.vstack(
                rx.heading("CodeDojo", size="9"),
                rx.text(
                    rx.cond(
                        State.current_challenge,
                        State.current_challenge.prompt,
                        "Select a subcategory to start training."
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
        on_mount=State.load_categories,
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
