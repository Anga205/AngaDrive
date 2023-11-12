"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx
import website.updating_components as updating_components
import website.dashboard_pages as dashboard_pages
from website.State import State
from website.account_login import login, add_TPU_to_account


def index():
    return rx.box(
        rx.tablet_and_desktop( 
            rx.vstack(
                rx.hstack(
                    rx.box(width="21vh"),
                    rx.image(src="/logo.png", width="7.875vh", height="7.875vh", on_click=rx.redirect("/")),
                    rx.spacer(),
                    rx.hstack(
                        rx.menu(
                            rx.menu_button(
                                rx.heading(
                                    "Contact", 
                                    color="WHITE",
                                    font_size="2.1vh"
                                    ), 
                                ),
                            rx.menu_list(
                                rx.menu_item("Discord", on_click=rx.redirect("https://discord.gg/DgxppCZnJb", external=True)),
                                rx.menu_item("Instagram", on_click=rx.redirect("https://instagram.com/_anga205", external=True)),
                                rx.menu_item("Threads", on_click=rx.redirect("https://threads.net/@_anga205", external=True)),
                                rx.menu_item("𝕏.com", on_click=rx.redirect("https://x.com/_anga205", external=True)),
                                rx.menu_item("Email", on_click=rx.redirect("mailto:support@anga.pro", external=True)),
                                rx.menu_item("GitHub", on_click=rx.redirect("https://github.com/Anga205", external=True)),
                                rx.menu_item("Telegram", on_click=rx.redirect("https://t.me/Anga205", external=True))
                            ),
                        ),
                        rx.menu(
                            rx.menu_button(
                                rx.hstack(
                                    rx.heading(
                                        State.account_manager_navbar_menu_text,                                    
                                        color="WHITE",
                                        font_size="2.1vh"
                                        ),
                                    rx.icon(
                                        tag="chevron_down",
                                        color="white",
                                        width="2.625vh",
                                        height="auto"
                                    ),
                                    spacing="0px"
                                ), 
                            ),
                            rx.cond(
                                State.username,
                                rx.menu_list(
                                    rx.menu_item("Manage Account", on_click=lambda: rx.redirect("/dashboard")),
                                    rx.menu_item("My Services"),
                                    rx.menu_divider(),
                                    rx.menu_item("Logout", on_click=State.logout)
                                ),
                                rx.menu_list(
                                    rx.hstack(rx.box(),rx.text("You are not logged in")),
                                    rx.box(height="0.84vh"),
                                    rx.hstack(rx.box(),rx.button("LOGIN", bg="GREEN", color="WHITE", on_click=rx.redirect("/login"))),
                                    rx.menu_divider(),
                                    rx.hstack(rx.box(),rx.text("Dont have an account?")),
                                    rx.box(height="0.84vh"),
                                    rx.hstack(rx.box(),rx.button("SIGN UP", bg="#00008B", color="WHITE", on_click=State.navbar_signup))
                                ),
                            )
                        ),
                        spacing="3.15vh"
                    ),
                    rx.box(width="10.5vh"),
                    width="100%",
                    bg="black",
                    position="fixed",
                    height="10.4vh",
                ),
                rx.vstack(
                    rx.box(height="40vh"),
                    rx.cond(
                        State.username,
                        rx.heading(
                            rx.span("Welcome back, ", color="WHITE"),
                            rx.span(State.username, color=State.random_light_color),
                            font_size="4vh"
                        ),
                        rx.heading(
                            rx.span("Cloud hosting for files", color="WHITE"),
                            font_size="4vh"
                        )
                    ),
                    rx.hstack(
                        rx.cond(
                            State.username,
                            rx.button(
                                rx.span("Go to panel ", on_click=rx.redirect("/dashboard")),
                                rx.span(rx.icon(tag="external_link")),
                                font_size="1.6vh",
                                bg="GREEN",
                                color="WHITE",
                                height="4vh",
                                width="13vh"
                            ),
                            rx.button(
                                rx.span("Login to your account"),
                                rx.span(rx.icon(tag="lock")),
                                font_size="1.6vh",
                                color="WHITE",
                                bg="BLUE",
                                on_click=rx.redirect("/login"),
                                width="20vh",
                                height="4vh"
                            )
                        ),
                        rx.button(
                            rx.span("View project on Github", font_size="1.4vh"),
                            rx.span(width="0.9vh"),
                            rx.image(
                                src="/github.png",
                                height="1.7vh",
                                width="1.7vh"
                            ),
                            spacing="0vh",
                            height="4vh",
                            bg="BLACK",
                            color="WHITE",
                            width="20vh",
                            on_click=rx.redirect("https://github.com/Anga205/anga.pro/")
                        ),
                        spacing="1vh"
                    ),
                    bg="#0E0019",
                    width="100%",
                    height="90vh",
                    spacing="2.1vh",
                    on_mouse_over=State.stop_timer,on_mouse_enter=State.stop_timer,
                ),
                rx.vstack(
                    rx.box(height="10vh"),
                    rx.heading(
                        rx.span("Why use "),
                        rx.span("anga", color="#ffcccb"),
                        rx.span(".", color="#90EE90"),
                        rx.span("pro", color="#ADD8E6"),
                        rx.span("?"),
                        color='WHITE',
                        font_size="4vh"
                    ),
                    rx.center(
                        rx.hstack(
                            rx.vstack(
                                rx.image(src="open-source.png", height="8vh", width="auto"),
                                rx.heading("Open Source", _as="b", color="WHITE", font_size="3vh", text_align="center"),
                                rx.center(
                                    rx.text("All of my projects (including this website!) are open source, and availible on my github page, if you doubt my hosting, you can always download and host by yourself", text_align="center", color="WHITE", font_size="1.66vh")
                                ),
                                width="22vh",
                                border_radius="0.525vh",
                                bg="BLACK",
                                border_width="2.1vh",
                                border_color="BLACK",
                                height="41vh",
                                spacing="0.5vh"
                            ),
                            rx.vstack(
                                rx.image(src="attention.png", height="8vh", width="auto"),
                                rx.heading("Personalized Attention", _as="b", color="WHITE", font_size="3vh", text_align="center"),
                                rx.center(
                                    rx.text("Due to the small-scale nature of anga.pro, any issues you have, will be personally looked into (and hopefully solved) by me, there is no elaborate beaureocracy to navigate for support", text_align="center", color="WHITE", font_size="1.66vh")
                                ),
                                width="22vh",
                                border_radius="0.525vh",
                                bg="BLACK",
                                border_width="2.1vh",
                                border_color="BLACK",
                                height="41vh",
                                spacing="0.5vh"
                            ),
                            rx.vstack(
                                rx.image(src="money.png", height="8vh", width="auto"),
                                rx.heading("Cost Effective", _as="b", color="WHITE", font_size="3vh", text_align="center"),
                                rx.center(
                                    rx.text("anga.pro is an indie project and therefore prioritizes cost effectiveness over everything, although i will always try to maintain quality in my work", text_align="center", color="WHITE", font_size="1.66vh")
                                ),
                                width="22vh",
                                border_radius="0.525vh",
                                bg="BLACK",
                                border_width="2.1vh",
                                border_color="BLACK",
                                height="41vh",
                                spacing="0.5vh"
                            ),
                            rx.vstack(
                                rx.image(src="flower.png", height="8vh", width="auto"),
                                rx.heading("Customized Solutions", _as="b", color="WHITE", font_size="3vh", text_align="center"),
                                rx.center(
                                    rx.text("If a public project of mine does not suit exactly your hosting needs, just contact me and tell me exactly what you desire, i will try to help you out", text_align="center", color="WHITE", font_size="1.66vh")
                                ),
                                width="22vh",
                                border_radius="0.525vh",
                                bg="BLACK",
                                border_width="2.1vh",
                                border_color="BLACK",
                                height="41vh",
                                spacing="0.5vh"
                            ),
                            rx.vstack(
                                rx.image(src="lock.png", height="8vh", width="auto"),
                                rx.heading("Privacy", _as="b", color="WHITE", font_size="3vh", text_align="center"),
                                rx.center(
                                    rx.text("Any projects i make specifically for you will not be published to open source without your explicit consent, on the off chance i do publish it, ill refund you and you can use it for free", text_align="center", color="WHITE", font_size="1.66vh")
                                ),
                                width="22vh",
                                border_radius="0.525vh",
                                bg="BLACK",
                                border_width="2.1vh",
                                border_color="BLACK",
                                height="41vh",
                                spacing="0.5vh"
                            ),
                            rx.vstack(
                                rx.image(src="kling.png", height="8vh", width="auto"),
                                rx.heading("Track Record", _as="b", color="WHITE", font_size="3vh", text_align="center"),
                                rx.center(
                                    rx.text("I have somewhat of a positive track record, You may know my previous project, KlingMC, which remained up to date while it was active.", text_align="center", color="WHITE", font_size="1.66vh")
                                ),
                                width="22vh",
                                border_radius="0.525vh",
                                bg="BLACK",
                                border_width="2.1vh",
                                border_color="BLACK",
                                height="41vh",
                                spacing="0.5vh"
                            ),
                            spacing="3.15vh",
                            width="80%"
                        ),
                        width="100%"
                    ),
                    bg="#190000",
                    width="100%",
                    height="75vh",
                    spacing="3.15vh",
                ),
                rx.vstack(
                    rx.box(height="6vh"),
                    rx.heading("Some interesting statistics about this website:", color="WHITE", font_size="3.5vh"),
                    rx.text("This data is live updated, refresh this page to see the numbers change!", color="WHITE", font_size="1.5vh"),
                    rx.hstack(
                        rx.vstack(
                            rx.recharts.line_chart(
                                rx.recharts.line(
                                    data_key="Page loads",
                                    stroke="BLACK"
                                ),
                                rx.recharts.x_axis(data_key="Date"),
                                rx.recharts.y_axis(),
                                rx.recharts.graphing_tooltip(),
                                data=State.loads_per_day,
                                height="90%",
                                width="100%",
                            ),
                            rx.hstack(
                                rx.spacer(),
                                rx.heading("Number of times this page was loaded today: ", font_size="2vh"), 
                                rx.heading(State.loads_today, font_size="2vh"), 
                                rx.spacer(),
                                bg="#00fff5",
                                spacing="0vh",
                                width="100%",
                                align_items="center",
                            ),
                            align_items="center",
                            bg="#00fff5",
                            border_radius="1vh",
                            spacing="0vh",
                            width="65vh",
                            height="30vh",
                            border_width="1vh",
                            border_color="#00fff5"
                        ),
                        rx.vstack(
                            rx.heading("Time since last update (to this website):", font_size="1.7vh"),
                            rx.heading(State.uptime, font_size="2.4vh"),
                            rx.heading(rx.span("You can "), rx.span("click here"), rx.span(" to see details about updates"), font_size="1.7vh"),
                            width="36vh",
                            height="100%",
                            bg="#00fff5",
                            border_radius="1vh",
                            border_color="#00fff5",
                            border_width="5px",
                        ),
                        align_items="stretch",
                        spacing="5vh"
                    ),
                    rx.box(
                            height="10vh"
                        ),
                   # height="60vh",
                    width="100%",
                    bg="#001918",
                    spacing="0.3vh",
                    on_mouse_over=State.start_timer,on_mouse_enter=State.start_timer,
                ),
                rx.vstack(
                    rx.box(height="1vh"),
                    rx.text(rx.span("All visible content on this website is available under the ",rx.span(rx.link("GNU affero general public license", href="https://github.com/Anga205/anga.pro/blob/main/LICENSE", color="#ADD8E6"))), color="WHITE", font_size="1.4vh"),
                    spacing="3.15vh",
                    width="100%",
                    height="10vh",
                    bg="#000f19"
                ),
                width="100%",
                spacing="0px"
            )
        ),
        rx.mobile_only(
            rx.vstack(
                rx.hstack(
                    rx.box(width="2%"),
                    rx.icon(tag="hamburger", color="WHITE", font_size="3xl", on_click=State.turn_on_mobile_homepage_drawer),
                    rx.drawer(
                            rx.drawer_overlay(
                                rx.drawer_content(
                                    rx.drawer_header("Anga.pro", color="WHITE"),
                                    rx.drawer_body(
                                        rx.accordion(
                                            rx.accordion_item(
                                                rx.accordion_button(
                                                    rx.heading("Contact", color="WHITE"),
                                                    rx.accordion_icon(),
                                                ),
                                                rx.accordion_panel(
                                                    rx.text("Discord", on_click=rx.redirect("https://discord.gg/DgxppCZnJb", external=True), color="WHITE"),
                                                    rx.text("Instagram", on_click=rx.redirect("https://instagram.com/_anga205", external=True), color="WHITE"),
                                                    rx.text("Threads", on_click=rx.redirect("https://threads.net/@_anga205", external=True), color="WHITE"),
                                                    rx.text("𝕏.com", on_click=rx.redirect("https://x.com/_anga205", external=True), color="WHITE"),
                                                    rx.text("Email", on_click=rx.redirect("mailto:support@anga.pro", external=True), color="WHITE"),
                                                    rx.text("GitHub", on_click=rx.redirect("https://github.com/Anga205", external=True), color="WHITE"),
                                                    rx.text("Telegram", on_click=rx.redirect("https://t.me/Anga205", external=True), color="WHITE"),
                                                ),
                                            ),
                                            allow_toggle=True,
                                            width="100%",
                                        ),
                                        rx.accordion(
                                            rx.accordion_item(
                                                rx.accordion_button(
                                                    rx.heading(State.account_manager_navbar_menu_text, color="WHITE"),
                                                    rx.accordion_icon(),
                                                ),
                                                rx.accordion_panel(
                                                    rx.cond(
                                                        State.username,
                                                        rx.vstack(
                                                            rx.text("Manage Account", color="GRAY", on_click=rx.redirect("/dashboard")),
                                                            rx.text("My Services", color="GRAY", on_click=rx.redirect("/dashboard")),
                                                            rx.divider(border_color="GRAY"),
                                                            rx.text("Logout", color="GRAY", on_click=State.logout)
                                                        ),
                                                        rx.vstack(
                                                            rx.hstack(rx.box(),rx.text("You are not logged in", color="WHITE")),
                                                            rx.box(height="0.84vh"),
                                                            rx.hstack(rx.box(),rx.button("LOGIN", bg="GREEN", color="WHITE", on_click=rx.redirect("/login"))),
                                                            rx.divider(border_color="GRAY"),
                                                            rx.hstack(rx.box(),rx.text("Dont have an account?", color="WHITE")),
                                                            rx.box(height="0.84vh"),
                                                            rx.hstack(rx.box(),rx.button("SIGN UP", bg="#00008B", color="WHITE", on_click=State.navbar_signup))
                                                        )
                                                    )
                                                ),
                                            ),
                                            allow_toggle=True,
                                            width="100%",
                                        )
                                    ),
                                    rx.drawer_footer(
                                        rx.button(
                                            "Close", on_click=State.turn_off_mobile_homepage_drawer
                                        )
                                    ),
                                    bg="rgba(0, 0, 0, 0.3)",
                                )
                            ),
                            placement="left",
                            is_open=State.mobile_homepage_drawer
                        ),
                    rx.spacer(),
                    rx.image(src="/logo.png", height="13vh"),
                    bg="BLACK",
                    height="12vh",
                    width="100%",
                    position="fixed"
                ),
                rx.vstack(
                    rx.box(height="30vh"),
                    rx.cond(
                        State.username,
                        rx.heading(
                            rx.span("Welcome back, ", color="WHITE"),
                            rx.span(State.username, color=State.random_light_color),
                            font_size="7vh",
                            style={"text-align":"center"}
                        ),
                        rx.heading(
                            rx.span("Cloud hosting for files", color="WHITE"),
                            font_size="7vh",
                            style={"text-align":"center"}
                        )
                    ),
                    rx.vstack(
                        rx.cond(
                            State.username,
                            rx.button(
                                rx.span("Go to panel ", on_click=rx.redirect("/dashboard"), font_size="2vh"),
                                rx.span(rx.icon(tag="external_link"), font_size="2vh"),
                                bg="GREEN",
                                color="WHITE",
                                height="5vh"
                            ),
                            rx.button(
                                rx.span("Login to your account", font_size="2vh"),
                                rx.span(rx.icon(tag="lock"), font_size="2vh"),
                                color="WHITE",
                                bg="BLUE",
                                on_click=rx.redirect("/login"),
                                height="5vh",
                                width="26vh"
                            )
                        ),
                        rx.button(
                            rx.span("View project on Github", font_size="2vh"),
                            rx.span(width="1vh"),
                            rx.image(
                                src="/github.png",
                                height="1.7vh",
                                width="1.7vh"
                            ),
                            height="5vh",
                            width="27vh",
                            bg="BLACK",
                            color="WHITE",
                            on_click=rx.redirect("https://github.com/Anga205/anga.pro/")
                        ),
                        spacing="1vh"
                    ),
                    bg="#0E0019",
                    height="80vh",
                    width="100%",
                    on_mouse_over=State.stop_timer,on_mouse_enter=State.stop_timer,
                ),
                rx.vstack(
                    rx.box(height="5vh"),
                    rx.heading("Why use ", 
                        rx.span("anga", color="#ffcccb"),
                        rx.span(".", color="#90EE90"),
                        rx.span("pro", color="#ADD8E6"),
                        "?",
                        font_size="7vh", 
                        color="WHITE",
                        style={"text-align":"center"}
                        ),
                    rx.hstack(
                        rx.image(
                            src="/open-source.png",
                            height="auto",
                            width="50%",
                            ),
                        rx.vstack(
                            rx.heading(
                                "Open Source",
                                font_size="3.5vh",
                                color="WHITE"
                            ),
                            rx.text(
                                "All of my projects (including this website!) are open source, and availible on my github page, if you doubt my hosting, you can always download and host by yourself",
                                font_size="1.5vh",
                                color="WHITE",
                                style={"text-align":"center"}
                            ),
                            spacing="0.5vh"
                        ),
                        bg="BLACK",
                        width="90%",
                        border_radius="1vh",
                        border_color="BLACK",
                        border_width="1vh"
                    ),
                    rx.hstack(
                        rx.image(
                            src="/attention.png",
                            height="auto",
                            width="50%",
                            ),
                        rx.vstack(
                            rx.heading(
                                "Personalized Attention",
                                font_size="3.5vh",
                                color="WHITE"
                            ),
                            rx.text(
                                "Due to the small-scale nature of anga.pro, any issues you have, will be personally looked into (and hopefully solved) by me, there is no elaborate beaureocracy to navigate for support",
                                font_size="1.5vh",
                                color="WHITE",
                                style={"text-align":"center"}
                            ),
                            spacing="0.5vh"
                        ),
                        bg="BLACK",
                        width="90%",
                        border_radius="1vh",
                        border_color="BLACK",
                        border_width="1vh"
                    ),
                    rx.hstack(
                        rx.image(
                            src="/money.png",
                            height="auto",
                            width="50%",
                            ),
                        rx.vstack(
                            rx.heading(
                                "Cost Effective",
                                font_size="3.5vh",
                                color="WHITE"
                            ),
                            rx.text(
                                "anga.pro is an indie project and therefore prioritizes cost effectiveness over everything, although i will always try to maintain quality in my work",
                                font_size="1.5vh",
                                color="WHITE",
                                style={"text-align":"center"}
                            ),
                            spacing="0.5vh"
                        ),
                        bg="BLACK",
                        width="90%",
                        border_radius="1vh",
                        border_color="BLACK",
                        border_width="1vh"
                    ),
                    rx.hstack(
                        rx.image(
                            src="/flower.png",
                            height="auto",
                            width="50%",
                            ),
                        rx.vstack(
                            rx.heading(
                                "Customized Solutions",
                                font_size="3.5vh",
                                color="WHITE"
                            ),
                            rx.text(
                                "If a public project of mine does not suit exactly your hosting needs, just contact me and tell me exactly what you desire, i will try to help you out",
                                font_size="1.5vh",
                                color="WHITE",
                                style={"text-align":"center"}
                            ),
                            spacing="0.5vh"
                        ),
                        bg="BLACK",
                        width="90%",
                        border_radius="1vh",
                        border_color="BLACK",
                        border_width="1vh"
                    ),
                    rx.hstack(
                        rx.image(
                            src="/lock.png",
                            height="auto",
                            width="50%",
                            ),
                        rx.vstack(
                            rx.heading(
                                "Privacy",
                                font_size="3.5vh",
                                color="WHITE"
                            ),
                            rx.text(
                                "Any projects i make specifically for you will not be published to open source without your explicit consent, on the off chance i do publish it, ill refund you and you can use it for free",
                                font_size="1.5vh",
                                color="WHITE",
                                style={"text-align":"center"}
                            ),
                            spacing="0.5vh"
                        ),
                        bg="BLACK",
                        width="90%",
                        border_radius="1vh",
                        border_color="BLACK",
                        border_width="1vh"
                    ),
                    rx.hstack(
                        rx.image(
                            src="/kling.png",
                            height="auto",
                            width="50%",
                            ),
                        rx.vstack(
                            rx.heading(
                                "Track Record",
                                font_size="3.5vh",
                                color="WHITE"
                            ),
                            rx.text(
                                "I have somewhat of a positive track record, You may know my previous project, KlingMC, which remained up to date while it was active.",
                                font_size="1.5vh",
                                color="WHITE",
                                style={"text-align":"center"}
                            ),
                            spacing="0.5vh"
                        ),
                        bg="BLACK",
                        width="90%",
                        border_radius="1vh",
                        border_color="BLACK",
                        border_width="1vh"
                    ),
                    rx.box(height="5vh"),
                    bg="#190000",
                ),
                rx.vstack(
                    rx.box(
                        height="5vh"
                    ),
                    rx.heading(
                        "Some interesting stats about this website:",
                        color="WHITE",
                        style={"text-align":"center"},
                        font_size="6vh"
                    ),
                    rx.text("This data is live updated, refresh this page to see the numbers change!", color="WHITE", font_size="1.2vh"),
                    rx.vstack(
                        rx.vstack(
                            rx.recharts.line_chart(
                                rx.recharts.line(
                                    data_key="Page loads",
                                    #type_="monotone",
                                    stroke="BLACK"
                                ),
                                rx.recharts.x_axis(data_key="Date"),
                                rx.recharts.y_axis(),
                                rx.recharts.graphing_tooltip(),
                                data=State.loads_per_day,
                                height="90%",
                                width="100%",
                            ),
                        rx.box(
                            rx.heading(rx.span("Number of times this page was loaded today: "), rx.span(State.loads_today), font_size="1.7vh", style={"text-align":"center"})
                            ),
                        bg="#00fff5",
                        border_color="#00fff5",
                        border_radius="1vh",
                        height="40vh",
                        width="100%"
                        )
                    ),
                    rx.vstack(
                        rx.heading("Time since last update (to this website):", font_size="1.7vh"),
                        rx.heading(State.uptime, font_size="2.4vh"),
                        rx.heading(rx.span("You can "), rx.span("click here"), rx.span(" to see details about updates"), font_size="1.7vh"),
                        width="90%",
                        bg="#00fff5",
                        border_radius="1vh",
                        border_color="#00fff5",
                        border_width="5px",
                    ),
                    rx.box(height="3vh"),
                    bg="#001918",
                    on_mouse_over=State.start_timer,on_mouse_enter=State.start_timer,
                    on_mouse_leave=State.stop_timer,
                ),
                rx.vstack(
                    rx.box(height="1vh"),
                    rx.text(rx.span("All visible content on this website is available under the ",rx.span(rx.link("GNU affero general public license", href="https://github.com/Anga205/anga.pro/blob/main/LICENSE", color="#ADD8E6"))), color="WHITE", font_size="1.4vh", style={"text-align":"center"}),
                    rx.box(height="1vh"),
                    width="100%",
                    bg="#000f19"
                ),
                spacing="0px"
            )
        ),
        on_unmount=State.unload_homepage
    )

