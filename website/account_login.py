import reflex as rx
from website.State import State
import website.TPU_cmds as TPU

def login() -> rx.Component:
    return rx.box(
    rx.desktop_only(
        rx.hstack(
            rx.center( 
                rx.vstack(
                    rx.box(height="33vh", width="100%"),
                    rx.vstack(
                        rx.box(height="1vh"),
                        rx.heading("Login", font_size="4vh"),
                        rx.box(height="1.05vh"),
                        rx.input(
                            placeholder="Enter e-mail address",
                            on_blur=State.set_email,
                            bg=State.email_color_bg,
                            width="80%",
                            font_size="1.65vh",
                            height="4vh"
                            ),
                        rx.password(
                            placeholder="Enter password",
                            on_blur=State.set_password,
                            width="80%",
                            font_size="1.65vh",
                            height="4vh"
                        ),
                        rx.button("LOGIN", bg="PURPLE", color="WHITE", on_click=State.submit_login, font_size="1.7vh", width="8vh", height="3.5vh"),
                        rx.hstack(
                            rx.text("Dont have an account?"),
                            rx.link("Sign up!",on_click=State.SignUpEnable),
                            font_size="1.65vh"
                        ),
                        TPU.login_page_TPU_button("Desktop"),
                        rx.box(height="1vh"),
                        spacing="2.1vh",
                        bg="WHITE", 
                        width="100%",
                        border_radius="2.1vh 0vh",
                        border_color="BLUE",
                        border_width="1.05vh"
                        ),
                    rx.box(height="40vh", width="100%"),
                    width="20%",
                    height="100vh"
                ),
                width="100%"
            ),
            rx.alert_dialog(
                rx.alert_dialog_overlay(
                    rx.alert_dialog_content(
                        rx.alert_dialog_header("Sign Up"),
                        rx.alert_dialog_body(
                            rx.vstack(
                                rx.input(placeholder="Enter a username", on_blur=State.set_sign_up_username),
                                rx.input(placeholder="Enter an e-mail ID", bg=State.signup_email_color_bg, on_blur=State.set_SignUp_email),
                                rx.password(placeholder="Enter a password", on_blur=State.set_sign_up_password),
                                rx.heading(rx.span("This should go without saying but, please "), rx.span("DO NOT USE THE SAME PASSWORD EVERYWHERE", color="RED", _as="b"), font_size="xs")
                            )
                        ),
                        rx.alert_dialog_footer(
                            rx.hstack(
                                rx.button(
                                    "Close",
                                    on_click=State.SignUpEnable
                                ),
                                rx.button(
                                    "Submit",
                                    on_click=State.submit_signup,
                                )
                            )
                        ),
                    )
                ),
                is_open=State.SignUpEnabled,
            ),
            width="100%",
            bg="BLACK",
        )
    ),
    rx.mobile_and_tablet(
        rx.vstack(
            rx.box(height="10vh"),
            rx.vstack(
                rx.box(height="5vh"),
                rx.heading("Login", font_size="4vh"),
                rx.box(height="2vh"),
                rx.input(placeholder="Enter e-mail address", width="85%",on_blur=State.set_email, bg=State.email_color_bg),
                rx.box(height="2vh"),
                rx.input(placeholder="Enter password", width="85%", on_blur=State.set_password),
                rx.box(height="2vh"),
                rx.button("LOGIN",bg="PURPLE", color="WHITE", on_click=State.submit_login),
                rx.box(height="1vh"),
                rx.text("Dont have an account? ", rx.span(rx.link("Sign up!", on_click=State.SignUpEnable))),
                TPU.login_page_TPU_button("Mobile"),
                rx.box(height="7vh" if not TPU.enable_TPU else "3vh"),
                spacing="0vh",
                width="90%",
                bg="WHITE",
                border_radius="2vh 0px",
                border_color="BLUE",
                border_width="1vh"
                ),
            height="100vh",
            position="fixed",
            bg="BLACK",
            width="100%"
        )
    ),
)


def add_TPU_to_account():
    return rx.vstack(
        rx.spacer(),
        rx.vstack(
            rx.spacer(),
            rx.vstack(
                rx.heading("An Account with this email already exists", font_size="3vh"),
                rx.text("Log in to add this TPU account to your anga.pro account", font_size="1.65vh"),
                rx.spacer(),
                rx.password(placeholder="Enter password here", is_required=True, bg="#e2e6f0", font_size="1.65vh", height="4vh", on_blur=State.set_add_tpu_password_value),
                rx.spacer(),
                rx.button("Add Account", color_scheme="blue", font_size="1.65vh", width="100%", height="4vh", on_click=State.submit_password_to_add_tpu_to_account),
                spacing="1vh"
            ),
            rx.spacer(),
            border_radius="5vh",
            spacing="0vh",
            border_color="white",
            border_width="5vh",
            bg="white",
            width="50vh"
        ),
        rx.spacer(),
        bg="BLACK",
        spacing="0vh",
        height="100vh"
    )