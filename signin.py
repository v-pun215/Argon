import customtkinter as ct
import ctypes, PIL
import json
import uuid
import requests
from CTkMessagebox import CTkMessagebox as msg # type: ignore (My VSCode is cooked fr)
import subprocess, sys, string, random, os
import platform
from pathlib import Path
import psutil
import minecraft_launcher_lib
version = "1.4"

# Check if we're on macOS, first.
if platform.system() == 'Darwin':
    from Foundation import NSBundle
    bundle = NSBundle.mainBundle()
    if bundle:
        info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
        if info and info['CFBundleName'] == 'Python':
            info['CFBundleName'] = "Argon"
            info['CFBundleVersion'] = version
            info['CFBundleShortVersionString'] = version
            info['CFBundleIdentifier'] = f'org.vpun215.argon'
            info['CFBundleExecutable'] = 'Argon'
            info['CFBundleIconFile'] = 'img/macicon.icns'
            info['CFBundleGetInfoString'] = 'Argon v{version}, © 2025 v-pun215'
            info['CFBundleLongVersionString'] = 'Argon v{version}, © 2025 v-pun215'
            info['NSHumanReadableCopyright'] = '© 2025 v-pun215'

argonVersion = version

argonFont = "Inter"


os_name = platform.system()
if os_name == "Darwin":
    argonFont = ""
usr_accnt = str(Path.home()).replace("\\", "/").split("/")[-1]
mc_dir = minecraft_launcher_lib.utils.get_minecraft_directory()
latest_version = minecraft_launcher_lib.utils.get_latest_version()
latest_release = latest_version["release"]
svmem = psutil.virtual_memory()
currn_dir = os.getcwd()
def check_java():
    '''
    Checks if java is installed (meant for linux and macOS)
    Returns True if java is installed, False otherwise.
    '''
    try:
        process = subprocess.run(['java', '-version'], capture_output=True, text=True, check=True)
        if "Unable to locate" in process.stderr: # macOS specific error message
            raise subprocess.CalledProcessError(1, 'java')
        return True
    except subprocess.CalledProcessError as e:
        print("Java is not installed or not in PATH.")
        print(e)
        return False
    except FileNotFoundError:
         print("Java is not installed or not in PATH.")
         return False

if os_name == "Linux" or os_name == "Darwin":
    if check_java():
        java_home = subprocess.run(['which', 'java'], capture_output=True, text=True).stdout
        java_home = java_home.replace("\n", "")
    else:
        java_home = ""
elif os_name == "Windows":
    try:
        java_home = os.getenv("JAVA_HOME")+r"\\bin\\java.exe"
        java_home = java_home.replace("\\", "/")
    except TypeError:
        print("Java is not installed, or it is not installed to the PATH (system environment variable). Please (re)install Java and try again.")
        os.system("pause")
        sys.exit()
try: 
    if os_name == "Windows":
        java_loc = os.getenv('JAVA_HOME').replace("\\", "/")+str(r"\\bin\\java.exe")
    elif os_name == "Linux":
        java_loc = java_home
    elif os_name == "Darwin":
        java_loc = java_home
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
                        "verbose": True,
                        "customBackground": [
                            False,
                            ""
                        ],
                        "theme": "System"
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
            "icon4": "gold_block",
            "icon5": "diamond_block",
            "icon6": "emerald_block",
            "icon7": "acacia_log",
            "icon8": "birch_log",
            "icon9": "cherry_log",
            "icon10": "dark_oak_log",
            "icon11": "jungle_log",
            "icon12": "oak_log",
            "icon13": "pale_oak_log",
            "icon14": "spruce_log",
            "icon15": "mangrove_log",
            "icon16": "glass",
            "icon17": "copper_block",
            "icon18": "crafting_table",
            "icon19": "furnace",
            "icon20": "anvil",
            "icon21": "tnt",
            "icon22": "obsidian",
            "icon23": "netherite_block",
            "icon24": "grass_block",
            "icon25": "cherry_planks",
            "icon26": "oak_planks",
            "icon27": "spruce_planks",
            "icon28": "cobblestone"
        }
    ],
    "all-instances": [
        {}
    ]
}
if os_name == "Windows":
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
elif os_name == "Linux":
    if not os.path.exists(f"{currn_dir}/settings.json"):
        with open("settings.json", "w") as js_set:
            json.dump(settings, js_set, indent=4)
            js_set.close()
    else:
        pass
    if not os.path.exists(f"{mc_dir}/launcherProfiles.json"):
        with open("launcherProfiles.json", "w") as js_set:
            json.dump(launcher_profiles, js_set, indent=4)
            js_set.close()
    else:
        pass
