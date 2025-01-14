import customtkinter as ct
import ctypes, PIL
import json
import uuid
import requests
from CTkMessagebox import CTkMessagebox as msg
import subprocess, sys, string, random, os
import platform
from pathlib import Path
import psutil
import minecraft_launcher_lib

usr_accnt = str(Path.home()).replace("\\", "/").split("/")[-1]
mc_dir = minecraft_launcher_lib.utils.get_minecraft_directory()
latest_version = minecraft_launcher_lib.utils.get_latest_version()
latest_release = latest_version["release"]
svmem = psutil.virtual_memory()
currn_dir = os.getcwd()
java_home = os.getenv("JAVA_HOME")+r"\\bin\\java.exe"
java_home = java_home.replace("\\", "/")
try: 
    java_loc = os.getenv('JAVA_HOME').replace("\\", "/")+str(r"\\bin\\java.exe")
except:
    print("Java is not installed, or it is not installed to the PATH (system environment variable). Please (re)install Java and try again.")
    os.system("pause")
    sys.exit()
def get_size(bytes, suffix="B"):
    """ 
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

latestRelease = str("vanilla release " + latest_release)

settings = {
                "accessToken": None,
                "clientToken": None,
                "User-info" : [
                    {
                        "username": None,
                        "AUTH_TYPE": None,
                        "UUID": None,
                        "cracked_password": None
                    }
                ],
                "PC-info" : [
                    {
                        "OS": platform.platform(),
                        "Total-Ram": f"{get_size(svmem.total)}",
                    }
                ],
                "Microsoft-settings" : [
                    {
                        "refresh_token": None
                    }
                ],
                "Minecraft-home" : mc_dir,
                "selected-version": latestRelease,
                "selected-instance": "Latest Release",
                "settings" : [
                    {
                        "allocated_ram" : 3000,
                        "jvm-args": None,
                        "executablePath": f"{java_loc}",
                        "ramlimiterExceptionBypassed": False,
                        "ramlimiterExceptionBypassedSelected": False,
                        "verbose": True
                    }
                ],
            }

launcher_profiles = {
    "pinned-icons": [
        {
            "pinned1": None,
            "pinned2": None,
            "pinned3": None,
            "pinned4": None,
            "pinned5": None,
            "pinned6": None,
            "pinned7": None,
            "pinned8": None,
            "pinned9": None
        }
    ],
    "pinned-instances": [
        {
            "pinned1": None,
            "pinned2": None,
            "pinned3": None,
            "pinned4": None,
            "pinned5": None,
            "pinned6": None,
            "pinned7": None,
            "pinned8": None,
            "pinned9": None
        }
    ],
    "icons": [
        {
            "icon1": "release",
            "icon2": "snapshot",
            "icon3": "iron_block",
            "icon4": None,
            "icon5": None,
            "icon6": None,
            "icon7": None,
            "icon8": None,
            "icon9": None,
            "icon10": None,
            "icon11": None,
            "icon12": None,
            "icon13": None,
            "icon14": None,
            "icon15": None,
            "icon16": None,
            "icon17": None
        }
    ],
    "all-instances": [
        {}
    ]
}
if not os.path.exists(r"{}/settings.json".format(currn_dir)):
    with open("settings.json", "w") as js_set:
        json.dump(settings, js_set, indent=4)
        js_set.close()
else:
    pass
if not os.path.exists(r"launcherProfiles.json".format(mc_dir)):
     with open("launcherProfiles.json", "w") as js_set:
        json.dump(launcher_profiles, js_set, indent=4)
        js_set.close()
else:
    pass
with open("settings.json", "r") as js_read:
    s = js_read.read()
    s = s.replace('\t','')  #Trailing commas in dict cause file read problems, these lines will fix it.
    s = s.replace('\n','')  #Found this on stackoverflow.
    s = s.replace(',}','}')
    s = s.replace(',]',']')
    data = json.loads(s)
    #print(json.dumps(data, indent=4,))

os_name = data["PC-info"][0]["OS"]
mc_home = data["Minecraft-home"]
username = data["User-info"][0]["username"]
uid = data["User-info"][0]["UUID"]
accessToken = data["accessToken"]
mc_dir = data["Minecraft-home"]
auth_type = data["User-info"][0]["AUTH_TYPE"]
selected_ver = data["selected-version"]
allocated_ram = data["settings"][0]["allocated_ram"]
jvm_args = data["settings"][0]["jvm-args"]
ramlimiterExceptionBypassed = data["settings"][0]["ramlimiterExceptionBypassed"]
ramlimiterExceptionBypassedSelected = data["settings"][0]["ramlimiterExceptionBypassedSelected"]
verbose = data["settings"][0]["verbose"]
refresh_token = data["Microsoft-settings"][0]["refresh_token"]

ct.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ct.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
myappid = u'vpun215.argon.release.1.0' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
class WelcomeToArgon(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x600")
        self.wm_iconbitmap("img/icon.ico")
        self.resizable(False, False)
        self.title("Welcome to Argon")
        self.background_image = ct.CTkImage(PIL.Image.open("img/welcome/background.jpg"), size=(1024, 600))
        self.background_label = ct.CTkLabel(self, image=self.background_image, text="")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.main_frame = ct.CTkFrame(self, bg_color="transparent", width=500, height=400, fg_color="#1f1f1f", corner_radius=0)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.logo_img = ct.CTkImage(PIL.Image.open("img/logo.png"), size=(70, 70))
        self.logo_label = ct.CTkLabel(self.main_frame, image=self.logo_img, text="")
        self.logo_label.place(relx=0.20, rely=0.15, anchor="center")
        self.logo_text = ct.CTkLabel(self.main_frame, text="Argon Launcher", font=("Inter", 35, "bold"), bg_color="transparent", fg_color="transparent", text_color="white")
        self.logo_text.place(relx=0.57, rely=0.15, anchor="center")
        self.instruction = ct.CTkLabel(self.main_frame, text="Choose Account Type", font=("Inter", 15, "bold"), bg_color="transparent", fg_color="transparent", text_color="#b3b3b3")
        self.instruction.place(relx=0.5, rely=0.30, anchor="center")
        self.radio_label = ct.CTkLabel(self.main_frame, text="Microsoft", font=("Inter", 15), bg_color="transparent", fg_color="transparent", text_color="white")
        self.radio_label.place(relx=0.3, rely=0.38, anchor="center")
        self.radio_label2 = ct.CTkLabel(self.main_frame, text="Ely.by", font=("Inter", 15), bg_color="transparent", fg_color="transparent", text_color="white")
        self.radio_label2.place(relx=0.5, rely=0.38, anchor="center")
        self.radio_label3 = ct.CTkLabel(self.main_frame, text="Offline", font=("Inter", 15), bg_color="transparent", fg_color="transparent", text_color="white")
        self.radio_label3.place(relx=0.7, rely=0.38, anchor="center")
        def radiobutton_event():
            print("radiobutton toggled, current value:", self.radio_var.get())
            if self.radio_var.get() == 1:
                self.elyby_frame.place_forget()
                self.offline_frame.place_forget()
                self.microsoft_frame.place(relx=0.5, rely=0.75, anchor="center")
            elif self.radio_var.get() == 2:
                self.microsoft_frame.place_forget()
                self.offline_frame.place_forget()
                self.elyby_frame.place(relx=0.5, rely=0.75, anchor="center")
            elif self.radio_var.get() == 3:
                self.microsoft_frame.place_forget()
                self.elyby_frame.place_forget()
                self.offline_frame.place(relx=0.5, rely=0.75, anchor="center")
            else:
                self.microsoft_frame.place_forget()
                self.elyby_frame.place_forget()
                self.offline_frame.place_forget()
        self.radio_var = ct.IntVar(value=0)
        self.radiobutton_1 = ct.CTkRadioButton(self.main_frame, text="",
                                             command=radiobutton_event, variable=self.radio_var, value=1)
        self.radiobutton_2 = ct.CTkRadioButton(self.main_frame, text="",command=radiobutton_event, variable=self.radio_var, value=2)
        self.radiobutton_3 = ct.CTkRadioButton(self.main_frame, text="",command=radiobutton_event, variable=self.radio_var, value=3)
        self.radiobutton_1.place(relx=0.38, rely=0.48, anchor="center")
        self.radiobutton_2.place(relx=0.58, rely=0.48, anchor="center")
        self.radiobutton_3.place(relx=0.78, rely=0.48, anchor="center")
        self.microsoft_frame = ct.CTkFrame(self.main_frame, bg_color="transparent", width=450, height=155, fg_color="#2b2b2b", corner_radius=8)
        self.elyby_frame = ct.CTkFrame(self.main_frame, bg_color="transparent", width=450, height=155, fg_color="#2b2b2b", corner_radius=8)
        self.offline_frame = ct.CTkFrame(self.main_frame, bg_color="transparent", width=450, height=155, fg_color="#2b2b2b", corner_radius=8)
        self.ms_login_label = ct.CTkLabel(self.microsoft_frame, text="Login to your Microsoft Account", font=("Inter", 15, "bold"), bg_color="transparent", fg_color="transparent", text_color="white")
        self.ms_login_label.place(relx=0.5, rely=0.3, anchor="center")
        self.ms_login_btn  = ct.CTkButton(self.microsoft_frame, text="Login",  command=self.ms_login, bg_color="transparent", corner_radius=5)
        self.ms_login_btn.place(relx=0.5, rely=0.65, anchor="center")
        self.elyby_login_label = ct.CTkLabel(self.elyby_frame, text="Login to your Ely.by Account", font=("Inter", 15, "bold"), bg_color="transparent", fg_color="transparent", text_color="white")
        self.elyby_login_label.place(relx=0.5, rely=0.15, anchor="center")
        self.elyby_login_username = ct.CTkEntry(self.elyby_frame, font=("Inter", 15), bg_color="transparent", fg_color="#3b3b3b", corner_radius=5, placeholder_text="Username")
        self.elyby_login_username.place(relx=0.5, rely=0.4, anchor="center")
        self.elyby_login_password = ct.CTkEntry(self.elyby_frame, font=("Inter", 15), bg_color="transparent", fg_color="#3b3b3b", corner_radius=5, placeholder_text="Password", show="•")
        self.elyby_login_password.place(relx=0.5, rely=0.6, anchor="center")
        self.elyby_login_btn = ct.CTkButton(self.elyby_frame, text="Login",  command=self.ely_authenticate, bg_color="transparent", corner_radius=5)
        self.elyby_login_btn.place(relx=0.5, rely=0.82, anchor="center")
        self.offline_login_label = ct.CTkLabel(self.offline_frame, text="Login to an Offline Account", font=("Inter", 15, "bold"), bg_color="transparent", fg_color="transparent", text_color="white")
        self.offline_login_label.place(relx=0.5, rely=0.15, anchor="center")
        self.offline_login_username = ct.CTkEntry(self.offline_frame, font=("Inter", 15), bg_color="transparent", fg_color="#3b3b3b", corner_radius=5, placeholder_text="Username")
        self.offline_login_username.place(relx=0.5, rely=0.4, anchor="center")
        self.offline_login_btn = ct.CTkButton(self.offline_frame, text="Login",  command=self.offline_login, bg_color="transparent", corner_radius=5)
        self.offline_login_btn.place(relx=0.5, rely=0.82, anchor="center")


    def ms_login(self):
        from microsoftAuth import Authenticate
        Authenticate()


    def ely_authenticate(self):
        self.usr = self.elyby_login_username.get()
        self.pwd = self.elyby_login_password.get()
        self.client_token = str(uuid.uuid4())
        self.acc_data ={
            "username": self.usr,
            "password": self.pwd,
            "clientToken" : self.client_token,
            "requestUser" : True
        }
        self.r = requests.get(f"https://authserver.ely.by/api/users/profiles/minecraft/{self.usr}")
        if self.r.status_code == 200:
            self.r1 = requests.post(f"https://authserver.ely.by/auth/authenticate", data=self.acc_data)
            if self.r1.status_code == 200:
                print("Status Code: 200")
                print("User found.")
                self.accessToken = self.r1.json()["accessToken"]
                self.uid = self.r1.json()["user"]["id"]
                self.username = self.r1.json()["user"]["username"]
                print(f"User: {self.username} Authenticated.")
                data["User-info"][0]["username"] = self.username
                data["User-info"][0]["AUTH_TYPE"] = "ElyBy"
                data["User-info"][0]["cracked_password"] = self.pwd
                data["User-info"][0]["UUID"] = self.uid
                data["clientToken"] = self.client_token
                data["accessToken"] = self.accessToken

                with open("settings.json", "w") as f:
                    json.dump(data, f, indent=4 )
                    f.close()
                msg(title="Success", message=f"User: {self.username} Authenticated.", icon="check", option_1="Ok")
                self.exit_to_argon()
            elif self.r1.status_code == 404:
                msg(title="Error", message=f"Data entered is either incomplete or account is secured with Oauth2. Error code: {self.r1.status_code}", icon="cancel")
                print("Data entered is either incomplete or account is secured with Oauth2")
            else:
                print(f"Error Code: {self.r1.status_code}")
                msg(title="Error", message=f"An error occurred while authenticating. Error code: {self.r1.status_code}", icon="cancel")
        elif self.r.status_code == 404:
            print("[ERROR] 404", "User does not exist.")
            msg(title="Error", message=f"The specified user does not exist. Error code: {self.r.status_code}", icon="cancel")
        else:
            print(f"Error Code: {self.r.status_code}")
            msg(title="Error", message=f"Data entered is either incomplete or an error occurred while authenticating. Error code: {self.r.status_code}", icon="cancel")


    def offline_login(self):
        self.usr = self.offline_login_username.get()
        data["User-info"][0]["username"] = self.usr
        data["User-info"][0]["AUTH_TYPE"] = "Offline"
        data["User-info"][0]["cracked_password"] = self.generate_cracked_password()
        self.uuid = uuid.uuid4().hex
        data["User-info"][0]["UUID"] = self.uuid
        print(f"User: {self.usr} Logged In.")
        with open("settings.json", "w") as f:
            json.dump(data, f, indent=4 )
            f.close()
        popup = msg(title="Success", message=f"User: {self.usr} Logged In.", icon="check", option_1="Ok")
        if popup.get()=="Ok":
            self.exit_to_argon()
        else:
            pass


    def exit_to_argon(self):
        self.destroy()
        os.system("python main.py")
        sys.exit()

    def generate_cracked_password(self):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(10))
        print("Cracked password generated:", result_str)
        return result_str

    def generate_cracked_uuid(self):
        if data["User-info"][0]["UUID"] == None:
            self.uuid = uuid.uuid4().hex
            with open("settings.json", "w") as js_set:
                        json.dump(data, js_set, indent=4)
                        js_set.close()
        elif data["User-info"][0]["UUID"] != None:
            self.uuid = data["User-info"][0]["UUID"]




app = WelcomeToArgon()
app.mainloop()