def user_profile_pic(side=100):
    return rx.cond(
        State.pfp_exists,
        rx.image(src=f"/pfps/{State.email}"),
        rx.avatar(name=State.username, border_radius=f"{side/2}vh", height=f"{side}vh", width=f"{side}vh")
    )

def account_editor():
    return rx.vstack(
                rx.heading("Account Details", color="WHITE", font_size="5vh"),
                rx.divider(border_color="WHITE"),
                rx.hstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text("Username:", width="14vh", color="WHITE", font_size="2.3vh"), 
                            rx.text("E-mail:", width="14vh", color="WHITE", font_size="2.3vh"),
                            spacing="0px"
                            ),
                        rx.vstack(
                            rx.cond(
                                State.enable_username_editor_in_dashboard,
                                rx.input(default_value=State.username, on_blur=State.change_username_thru_dashboard, color="WHITE", height="2.3vh"),
                                rx.text(State.username, color="WHITE", font_size="2.3vh", width="100%", on_click=State.switch_username_editor_in_dashboard),
                            ),
                            rx.text(State.email, color="WHITE", font_size="2.3vh", width="100%", on_click=rx.window_alert("E-mail cannot be edited (yet)")),
                            spacing="0px"
                            
                        ),
                        spacing="0px"
                    ),
                    rx.box(width="1vh"),
                    user_profile_pic(10),
                    spacing="0vh"
                ),
                border_radius="2vh",
                bg="#0F0F10",
                spacing="0.5vh",
                border_color="#0F0F10",
                border_width="1vh"
            )

