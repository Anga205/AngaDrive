"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx
import website.library as func
import random

class State(rx.State):
    username=""
    email = ""
    password = ""

    signup_email_color_bg="WHITE"
    email_color_bg="WHITE"

    arrow_over_pfp_in_dashboard=False

    def func_mouse_hover_pfp_in_dashboard(self):
        self.arrow_over_pfp_in_dashboard=not self.arrow_over_pfp_in_dashboard

    SignUpEnabled = False

    SignUp_username=""
    SignUp_email=""
    SignUp_password=""

    navbar_contact_color="WHITE"

    def navbar_contact_hover(self):
        self.navbar_contact_color="#D3D3D3"
    
    def navbar_contact_unhover(self):
        self.navbar_contact_color="WHITE"

    navbar_my_account_color="WHITE"

    def navbar_my_account_hover(self):
        self.navbar_my_account_color="#D3D3D3"
    
    def navbar_my_account_unhover(self):
        self.navbar_my_account_color="WHITE"

    @rx.var
    def account_manager_navbar_menu_text(self):
        if self.username=="":
            return "Account"
        return self.username

            
    def SignUpEnable(self):
        self.SignUpEnabled=not self.SignUpEnabled

    def navbar_signup(self):
        self.SignUpEnabled=True
        return rx.redirect("/login")

    def set_SignUp_email(self, email):
        if func.is_valid_email(email):
            self.SignUp_email=email
            self.signup_email_color_bg="WHITE"
        else:
            self.signup_email_color_bg="RED"
            self.SignUp_email=""

    def submit_signup(self):
        if self.SignUp_username=="":
            return rx.window_alert("Username is empty")
        if self.SignUp_email=="":
            return rx.window_alert("Please enter a valid email address")
        if self.SignUp_password=="":
            return rx.window_alert("Password field is empty")
        for i in [self.SignUp_username, self.SignUp_email, self.SignUp_password]:
            if func.find_sql_insertion(i):
                return rx.window_alert('''Potential SQL insertion detected, please avoid charectors like ', ", } etc.''')
        insertion = func.new_user_signup(self.SignUp_username, self.SignUp_email, self.SignUp_password)
        if insertion==True:
            self.username, self.email, self.password=self.SignUp_username, self.SignUp_email, self.SignUp_password
            print(f"{self.username} just registered a new account!")
            return rx.window_alert("Signup Successful!")
        else:
            return rx.window_alert(insertion)

    def logout(self):
        self.username=""
        self.email=""
        self.password=""
        self.SignUp_password=""
        self.SignUp_username=""
        self.SignUp_email=""
        return rx.clear_local_storage()

    def set_email(self, email):
        if email=="":
            self.email_color_bg="WHITE"
        elif func.is_valid_email(email):
            self.email=email
            self.email_color_bg="WHITE"
        else:
            self.email_color_bg="RED"
            self.email=""        

    def submit_login(self):
        if self.email=="" or self.password=="":
            return rx.window_alert("Please enter a valid email id and password")
        else:
            login_data=func.login_user(self.email, self.password)
            if (True in login_data):
                self.username=login_data[1]
                
                return [rx.set_local_storage("accounts",str({"username":self.username,"email":self.email,"password":self.password})),rx.window_alert(f"Login for {self.username} successful!")]
            else:
                print(login_data)
                return rx.window_alert(login_data[1])

    @rx.var
    def welcome_message(self):
        if self.username=="":
            return "Welcome to anga.pro"
        else:
            return f"Welcome back, {self.username}"
    
    @rx.var
    def random_light_color(self):
        return random.choice(["#ffcccb","#90EE90","#ADD8E6"])


    def local_storage_value(self):
        try:
            return rx.get_local_storage("accounts")
        except Exception as e:
            print(f"local_storage_value error {e}")


    def page_load(self, storage):
        if self.username=="":
            try:
                if storage==None:
                    print("No local storage found")
                else:
                    login_data=eval(storage)
                    response=func.login_user(login_data["email"],login_data["password"])
                    if response[0]:
                        self.username=response[1]
                        self.email=login_data["email"]
                        self.password=login_data["password"]
                        rx.set_local_storage("accounts",{"username":self.username,"email":self.email,"password":self.password})
                        print(f"{self.username} logged in thru session")
                    else:
                        print(f"Login with details '{login_data['email']}', '{login_data['password']}' failed with reason {response[1]}")
                        rx.clear_local_storage()
            except Exception as e:
                print(e)
        else:
            print(f"{self.username} is already logged in")

    def login_page_load(self, storage):
        self.page_load(storage)
        if self.username=="":
            pass
        else:
            return rx.redirect("/dashboard")


