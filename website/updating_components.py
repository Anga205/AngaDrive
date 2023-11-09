import reflex as rx
from website.State import State



def add_TPU_to_account_widget(tpu_verified_var):
    return rx.cond(
    tpu_verified_var,
    rx.box(
        height="0vh",
        width="0vh",
        bg="BLACK",
        spacing="0vh"
    ),
    rx.vstack(
        rx.box(height="1vh"),
        rx.button(
            rx.span(
                rx.image(
                    src="/TPU-logo.png", 
                    height="3vh", 
                    width="2.3vh"
                )
            ), 
            rx.span(
                width="2vh"
            ), 
            rx.span(
                "Sign in with TPU", 
                color="WHITE",
            ),
            font_size="1.6vh",
            height="5vh", 
            bg="BLACK",
            width="22vh",
            border_radius="1vh",
            _hover={"bg":"#1F1F3F"},
            on_click=rx.redirect("https://privateuploader.com/oauth/9f032bfb-7553-4a5d-9727-217f34537f1e")
        ),
        color="WHITE",
        bg="#0F0F10",
        border_color="#0F0F10",
        border_radius="1vh",
        border_width="1vh",
        spacing="0.5vh",
    ),
)



def account_manager():
    return rx.vstack(
        rx.heading("Manage account", font_size="4vh", color="WHITE"),
        rx.divider(border_color="WHITE"),
        add_TPU_to_account_widget(State.TPU_verified),
        border_radius="2vh",
        bg="#0F0F10",
        spacing="0.5vh",
        width="100%",
        border_color="#0F0F10",
        border_width="1vh"
    )