def notifications_tab():
    return rx.vstack(
        rx.heading("Account Notifications", color="WHITE", font_size="5vh"),
        rx.divider(border_color="WHITE"),
        rx.text("No Notifications found at the moment", color="WHITE", font_size="2vh"),
        border_radius="2vh",
        border_color="#0F0F10",
        bg="#0F0F10", 
        border_width="1vh",
        spacing="0.5vh"
    )

def announcements_tab():
    return rx.vstack(
        rx.heading("Site-Wide Announcements", color="WHITE", font_size="3.5vh"),
        rx.divider(border_color="WHITE"),
        rx.text("None for now", color="WHITE", font_size="1.65vh"),
        bg="#0F0F10",
        border_color="#0F0F10",
        border_radius="1vh",
        border_width="1vh",
        spacing="0.5vh"
    )

def account_manager():
    return rx.hstack(
    rx.vstack(
        account_editor(),
        notifications_tab(),
        spacing="2vh"
        ),
    rx.vstack(
        updating_components.account_manager(),
        announcements_tab(),
        spacing="2vh"
        ),
    align_items="top",
    spacing="5vh"
    )

def dashboard():
    return rx.hstack(
#-------------------------------------------------------------------------------------------------------------------------------------------------
#                                                              SIDEBAR
#-------------------------------------------------------------------------------------------------------------------------------------------------
        rx.vstack(
            rx.box(height="5vh"),
            rx.button(
                rx.span(
                    rx.image(src="/account.png"), 
                    width="2.1vh", 
                    height="2.1vh", 
                    style={"margin-top": "0.315vh"}
                    ), 
                rx.span("", width="2.1vh"), 
                rx.span("Manage Account"), 
                rx.spacer(), 
                color="WHITE", 
                font_size="2.1vh", 
                bg="#0E0019", 
                on_click=State.set_dashboard_to_account_manager,
                width="100%",
                height="4.5vh",
                spacing="0px",
                _hover={"bg":"BLACK"}
                ),
            rx.button(
                rx.span(
                    rx.image(src="/file_host.png"), 
                    width="2.1vh", 
                    height="2.1vh", 
                    style={"margin-top": "0.315vh"}
                    ), 
                rx.span("", width="2.1vh"), 
                rx.span("File Hosting"), 
                rx.spacer(), 
                color="WHITE", 
                on_click=State.set_dashboard_to_file_hosting,
                font_size="2.1vh", 
                bg="#0E0019", 
                width="100%",
                height="4.5vh",
                _hover={"bg":"BLACK"}
                ),
            rx.button(
                rx.span(
                    rx.image(src="/support.png"), 
                    width="2.1vh", 
                    height="2.1vh", 
                    style={"margin-top": "0.315vh"}
                    ), 
                rx.span("", width="2.1vh"), 
                rx.span("Support"), 
                rx.spacer(), 
                color="WHITE", 
                font_size="2.1vh", 
                bg="#0E0019", 
                width="100%",
                height="4.5vh",
                _hover={"bg":"BLACK"},
                on_click=State.set_dashboard_to_support_page
                ),
            rx.button(
                rx.span(
                    rx.icon(tag="delete"), 
                    style={"margin-top": "-0.525vh"}
                    ), 
                rx.span(
                    "", 
                    width="2.1vh"
                    ), 
                rx.span("Delete Account"), 
                rx.spacer(), 
                color="RED", 
                font_size="2.1vh", 
                bg="#0E0019", 
                width="100%",
                on_click=State.dashboard_delete_account,
                height="4.5vh",
                _hover={"bg":"BLACK"},
                spacing="0vh"
                ),
            spacing="1vh",
            width="15%",
            height="100vh",
            bg="#0E0019",
            position="fixed",
        ),
        rx.spacer(),
        rx.vstack(
#-------------------------------------------------------------------------------------------------------------------------------------------------
#                                                              TOPBAR
#-------------------------------------------------------------------------------------------------------------------------------------------------
            rx.hstack(
                rx.box(width="6%"),
                rx.image(src="/logo.png", height="6vh", width="auto"),
                rx.spacer(),
                bg="#000d19",
                height="6vh",
                width="85%",
                position="fixed",
                spacing="0px"
            ),
            rx.box(height="7vh"),
            rx.cond(
                State.dashboard_is_account_page,
                account_manager(),
                rx.cond(
                    State.dashboard_is_hosting_page,
                    dashboard_pages.file_hosting_page(State, State.bool_files_associated_with_account,State.enable_popup_to_upload, State.turn_off_popup_to_upload, State.turn_on_popup_to_upload, State.handle_upload),
                    dashboard_pages.support_page(State)
                )
            ),
            height="100vh", 
            width="85%", 
            bg="BLACK", 
            style={"margin-left":"15%"},
            spacing="0px"
            ),
        spacing="0px",
    )

def TPU_login():
    return rx.box(
        rx.text("Please wait for a few seconds for your TPU login to be verified....."),
    )

# Add state and page to the app.
app = rx.App()
app.add_page(login, title="Login Page - anga.pro", description="log into anga.pro to access dashboard", on_load=State.login_page_load)
app.add_page(dashboard, title="Dashboard - anga.pro", description="Manage account and services", on_load=State.dashboard_load)
app.add_page(index, title="Home - anga.pro", description="Open source cloud hosting service for files", on_load=State.homepage_load)
app.add_page(TPU_login, title="TPU - anga.pro", description="Oauth2 Link", route="/tpulogin", on_load=State.TPU_verify)
app.add_page(add_TPU_to_account, title="TPU signup - anga.pro", description="This page opens when the email id attached to a tpu account already has an account in anga.pro", route="/tpusignup", on_load=State.signup_page_load)
app.add_page(rx.fragment(), route="/signup", on_load=State.signup_page_load)
app.compile()