elif os_name == "Darwin":
    if not os.path.exists(f"{currn_dir}/settings.json"):
        with open("settings.json", "w") as js_set:
            json.dump(settings, js_set, indent=4)
            js_set.close()
    else:
        pass
    if not os.path.exists(f"{mc_dir}/launcherProfiles.json"):
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

os_name_settings = data["PC-info"][0]["OS"]
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
if os_name == "Windows":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
else:
    pass
class WelcomeToArgon(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x600")
        if os_name == "Windows":
            self.wm_iconbitmap("img/icon.ico")
        elif os_name == "Linux":
            self.wm_iconbitmap("img/logo.png")
        self.resizable(False, False)
        self.title("Argon")
        if not os.path.exists("instances/"):
            os.makedirs("instances/")
        self.background_image = ct.CTkImage(PIL.Image.open("img/welcome/background.jpg"), size=(1024, 600))
        self.background_label = ct.CTkLabel(self, image=self.background_image, text="")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.main_frame = ct.CTkFrame(self, bg_color="transparent", width=300, height=600, fg_color="#1f1f1f", corner_radius=0)
        self.main_frame.place(relx=0, rely=0.5, anchor="w")
        self.logo_img = ct.CTkImage(PIL.Image.open("img/argon.png"), size=(200, 65))
        self.logo_label = ct.CTkLabel(self.main_frame, image=self.logo_img, text="")
        self.logo_label.place(relx=0.5, rely=0.15, anchor="center")
        micro_img = ct.CTkImage(PIL.Image.open("img/welcome/microsoft.png"), size=(15, 15))
        self.microsft_btn = ct.CTkButton(self.main_frame, text="Login with Microsoft", image=micro_img, font=(argonFont, 15),  command=lambda: radiobutton_event(1), bg_color="transparent",width=200, corner_radius=5)
        self.microsft_btn.place(relx=0.5, rely=0.35, anchor="center")
        ely_img = ct.CTkImage(PIL.Image.open("img/welcome/ely.jpg"), size=(15, 15))
        self.ely_btn = ct.CTkButton(self.main_frame, text="Login with Ely.by", image=ely_img, font=(argonFont, 15),  command=lambda: radiobutton_event(2), bg_color="transparent",width=200, corner_radius=5)
        self.ely_btn.place(relx=0.5, rely=0.41, anchor="center")
        off_img = ct.CTkImage(PIL.Image.open("img/welcome/offline.png"), size=(15, 15))
        self.offline_btn = ct.CTkButton(self.main_frame, text="Login Offline", image=off_img, font=(argonFont, 15),  command=lambda: radiobutton_event(3), bg_color="transparent",width=200, corner_radius=5)
        self.offline_btn.place(relx=0.5, rely=0.47, anchor="center")


        self.version_label = ct.CTkLabel(self.main_frame, text=f"Argon v{argonVersion}", font=(argonFont, 10), bg_color="transparent", fg_color="transparent", text_color="#b3b3b3")

        '''
        self.instruction = ct.CTkLabel(self.main_frame, text="Choose Account Type", font=(argonFont, 15, "bold"), bg_color="transparent", fg_color="transparent", text_color="#b3b3b3")
        self.instruction.place(relx=0.5, rely=0.30, anchor="center")
        self.radio_label = ct.CTkLabel(self.main_frame, text="Microsoft", font=(argonFont, 15), bg_color="transparent", fg_color="transparent", text_color="white")
        self.radio_label.place(relx=0.3, rely=0.38, anchor="center")
        self.radio_label2 = ct.CTkLabel(self.main_frame, text="Ely.by", font=(argonFont, 15), bg_color="transparent", fg_color="transparent", text_color="white")
        self.radio_label2.place(relx=0.5, rely=0.38, anchor="center")
        self.radio_label3 = ct.CTkLabel(self.main_frame, text="Offline", font=(argonFont, 15), bg_color="transparent", fg_color="transparent", text_color="white")
        self.radio_label3.place(relx=0.7, rely=0.38, anchor="center")'''
        def radiobutton_event(var):
            if var == 1:
                self.elyby_frame.place_forget()
                self.offline_frame.place_forget()
                self.microsoft_frame.place_forget()
                self.after(200, self.ms_login)
            elif var == 2:
                self.microsoft_frame.place_forget()
                self.offline_frame.place_forget()
                self.elyby_frame.place(relx=0.5, rely=0.75, anchor="center")
            elif var == 3:
                self.microsoft_frame.place_forget()
                self.elyby_frame.place_forget()
                self.offline_frame.place(relx=0.5, rely=0.75, anchor="center")
            else:
                self.microsoft_frame.place_forget()
                self.elyby_frame.place_forget()
                self.offline_frame.place_forget()
        
       
        self.microsoft_frame = ct.CTkFrame(self.main_frame, bg_color="transparent", width=300, height=155, fg_color="transparent")
        self.elyby_frame = ct.CTkFrame(self.main_frame, bg_color="transparent", width=300, height=155, fg_color="transparent")
        self.offline_frame = ct.CTkFrame(self.main_frame, bg_color="transparent", width=300, height=155, fg_color="transparent")
        self.ms_login_label = ct.CTkLabel(self.microsoft_frame, text="Login to your Microsoft Account", font=(argonFont, 15, "bold"), bg_color="transparent", fg_color="transparent", text_color="white")
        self.ms_login_label.place(relx=0.5, rely=0.3, anchor="center")
        self.ms_login_btn  = ct.CTkButton(self.microsoft_frame, text="Login",  command=self.ms_login, bg_color="transparent", corner_radius=5)
        self.ms_login_btn.place(relx=0.5, rely=0.65, anchor="center")
        self.elyby_login_label = ct.CTkLabel(self.elyby_frame, text="Login to your Ely.by Account", font=(argonFont, 15, "bold"), bg_color="transparent", fg_color="transparent", text_color="white")
        self.elyby_login_label.place(relx=0.5, rely=0.15, anchor="center")
        self.elyby_login_username = ct.CTkEntry(self.elyby_frame, font=(argonFont, 15), bg_color="transparent", fg_color="#3b3b3b", corner_radius=5, placeholder_text="Username")
        self.elyby_login_username.place(relx=0.5, rely=0.4, anchor="center")
        self.elyby_login_password = ct.CTkEntry(self.elyby_frame, font=(argonFont, 15), bg_color="transparent", fg_color="#3b3b3b", corner_radius=5, placeholder_text="Password", show="•")
        self.elyby_login_password.place(relx=0.5, rely=0.6, anchor="center")
        self.elyby_login_btn = ct.CTkButton(self.elyby_frame, text="Login",  command=self.ely_authenticate, bg_color="transparent", corner_radius=5)
        self.elyby_login_btn.place(relx=0.5, rely=0.82, anchor="center")
        self.offline_login_label = ct.CTkLabel(self.offline_frame, text="Login to an Offline Account", font=(argonFont, 15, "bold"), bg_color="transparent", fg_color="transparent", text_color="white")
        self.offline_login_label.place(relx=0.5, rely=0.15, anchor="center")
        self.offline_login_username = ct.CTkEntry(self.offline_frame, font=(argonFont, 15), bg_color="transparent", fg_color="#3b3b3b", corner_radius=5, placeholder_text="Username")
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
        print("Exiting to Argon...")
        self.destroy()
        if os_name == "Windows":
            os.execvp("python", ["python", "main.py"])
        elif os_name == "Linux" or os_name == "Darwin":
            os.execvp("python3", ["python3", "main.py"])

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
