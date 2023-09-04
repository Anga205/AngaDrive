import reflex as rx


def add_TPU_to_account_widget(tpu_verified_var):
    return rx.cond(
    tpu_verified_var,
    rx.vstack(
        rx.heading("Manage TPU account"),
        rx.divider(border_color="WHITE"),
        bg="#0F0F10",
        border_color="#0F0F10",
        border_radius="1vh",
        border_width="1vh",
        spacing="0.5vh",
        color="WHITE"
    ),
    rx.vstack(
        rx.heading("Add your TPU account", font_size="4vh"),
        rx.divider(border_color="WHITE"),
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