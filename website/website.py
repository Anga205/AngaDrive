"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx
import website.library as func
import random, os, time

class State(rx.State):
    username=""
    email = ""
    password = ""
    signup_email_color_bg="WHITE"
    email_color_bg="WHITE"
    arrow_over_pfp_in_dashboard=False
    SignUpEnabled = False
    SignUp_username=""
    SignUp_email=""
    SignUp_password=""
    navbar_contact_color="WHITE"
    enable_change_pfp_gui=False
    
    @rx.var
    def loads_today(self):
        return func.calls_per_day(func.get_timestamps())[-1]

    def func_mouse_hover_pfp_in_dashboard(self):
        self.arrow_over_pfp_in_dashboard=not self.arrow_over_pfp_in_dashboard

    @rx.var
    def loads_per_day(self) -> list[int]:
        timestamps=func.get_timestamps()
        earliest_day=timestamps[0]-86400
        all_days=[]
        for i in range(len(func.calls_per_day(timestamps))+1):
            all_days.append(" ".join(time.ctime(earliest_day).split()[1:3]))
            earliest_day+=86400
        return rx.data(
            "line",
            x=all_days,
            y=[0]+func.calls_per_day(timestamps),
        )
    
    def homepage_load(self):
        func.insert_timestamp()

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
            return [rx.window_alert("Signup Successful!"), rx.redirect("/dashboard"), rx.set_local_storage("accounts",str({"username":self.username,"email":self.email,"password":self.password}))]
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
    
    def dashboard_delete_account(self):
        if func.delete_account(self.email):
            self.username=""
            self.email=""
            self.password=""
            self.SignUp_password=""
            self.SignUp_username=""
            self.SignUp_email=""
            return [rx.clear_local_storage(), rx.window_alert("Account deletion was successful!"), rx.redirect("/login")]
        else:
            return [rx.window_alert("An error occured while deleting your account")]
            

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
                
                return [rx.set_local_storage("accounts",str({"username":self.username,"email":self.email,"password":self.password})),rx.window_alert(f"Login for {self.username} successful!"), rx.redirect("/dashboard")]
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

    def page_load(self, storage):
        if self.username=="":
            try:
                if storage==None:
                    pass
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
                        return rx.clear_local_storage()
            except Exception as e:
                print(e)
        else:
            pass

    def login_page_load(self, storage):
        self.page_load(storage)
        if self.username=="":
            pass
        else:
            return rx.redirect("/dashboard")
        
    dashboard_gui_to_edit_username=False

    def switch_dashboard_gui_to_edit_username(self):
        self.dashboard_gui_to_edit_username= not self.dashboard_gui_to_edit_username 

    def dashboard_username_editor(self, new_username):
        self.switch_dashboard_gui_to_edit_username()
        if func.edit_username(new_username, self.email):
            self.username=new_username
            return rx.window_alert("Changes were applied successfully")
        else:
            return rx.window_alert("An error occured")

    def dashboard_load(self, local_storage):
        self.page_load(local_storage)
        if self.username:
            pass
        else:
            return rx.redirect("/login")

    def switch_enable_change_pfp_gui(self):
        self.enable_change_pfp_gui = not self.enable_change_pfp_gui

    @rx.var
    def pfp_exists(self):
        return os.path.exists(os.path.exists(f"assets\\pfps\\{self.email}"))

    mobile_homepage_drawer=False
    def switch_mobile_homepage_drawer(self):
        self.mobile_homepage_drawer=not self.mobile_homepage_drawer

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
                            rx.password(placeholder="Enter a password", on_blur=State.set_SignUp_password),
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
        OnLoadHack.create(on_load=lambda: State.login_page_load(rx.get_local_storage("accounts"))),
        width="100%",
        bg="BLACK",
    )


