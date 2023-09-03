import reflex as rx


def add_TPU_to_account_widget(tpu_verified_var):
    return rx.cond(
    tpu_verified_var,
    rx.vstack(
        rx.heading("Add your TPU account"),
        color="WHITE"
    ),
    rx.vstack(
        rx.heading("Manage TPU account"),
        rx.spacer(),
        bg="#0F0F10",
        border_color="#0F0F10",
        border_radius="1vh",
        border_width="1vh",
        spacing="0.5vh",
        color="WHITE"
    ),
)