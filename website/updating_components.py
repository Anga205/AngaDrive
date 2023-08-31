import reflex as rx
def changelog(is_safe_var):
    return rx.vstack(
        rx.cond(
            is_safe_var,
            rx.hstack(
                rx.text_area()
            ),
        ),
        bg="#120511",
        width="100%",
        height="80vh"
    )