def navbar():
    return rx.hstack(
        rx.box(width="21vh"),
        rx.image(src="/logo.png", width="7.875vh", height="7.875vh", on_click=rx.redirect("/")),
        rx.spacer(),
        rx.hstack(
            rx.menu(
                rx.menu_button(
                    rx.heading(
                        "Contact", 
                        color=State.navbar_contact_color, 
                        font_size="2.1vh"
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
        OnLoadHack.create(on_load=lambda: State.page_load(rx.get_local_storage("accounts"))),
        width="100%",
        bg="black",
        position="fixed",
        height="10.4vh"
    )


def index():
    return rx.box(
        rx.tablet_and_desktop( 
            rx.vstack(
                navbar(),
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
                            rx.span("Welcome to ", color="WHITE"),
                            rx.span("anga", color="#ffcccb"),
                            rx.span(".", color="#90EE90"),
                            rx.span("pro", color="#ADD8E6"),
                            font_size="4vh"
                        )
                    ),
                    rx.cond(
                        State.username,
                        rx.button(
                            rx.span("Go to panel ", on_click=rx.redirect("/dashboard")),
                            rx.span(rx.icon(tag="external_link")),
                            bg="GREEN",
                            color="WHITE",
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
                    bg="#0E0019",
                    width="100%",
                    height="90vh",
                    spacing="2.1vh"
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
                    rx.heading("Some interesting statistics about this website:", color="WHITE"),
                    rx.text("This data is live updated, refresh this page to see the numbers change!", color="WHITE"),
                    rx.hstack(
                        rx.vstack(
                            rx.chart(
                                rx.line(
                                    data=State.loads_per_day,
                                ),
                            ),
                            rx.heading(rx.span("Number of times this page was loaded today: "), rx.span(State.loads_today), font_size="lg"),
                            bg="#00fff5",
                            border_radius="5px",
                            spacing="0px",
                            border_width="5px",
                            border_color="#00fff5"
                        ),
                    ),
                    height="60vh",
                    width="100%",
                    bg="#001918",
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
        ),
        rx.mobile_only(
            rx.vstack(
                rx.hstack(
                    rx.box(width="2%"),
                    rx.icon(tag="hamburger", color="WHITE", font_size="3xl", on_click=State.switch_mobile_homepage_drawer),
                    rx.spacer(),
                    rx.image(src="/logo.png", height="13vh"),
                    bg="BLACK",
                    height="12vh",
                    width="100%"
                ),
                rx.vstack(
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
                    height="60vh"
                ),
                spacing="0px"
            )
        )
    )

def user_profile_pic(side=100):
    return rx.cond(
        State.pfp_exists,
        rx.image(src=f"/pfps/{State.email}"),
        rx.avatar(name=State.username, border_radius=f"{side/2}px", height=f"{side}px", width=f"{side}px")
    )

def dashboard():
    return rx.hstack(
#-------------------------------------------------------------------------------------------------------------------------------------------------
#                                                              SIDEBAR
#-------------------------------------------------------------------------------------------------------------------------------------------------
        rx.vstack(
            rx.button(
                rx.span(
                    rx.image(src="/account.png"), 
                    width="20px", 
                    height="20px", 
                    style={"margin-top": "3px"}
                    ), 
                rx.span("", width="20px"), 
                rx.span("Manage Account"), 
                rx.spacer(), 
                color="WHITE", 
                font_size="20px", 
                bg="#0E0019", 
                width="100%"
                ),
            rx.button(
                rx.span(
                    rx.image(src="/file_host.png"), 
                    width="20px", 
                    height="20px", 
                    style={"margin-top": "3px"}
                    ), 
                rx.span("", width="20px"), 
                rx.span("File Hosting"), 
                rx.spacer(), 
                color="WHITE", 
                font_size="20px", 
                bg="#0E0019", 
                width="100%"
                ),
            rx.button(
                rx.span(
                    rx.image(src="/support.png"), 
                    width="20px", 
                    height="20px", 
                    style={"margin-top": "3px"}
                    ), 
                rx.span("", width="20px"), 
                rx.span("Support"), 
                rx.spacer(), 
                color="WHITE", 
                font_size="20px", 
                bg="#0E0019", 
                width="100%"
                ),
            rx.button(
                rx.span(
                    rx.icon(tag="delete"), 
                    style={"margin-top": "-5px"}
                    ), 
                rx.span(
                    "", 
                    width="20px"
                    ), 
                rx.span("Delete Account"), 
                rx.spacer(), 
                color="RED", 
                font_size="20px", 
                bg="#0E0019", 
                width="100%",
                on_click=State.dashboard_delete_account
                ),
            width="15%",
            height="100vh",
            bg="#0E0019",
            position="fixed",
        ),
#-------------------------------------------------------------------------------------------------------------------------------------------------
#                                                              TOPBAR
#-------------------------------------------------------------------------------------------------------------------------------------------------
        rx.vstack(
            rx.hstack(
                rx.box(width="6%"),
                rx.image(src="/logo.png", height="6vh", width="auto"),
                rx.spacer(),
                bg="#000d19",
                height="6vh",
                width="100%"
            ),
            height="100vh", 
            width="85%", 
            bg="BLACK", 
            style={"margin-left":"15%"}
            ),

        OnLoadHack.create(on_load=lambda: State.dashboard_load(rx.get_local_storage("accounts")))
    )

# Add state and page to the app.
app = rx.App()
app.add_page(login, title="Login Page - anga.pro", description="Website is under construction")
app.add_page(dashboard, title="Dashboard - anga.pro", description="Website is under construction")
app.add_page(index, title="Home - anga.pro", description="Website is under construction", on_load=State.homepage_load)
app.compile()
