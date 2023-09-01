"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx
import website.library as func
import random, os, time, bcrypt, asyncio
import website.TPU_cmds as TPU
import website.updating_components as updating_components

startup_time=time.time()

class State(rx.State):
    username=""
    email = ""
    password = ""
    signup_email_color_bg="WHITE"
    email_color_bg="WHITE"
    SignUpEnabled = False
    SignUp_username=""
    SignUp_email=""
    SignUp_password=""
    TPU_verified=False
    navbar_contact_color="WHITE"

    open_time=0
    @rx.var
    def uptime(self):
        if self.open_time==0:
            self.open_time=time.time()
            global startup_time
            round(time.time()-startup_time)
        else:
            time.sleep(0.5)
            self.uptime+1
    
    @rx.var
    def loads_today(self):
        return list(func.calls_per_day(func.get_timestamps()).values())[-1]


    @rx.var
    def loads_per_day(self) -> list[int]:
        calls=list(func.calls_per_day(func.get_timestamps()).values())
        timestamps=list(func.calls_per_day(func.get_timestamps()).keys())
        return rx.data(
            "line",
            x=timestamps,
            y=calls,
        )
    

    def start_updater(self):
        asyncio.sleep(1)
        return State.start_updater()

    def homepage_load(self):
        func.insert_timestamp()
        self.start_updater()

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
        print("Checkpoint 1")
        insertion = func.new_user_signup(self.SignUp_username, self.SignUp_email, bcrypt.hashpw(self.SignUp_password.encode('utf-8'), bcrypt.gensalt()).hex())
        print("Checkpoint 2")
        if not insertion:
            self.username, self.email, self.password=self.SignUp_username, self.SignUp_email, self.SignUp_password
            print(f"[{time.ctime(time.time())}] {self.username} just registered a new account!")
            return [rx.redirect("/dashboard"), rx.set_local_storage("accounts",str({"username":self.username,"email":self.email,"password":self.password})), rx.window_alert("Signup Successful!")]
        else:
            return rx.window_alert(insertion)

    def logout(self):
        self.username=""
        self.email=""
        self.password=""
        self.SignUp_password=""
        self.SignUp_username=""
        self.SignUp_email=""
        self.TPU_verified=False
        return rx.clear_local_storage()
    
    def dashboard_delete_account(self):
        if func.delete_account(self.email):
            self.username=""
            self.email=""
            self.password=""
            self.SignUp_password=""
            self.SignUp_username=""
            self.SignUp_email=""
            return [rx.clear_local_storage(), rx.redirect("/login"), rx.window_alert("Account deletion was successful!")]
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
            login_data=func.login_user(self.email, bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()))
            if type(login_data)==type({}):
                self.username=login_data['username']
                self.email=login_data['email']
                return [rx.set_local_storage("accounts",str({"username":self.username,"email":self.email,"password":bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())})), rx.redirect("/dashboard")]
            else:
                print(login_data)
                return rx.window_alert(login_data)

    @rx.var
    def welcome_message(self):
        if self.username=="":
            return "Welcome to anga.pro"
        else:
            return f"Welcome back, {self.username}"
    
    @rx.var
    def random_light_color(self):
        return random.choice(["#ffcccb","#90EE90","#ADD8E6"])

    def page_load(self, storage, TPU_var):
        if self.username=="":
            try:
                if storage==None and TPU_var==None:
                    pass
                elif TPU_var==None:
                    login_data=eval(storage)
                    print(login_data)
                    print(type(login_data['password']))
                    response=func.login_user(login_data["email"],bcrypt.hashpw(str(login_data['password']).encode('utf-8'), bcrypt.gensalt()))
                    print("a")
                    if not type(response)==type(""):
                        print(f"response: {response}")
                        self.username=response['username']
                        self.email=login_data["email"]
                        self.password=login_data["password"]
                        rx.set_local_storage("accounts",{"username":self.username,"email":self.email,"password":self.password})
                        print(f"[{time.ctime(time.time())}] {self.username} logged in thru session")
                    else:
                        print(f"Login with details '{login_data['email']}', '{login_data['password']}' failed with reason {response}")
                        return rx.clear_local_storage()
                elif storage==None:
                    login_info=TPU.verifier(TPU_var)
                    if login_info:
                        self.TPU_verified=TPU_var
                        self.username=login_info['username']
                        self.email=login_info['email']
                    else:
                        return rx.clear_local_storage()
            except Exception as e:
                print(e)
        else:
            pass

    def login_page_load(self, storage, TPU_token):
        self.page_load(storage, TPU_token)
        if self.username=="":
            pass
        else:
            return rx.redirect("/dashboard")
    
    def dashboard_load(self, account_var, TPU_var):
        self.page_load(account_var, TPU_var)
        if self.username:
            pass
        else:
            return rx.redirect("/login")

    mobile_homepage_drawer=False
    def switch_mobile_homepage_drawer(self):
        self.mobile_homepage_drawer=not self.mobile_homepage_drawer

    enable_username_editor_in_dashboard=False
    def switch_username_editor_in_dashboard(self):
        self.enable_username_editor_in_dashboard = not self.enable_username_editor_in_dashboard

    def change_username_thru_dashboard(self, new_username):
        if new_username.strip()==self.username.strip():
            pass
        else:
            self.username=new_username
            func.edit_username(new_username, self.email)
            self.switch_username_editor_in_dashboard()
            return rx.window_alert("Username was changed successfully")
    @rx.var
    def pfp_exists(self):
        os.path.exists(f"assets/pfps/{self.email}")

    def TPU_verify(self):
        data=self.get_query_params().get("code",None)
        login_info=TPU.verifier(data)
        token=data
        if login_info:
            tpu_database_error=func.TPU_signin(login_info['id'], login_info['email'], login_info['username'], data, login_info['avatar'])
            if tpu_database_error:
                return [rx.redirect("/login"), rx.window_alert(tpu_database_error)]
            self.TPU_verified=data
            self.username=login_info['username']
            self.email=login_info['email']
            print(f"{self.username} logged in thru TPU")
            return [rx.redirect('/dashboard'), rx.set_local_storage("TPU",token)]
        else:
            return [rx.redirect("/login"), rx.window_alert("login with TPU failed")]
    
    @rx.var
    def TPU_login_info(self):
        if self.TPU_verified:
            data=TPU.verifier(self.TPU_verified)
            self.username=data['username']
            self.email=data['email']

    @rx.var
    def is_admin(self):
        if self.email=="":
            return False
        elif self.email.split("@")[1]=="angadbhalla.com" and self.TPU_verified:
            return True
        else:
            return False


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
    on_mount=lambda: State.login_page_load(rx.get_local_storage("accounts"), rx.get_local_storage("TPU"))
)

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
                    width="100%",
                    bg="black",
                    position="fixed",
                    height="10.4vh"
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
                            rx.span("Welcome to ", color="WHITE"),
                            rx.span("anga", color="#ffcccb"),
                            rx.span(".", color="#90EE90"),
                            rx.span("pro", color="#ADD8E6"),
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
                    rx.heading("Some interesting statistics about this website:", color="WHITE", font_size="3.5vh"),
                    rx.text("This data is live updated, refresh this page to see the numbers change!", color="WHITE", font_size="1.5vh"),
                    rx.hstack(
                        rx.vstack(
                            rx.box(
                                rx.chart(
                                    rx.line(
                                        data=State.loads_per_day,
                                        width="100vh"
                                    ),
                                )
                            ),
                            rx.heading(rx.span("Number of times this page was loaded today: "), rx.span(State.loads_today), font_size="2vh", bg="#00fff5"),
                            bg="#00fff5",
                            border_radius="5px",
                            spacing="0vh",
                            border_width="5px",
                            border_color="#00fff5",
                            height="36vh"
                        ),
                        rx.vstack(
                            rx.heading("Time since last update (to this website):", font_size="1.7vh"),
                            rx.heading(State.uptime, font_size="2.4vh"),
                            rx.heading(rx.span("You can "), rx.span("click here"), rx.span(" to see details about updates"), font_size="1.7vh"),
                            width="36vh",
                            height="36vh",
                            bg="#00fff5"
                        ),
                        spacing="10vh"
                    ),
                    height="60vh",
                    width="100%",
                    bg="#001918",
                    spacing="0.3vh"
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
                    rx.icon(tag="hamburger", color="WHITE", font_size="3xl", on_click=State.switch_mobile_homepage_drawer),
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
                                                    rx.text("Discord", on_click=rx.redirect("https://discord.gg/DgxppCZnJb"), color="GRAY"),
                                                    rx.text("Instagram", on_click=rx.redirect("https://instagram.com/_anga205"), color="GRAY"),
                                                    rx.text("Threads", on_click=rx.redirect("https://threads.net/@_anga205"), color="GRAY"),
                                                    rx.text("𝕏.com", on_click=rx.redirect("https://x.com/_anga205"), color="GRAY"),
                                                    rx.text("Email", on_click=rx.redirect("mailto:support@anga.pro"), color="GRAY"),
                                                    rx.text("GitHub", on_click=rx.redirect("https://github.com/Anga205"), color="GRAY"),
                                                    rx.text("Telegram", on_click=rx.redirect("https://t.me/Anga205"), color="GRAY"),
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
                                            "Close", on_click=State.switch_mobile_homepage_drawer
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
                            rx.span("Welcome to ", color="WHITE"),
                            rx.span("anga", color="#ffcccb"),
                            rx.span(".", color="#90EE90"),
                            rx.span("pro", color="#ADD8E6"),
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
                    width="100%"
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
                        rx.box(
                            rx.chart(
                                rx.line(
                                    data=State.loads_per_day,
                                ),
                            ),
                        rx.box(
                            rx.heading(rx.span("Number of times this page was loaded today: "), rx.span(State.loads_today), font_size="1.7vh", style={"text-align":"center"})
                            ),
                        bg="#00fff5",
                        border_radius="1vh",
                        width="90%"
                        )
                    ),
                    rx.box(height="3vh"),
                    bg="#001918"
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
        on_mount=lambda: State.page_load(rx.get_local_storage("accounts"), rx.get_local_storage("TPU")),
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
        rx.heading("Site-Wide Announcements", color="WHITE", font_size="3vh"),
        rx.divider(border_color="WHITE"),
        rx.text("None for now"),
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
    announcements_tab(),
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
                width="100%",
                height="4.5vh",
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
                _hover={"bg":"BLACK"}
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
                _hover={"bg":"BLACK"}
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
                position="fixed"
            ),
            rx.box(height="6vh"),
            account_manager(),
            height="100vh", 
            width="85%", 
            bg="BLACK", 
            style={"margin-left":"15%"}
            ),
        on_mount=lambda: State.dashboard_load(rx.get_local_storage("accounts"),rx.get_local_storage("TPU")),
        spacing="0px",
    )

def TPU_login():
    return rx.box(
        rx.text("Please wait for a few seconds for your TPU login to be verified....."),
    )

# Add state and page to the app.
app = rx.App()
app.add_page(login, title="Login Page - anga.pro", description="Website is under construction")
app.add_page(dashboard, title="Dashboard - anga.pro", description="Website is under construction")
app.add_page(index, title="Home - anga.pro", description="Website is under construction", on_load=State.homepage_load)
app.add_page(TPU_login, title="TPU - anga.pro", description="Temporary link", route="/tpulogin", on_load=State.TPU_verify)
app.compile()
