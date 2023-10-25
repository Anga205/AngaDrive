import reflex as rx
import random, time, bcrypt, asyncio, threading, os
import website.library as func
import website.TPU_cmds as TPU

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

    @rx.var
    def loads_today(self):
        return list(func.calls_per_day(func.get_timestamps()).values())[-1]

    global startup_time
    uptime=func.convert_to_time_value(time.time()-startup_time)


    @rx.var
    def loads_per_day(self) -> list[int]:
        calls=list(func.calls_per_day(func.get_timestamps()).values())
        timestamps=list(func.calls_per_day(func.get_timestamps()).keys())
        return rx.data(
            "line",
            x=timestamps,
            y=calls,
        )

    def homepage_load(self):
        func.insert_timestamp()

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
        insertion = func.new_user_signup(self.SignUp_username, self.SignUp_email, bcrypt.hashpw(self.SignUp_password.encode('utf-8'), bcrypt.gensalt()).hex())
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
            login_data=func.login_user(self.email, self.password)
            if type(login_data)==type({}):
                self.username=login_data['username']
                self.email=login_data['email']
                return [rx.set_local_storage("accounts",str({"username":self.username,"email":self.email,"password":self.password})), rx.redirect("/dashboard")]
            else:
                print(login_data)
                return rx.window_alert(login_data)

    @rx.var
    def welcome_message(self):
        if self.username=="":
            return "Welcome to anga.pro"
        else:
            return f"Welcome back, {self.username}"
    
    random_light_color=random.choice(["#ffcccb","#90EE90","#ADD8E6"])

    def page_load(self, storage, TPU_var):
        if self.username=="":
            try:
                if storage==None and TPU_var==None:
                    pass
                elif TPU_var==None:
                    login_data=eval(storage)
                    response=func.login_user(login_data["email"],login_data['password'])
                    if not type(response)==type(""):
                        self.username=response['username']
                        self.email=login_data["email"]
                        self.password=login_data["password"]
                        rx.set_local_storage("accounts",{"username":self.username,"email":self.email,"password":self.password})
                        print(f"[{time.ctime(time.time())}] {self.username} logged in thru session")
                    else:
                        print(f"[{time.ctime(time.time())}] Login with details '{login_data['email']}', '{login_data['password']}' failed with reason {response}")
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

    timer_started=False

    async def tick(self):
        try:
            if self.timer_started:
                await asyncio.sleep(0.3)
                self.uptime=func.convert_to_time_value(time.time()-startup_time)
                return State.tick
        except KeyboardInterrupt:
            exit()

    def index_page_load(self, local_storage, TPU_storage):
        threading.Thread(target= lambda: self.page_load(local_storage, TPU_storage)).start()
#        self.timer_started=True
#        return State.tick

    def start_timer(self):
        if not self.timer_started:
            self.timer_started=True
            return State.tick
    
    def stop_timer(self):
        if self.timer_started:
            self.timer_started=False

    def unload_homepage(self):
        self.stop_timer()
    

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
    def turn_on_mobile_homepage_drawer(self):
        self.mobile_homepage_drawer=True

    def turn_off_mobile_homepage_drawer(self):
        self.mobile_homepage_drawer=False

    enable_username_editor_in_dashboard=False
    def switch_username_editor_in_dashboard(self):
        if not self.TPU_verified:
            self.enable_username_editor_in_dashboard = not self.enable_username_editor_in_dashboard
        else:
            return rx.window_alert("TPU accounts can only be renamed thru TPU dashboard")


    def change_username_thru_dashboard(self, new_username):
        if new_username.strip()==self.username.strip():
            func.edit_username(new_username, self.email)
        else:
            self.username=new_username
            try:
                func.edit_username(new_username, self.email)
            except:
                pass
            self.switch_username_editor_in_dashboard()
            return rx.window_alert("Username was changed successfully")

    pfp_exists=False

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

    if TPU_verified:
        data=TPU.verifier(TPU_verified)
        username=data['username']
        email=data['email']

    @rx.var
    def is_admin(self):
        if self.email=="":
            return False
        elif self.email.split("@")[1]=="angadbhalla.com" and self.TPU_verified:
            return True
        else:
            return False


    dashboard_page="account"

    def set_dashboard_to_file_hosting(self):
        if self.dashboard_page=="hosting":
            pass
        else:
            self.dashboard_page="hosting"
    
    def set_dashboard_to_support_page(self):
        if self.dashboard_page=="support":
            pass
        else:
            self.dashboard_page="support"

    @rx.var
    def dashboard_is_hosting_page(self):
        return self.dashboard_page=="hosting" 
    
    @rx.var
    def dashboard_is_support_page(self):
        return self.dashboard_page=="support" 

    def set_dashboard_to_account_manager(self):
        if self.dashboard_page=="account":
            pass
        else:
            self.dashboard_page="account"

    @rx.var 
    def dashboard_is_account_page(self):
        return self.dashboard_page=="account"
    

    enable_popup_to_upload=False
    def turn_off_popup_to_upload(self):
        self.enable_popup_to_upload=False
    def turn_on_popup_to_upload(self):
        self.enable_popup_to_upload=True


    img: list[str]

    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            new_file_name=func.obfuscate_filename(file.filename)
            outfile=os.path.join("assets","i",new_file_name)

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            func.add_file(new_file_name, func.get_token_from_username(self.username), time.time(), file.filename)

            # Update the img var.
            self.img.append(file.filename)
            print(f"handled {file.filename}")
        self.enable_popup_to_upload=False


    @rx.var
    def files_associated_with_account(self) -> list[str]:
        return func.get_files(func.get_token_from_username(self.username))
    
    @rx.var
    def bool_files_associated_with_account(self) -> bool:
        return bool(self.files_associated_with_account)
    
    @rx.var
    def new_file_names_associated_with_account(self) -> list[str]:
#        print(func.get_new_file_names(func.get_token_from_username(self.username)))
        return func.get_new_file_names(func.get_token_from_username(self.username))
    
    @rx.var
    def file_data_list_associated_with_account(self) -> list[list[str]]:
        data_list=func.get_file_info_from_account_token(func.get_token_from_username(self.username))
        final_list=[]
        for i in data_list:
            final_list.append(i+[f"{self.get_headers().get('origin')}/i/{i[0]}"])
        return final_list

    @rx.var
    def file_sizes_associated_with_account(self) -> list[str]:
        return func.get_file_sizes(func.get_token_from_username(self.username))

    def delete_file(self, file_name):
        file_name=file_name.lstrip("https://i.anga.pro/")
        func.delete_file(file_name)
        try:
            os.remove(os.path.join("assets","i",file_name))
        except Exception as e:
            print(e)
        return rx.window_alert(f"{file_name} removed")
    