class OnLoadHack(rx.Fragment):
    def _get_hooks(self):
        formatted_on_load = rx.components.tags.tag.Tag.format_prop(
            self.event_triggers["on_load"]
        )[7:-6] + ")"
        return f"""
        useEffect(() => {{
            {formatted_on_load}
        }}, [])
        """

    def get_triggers(self):
        return super().get_triggers() | {"on_load"}

    def render(self) -> str:
        return ""



def login() -> rx.Component:
    return rx.hstack(
        rx.center( 
            rx.vstack(
                rx.box(height="40vh", width="100%"),
                rx.center(
                    rx.vstack(
                        rx.heading("Login"),
                        rx.box(height="10px"),
                        rx.input(
                            placeholder="Enter e-mail address",
                            on_blur=State.set_email,
                            bg=State.email_color_bg
                            ),
                        rx.password(
                            placeholder="Enter password",
                            on_blur=State.set_password
                        ),
                        rx.button("LOGIN", bg="PURPLE", color="WHITE", on_click=State.submit_login),
                        rx.hstack(
                            rx.text("Dont have an account?"),
                            rx.link("Sign up!", as_="b" ,on_click=State.SignUpEnable),
                        ),
                        spacing="20px"
                    ),
                    height="50vh", 
                    bg="WHITE", 
                    width="100%",
                    border_radius="20px 0px 20px 0px",
                    border_color="BLUE",
                    border_width="10px"
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
                            rx.input(placeholder="Enter a username", on_blur=State.set_SignUp_username),
                            rx.input(placeholder="Enter an e-mail ID", bg=State.signup_email_color_bg, on_blur=State.set_SignUp_email),
                            rx.password(placeholder="Enter a password", on_blur=State.set_SignUp_password)
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
        OnLoadHack.create(on_load=lambda: State.login_page_load(rx.get_local_storage("accounts"))),
        width="100%",
        bg="BLACK",
    )


def navbar():
    return rx.hstack(
        rx.box(width="200px"),
        rx.image(src="/logo.png", width="75px", height="75px", on_click=rx.redirect("/")),
        rx.spacer(),
        rx.hstack(
            rx.menu(
                rx.menu_button(
                    rx.heading(
                        "Contact", 
                        color=State.navbar_contact_color, 
                        size="md"
                        ), 
                    on_mouse_enter=State.navbar_contact_hover, 
                    on_mouse_leave=State.navbar_contact_unhover
                    ),
                rx.menu_list(
                    rx.menu_item("Discord", on_click=rx.redirect("https://discord.gg/DgxppCZnJb")),
                    rx.menu_item("Instagram", on_click=rx.redirect("https://instagram.com/_anga205")),
                    rx.menu_item("Threads", on_click=rx.redirect("https://threads.net/@_anga205")),
                    rx.menu_item("𝕏.com", on_click=rx.redirect("https://x.com/_anga205")),
                    rx.menu_item("Email", on_click=rx.redirect("mailto:support@anga.pro")),
                    rx.menu_item("GitHub", on_click=rx.redirect("https://github.com/Anga205")),
                    rx.menu_item("Telegram", on_click=rx.redirect("https://t.me/Anga205"))
                )
            ),
            rx.menu(
                rx.menu_button(
                    rx.hstack(
                        rx.heading(
                            State.account_manager_navbar_menu_text, 
                            color=State.navbar_my_account_color, 
                            size="md"
                            ),
                        rx.icon(
                            tag="chevron_down",
                            color="white",
                            width="25px",
                            height="auto"
                        ),
                        spacing="0px"
                    ), 
                    on_mouse_enter=State.navbar_my_account_hover, 
                    on_mouse_leave=State.navbar_my_account_unhover
                ),
                rx.cond(
                    State.username,
                    rx.menu_list(
                        rx.menu_item("Manage Account"),
                        rx.menu_item("My Services"),
                        rx.menu_divider(),
                        rx.menu_item("Logout", on_click=State.logout)
                    ),
                    rx.menu_list(
                        rx.hstack(rx.box(),rx.text("You are not logged in")),
                        rx.box(height="8px"),
                        rx.hstack(rx.box(),rx.button("LOGIN", bg="GREEN", color="WHITE", on_click=rx.redirect("/login"))),
                        rx.menu_divider(),
                        rx.hstack(rx.box(),rx.text("Dont have an account?")),
                        rx.box(height="8px"),
                        rx.hstack(rx.box(),rx.button("SIGN UP", bg="#00008B", color="WHITE", on_click=State.navbar_signup))
                    ),
                )
            ),
            spacing="30px"
        ),
        rx.box(width="100px"),
        OnLoadHack.create(on_load=lambda: State.page_load(rx.get_local_storage("accounts"))),
        width="100%",
        bg="black",
        position="fixed",
        height="100px"
    )


def index():
    return rx.vstack(
        navbar(),
        rx.vstack(
            rx.box(height="40vh"),
            rx.cond(
                State.username,
                rx.heading(
                    rx.span("Welcome back, ", color="WHITE"),
                    rx.span(State.username, color=State.random_light_color),
                    font_size="5xl"
                ),
                rx.heading(
                    rx.span("Welcome to ", color="WHITE"),
                    rx.span("anga", color="#ffcccb"),
                    rx.span(".", color="#90EE90"),
                    rx.span("pro", color="#ADD8E6"),
                    font_size="5xl"
                )
            ),
            rx.cond(
                State.username,
                rx.button(
                    rx.span("Go to panel ", on_click=rx.redirect("/dashboard")),
                    rx.span(rx.icon(tag="external_link")),
                    bg="GREEN",
                    color="WHITE"
                ),
                rx.button(
                    rx.span("Login to your account"),
                    rx.span(rx.icon(tag="lock")),
                    color="WHITE",
                    bg="BLUE",
                    on_click=rx.redirect("/login")
                )
            ),
            bg="#0E0019",
            width="100%",
            height="90vh",
            spacing="20px"
        ),
        rx.vstack(
            rx.box(height="10vh"),
            rx.heading(
                rx.span("Why use "),
                rx.span("anga", color="#ffcccb"),
                rx.span(".", color="#90EE90"),
                rx.span("pro", color="#ADD8E6"),
                rx.span("?"),
                color='WHITE'
            ),
            rx.center(
                rx.hstack(
                    rx.vstack(
                        rx.image(src="open-source.png", height="75px", width="auto"),
                        rx.heading("Open Source", _as="b", color="WHITE", font_size="3xl", text_align="center"),
                        rx.center(
                            rx.text("All of my projects (including this website!) are open source, and availible on my github page, if you doubt my hosting, you can always download and host by yourself", text_align="center", color="WHITE")
                        ),
                        width="14%",
                        border_radius="5px",
                        bg="BLACK",
                        border_width="20px",
                        border_color="BLACK",
                        height="400px"
                    ),
                    rx.vstack(
                        rx.image(src="attention.png", height="75px", width="auto"),
                        rx.heading("Personalized Attention", _as="b", color="WHITE", font_size="3xl", text_align="center"),
                        rx.center(
                            rx.text("Due to the small-scale nature of anga.pro, any issues you have, will be personally looked into (and hopefully solved) by me, there is no elaborate beaureocracy to navigate for support", text_align="center", color="WHITE")
                        ),
                        width="14%",
                        border_radius="5px",
                        bg="BLACK",
                        border_width="20px",
                        border_color="BLACK",
                        height="400px"
                    ),
                    rx.vstack(
                        rx.image(src="money.png", height="75px", width="auto"),
                        rx.heading("Cost Effective", _as="b", color="WHITE", font_size="3xl", text_align="center"),
                        rx.center(
                            rx.text("anga.pro is an indie project and therefore prioritizes cost effectiveness over everything, although i will always try to maintain quality in my work", text_align="center", color="WHITE")
                        ),
                        width="14%",
                        border_radius="5px",
                        bg="BLACK",
                        border_width="20px",
                        border_color="BLACK",
                        height="400px"
                    ),
                    rx.vstack(
                        rx.image(src="flower.png", height="75px", width="auto"),
                        rx.heading("Customized Solutions", _as="b", color="WHITE", font_size="3xl", text_align="center"),
                        rx.center(
                            rx.text("If a public project of mine does not suit exactly your hosting needs, just contact me and tell me exactly what you desire, i will try to help you out", text_align="center", color="WHITE")
                        ),
                        width="14%",
                        border_radius="5px",
                        bg="BLACK",
                        border_width="20px",
                        border_color="BLACK",
                        height="400px"
                    ),
                    rx.vstack(
                        rx.image(src="lock.png", height="75px", width="auto"),
                        rx.heading("Privacy", _as="b", color="WHITE", font_size="3xl", text_align="center"),
                        rx.center(
                            rx.text("Any projects i make specifically for you will not be published to open source without your explicit consent, on the off chance i do publish it, ill refund you and you can use it for free", text_align="center", color="WHITE")
                        ),
                        width="14%",
                        border_radius="5px",
                        bg="BLACK",
                        border_width="20px",
                        border_color="BLACK",
                        height="400px"
                    ),
                    rx.vstack(
                        rx.image(src="kling.png", height="75px", width="auto"),
                        rx.heading("Track Record", _as="b", color="WHITE", font_size="3xl", text_align="center"),
                        rx.center(
                            rx.text("I have somewhat of a positive track record, You may know my previous project, KlingMC, which remained up to date while it was active.", text_align="center", color="WHITE")
                        ),
                        width="14%",
                        border_radius="5px",
                        bg="BLACK",
                        border_width="20px",
                        border_color="BLACK",
                        height="400px"
                    ),
                    spacing="30px",
                    width="80%"
                ),
                width="100%"
            ),
            bg="#190000",
            width="100%",
            height="75vh",
            spacing="30px",
        ),
        rx.vstack(
            rx.box(height="1vh"),
            rx.text(rx.span("All visible content on this website is available under the ",rx.span(rx.link("Creative Commons Attribution-ShareAlike License 4.0", href="https://creativecommons.org/licenses/by-sa/4.0/", color="#ADD8E6"))), color="WHITE"),
            spacing="30px",
            width="100%",
            height="10vh",
            bg="#000f19"
        ),
        width="100%",
        spacing="0px"
    )


def dashboard():
    return rx.hstack(
        rx.vstack(
            rx.box(height="105vh"),
            rx.cond(
                State.arrow_over_pfp_in_dashboard,
                rx.image(src="edit.png", height="100px", width="100px", border_radius="50px",on_mouse_leave=State.func_mouse_hover_pfp_in_dashboard),
                rx.avatar(name=State.username, height="100px", width="100px", on_mouse_enter=State.func_mouse_hover_pfp_in_dashboard),
            ),
            rx.hstack(
                rx.heading(State.username, color="WHITE"),
                rx.image(src="edit.png", width="30px", height="30px")
            ),
            width="20%",
            height="200vh",
            bg="#0E0019",
            position="fixed"
        ),
        OnLoadHack.create(on_load=lambda: State.page_load(rx.get_local_storage("accounts")))
    )

# Add state and page to the app.
app = rx.App()
app.add_page(login, title="Login Page - anga.pro", description="Website is under construction")
app.add_page(dashboard, title="Dashboard - anga.pro", description="Website is under construction")
app.add_page(index, title="Home - anga.pro", description="Website is under construction")
app.compile()
