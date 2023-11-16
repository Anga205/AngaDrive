import reflex as rx
from website.State import State



def add_TPU_to_account_widget(tpu_verified_var):
    return rx.vstack(
        rx.box(height="1vh"),
        rx.cond(
            State.TPU_verified,
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
                    "Sign out of TPU", 
                    color="WHITE",
                ),
                font_size="1.6vh",
                height="5vh", 
                bg="RED",
                width="22vh",
                border_radius="1vh",
                _hover={"bg":"#8B0000"},
                on_click=State.remove_tpu_account
            ),
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
                )
            ),
        color="WHITE",
        bg="#0F0F10",
        border_color="#0F0F10",
        border_radius="1vh",
        border_width="1vh",
        spacing="0.5vh",
    )



