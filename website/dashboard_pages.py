import reflex as rx

def file_hosting_page():
    return rx.vstack(
        rx.box(height="5vh"),
        rx.hstack(
            rx.box(width="5%"),
            rx.heading(
                "My files",
                color="WHITE",
                font_size="4vh"
                ),
            rx.spacer(),
            rx.button(
                "Upload",
                rx.box(width="10%"),
                rx.image(src="/upload.png",height="4vh"),
                bg="BLUE",
                color="WHITE",
                height="5vh",
                font_size="1.65vh",
                border_radius="1vh",
                width="13vh"
            ),
            rx.box(width="5%"),
            width="100%",
            spacing="0px"
        ),
        width="100%",
        spacing="1vh"
    )