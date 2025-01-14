import tkinter
import tkinter.messagebox
import customtkinter as ct
from PIL import Image, ImageTk
from ctypes import windll, byref, sizeof, c_int
import ctypes
import random
import keys
import urllib.request
import json, datetime
import threading
import time
import io
import re as regex
import pywinstyles
import psutil
import os
import getpass
import requests
import subprocess
import sys
import minecraft_launcher_lib as mc
from minecraft_launcher_lib.forge import install_forge_version, run_forge_installer, supports_automatic_install
from minecraft_launcher_lib.fabric import install_fabric, get_all_minecraft_versions, get_stable_minecraft_versions, get_latest_loader_version
import uuid
import CTkMessagebox as msg
import wget
from elySkinRenderer import render_skin, render_iso_skin
from mcNewsParser import get_json_file
from xml.dom.minidom import parse
import xml.dom.minidom, os, subprocess
import webbrowser
import functools
from pathlib import Path
from checkSkinChange import checkChangeSkin
from threading import Thread
from CTkScrollableDropdown import *
import mods

starttime = time.time()

'''Argon Metadata'''
author = "v_pun215"
version = "1.0-stable"
description = "A feature-rich minecraft launcher built in Python."
#--#


mcNewsHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
cl = keys.client
se = keys.secret
re = "https://eclient-done.vercel.app/"

currn_dir = os.getcwd()
usr_accnt = str(Path.home()).replace("\\", "/").split("/")[-1]
mc_dir = r"C:\\users\\{}\\AppData\\Roaming\\.minecraft".format(usr_accnt)
svmem = psutil.virtual_memory()
if not os.path.exists(r"{}/settings.json".format(currn_dir)):
    subprocess.Popen(["python", "welcome.pyw"])
    sys.exit()
else:
    pass


ct.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ct.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
myappid = u'vpun215.argon.release.2.0' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
print('''
 $$$$$$\                                          
$$  __$$\                                         
$$ /  $$ | $$$$$$\   $$$$$$\   $$$$$$\  $$$$$$$\  
$$$$$$$$ |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ 
$$  __$$ |$$ |  \__|$$ /  $$ |$$ /  $$ |$$ |  $$ |
$$ |  $$ |$$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |
$$ |  $$ |$$ |      \$$$$$$$ |\$$$$$$  |$$ |  $$ |
\__|  \__|\__|       \____$$ | \______/ \__|  \__|
                    $$\   $$ |                    
                    \$$$$$$  |                    
                     \______/                     
      ''')
print("")
print("---Console Starts Here---")

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
cracked_password = data["User-info"][0]["cracked_password"]
uid = data["User-info"][0]["UUID"]
accessToken = data["accessToken"]
mc_dir = data["Minecraft-home"]
auth_type = data["User-info"][0]["AUTH_TYPE"]
selected_ver = data["selected-version"]
selected_inst = data["selected-instance"]
allocated_ram = data["settings"][0]["allocated_ram"]
jvm_args = data["settings"][0]["jvm-args"]
javaPath = data["settings"][0]["executablePath"]
ramlimiterExceptionBypassed = data["settings"][0]["ramlimiterExceptionBypassed"]
ramlimiterExceptionBypassedSelected = data["settings"][0]["ramlimiterExceptionBypassedSelected"]
verbose = data["settings"][0]["verbose"]
refresh_token = data["Microsoft-settings"][0]["refresh_token"]

if username == None:
    subprocess.Popen(["pyw", "welcome.pyw"])
    sys.exit()
def reload_data():
    global mc_home
    global username
    global uid
    global os_name
    global mc_dir
    global selected_ver
    global ramlimiterExceptionBypassed
    global verbose
    global ramlimiterExceptionBypassedSelected
    global auth_type
    global jvm_args
    global allocated_ram
    global accessToken
    global refresh_token
    global cracked_password

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
    javaPath = data["settings"][0]["executablePath"]
    ramlimiterExceptionBypassed = data["settings"][0]["ramlimiterExceptionBypassed"]
    ramlimiterExceptionBypassedSelected = data["settings"][0]["ramlimiterExceptionBypassedSelected"]
    verbose = data["settings"][0]["verbose"]
    refresh_token = data["Microsoft-settings"][0]["refresh_token"]
    cracked_password = data["User-info"][0]["cracked_password"]


if os.path.exists(r"C:/Users/{}/AppData/Roaming/.minecraft".format(usr_accnt)):
    print("Existing minecraft installation, checking for versions...")

else:
     os.mkdir(r"C:/Users/{}/AppData/Roaming/.minecraft".format(usr_accnt))
     os.chdir(r"C:/Users/{}/AppData/Roaming/.minecraft".format(usr_accnt))
     os.mkdir("versions")

connected = True
def check_internet(url='https://www.google.com', timeout=5):
    global connected
    #Checks internet connection at startup
    try:
        r2 = requests.head(url, timeout=timeout)
        print("Connected to the Internet!")
        return True
    except requests.ConnectionError:
        connected = False
        print("No internet connection available.")
    except requests.exceptions.Timeout:
        connected = False
        print("Connection Timed Out.")


class Argon(ct.CTk):
    def __init__(self):
        super().__init__()
        self.search_list = None
        self.is_loading = True
        global mc_home
        global username
        global uid
        global os_name
        global mc_dir
        global selected_ver
        global ramlimiterExceptionBypassed
        global verbose
        global ramlimiterExceptionBypassedSelected
        global auth_type
        global jvm_args
        global allocated_ram
        global accessToken
        global refresh_token
        global cracked_password
        self.title("Argon")
        self.geometry(f"{1024}x{600}")
        self.wm_iconbitmap("img/icon.ico")
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        

        # Variables
        chosen_inst = selected_ver
        self.selected_version = selected_ver
        self.selected_instance = selected_inst

        # Splash Screen
        #self.loading_screen()  Future Update!
        
        ## Instance Icons
        with open("launcherProfiles.json", "r") as js_read:
            s = js_read.read()
            s = s.replace('\t','')  #Trailing commas in dict cause file read problems, these lines will fix it.
            s = s.replace('\n','')  #Found this on stackoverflow.
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            data = json.loads(s)
            #print(json.dumps(data, indent=4,))
        self.release_img = ct.CTkImage(light_image=Image.open("img/instance_icons/release.png"), dark_image=Image.open("img/instance_icons/release.png"), size=(23,23)) # Latest Release Icon
        self.snapshot_img = ct.CTkImage(light_image=Image.open("img/instance_icons/snapshot.png"), dark_image=Image.open("img/instance_icons/snapshot.png"), size=(23,23)) # Latest Snapshot Icon
        def get_icon(icon_name):
            if icon_name == None:
                return icon_name
            else:
                return ct.CTkImage(light_image=Image.open(f"img/instance_icons/{icon_name}.png"), dark_image=Image.open(f"img/instance_icons/{icon_name}.png"), size=(23,23))
            
        def get_pinned_inst(pinnedinst):
            if pinnedinst == None:
                return ""
            else:
                return pinnedinst
            
        def get_variable_name(var):
            for name, value in globals().items():
                if value is var:
                    return name
            return None
        self.pinned1 = get_pinned_inst(data["pinned-instances"][0]["pinned1"])
        self.pinned2 = get_pinned_inst(data["pinned-instances"][0]["pinned2"])
        self.pinned3 = get_pinned_inst(data["pinned-instances"][0]["pinned3"])
        self.pinned4 = get_pinned_inst(data["pinned-instances"][0]["pinned4"])
        self.pinned5 = get_pinned_inst(data["pinned-instances"][0]["pinned5"])
        self.pinned6 = get_pinned_inst(data["pinned-instances"][0]["pinned6"])
        self.pinned7 = get_pinned_inst(data["pinned-instances"][0]["pinned7"])
        self.pinned8 = get_pinned_inst(data["pinned-instances"][0]["pinned8"])
        self.pinned9 = get_pinned_inst(data["pinned-instances"][0]["pinned9"])
        self.state_pinned1 = "disabled"
        self.state_pinned2 = "disabled"
        self.state_pinned3 = "disabled"
        self.state_pinned4 = "disabled"
        self.state_pinned5 = "disabled"
        self.state_pinned6 = "disabled"
        self.state_pinned7 = "disabled"
        self.state_pinned8 = "disabled"
        self.state_pinned9 = "disabled"
        self.state_pinned = {f"state_pinned{i}": "disabled" for i in range(1, 10)}
        self.pinned1_img = get_icon(data["pinned-icons"][0]["pinned1"])
        self.pinned2_img = get_icon(data["pinned-icons"][0]["pinned2"])
        self.pinned3_img = get_icon(data["pinned-icons"][0]["pinned3"])
        self.pinned4_img = get_icon(data["pinned-icons"][0]["pinned4"])
        self.pinned5_img = get_icon(data["pinned-icons"][0]["pinned5"])
        self.pinned6_img = get_icon(data["pinned-icons"][0]["pinned6"])
        self.pinned7_img = get_icon(data["pinned-icons"][0]["pinned7"])
        self.pinned8_img = get_icon(data["pinned-icons"][0]["pinned8"])
        self.pinned9_img = get_icon(data["pinned-icons"][0]["pinned9"])
        self.username_head_img = None

        def get_latest_forge_versions():
            import xml.etree.ElementTree as ET
            """
            Fetches the latest Forge version for every Minecraft version from the Maven metadata XML.

            Returns:
                list: A list of tuples where each tuple contains the Minecraft version and the latest full Forge version (e.g., '1.21-51.0.33'),
                    ordered as found in the XML file.
            """
            forge_versions = {}
            url = "https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml"

            try:
                # Fetch the Maven metadata XML
                response = requests.get(url)
                response.raise_for_status()

                # Parse the XML
                root = ET.fromstring(response.content)

                # Extract versioning information
                versions = root.find("versioning").find("versions").findall("version")

                # Process each version in XML order
                for version in versions:
                    full_version = version.text
                    if "-" in full_version:
                        # Split into Minecraft version and Forge version
                        mc_version, forge_version = full_version.split("-", 1)
                        # Store only the latest Forge version for each Minecraft version
                        if mc_version not in forge_versions or forge_version > forge_versions[mc_version].split("-", 1)[1]:
                            forge_versions[mc_version] = full_version

                # Preserve order from XML file
                ordered_versions = [(mc_version, forge_versions[mc_version]) for mc_version, _ in forge_versions.items()]
                return ordered_versions

            except Exception as e:
                print(f"An error occurred: {e}")
                return []
        self.available_versions = mc.utils.get_available_versions(mc_dir)
        forge_versions = get_latest_forge_versions()
        self.forge_versions_all = []
        for mc_version, full_version in forge_versions:
            self.forge_versions_all.append(full_version)
        self.fabric_versions_all = mc.fabric.get_all_minecraft_versions()
        # Microsoft Authentication
        if auth_type == "Microsoft":
            try:
                account_informaton = mc.microsoft_account.complete_refresh(cl, se, re, refresh_token)
                global msaoptions
                msaoptions = {
                    "username": account_informaton["name"],
                    "uuid": account_informaton["id"],
                    "token": account_informaton["access_token"],
                }
                username = msaoptions["username"]
                uid = msaoptions["uuid"]
                accessToken = msaoptions["token"]
                auth_type = "Microsoft"
                print("Logged in as: ", username)
                if not os.path.exists(f"img/user/{username}.png"):
                    print("Downloading head image...")
                    os.chdir("img/user")
                    wget.download(f"https://crafatar.com/renders/head/{uid}?overlay" , f"{username}.png")
                    os.chdir(currn_dir)

                elif checkChangeSkin(f"https://crafatar.com/renders/head/{uid}?overlay", f"img/user/{username}.png") == True:
                    print("Skin has changed, re-rendering skin...")
                    os.remove(f"img/user/{username}.png")
                    os.chdir("img/user")
                    wget.download(f"https://crafatar.com/renders/head/{uid}?overlay", f"{username}.png")
                    os.chdir(currn_dir)
                else:
                    print("Head image already exists, and is same as on server.")
                    pass
                


            # Show the window if the refresh token is invalid
            except mc.exceptions.InvalidRefreshToken:
                if connected == True:
                    msg(title="Microsoft Account", message="Unable to refresh Microsoft Account. Please login again.", icon="warning")
                    #self.mc_login()
                else:
                    msg(title="Error", message=" Your Microsoft Account is unreachable due to no internet access. You will be able to play only using offline mode.", icon="cancel")
                    auth_type = "Offline"

        elif auth_type == "ElyBy":
            self.ely_authenticate()
            print("[ElyBy] Logged in as:", username)
            if not os.path.exists(f"img/user/ely-{username}-raw-skin.png"):
                wget.download(f"http://skinsystem.ely.by/skins/{username}.png", f"img/user/ely-{username}-raw-skin.png")
                print("[ElyBy] Downloaded skin of:", username)
                print("[ElyBy] Rendering skin of:", username)
                render_skin(f"img/user/ely-{username}-raw-skin.png")
                print("[ElyVy] Rendered skin")


            
            elif checkChangeSkin(f"http://skinsystem.ely.by/skins/{username}.png", f"img/user/ely-{username}-raw-skin.png") == True:
                print("[ElyBy] Skin has changed, re-rendering skin...")
                os.remove(f"img/user/ely-{username}.png")
                os.remove(f"img/user/ely-{username}-raw-skin.png")
                wget.download(f"http://skinsystem.ely.by/skins/{username}.png", f"img/user/ely-{username}-raw-skin.png")
                render_skin(f"img/user/ely-{username}-raw-skin.png")
                print("[ElyBy] Rendered skin")
            else:
                pass
            if not os.path.exists(f"img/user/ely-{username}-skin.png"):
                render_iso_skin(f"img/user/ely-{username}-raw-skin.png")
                print("[ElyBy] Rendered iso skin")
            elif checkChangeSkin(f"http://skinsystem.ely.by/skins/{username}.png", f"img/user/ely-{username}-raw-skin.png") == True:
                print("[ElyBy] Skin has changed, re-rendering iso skin...")
                os.remove(f"img/user/ely-{username}-skin.png")
                render_iso_skin(f"img/user/ely-{username}-raw-skin.png")
                print("[ElyBy] Rendered iso skin")
            else:
                pass
        elif auth_type == "Offline":
            print("[OFFLINE] Logged in as: ", username)

        self.addInstance()

        if auth_type == "Microsoft":
            self.username_head_img = Image.open(f"img/user/{username}.png")
        elif auth_type == "ElyBy":
            self.username_head_img = Image.open(f"img/user/ely-{username}.png")
        elif auth_type == "Offline":
            self.username_head_img = Image.open("img/user/steve.png")
        


        # Sidebar
        self.sidebar_frame = ct.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        skin_size = (50, 50) if auth_type == "Offline" else (55, 50)
        self.skin_head = ct.CTkImage(light_image=self.username_head_img, dark_image=self.username_head_img, size=skin_size)
        self.skin_head_label = ct.CTkLabel(self.sidebar_frame,text="",image=self.skin_head, bg_color="transparent")
        self.skin_head_label.place(x=20 if auth_type=="Offline" else 10, y=10)
        self.login_label = ct.CTkLabel(self.sidebar_frame, text="Logged in as", font=ct.CTkFont(size=16, family="Inter"), anchor="w", text_color="#b3b3b3")
        self.login_label.place(x=80, y=8)
        self.username_label = ct.CTkLabel(self.sidebar_frame, text=username, font=ct.CTkFont(size=20, weight="bold", family="Inter"), anchor="w", text_color="white", bg_color="transparent", fg_color="transparent")
        self.username_label.place(x=80, y=31)
        self.home_img = ct.CTkImage(light_image=Image.open("img/home.png"), dark_image=Image.open("img/home.png"), size=(23, 17))
        self.inst_img = ct.CTkImage(light_image=Image.open("img/inst.png"), dark_image=Image.open("img/inst.png"), size=(23,17))
        self.set_img = ct.CTkImage(light_image=Image.open("img/settings.png"), dark_image=Image.open("img/settings.png"), size=(23,17))
        self.acc_img = ct.CTkImage(light_image=Image.open("img/account.png"), dark_image=Image.open("img/account.png"), size=(23,17))
        self.home = ct.CTkButton(self.sidebar_frame,text="Home", font=ct.CTkFont(size=15, family="Inter"), command=self.go_to_home, height=30, width=200, corner_radius=0, anchor="w", image=self.home_img, compound="left")
        self.home.place(x=0, y=75)
        self.inst = ct.CTkButton(self.sidebar_frame,text="Instances", font=ct.CTkFont(size=15, family="Inter"), command=self.go_to_inst, height=30, corner_radius=0, width=200, anchor="w", image=self.inst_img, compound="left")
        self.inst.place(x=0, y=106)
        self.settings = ct.CTkButton(self.sidebar_frame,text="Settings", font=ct.CTkFont(size=15, family="Inter"), command=self.go_to_set, height=30, width=200, corner_radius=0, anchor="w", image=self.set_img, compound="left")
        self.settings.place(x=0, y=137)
        self.account = ct.CTkButton(self.sidebar_frame,text="Account", font=ct.CTkFont(size=15, family="Inter"), command=self.go_to_acc, height=30, width=200, corner_radius=0, anchor="w", image=self.acc_img, compound="left")
        self.account.place(x=0, y=168)
        for i in range(1, 10):
            if getattr(self, f"pinned{i}") != "":
                self.state_pinned[f"state_pinned{i}"] = "normal"
        ltvers = mc.utils.get_latest_version()
        latestRelease = f"vanilla release {ltvers['release']}"
        print(latestRelease)
        latestSnapshot = f"vanilla snapshot {ltvers['snapshot']}"
        print(latestSnapshot)
        self.pinned_inst = {}
        
        self.pinned_inst1 = ct.CTkButton(self.sidebar_frame,text="Latest Release",image=self.release_img, font=ct.CTkFont(size=15, family="Inter"), command=lambda: self.choose_inst("Latest Release", latestRelease), height=30, width=200, corner_radius=0, anchor="w", fg_color="transparent", bg_color="#262626", hover_color="#1a1a1a", compound="left")
        self.pinned_inst1.place(x=0, y=210)
        self.pinned_inst2 = ct.CTkButton(self.sidebar_frame,text="Latest Snapshot",image=self.snapshot_img, font=ct.CTkFont(size=15, family="Inter"), command=lambda: self.choose_inst("Latest Snapshot", latestSnapshot), height=30, width=200, corner_radius=0, anchor="w", fg_color="transparent", bg_color="transparent", hover_color="#1a1a1a", compound="left")
        self.pinned_inst2.place(x=0, y=240)
        '''for i in range(3, 12):
            pinned_text = getattr(self, f"pinned{i-2}")
            pinned_img = getattr(self, f"pinned{i-2}_img")
            self.pinned_inst[i] = ct.CTkButton(self.sidebar_frame, text=pinned_text, image=pinned_img, font=ct.CTkFont(size=15, family="Inter"), command=self.sidebar_button_event, height=30, width=200, corner_radius=0, anchor="w", state=self.state_pinned[f"state_pinned{i-2}"])
            self.pinned_inst[i].place(x=0, y=210 + (i - 1) * 30)
            if i % 2 != 0:  # Odd number
                self.pinned_inst[i].configure(bg_color="#262626", hover_color="#1a1a1a")
            else:  # Even number
                self.pinned_inst[i].configure(bg_color="transparent", hover_color="#1a1a1a")'''

        for i in range(1, 10):
            pinned_text = getattr(self, f"pinned{i}")
            pinned_img = getattr(self, f"pinned{i}_img")
            fg_color = "#262626" if i % 2 != 0 else "transparent"
            hover_color = "#1a1a1a"
            print(pinned_text)
            self.pinned_inst[f"pinned{i}"] = ct.CTkButton(self.sidebar_frame, text=pinned_text, image=pinned_img, font=ct.CTkFont(size=15, family="Inter"), command=lambda pinned_text=pinned_text: self.select_pinned_instance(pinned_text), height=30, width=200, corner_radius=0, anchor="w", state=self.state_pinned[f"state_pinned{i}"], fg_color=fg_color, hover_color=hover_color)
            self.pinned_inst[f"pinned{i}"].place(x=0, y=210 + (i + 1) * 30)

        '''
        self.pinned_inst3 = ct.CTkButton(self.sidebar_frame,text=self.pinned1,image=self.pinned1_img, font=ct.CTkFont(size=15, family="Inter"), command=self.sidebar_button_event, height=30, width=200, corner_radius=0, anchor="w",text_color="white", fg_color="transparent", bg_color="#262626", hover_color="#1a1a1a", compound="left", state=self.state_pinned["state_pinned1"])
        self.pinned_inst3.place(x=0, y=270)
        self.pinned_inst4 = ct.CTkButton(self.sidebar_frame,text=self.pinned2,image=self.pinned2_img, font=ct.CTkFont(size=15, family="Inter"), command=self.sidebar_button_event, height=30, width=200, corner_radius=0, anchor="w",text_color="white", fg_color="transparent", bg_color="transparent", hover_color="#1a1a1a", compound="left", state=self.state_pinned["state_pinned2"])
        self.pinned_inst4.place(x=0, y=300)
        self.pinned_inst5 = ct.CTkButton(self.sidebar_frame,text=self.pinned3,image=self.pinned3_img, font=ct.CTkFont(size=15, family="Inter"), command=self.sidebar_button_event, height=30, width=200, corner_radius=0, anchor="w",text_color="white", fg_color="transparent", bg_color="#262626", hover_color="#1a1a1a", compound="left", state=self.state_pinned["state_pinned3"])
        self.pinned_inst5.place(x=0, y=330)
        self.pinned_inst6 = ct.CTkButton(self.sidebar_frame,text=self.pinned4,image=self.pinned4_img, font=ct.CTkFont(size=15, family="Inter"), command=self.sidebar_button_event, height=30, width=200, corner_radius=0, anchor="w",text_color="white", fg_color="transparent", bg_color="transparent", hover_color="#1a1a1a", compound="left", state=self.state_pinned["state_pinned4"])
        self.pinned_inst6.place(x=0, y=360)
        self.pinned_inst7 = ct.CTkButton(self.sidebar_frame,text=self.pinned5,image=self.pinned5_img, font=ct.CTkFont(size=15, family="Inter"), command=self.sidebar_button_event, height=30, width=200, corner_radius=0, anchor="w",text_color="white", fg_color="transparent", bg_color="#262626", hover_color="#1a1a1a", compound="left", state=self.state_pinned["state_pinned5"])
        self.pinned_inst7.place(x=0, y=390)
        self.pinned_inst8 = ct.CTkButton(self.sidebar_frame,text=self.pinned6,image=self.pinned6_img, font=ct.CTkFont(size=15, family="Inter"), command=self.sidebar_button_event, height=30, width=200, corner_radius=0, anchor="w",text_color="white", fg_color="transparent", bg_color="transparent", hover_color="#1a1a1a", compound="left", state=self.state_pinned["state_pinned6"])
        self.pinned_inst8.place(x=0, y=420)
        self.pinned_inst9 = ct.CTkButton(self.sidebar_frame,text=self.pinned7,image=self.pinned7_img, font=ct.CTkFont(size=15, family="Inter"), command=self.sidebar_button_event, height=30, width=200, corner_radius=0, anchor="w",text_color="white", fg_color="transparent", bg_color="#262626", hover_color="#1a1a1a", compound="left", state=self.state_pinned["state_pinned7"])
        self.pinned_inst9.place(x=0, y=450)
        self.pinned_inst10 = ct.CTkButton(self.sidebar_frame,text=self.pinned8,image=self.pinned8_img, font=ct.CTkFont(size=15, family="Inter"), command=self.sidebar_button_event, height=30, width=200, corner_radius=0, anchor="w",text_color="white", fg_color="transparent", bg_color="transparent", hover_color="#1a1a1a", compound="left", state=self.state_pinned["state_pinned8"])
        self.pinned_inst10.place(x=0, y=480)
        self.pinned_inst11 = ct.CTkButton(self.sidebar_frame,text=self.pinned9,image=self.pinned9_img, font=ct.CTkFont(size=15, family="Inter"), command=self.sidebar_button_event, height=30, width=200, corner_radius=0, anchor="w",text_color="white", fg_color="transparent", bg_color="#262626", hover_color="#1a1a1a", compound="left", state=self.state_pinned["state_pinned9"])
        self.pinned_inst11.place(x=0, y=510)'''
            

        self.play = ct.CTkButton(self.sidebar_frame,text=f"Play\n{str(self.selected_instance)}", font=ct.CTkFont(size=17, family="Inter"), command=self.runMinecraft, width=200, height=60, corner_radius=0)
        self.play.place(x=0, y=540)
        
        # Home
        self.ch_frame = ct.CTkFrame(self, corner_radius=0, height=600, fg_color="transparent")
        self.ch_frame.grid(row=0, column=1, sticky="nsew")
        self.ch_frame.grid_columnconfigure(0, weight=1)
        self.logo_image = ct.CTkImage(light_image=Image.open("img/logo.png"),dark_image=Image.open("img/logo.png"), size=(70, 70))
        #self.image_label = ct.CTkLabel(self.ch_frame, image=self.logo_image, text="", bg_color="transparent")
        #self.image_label.place(x=195, y=20)
        #self.ch_label = ct.CTkLabel(self.ch_frame, text="Argon Launcher", font=ct.CTkFont(size=40, weight="bold", family="Inter"), fg_color="transparent")
        #self.ch_label.place(x=275, y=30)
        self.logo_img = ct.CTkImage(light_image=Image.open("img/argon.png"), dark_image=Image.open("img/argon.png"), size=(300, 100))
        self.logo_label = ct.CTkLabel(self.ch_frame, text="",image=self.logo_img, bg_color="transparent")
        self.logo_label.place(relx=0.5, rely=0.1, anchor="center")
        self.news_frame = ct.CTkFrame(self.ch_frame, corner_radius=10, height=450,width=850, bg_color="transparent")
        self.news_frame.place(relx=0.501, rely=0.6, anchor="center")
        try:
            get_json_file()
            with open("mcNewsletter.json", "r") as js_read:
                raw = json.loads(js_read.read())
            news = raw["entries"]
            counter = 0
            def open_url(url):
                webbrowser.open(url)
            print("Loading MC Changelog... (this may take some time)")
            def short(text, max_length):
                if len(text) > max_length:
                    return text[:max_length - 3] + "..."
                else:
                    return text
            for new in news:
                title = short(new["title"], 40)
                description = short(new["text"], 72)
                imageURL = new["playPageImage"]["url"]
                guid = new["readMoreLink"]
                pubDate = new["date"]
                var_name = "self.news"+str(counter)+"_frame"
                globals()[var_name] = ct.CTkFrame(self.news_frame, corner_radius=5, height=100,width=780,fg_color="#262626", bg_color="transparent")
                globals()[var_name].grid(row=counter, column=0, sticky="nsew", pady=7, padx=7)
                var_name2 = "self.news"+str(counter)+"_img"
                globals()[var_name2] = ct.CTkImage(light_image=Image.open(requests.get("https://launchercontent.mojang.com"+str(imageURL), stream=True,headers=mcNewsHeaders).raw), dark_image=Image.open(requests.get("https://launchercontent.mojang.com"+str(imageURL), stream=True, headers=mcNewsHeaders).raw), size=(80, 80))
                var_name3 = "self.news"+str(counter)+"_img_label"
                globals()[var_name3] = ct.CTkLabel(globals()[var_name], text="", image=globals()[var_name2], bg_color="transparent", corner_radius=5)
                globals()[var_name3].place(x=5, y=10)
                var_name4 = "self.news"+str(counter)+"_title"
                globals()[var_name4] = ct.CTkLabel(globals()[var_name], text=title, font=ct.CTkFont(size=25, weight="bold", family="Inter"),text_color="white", bg_color="transparent")
                globals()[var_name4].place(x=110, y=10)
                var_name5 = "self.news"+str(counter)+"_description"
                globals()[var_name5] = ct.CTkLabel(globals()[var_name], text=description, font=ct.CTkFont(size=15, family="Inter"),text_color="#b3b3b3", bg_color="transparent")
                globals()[var_name5].place(x=110, y=60)
                var_name6 = "self.news"+str(counter)+"_readmore"
                globals()[var_name6] = ct.CTkButton(globals()[var_name], text="Read More", font=ct.CTkFont(size=15, family="Inter"), command=functools.partial(open_url, guid), height=30, width=80, corner_radius=5, anchor="w", fg_color="transparent", bg_color="#262626", hover_color="#1a1a1a")
                globals()[var_name6].place(x=680, y=60)
                var_name7 = "self.news"+str(counter)+"_date"
                globals()[var_name7] = ct.CTkLabel(globals()[var_name], text=str(pubDate), font=ct.CTkFont(size=15, family="Inter"),text_color="#b3b3b3", bg_color="transparent")
                globals()[var_name7].place(x=680, y=10)
                if counter == 3:
                    break
                else:
                    counter = counter+1
        except Exception as e:
            os.execv(sys.argv[0], sys.argv)
        

        # Instances
        with open("launcherProfiles.json", "r") as js_read:
            s = js_read.read()
            s = s.replace('\t','')  #Trailing commas in dict cause file read problems, these lines will fix it.
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            data = json.loads(s)
        
        instances = data["all-instances"]


        


        def get_icon_PIL(icon_name):
            if icon_name == None:
                return Image.open("img/instance_icons/none.png")
            else:
                return Image.open(f"img/instance_icons/{icon_name}.png")
            


        self.inst_frame = ct.CTkFrame(self, corner_radius=0, height=600, fg_color="transparent")
        self.inst_frame.grid(row=0, column=1, sticky="nsew")
        self.inst_frame.grid_columnconfigure(0, weight=1)
        self.inst_title = ct.CTkLabel(self.inst_frame, text="Instances", font=ct.CTkFont(size=40, weight="bold", family="Inter"), fg_color="transparent")
        self.inst_title.place(x=40, y=20)
        self.add_inst_button = ct.CTkButton(self.inst_frame, text="Add Instance", font=ct.CTkFont(size=15, family="Inter"), command=self.showAddInstanceWindow, height=30, width=120, corner_radius=5, anchor="center")
        self.add_inst_button.place(x=680, y=35)
        self.inst_list = ct.CTkScrollableFrame(self.inst_frame, corner_radius=8, height=468,width=765, fg_color="#2b2b2b", bg_color="transparent")
        self.inst_list.place(relx=0.501, rely=0.55, anchor="center")
        instance_frames = {}

        row_index = 0
        if instances == [{}]:
            no_inst_label = ct.CTkLabel(self.inst_list, text="No instances found", font=ct.CTkFont(size=30, family="Inter"), bg_color="transparent", text_color="#b3b3b3")
            no_inst_label.grid(row=0, column=0, sticky="nsew", pady=10, padx=10)
        for instance_dict in instances:
            for instance_name, instance_data_list in instance_dict.items():
                instance_data = instance_data_list[0]

                frame = ct.CTkFrame(self.inst_list, corner_radius=7, height=125, width=745, fg_color="#262626")
                frame.grid(row=row_index, column=0, sticky="nsew", pady=7, padx=7)
                
                img = ct.CTkImage(light_image=get_icon_PIL(instance_data["icon"]), dark_image=get_icon_PIL(instance_data["icon"]), size=(50,50))
                img_label = ct.CTkLabel(frame, text="", image=img, bg_color="transparent")
                img_label.place(x=10, y=10)
                
                name_label = ct.CTkLabel(frame, text=instance_data["name"], font=ct.CTkFont(size=30, weight="bold", family="Inter"), bg_color="transparent")
                name_label.place(x=70, y=13)

                version_label = ct.CTkLabel(frame, text=str(instance_data["method"]).capitalize() + " " + str(instance_data["type"]).capitalize() + " " + instance_data["version"], font=ct.CTkFont(size=15, family="Inter"), bg_color="transparent", text_color="#b3b3b3")
                version_label.place(x=70, y=50)

                select_button = ct.CTkButton(frame, text="Select", font=ct.CTkFont(size=15, family="Inter"), command=functools.partial(self.choose_inst, instance_data["name"], instance_data["method"] + " " + instance_data["type"] + " " + instance_data["version"]), height=30, width=80, corner_radius=5, anchor="center")
                select_button.place(x=655, y=10)
                
                settings_button = ct.CTkButton(frame, text="Settings", font=ct.CTkFont(size=15, family="Inter"), command=lambda instee_name=instance_data["name"], instee_icon=instance_data["icon"], instee_version=instance_data["method"] + " " + instance_data["type"] + " " + instance_data["version"]: self.instance_settings(instee_name, instee_icon, instee_version), height=30, width=80, corner_radius=5, anchor="center")
                settings_button.place(x=655, y=50)

                pinned_text_label = ct.CTkLabel(frame, text="Pinned:", font=ct.CTkFont(size=15, family="Inter"), bg_color="transparent", text_color="white")
                pinned_text_label.place(x=12, y=83)
                var_name = "self.pinned_var"+str(row_index)
                pinned_var = ct.StringVar(value="on" if instance_data["pinned"] else "off")
                #globals()[var_name] = pinned_var
                pinned_checkbox = ct.CTkCheckBox(frame,text="", corner_radius=5, fg_color="white", bg_color="#262626", command=lambda name=instance_data["name"], icon=instance_data["icon"], pinD_var=pinned_var, inst_name=instance_name: self.pinInstance(name, icon, pinD_var, inst_name), variable=pinned_var, onvalue="on",offvalue="off", checkbox_height=20, checkbox_width=20)
                pinned_checkbox.place(x=75, y=85)

                # Store the frame in the dictionary
                instance_frames[instance_name] = frame

                row_index += 1

        '''
        self.instance1 = ct.CTkFrame(self.inst_list, corner_radius=7, height=190,width=230, fg_color="#262626")
        self.instance1.grid(row=0, column=0, sticky="nsew", pady=10, padx=10)
        self.instance1_img = ct.CTkImage(light_image=get_icon_PIL(instance1[0]["icon"]), dark_image=get_icon_PIL(instance1[0]["icon"]), size=(50,50))
        self.instance1_img_label = ct.CTkLabel(self.instance1, text="", image=self.instance1_img, bg_color="transparent")
        self.instance1_img_label.place(x=10, y=10)
        self.instance1_name = ct.CTkLabel(self.instance1, text=instance1[0]["name"], font=ct.CTkFont(size=20, weight="bold", family="Inter"), fg_color="white", bg_color="transparent")
        self.instance1_name.place(x=70, y=20)
        self.instance2 = ct.CTkFrame(self.inst_list, corner_radius=7, height=190,width=230, fg_color="#262626")
        self.instance2.grid(row=0, column=1, sticky="nsew", pady=10, padx=10)
        self.instance3 = ct.CTkFrame(self.inst_list, corner_radius=7, height=190,width=230, fg_color="#262626")
        self.instance3.grid(row=0, column=2, sticky="nsew", pady=10, padx=10)'''


        # Settings
        self.set_frame = ct.CTkFrame(self, corner_radius=0, height=600, fg_color="transparent")
        self.set_frame.grid(row=0, column=1, sticky="nsew")
        self.set_frame.grid_columnconfigure(0, weight=1)
        self.settings_title = ct.CTkLabel(self.set_frame, text="Settings", font=ct.CTkFont(size=40, weight="bold", family="Inter"), fg_color="transparent")
        self.settings_title.place(x=40, y=20)
        self.settings_frame = ct.CTkFrame(self.set_frame, corner_radius=10, height=480,width=780, bg_color="transparent")
        self.settings_frame.place(relx=0.5, rely=0.555, anchor="center")
        variable = ct.StringVar(value="Minecraft")
        def switch_tabs():
            if variable.get() == "Minecraft":
                self.mc_settings_frame.place_forget()
                self.argon_settings_frame.place_forget()
                self.mc_settings_frame.place(relx=0.5, rely=0.52, anchor="center")
            elif variable.get() == "Argon":
                self.mc_settings_frame.place_forget()
                self.argon_settings_frame.place_forget()
                self.argon_settings_frame.place(relx=0.5, rely=0.52, anchor="center")
        self.switchtabs_segmentedbtn = ct.CTkSegmentedButton(self.settings_frame, command=lambda event: switch_tabs(), variable=variable, values=["Minecraft", "Argon"], font=ct.CTkFont(size=20, family="Inter"), height=30, width=120)
        self.switchtabs_segmentedbtn.place(relx=0.4, y=10)

        self.mc_settings_frame = ct.CTkFrame(self.settings_frame, height=400, width=780, bg_color="transparent", fg_color="transparent")
        self.mc_settings_frame.place(relx=0.5, rely=0.52, anchor="center")
        self.mc_dir_labl = ct.CTkLabel(self.mc_settings_frame, text="Minecraft Directory", font=ct.CTkFont(size=25, family="Inter"), fg_color="transparent", text_color="white")
        self.mc_dir_labl.place(x=20, y=10)
        mc_dir_var = ct.StringVar(value=mc_dir)
        self.mc_dir_entry = ct.CTkEntry(self.mc_settings_frame, font=ct.CTkFont(size=20, family="Inter"), width=500, corner_radius=5, textvariable=mc_dir_var)
        self.mc_dir_entry.place(x=20, y=50)

        self.ram_label = ct.CTkLabel(self.mc_settings_frame, text="RAM Allocation", font=ct.CTkFont(size=25, family="Inter"), fg_color="transparent", text_color="white")
        self.ram_label.place(x=20, y=100)
        with open ("settings.json", "r") as js_read:
            s = js_read.read()
            s = s.replace('\t','')
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            settings = json.loads(s)
        allocated_ram = settings["settings"][0]["allocated_ram"]
        ramlimiterExceptionBypassed = settings["settings"][0]["ramlimiterExceptionBypassed"]
        ramlimiterExceptionBypassedSelected = settings["settings"][0]["ramlimiterExceptionBypassedSelected"]
        verbose = settings["settings"][0]["verbose"]
        def get_total_ram():
            mem = psutil.virtual_memory()
            return mem.total / (1024 * 1024)
        total_ram = round(get_total_ram())
        ram_var = ct.IntVar(value=allocated_ram)
        self.ram_slider = ct.CTkSlider(self.mc_settings_frame, from_=100, to=total_ram, orientation="horizontal", width=500, fg_color="#7a7a7a", bg_color="transparent", corner_radius=5, variable=ram_var, command=lambda x: self.sel_ram.configure(text=f"Selected RAM: {ram_var.get()}MB"))
        self.ram_slider.place(x=20, y=140)
        self.sel_ram = ct.CTkLabel(self.mc_settings_frame, text=f"Selected RAM: {ram_var.get()}MB", font=ct.CTkFont(size=15, family="Inter"), fg_color="transparent", text_color="#7a7a7a")
        self.sel_ram.place(x=20, y=165)
        self.total_ram = ct.CTkLabel(self.mc_settings_frame, text=f"Total RAM: {total_ram}MB", font=ct.CTkFont(size=15, family="Inter"), fg_color="transparent", text_color="#7a7a7a")
        self.total_ram.place(x=20, y=190)
        self.bypass_label = ct.CTkLabel(self.mc_settings_frame, text="Bypass RAM Limiter", font=ct.CTkFont(size=25, family="Inter"), fg_color="transparent", text_color="white")
        self.bypass_label.place(x=20, y=220)
        if ramlimiterExceptionBypassed == True:
            switch_var = ct.StringVar(value="on")
        else:
            switch_var = ct.StringVar(value="off")
        self.by_switch = ct.CTkSwitch(self.mc_settings_frame, width=50, height=30, corner_radius=15, bg_color="transparent", fg_color="white", text="", variable=switch_var, onvalue="on", offvalue="off")
        self.by_switch.place(x=280, y=220)
        def save_settings():
            if switch_var.get() == "on":
                ramlimiterExceptionBypassed = True
            else:
                ramlimiterExceptionBypassed = False
            ramlimiterExceptionBypassedSelected = ramlimiterExceptionBypassed
            allocated_ram = ram_var.get()
            mc_dir_new = mc_dir_var.get()
            if mc_dir_new != mc_dir:
                try:
                    os.chdir(mc_dir_new)
                    if not os.path.exists("\\mods"):
                        os.mkdir("mods")
                    elif not os.path.exists("\\versions"):
                        os.mkdir("versions")
                    elif not os.path.exists("\\resourcepacks"):
                        os.mkdir("resourcepacks")
                    elif not os.path.exists("\\shaderpacks"):
                        os.mkdir("shaderpacks")
                    elif not os.path.exists("\\saves"):
                        os.mkdir("saves")
                    elif not os.path.exists("\\texturepacks"):
                        os.mkdir("texturepacks")
                    else:
                        pass
                    os.chdir(currn_dir)
                    mc_dir_newee = mc_dir_new
                except:
                    msg.CTkMessagebox(title="Invalid Minecraft Directory", message="The minecraft directory you entered is invalid.", icon="cancel")
                    return
            settings["settings"][0]["allocated_ram"] = allocated_ram
            settings["settings"][0]["ramlimiterExceptionBypassed"] = ramlimiterExceptionBypassed
            settings["settings"][0]["ramlimiterExceptionBypassedSelected"] = ramlimiterExceptionBypassedSelected
            settings["Minecraft-home"] = mc_dir_newee
            with open("settings.json", "w") as js_write:
                js_write.write(json.dumps(settings, indent=4))
            print("Settings saved.")
            msg.CTkMessagebox(title="Settings Saved", message="Settings have been saved successfully.", icon="check")
        self.save_button = ct.CTkButton(self.mc_settings_frame, text="Save", font=ct.CTkFont(size=20, family="Inter"), command=save_settings, height=30, width=100, corner_radius=5, anchor="center")
        self.save_button.place(relx = 0.5, rely=0.95, anchor="center")
        
        self.argon_settings_frame = ct.CTkFrame(self.settings_frame, height=400, width=780, bg_color="transparent", fg_color="transparent")
        self.argon_settings_frame.place(relx=0.5, rely=0.52, anchor="center")
        self.verbose_label = ct.CTkLabel(self.argon_settings_frame, text="Verbose Mode", font=ct.CTkFont(size=25, family="Inter"), fg_color="transparent", text_color="white")
        self.verbose_label.place(x=20, y=10)
        if verbose == True:
            verbose_var = ct.StringVar(value="on")
        else:
            verbose_var = ct.StringVar(value="off")
        self.verbose_switch = ct.CTkSwitch(self.argon_settings_frame, width=50, height=30, corner_radius=15, bg_color="transparent", fg_color="white", text="", variable=verbose_var, onvalue="on", offvalue="off")
        self.verbose_switch.place(x=220, y=10)

        self.save_button = ct.CTkButton(self.argon_settings_frame, text="Save", font=ct.CTkFont(size=20, family="Inter"), command=save_settings, height=30, width=100, corner_radius=5, anchor="center")
        self.save_button.place(relx = 0.5, rely=0.95, anchor="center")



        self.argon_settings_frame.place_forget()
        

        # Account
        self.acc_frame = ct.CTkFrame(self, corner_radius=0, height=600, fg_color="transparent")
        self.acc_frame.grid(row=0, column=1, sticky="nsew")
        self.acc_frame.grid_columnconfigure(0, weight=1)
        if auth_type == "Microsoft":
            req = urllib.request.Request(f"https://nmsr.nickac.dev/fullbody/{uid}", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as u:
                raw_data = u.read()
            image = Image.open(io.BytesIO(raw_data))
            photo = ct.CTkImage(light_image=image, dark_image=image, size=(150, 254))
        elif auth_type == "ElyBy":
            photo = ct.CTkImage(light_image=Image.open(f"img/user/ely-{username}-skin.png"), dark_image=Image.open(f"img/user/ely-{username}-skin.png"), size=(148, 307))
        elif auth_type == "Offline":
            photo = ct.CTkImage(light_image=Image.open("img/user/steve-skin.png"), dark_image=Image.open("img/user/steve-skin.png"), size=(118, 257))
        self.skin_label = ct.CTkLabel(self.acc_frame, text="", image=photo, bg_color="transparent")
        if auth_type == "ElyBy":
            self.skin_label.place(x=180, y=110)
        else:
            self.skin_label.place(x=190, y=140)
        self.username_labelBig = ct.CTkLabel(self.acc_frame, text=username, font=ct.CTkFont(size=50, weight="bold", family="Inter"), text_color="white", bg_color="transparent")
        self.username_labelBig.place(x=350, y=140)
        self.account_label = ct.CTkLabel(self.acc_frame, text=f"{auth_type} Account", font=ct.CTkFont(size=20, family="Inter"), fg_color="transparent", text_color="#7a7a7a")
        self.account_label.place(x=350, y=200)
        self.change_skin_btn = ct.CTkButton(self.acc_frame, text="Change Skin", font=ct.CTkFont(size=15, family="Inter"), command=self.change_skin, height=30, width=120, corner_radius=5, anchor="center")
        self.change_skin_btn.place(x=350, y=250)
        def sign_out_confirm():
            con = msg.CTkMessagebox(title="Sign Out", message="Are you sure you want to sign out?", icon="warning", option_1="No", option_2="Yes")
            response = con.get()
            if response == "Yes":
                self.sign_out()
            else:
                pass
        self.signout_btn = ct.CTkButton(self.acc_frame, text="Sign Out", font=ct.CTkFont(size=15, family="Inter"), command=sign_out_confirm, height=30, width=120, corner_radius=5, anchor="center", fg_color="#cc0000", hover_color="#990000")
        self.signout_btn.place(x=350, y=290)
        self.argon_version = ct.CTkLabel(self.acc_frame, text=f"Argon v{version}", font=ct.CTkFont(size=15, family="Inter"), fg_color="transparent", text_color="#7a7a7a")
        self.argon_version.place(x=10, y=570)
        self.builtby = ct.CTkLabel(self.acc_frame, text="Made by v-pun215.", font=ct.CTkFont(size=15, family="Inter"), fg_color="transparent", text_color="#7a7a7a")
        self.builtby.place(x=680, y=570)
        self.select_frame("home")
        endtime = time.time()
        print(f"Argon loaded in {round(endtime - starttime, 2)} seconds.")
        pywinstyles.change_header_color(self, color="#242424")
        self.deiconify()

    '''  Future Update!
    def loading_screen(self):
        self.splash_screen = ct.CTkToplevel(self)
        self.splash_screen.title("Argon")
        self.splash_screen.geometry("400x300")
        self.splash_screen.resizable(False, False)
        self.splash_screen.overrideredirect(True)
        self.splash_screen.configure(bg="#262626")
        self.splash_screen.destroy()
    '''
    def refresh_pinned(self):
        for i in range(1, 10):
            pinned_text = getattr(self, f"pinned{i}")
            pinned_img = getattr(self, f"pinned{i}_img")
            fg_color = "#262626" if i % 2 != 0 else "transparent"
            hover_color = "#1a1a1a"
            print(pinned_text)
            self.pinned_inst[f"pinned{i}"].destroy()

        for i in range(1, 10):
            pinned_text = getattr(self, f"pinned{i}")
            pinned_img = getattr(self, f"pinned{i}_img")
            fg_color = "#262626" if i % 2 != 0 else "transparent"
            hover_color = "#1a1a1a"
            print(pinned_text)
            self.pinned_inst[f"pinned{i}"] = ct.CTkButton(self.sidebar_frame, text=pinned_text, image=pinned_img, font=ct.CTkFont(size=15, family="Inter"), command=lambda pinned_text=pinned_text: self.select_pinned_instance(pinned_text), height=30, width=200, corner_radius=0, anchor="w", state=self.state_pinned[f"state_pinned{i}"], fg_color=fg_color, hover_color=hover_color)
            self.pinned_inst[f"pinned{i}"].place(x=0, y=210 + (i + 1) * 30)
    def select_pinned_instance(self, instance_name):
        print(instance_name)
        inst = instance_name
        with open("launcherProfiles.json", "r") as js_read:
            s = js_read.read()
            s = s.replace('\t','')
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            data = json.loads(s)

        instances = data["all-instances"]
        inst_ver = None
        for instance_dict in instances:
            
            for instance_name, instance_data_list in instance_dict.items():
                instance_data = instance_data_list[0]
                print(instance_name)
                if instance_name == inst:
                    inst_ver = instance_data["method"] + " " + instance_data["type"] + " " + instance_data["version"]
                    print(f"Selected instance: {inst} ({inst_ver})")

        self.choose_inst(inst, inst_ver)
        

    def change_settings_tab(self, event):
        if self.instance_settings_var.get() == "Settings":
            self.ins_settings_frame.place(relx=0.5, rely=0.53, anchor="center")
            self.mods_frame.place_forget()
        elif self.instance_settings_var.get() == "Mods":
            self.mods_frame.place(relx=0.5, rely=0.53, anchor="center")
            self.ins_settings_frame.place_forget()
    def instance_settings(self, inst_name, inst_icon, inst_version):
        self.instance_settings_window = ct.CTkToplevel(self)
        self.instance_settings_window.title(f"Instance {inst_name} Settings")
        self.instance_settings_window.geometry("800x500")
        self.instance_settings_window.resizable(False, False)
        self.instance_settings_window.configure(bg="#262626")
        self.instance_settings_window.protocol("WM_DELETE_WINDOW", self.instance_settings_window.destroy)
        self.instance_settings_window.after(200, lambda: self.instance_settings_window.iconbitmap("img/icon.ico"))
        self.instance_settings_window.grab_set()
        self.instance_settings_var = ct.StringVar(value="Settings")

        self.menubar = ct.CTkSegmentedButton(self.instance_settings_window, values=["Settings", "Mods"], variable=self.instance_settings_var, height=30, width=200, command=self.change_settings_tab)
        self.menubar.place(relx=0.5, y=25, anchor="center")

        self.ins_settings_frame = ct.CTkFrame(self.instance_settings_window, corner_radius=10, height=435, bg_color="#262626", width=770)
        self.ins_settings_frame.place(relx=0.5, rely=0.53, anchor="center")
        namevar = ct.StringVar(value=inst_name)
        self.name_entry = ct.CTkEntry(self.ins_settings_frame, textvariable=namevar, width=300, corner_radius=5,  font=ct.CTkFont(size=25, family="Inter"), fg_color="#404040", bg_color="transparent", placeholder_text="Name", placeholder_text_color="#b3b3b3")
        self.name_entry.place(x=20, y=20)
        self.name_entry.configure
        with open("launcherProfiles.json", "r") as js_read:
            s = js_read.read()
            s = s.replace('\t','')
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            data = json.loads(s)
        icon_list = data["icons"]
        self.chosen_icon = inst_icon
        def chooseIcon(icon_name):
            self.chosen_icon = icon_name
            inst_icon = icon_name
            self.icon_select_btn.destroy()
            counter = 0
            for icon in icon_list:
                for i in range(1,18):
                    if icon[f"icon{i}"] is not None:
                        counter += 1
                        if inst_icon == icon[f"icon{i}"]:
                            fg = "#1f6aa5"
                            hover = "#1a5380"
                        else:
                            fg = "transparent"
                            hover = "#1a1a1a"
                        self.icon_list.append(icon[f"icon{i}"])
                        self.icon_name = icon[f"icon{i}"]
                        self.icon_select_btn = ct.CTkButton(self.ins_settings_frame, text="", image=get_icon_PIL(icon[f"icon{i}"]), font=ct.CTkFont(size=30, family="Inter"), command=lambda icon_name=self.icon_name: chooseIcon(icon_name), height=50, width=50, corner_radius=5, anchor="center", fg_color=fg, bg_color="transparent", hover_color=hover, compound="left")
                        self.icon_select_btn.place(x=-30 + (i*50), y=70)
                    else:
                        pass
        def get_icon_PIL(icon_name):
            if icon_name == None:
                photo = Image.open("img/instance_icons/none.png")
                photo = ct.CTkImage(photo, size=(35,35))
                return photo
            else:
                photo = Image.open(f"img/instance_icons/{icon_name}.png")
                photo = ct.CTkImage(photo, size=(35,35))
                return photo

        self.icon_list = []
        counter = 0
        for icon in icon_list:
            for i in range(1,18):
                if icon[f"icon{i}"] is not None:
                    counter += 1
                    if inst_icon == icon[f"icon{i}"]:
                        fg = "#1f6aa5"
                        hover = "#1a5380"
                    else:
                        fg = "transparent"
                        hover = "#1a1a1a"
                    self.icon_list.append(icon[f"icon{i}"])
                    self.icon_name = icon[f"icon{i}"]
                    self.icon_select_btn = ct.CTkButton(self.ins_settings_frame, text="", image=get_icon_PIL(icon[f"icon{i}"]), font=ct.CTkFont(size=30, family="Inter"), command=lambda icon_name=self.icon_name: chooseIcon(icon_name), height=50, width=50, corner_radius=5, anchor="center", fg_color=fg, bg_color="transparent", hover_color=hover, compound="left")
                    self.icon_select_btn.place(x=-30 + (i*50), y=70)
                else:
                    pass
        def save_settings():
            if self.chosen_icon == None:
                msg.CTkMessagebox(title="Error", message="Please select an icon for the instance.", icon="cancel")
            elif namevar.get() == "":
                msg.CTkMessagebox(title="Error", message="Please enter a name for the instance.", icon="cancel")
            else:
                with open("launcherProfiles.json", "r") as js_read:
                    s = js_read.read()
                    s = s.replace('\t','')
                    s = s.replace('\n','')
                    s = s.replace(',}','}')
                    s = s.replace(',]',']')
                    data = json.loads(s)
                for instance in data["all-instances"]:
                    for instance_name, instance_data_list in instance.items():
                        instance_data = instance_data_list[0]
                        if instance_name == inst_name:
                            instance_name = self.name_entry.get()
                            instance_data["name"] = self.name_entry.get()
                            instance_data["icon"] = self.chosen_icon
                            instance[instance_name] = instance_data_list
                            if os.path.exists(f"instances\\{inst_name}"):
                                os.rename(f"instances\\{inst_name}", f"instances\\{instance_name}")
                            if instance_data["pinned"]:
                                pinned_instances = data["pinned-instances"][0]
                                pinned_icons = data["pinned-icons"][0]
                                for i in range(1, 10):
                                    pinned_key = f"pinned{i}"
                                    pinned_instances = data["pinned-instances"][0]
                                    pinned_icons = data["pinned-icons"][0]
                                    inst_name2 = pinned_instances[pinned_key]
                                    if pinned_instances[pinned_key] == inst_name:
                                        pinned_instances[pinned_key] = instance_name
                                        pinned_icons[pinned_key] = self.chosen_icon
                                        with open("launcherProfiles.json", "w") as js_write:
                                            json.dump(data, js_write, indent=4)
                                        def get_icon(icon_name):
                                            if icon_name == None:
                                                return icon_name
                                            else:
                                                return ct.CTkImage(light_image=Image.open(f"img/instance_icons/{icon_name}.png"), dark_image=Image.open(f"img/instance_icons/{icon_name}.png"), size=(23,23))

                                        pinned_img = get_icon(data["pinned-icons"][0][f"pinned{i}"])
                                        self.pinned_inst[f"pinned{i}"].configure(text=instance_name, state="normal", image=pinned_img)
                                        break
                                    else:
                                        pass
                            if instance_name != inst_name:
                                del instance[inst_name]
                            print("Hotdogs: ", instance_data["icon"])
                            break

                
                    
                    
                with open("launcherProfiles.json", "w") as js_write:
                    js_write.write(json.dumps(data, indent=4))

                msg.CTkMessagebox(title="Success", message="Instance settings have been saved.", icon="check")
                self.refresh_instances()

        def delete_instance():
            instance_icon = inst_icon
            q = msg.CTkMessagebox(title="Delete Instance", message="Are you sure you want to delete this instance?", icon="warning", option_1="No", option_2="Yes")
            response = q.get()
            if response == "Yes":
                with open("launcherProfiles.json", "r") as js_read:
                    s = js_read.read()
                    s = s.replace('\t', '')
                    s = s.replace('\n', '')
                    s = s.replace(',}', '}')
                    s = s.replace(',]', ']')
                    data = json.loads(s)
                for instance in data["all-instances"]:
                    for instance_name, instance_data_list in instance.items():
                        if instance_name == inst_name:
                            print("Lets goo")
                            del instance[instance_name]
                            print("deleted")
                            break

                
                with open("launcherProfiles.json", "w") as js_write:
                    js_write.write(json.dumps(data, indent=4))


                # Delete if pinned
                # Load the JSON data from the file
                with open("launcherProfiles.json", "r") as js_read:
                    s = js_read.read()
                    s = s.replace('\t','')  # Trailing commas in dict cause file read problems, these lines will fix it.
                    s = s.replace('\n','')
                    s = s.replace(',}','}')
                    s = s.replace(',]',']')
                    data = json.loads(s)
                
                pinned_instances = data["pinned-instances"][0]
                pinned_icons = data["pinned-icons"][0]
                name = instance

                # Unpin the instance
                for i in range(1, 10):
                    pinned_key = f"pinned{i}"
                    pinned_instances = data["pinned-instances"][0]
                    pinned_icons = data["pinned-icons"][0]
                    inst_name2 = pinned_instances[pinned_key]
                    print(instance_name)
                    if pinned_instances[pinned_key] == instance_name:
                        print("Instance found in pinned instances.")
                        pinned_instances = data["pinned-instances"][0]
                        pinned_icons = data["pinned-icons"][0]
                        pinned_instances[pinned_key] = None
                        pinned_icons[pinned_key] = None
                        self.state_pinned[pinned_key] = "disabled"
                        def get_icon_PIL(icon_name):
                            if icon_name == None:
                                photo = Image.open("img/instance_icons/none.png")
                                photo = ct.CTkImage(photo)
                                return photo
                            else:
                                photo = Image.open(f"img/instance_icons/{icon_name}.png")
                                photo = ct.CTkImage(photo)
                                return photo
                        self.pinned_inst[pinned_key].configure(text="", state="disabled", image=get_icon_PIL(None))
                        with open("launcherProfiles.json", "w") as js_write:
                            json.dump(data, js_write, indent=4)
                        print(f"Instance '{instance_name}' unpinned successfully.")
                        break
                    else:
                        print("Error: Instance not found in pinned instances.")
                self.instance_settings_window.destroy()
                self.refresh_instances()
                self.instance_settings_window.destroy()
            else:
                pass
                
        self.save_btn = ct.CTkButton(self.ins_settings_frame, text="Save", font=ct.CTkFont(size=20, family="Inter"), command=save_settings, height=30, width=100, corner_radius=5, anchor="center")
        self.save_btn.place(x=280, y=370)
        self.delete_btn = ct.CTkButton(self.ins_settings_frame, text="Delete", font=ct.CTkFont(size=20, family="Inter"), command=delete_instance, height=30, width=100, corner_radius=5, anchor="center", fg_color="#cc0000", hover_color="#990000")
        self.delete_btn.place(x=420, y=370)

        '''!!------------------MODS-----------------!!'''
        self.mods_frame = ct.CTkFrame(self.instance_settings_window, corner_radius=10, height=435, bg_color="#262626", width=770)
        self.mods_frame.place(relx=0.5, rely=0.53, anchor="center")
        self.mods_frame.place_forget()
        print(inst_version)
        if inst_version.startswith("forge") or inst_version.startswith("fabric"):
            method = inst_version.split(" ")[0]
            version = inst_version.split(" ")[2]
            mod_loader = method
            self.search_box = ct.CTkEntry(self.mods_frame, width=500, corner_radius=5,  font=ct.CTkFont(size=20, family="Inter"), fg_color="#404040", bg_color="transparent", placeholder_text="Search mods...", placeholder_text_color="#b3b3b3")
            self.search_box.place(x=10, y=10)
            self.instance_settings_window.bind("<Return>", lambda: self.search_mods(self.search_box.get(), inst_name, inst_version))
            self.search_image = ct.CTkImage(light_image=Image.open("img/search.png"), dark_image=Image.open("img/search.png"), size=(25,25))
            search_text = self.search_box.get()
            self.search_btn = ct.CTkButton(self.mods_frame, text="", image=self.search_image, font=ct.CTkFont(size=20, family="Inter"), command=lambda inst_name=inst_name, inst_version=inst_version: self.search_mods(query=self.search_box.get(), inst_name=inst_name, inst_version=inst_version), corner_radius=5, anchor="center", width=25, height=25, bg_color="transparent", fg_color="transparent", hover_color="#1a1a1a")
            self.search_btn.place(x=515, y=10)
            self.modrinth_logo = ct.CTkImage(light_image=Image.open("img/modrinth.png"), dark_image=Image.open("img/modrinth.png"), size=(25, 25))
            self.modrinth_btn = ct.CTkButton(self.mods_frame, text="", image=self.modrinth_logo, font=ct.CTkFont(size=20, family="Inter"), command=lambda: self.switchToModrinth(), corner_radius=5, anchor="center", width=25, height=25, bg_color="transparent", fg_color="#22da6f", hover_color="#19924c")
            self.modrinth_btn.place(x=670, y=10)
            self.folder_logo = ct.CTkImage(light_image=Image.open("img/folder.png"), dark_image=Image.open("img/folder.png"), size=(25, 25))
            self.folder_btn = ct.CTkButton(self.mods_frame, text="", image=self.folder_logo, font=ct.CTkFont(size=20, family="Inter"), command=lambda: self.switchToDir(instance_name=inst_name), corner_radius=5, anchor="center", width=25, height=25, bg_color="transparent", fg_color="white", hover_color="#929292")
            self.folder_btn.place(x=715, y=10)

            self.mods_list_frame = ct.CTkScrollableFrame(self.mods_frame, corner_radius=8, height=370, width=750, fg_color="#2b2b2b", bg_color="transparent")
            self.mods_list_frame.place(relx=0.5, rely=0.54, anchor="center")

            self.loading_label = ct.CTkLabel(
                self.mods_list_frame, 
                text="Loading...", 
                font=ct.CTkFont(size=20, family="Inter", weight="bold"), 
                text_color="#b3b3b3"
            )
            self.loading_label.grid(row=0, column=0, sticky="nsew", pady=20, padx=20)
            self.display_data(inst_name, inst_version)


            self.directory_frame = ct.CTkScrollableFrame(self.mods_frame, corner_radius=8, height=370, width=750, fg_color="#2b2b2b", bg_color="transparent")
            self.directory_frame.place(relx=0.5, rely=0.54, anchor="center")
            self.directory_frame.place_forget()

            dir = f"instances/{inst_name}/mods"
            if not os.path.exists(dir):
                self.noMods_label = ct.CTkLabel(self.directory_frame, text="This instance has no mods.", font=ct.CTkFont(size=20, family="Inter"), fg_color="transparent", bg_color="transparent", text_color="#b3b3b3")
                self.noMods_label.place(relx=0.5, rely=0.5, anchor="center")
            else:
                jar_files = [f for f in os.listdir(dir) if f.endswith('.jar')]
                row_index = 0
                for file in jar_files:
                    self.jar_frame = ct.CTkFrame(self.directory_frame, corner_radius=7, height=50, width=730, fg_color="#373737")
                    self.jar_frame.grid(row=row_index, column=0, sticky="nsew", pady=7, padx=7)
                    self.jar_title = ct.CTkLabel(self.jar_frame, text=file.strip(".jar"), font=ct.CTkFont(size=25, family="Inter"), text_color="white", fg_color="transparent", bg_color="transparent")
                    self.jar_title.place(x=10, y=10)
                    self.delete_img = ct.CTkImage(light_image=Image.open("img/delete.png"), dark_image=Image.open("img/delete.png"), size=(20, 20))
                    self.delete_btn = ct.CTkButton(self.jar_frame, text="", image=self.delete_img, font=ct.CTkFont(size=15, family="Inter"), command=lambda file=file: self.delete_mod(file, inst_name), height=20, width=20, corner_radius=5, anchor="center", fg_color="white", bg_color="transparent", hover_color="#8a8a8a")
                    self.delete_btn.place(x=685, y=10)
                    row_index += 1

        
        else:
            self.banner = ct.CTkLabel(self.mods_frame, text="This instance is not modded.", font=ct.CTkFont(size=30, family="Inter"), fg_color="transparent", bg_color="transparent", text_color="#b3b3b3")
            self.banner.place(relx=0.5, rely=0.5, anchor="center")

    def search_mods(self, query, inst_name, inst_version):
        self.mods_list_frame.place_forget()
        self.mods_list_frame = ct.CTkScrollableFrame(self.mods_frame, corner_radius=8, height=370, width=750, fg_color="#2b2b2b", bg_color="transparent")
        self.mods_list_frame.place(relx=0.5, rely=0.54, anchor="center")
        self.loading_label = ct.CTkLabel(
            self.mods_list_frame, 
            text="Loading...", 
            font=ct.CTkFont(size=30, family="Inter"), 
            text_color="#b3b3b3"
        )
        self.loading_label.grid(row=0, column=0, sticky="nsew", pady=20, padx=20)
        self.search_list1 = mods.Modrinth.search(query)
        print(query)
        self.process_data(inst_name, inst_version, list2=self.search_list1)
        self.loading_label.destroy()
    
    def refresh_mods(self, inst_name):
        self.directory_frame.place_forget()
        self.directory_frame = ct.CTkScrollableFrame(self.mods_frame, corner_radius=8, height=370, width=750, fg_color="#2b2b2b", bg_color="transparent")
        self.directory_frame.place(relx=0.5, rely=0.54, anchor="center")
        dir = f"instances/{inst_name}/mods"
        jar_files = [f for f in os.listdir(dir) if f.endswith('.jar')]
        row_index = 0
        for file in jar_files:
            self.jar_frame = ct.CTkFrame(self.directory_frame, corner_radius=7, height=50, width=730, fg_color="#373737")
            self.jar_frame.grid(row=row_index, column=0, sticky="nsew", pady=7, padx=7)
            self.jar_title = ct.CTkLabel(self.jar_frame, text=file.strip(".jar"), font=ct.CTkFont(size=25, family="Inter"), text_color="white", fg_color="transparent", bg_color="transparent")
            self.jar_title.place(x=10, y=10)
            self.delete_img = ct.CTkImage(light_image=Image.open("img/delete.png"), dark_image=Image.open("img/delete.png"), size=(20, 20))
            self.delete_btn = ct.CTkButton(self.jar_frame, text="", image=self.delete_img, font=ct.CTkFont(size=15, family="Inter"), command=lambda file=file: self.delete_mod(file, inst_name), height=20, width=20, corner_radius=5, anchor="center", fg_color="white", bg_color="transparent", hover_color="#8a8a8a")
            self.delete_btn.place(x=685, y=10)
            row_index += 1

    
    def delete_mod(self, file, inst_name):
        os.remove(f"instances/{inst_name}/mods/{file}")
        msg.CTkMessagebox(title="Mod Deleted", message="The mod has been deleted from the instance.", icon="check")
        self.directory_frame.place_forget()
        self.directory_frame = ct.CTkScrollableFrame(self.mods_frame, corner_radius=8, height=370, width=750, fg_color="#2b2b2b", bg_color="transparent")
        self.directory_frame.place(relx=0.5, rely=0.54, anchor="center")
        dir = f"instances/{inst_name}/mods"
        if not os.path.exists(dir):
            self.noMods_label = ct.CTkLabel(self.directory_frame, text="This instance has no mods.", font=ct.CTkFont(size=20, family="Inter"), fg_color="transparent", bg_color="transparent", text_color="#b3b3b3")
            self.noMods_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            jar_files = [f for f in os.listdir(dir) if f.endswith('.jar')]
            row_index = 0
            for file in jar_files:
                self.jar_frame = ct.CTkFrame(self.directory_frame, corner_radius=7, height=50, width=730, fg_color="#373737")
                self.jar_frame.grid(row=row_index, column=0, sticky="nsew", pady=7, padx=7)
                self.jar_title = ct.CTkLabel(self.jar_frame, text=file.strip(".jar"), font=ct.CTkFont(size=25, family="Inter", weight="bold"), text_color="white", fg_color="transparent", bg_color="transparent")
                self.jar_title.place(x=10, y=10)
                self.delete_img = ct.CTkImage(light_image=Image.open("img/delete.png"), dark_image=Image.open("img/delete.png"), size=(20, 20))
                self.delete_btn = ct.CTkButton(self.jar_frame, text="", image=self.delete_img, font=ct.CTkFont(size=15, family="Inter"), command=lambda file=file: self.delete_mod(file, inst_name), height=20, width=20, corner_radius=5, anchor="center", fg_color="white", bg_color="transparent", hover_color="#8a8a8a")
                self.delete_btn.place(x=685, y=10)
                row_index += 1
    def switchToModrinth(self):
        self.mods_list_frame.place_forget()
        self.directory_frame.place_forget()
        self.mods_list_frame.place(relx=0.5, rely=0.54, anchor="center")
    def switchToDir(self, instance_name):
        self.mods_list_frame.place_forget()
        self.directory_frame.place_forget()
        self.refresh_mods(instance_name)
        self.directory_frame.place(relx=0.5, rely=0.54, anchor="center")
        
    def load_data(self):
        # This function will run in a separate thread
        self.search_list = mods.Modrinth.search_homePage()
        self.is_loading = False

    def display_data(self, instname, inst_version):
        # Start the loading thread
        loading_thread = threading.Thread(target=self.load_data)
        loading_thread.start()

        # Periodically check if data is loaded
        def check_loading():
            if self.is_loading:
                # If still loading, keep checking
                self.after(500, check_loading)
            else:
                # Once done, update the UI
                self.loading_label.destroy()  # Remove the "Loading..." label
                loading_thread.join(1)  # Wait for the thread to finish
                self.process_data(instname, inst_version, list2=self.search_list)

        check_loading()
    def process_data(self, instname, inst_version, list2):
        mod_loader = inst_version.split(" ")[0]
        mc_version = inst_version.split(" ")[2]
        if list2 == None:
            self.loading_label = ct.CTkLabel(
                self.mods_list_frame, 
                text="Loading...", 
                font=ct.CTkFont(size=16, family="Inter", weight="bold"), 
                text_color="#b3b3b3"
            )
            self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
            self.display_data()
            return
        row_index = 0
        for mod in list2:
            self.mod_frame = ct.CTkFrame(
                self.mods_list_frame,
                corner_radius=7,
                height=100,
                width=730,
                fg_color="#373737",
            )
            self.mod_frame.grid(row=row_index, column=0, sticky="nsew", pady=7, padx=7)
            icon_url = mod["icon_url"]
            icon = requests.get(icon_url, stream=True, headers=mcNewsHeaders)
            icon = Image.open(icon.raw)
            icon = ct.CTkImage(light_image=icon, dark_image=icon, size=(80, 80))
            self.icon_label = ct.CTkLabel(
                self.mod_frame, text="", image=icon, bg_color="transparent"
            )
            self.icon_label.place(x=10, y=10)
            self.mod_title = ct.CTkLabel(
                self.mod_frame,
                text=mod["title"],
                font=ct.CTkFont(size=25, family="Inter", weight="bold"),
                text_color="white",
                fg_color="transparent",
                bg_color="transparent",
            )
            self.mod_title.place(x=110, y=10)
            self.description = ct.CTkLabel(self.mod_frame, text=mod["description"], font=ct.CTkFont(size=15, family="Inter"), text_color="#b3b3b3", fg_color="transparent", bg_color="transparent", wraplength=420, justify="left")
            self.description.place(x=110, y=40)
            self.down_img = ct.CTkImage(light_image=Image.open("img/download.png"), dark_image=Image.open("img/download.png"), size=(20, 20))
            if not mc_version in mod["versions"]:
                button_state = "normal"
                button_command = lambda: msg.CTkMessagebox(title="Error", message=f"This mod does not have a version for {mod_loader} {mc_version}.", icon="cancel")
            else:
                button_state = "normal"
                button_command = lambda mod_slug=mod["slug"], instance_name=instname, mod_loader=mod_loader, mc_version=mc_version: self.download_mod(mod_slug, instance_name, mod_loader, mc_version)
            self.download_mod_btn = ct.CTkButton(self.mod_frame, text="Download", image=self.down_img, font=ct.CTkFont(size=15, family="Inter"), command=button_command, height=20, width=60, corner_radius=5, anchor="w", state=button_state, fg_color="#1bd96a", bg_color="transparent", hover_color="#22ff84", text_color="black")
            self.download_mod_btn.place(relx=0.9, rely=0.3, anchor="center")
            see_more_img = ct.CTkImage(light_image=Image.open("img/seemore.png"), dark_image=Image.open("img/seemore.png"), size=(20, 20))
            self.see_more_btn = ct.CTkButton(self.mod_frame, image=see_more_img, text="See More", font=ct.CTkFont(size=15, family="Inter"), height=20, command=lambda mod_slug=mod["slug"]: webbrowser.open(f"https://modrinth.com/mod/{mod_slug}"), width=85, corner_radius=5, anchor="center", text_color="black", fg_color="white", bg_color="transparent", hover_color="#949494")
            self.see_more_btn.place(relx=0.9, rely=0.7, anchor="center")

            row_index += 1
            

        self.search_list = None
        self.is_loading = True
    def download_mod(self, slug, instance_name, mod_loader, mc_version):
        if not os.path.exists(f"instances/{instance_name}/mods"):
            os.chdir("instances")
            os.mkdir(instance_name)
            os.chdir(instance_name)
            os.mkdir("mods")
            os.chdir(currn_dir)
        else:
            pass
        try:
            mods.Modrinth.downloadLatestVersion(slug=slug, mc_ver=mc_version, mod_loader=mod_loader, dir=f"instances/{instance_name}/mods/")
            msg.CTkMessagebox(title="Mod Downloaded", message=f"The mod has been downloaded and added to instance '{instance_name}'.", icon="check")
        except Exception as e:
            print(e)
            msg.CTkMessagebox(title="Error", message=e, icon="cancel")
    def change_skin(self):
        if auth_type == "Microsoft":
            webbrowser.open("https://www.minecraft.net/en-us/msaprofile/mygames/editskin")
        elif auth_type == "ElyBy":
            webbrowser.open("https://ely.by/skins")
        elif auth_type == "Offline":
            msg.CTkMessagebox(title="Error", message="You cannot change the skin of an offline account.", icon="cancel")
    def sign_out(self):
        msg.CTkMessagebox(title="Sign Out", message="Are you sure you want to sign out?", icon="warning", option_1="No", option_2="Yes")
        response = msg.CTkMessagebox.get()
        if response == "Yes":

            os.remove("launcherProfiles.json")
            os.remove("settings.json")
            msg.CTkMessagebox(title="Sign Out", message="You have been signed out.", icon="check")
        else:
            pass
    def refresh_instances(self):
        self.inst_list.destroy()
        with open("launcherProfiles.json", "r") as js_read:
            s = js_read.read()
            s = s.replace('\t','')  #Trailing commas in dict cause file read problems, these lines will fix it.
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            data = json.loads(s)
        
        instances = data["all-instances"]


        


        def get_icon_PIL(icon_name):
            if icon_name == None:
                return Image.open("img/instance_icons/none.png")
            else:
                return Image.open(f"img/instance_icons/{icon_name}.png")
            
        self.inst_list = ct.CTkScrollableFrame(self.inst_frame, corner_radius=8, height=468,width=765, fg_color="#2b2b2b", bg_color="transparent")
        self.inst_list.place(relx=0.501, rely=0.55, anchor="center")
        instance_frames = {}

        row_index = 0
        for instance_dict in instances:
            for instance_name, instance_data_list in instance_dict.items():
                instance_data = instance_data_list[0]

                frame = ct.CTkFrame(self.inst_list, corner_radius=7, height=125, width=745, fg_color="#262626")
                frame.grid(row=row_index, column=0, sticky="nsew", pady=7, padx=7)
                
                img = ct.CTkImage(light_image=get_icon_PIL(instance_data["icon"]), dark_image=get_icon_PIL(instance_data["icon"]), size=(50,50))
                img_label = ct.CTkLabel(frame, text="", image=img, bg_color="transparent")
                img_label.place(x=10, y=10)
                
                name_label = ct.CTkLabel(frame, text=instance_data["name"], font=ct.CTkFont(size=30, weight="bold", family="Inter"), bg_color="transparent")
                name_label.place(x=70, y=13)

                version_label = ct.CTkLabel(frame, text=str(instance_data["method"]).capitalize() + " " + str(instance_data["type"]).capitalize() + " " + instance_data["version"], font=ct.CTkFont(size=15, family="Inter"), bg_color="transparent", text_color="#b3b3b3")
                version_label.place(x=70, y=50)

                select_button = ct.CTkButton(frame, text="Select", font=ct.CTkFont(size=15, family="Inter"), command=functools.partial(self.choose_inst, instance_data["name"], instance_data["method"] + " " + instance_data["type"] + " " + instance_data["version"]), height=30, width=80, corner_radius=5, anchor="center")
                select_button.place(x=655, y=10)
                
                settings_button = ct.CTkButton(frame, text="Settings", font=ct.CTkFont(size=15, family="Inter"), command=lambda instee_name=instance_data["name"], instee_icon=instance_data["icon"], instee_version=instance_data["method"] + " " + instance_data["type"] + " " + instance_data["version"]: self.instance_settings(instee_name, instee_icon, instee_version), height=30, width=80, corner_radius=5, anchor="center")
                settings_button.place(x=655, y=50)

                pinned_text_label = ct.CTkLabel(frame, text="Pinned:", font=ct.CTkFont(size=15, family="Inter"), bg_color="transparent", text_color="white")
                pinned_text_label.place(x=12, y=83)
                var_name = "self.pinned_var"+str(row_index)
                pinned_var = ct.StringVar(value="on" if instance_data["pinned"] else "off")
                #globals()[var_name] = pinned_var
                pinned_checkbox = ct.CTkCheckBox(frame,text="", corner_radius=5, fg_color="white", bg_color="#262626", command=lambda name=instance_data["name"], icon=instance_data["icon"], pinD_var=pinned_var, inst_name=instance_name: self.pinInstance(name, icon, pinD_var, inst_name), variable=pinned_var, onvalue="on",offvalue="off", checkbox_height=20, checkbox_width=20)
                pinned_checkbox.place(x=75, y=85)

                # Store the frame in the dictionary
                instance_frames[instance_name] = frame

                row_index += 1



    def select_frame(self, name):
        # set button color for selected button
        self.home.configure(fg_color=("#1f6aa5", "#1f6aa5") if name == "home" else "#404040", hover_color=("#144870") if name == "home" else "#333333")
        self.inst.configure(fg_color=("#1f6aa5", "#1f6aa5") if name == "installations" else "#404040", hover_color=("#144870") if name == "installations" else "#333333")
        self.settings.configure(fg_color=("#1f6aa5", "#1f6aa5") if name == "settings" else "#404040", hover_color=("#144870") if name == "settings" else "#333333")
        self.account.configure(fg_color=("#1f6aa5", "#1f6aa5") if name == "account" else "#404040", hover_color=("#144870") if name == "account" else "#333333")

        # show selected frame
        if name == "home":
            self.ch_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.ch_frame.grid_forget()
        if name == "installations":
            self.inst_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.inst_frame.grid_forget()
        if name == "settings":
            self.set_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.set_frame.grid_forget()
        if name == "account":
            self.acc_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.acc_frame.grid_forget()

    def go_to_home(self):
        self.select_frame("home")
    
    def go_to_inst(self):
        self.select_frame("installations")
    
    def go_to_set(self):
        self.select_frame("settings")

    def go_to_acc(self):
        self.select_frame("account")

    def sidebar_button_event(self):
        print("sidebar_button click")

    def runCommand(self, func, args):
        functools.partial(func, args)

    def getImageIcon(self, icon_name):
        if icon_name == None:
            return None
        else:
            return f"img/instance_icons/{icon_name}.png"
        

    def pinInstance(self, name, icon, pinned_var, inst_name):

            if pinned_var.get() == "on":
                print("on")
                # Load the JSON data from the file
                with open("launcherProfiles.json", "r") as js_read:
                    s = js_read.read()
                    s = s.replace('\t','')  # Trailing commas in dict cause file read problems, these lines will fix it.
                    s = s.replace('\n','')
                    s = s.replace(',}','}')
                    s = s.replace(',]',']')
                    data = json.loads(s)

                pinned_instances = data["pinned-instances"][0]
                pinned_icons = data["pinned-icons"][0]


                # Find the first available slot in pinned-instances
                for i in range(1, 10):
                    pinned_key = f"pinned{i}"
                    if pinned_instances[pinned_key] is None:
                        pinned_instances[pinned_key] = name
                        pinned_icons[pinned_key] = icon
                        self.state_pinned[pinned_key] = "normal"  # Enable the sidebar button
                        def get_icon_PIL(icon_name):
                            if icon_name == None:
                                photo = Image.open("img/instance_icons/none.png")
                                photo = ct.CTkImage(photo)
                                return photo
                            else:
                                photo = Image.open(f"img/instance_icons/{icon_name}.png")
                                photo = ct.CTkImage(photo)
                                return photo
                        self.pinned_inst[pinned_key].configure(text=name, state="normal", image=get_icon_PIL(icon), command=lambda pinned_key=name: self.select_pinned_instance(pinned_key))
                        data["all-instances"][0][inst_name][0]["pinned"] = True
                        with open("launcherProfiles.json", "w") as js_write:
                            json.dump(data, js_write, indent=4)
                        break
                    else:
                        print("Slot is occupied, moving to next slot.")
                    
                        

                # Save the updated JSON data back to the file
                with open("launcherProfiles.json", "w") as js_write:
                    json.dump(data, js_write, indent=4)

                print(f"Instance '{name}' pinned successfully.")
            elif pinned_var.get() == "off":
                print("off")
                # Load the JSON data from the file
                with open("launcherProfiles.json", "r") as js_read:
                    s = js_read.read()
                    s = s.replace('\t','')  # Trailing commas in dict cause file read problems, these lines will fix it.
                    s = s.replace('\n','')
                    s = s.replace(',}','}')
                    s = s.replace(',]',']')
                    data = json.loads(s)
                
                pinned_instances = data["pinned-instances"][0]
                pinned_icons = data["pinned-icons"][0]

                # Unpin the instance
                for i in range(1, 10):
                    pinned_key = f"pinned{i}"
                    pinned_instances = data["pinned-instances"][0]
                    pinned_icons = data["pinned-icons"][0]
                    if pinned_instances[pinned_key] == name:
                        pinned_instances = data["pinned-instances"][0]
                        pinned_icons = data["pinned-icons"][0]
                        pinned_instances[pinned_key] = None
                        pinned_icons[pinned_key] = None
                        self.state_pinned[pinned_key] = "disabled"
                        def get_icon_PIL(icon_name):
                            if icon_name == None:
                                photo = Image.open("img/instance_icons/none.png")
                                photo = ct.CTkImage(photo)
                                return photo
                            else:
                                photo = Image.open(f"img/instance_icons/{icon_name}.png")
                                photo = ct.CTkImage(photo)
                                return photo
                        self.pinned_inst[pinned_key].configure(text="", state="disabled", image=get_icon_PIL(None))
                        data["all-instances"][0][str(inst_name)][0]["pinned"] = False
                        with open("launcherProfiles.json", "w") as js_write:
                            json.dump(data, js_write, indent=4)
                        print(f"Instance '{name}' unpinned successfully.")
                        break
                    else:
                        print("Error: Instance not found in pinned instances.")

            self.refresh_instances()
    def showAddInstanceWindow(self):
        try:
            self.addInstance_window.deiconify()
        except:
            self.addInstance()
            self.addInstance_window.deiconify()
    def addInstance(self):
        self.addInstance_window = ct.CTkToplevel(self)
        self.addInstance_window.title("Create new instance")
        self.addInstance_window.geometry("700x400")
        self.addInstance_window.resizable(False, False)
        self.addInstance_window.configure(bg="#262626")
        self.addInstance_window.after(200, lambda: self.addInstance_window.iconbitmap("img/icon.ico"))
        self.addInstance_window.protocol("WM_DELETE_WINDOW", lambda: self.addInstance_window.withdraw())
        self.addInstance_window.withdraw()
        with open("launcherProfiles.json", "r") as js_read:
            s = js_read.read()
            s = s.replace('\t','')
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            data = json.loads(s)
        icon_list = data["icons"]
        self.chosen_icon = None
        def chooseIcon(icon_name):
            self.chosen_icon = icon_name
            counter = 0
            for icon in icon_list:
                for i in range(1,18):
                    if icon[f"icon{i}"] is not None:
                        counter += 1
                        if icon_name == icon[f"icon{i}"]:
                            fg = "#1f6aa5"
                            hover = "#1a5380"
                        else:
                            fg = "transparent"
                            hover = "#1a1a1a"
                        self.icon_list.append(icon[f"icon{i}"])
                        self.icon_name = icon[f"icon{i}"]
                        self.icon_select_btn = ct.CTkButton(self.addInstance_window, text="", image=get_icon_PIL(icon[f"icon{i}"]), font=ct.CTkFont(size=30, family="Inter"), command=lambda icon_name=self.icon_name: chooseIcon(icon_name), height=50, width=50, corner_radius=5, anchor="center", fg_color=fg, bg_color="transparent", hover_color=hover, compound="left", )
                        self.icon_select_btn.place(x=220 + (i * 50), y=10)
                    else:
                        pass
        def get_icon_PIL(icon_name):
            if icon_name == None:
                photo = Image.open("img/instance_icons/none.png")
                photo = ct.CTkImage(photo, size=(35,35))
                return photo
            else:
                photo = Image.open(f"img/instance_icons/{icon_name}.png")
                photo = ct.CTkImage(photo, size=(35,35))
                return photo

        self.icon_list = []
        counter = 0
        for icon in icon_list:
            for i in range(1,18):
                if icon[f"icon{i}"] is not None:
                    counter += 1
                    self.icon_list.append(icon[f"icon{i}"])
                    self.icon_name = icon[f"icon{i}"]
                    self.icon_select_btn = ct.CTkButton(self.addInstance_window, text="", image=get_icon_PIL(icon[f"icon{i}"]), font=ct.CTkFont(size=30, family="Inter"), command=lambda icon_name=self.icon_name: chooseIcon(icon_name), height=50, width=50, corner_radius=5, anchor="center", fg_color="transparent", bg_color="transparent", hover_color="#1a1a1a", compound="left", )
                    self.icon_select_btn.place(x=220 + (i * 50), y=10)
                else:
                    pass
        name_va1r = ct.StringVar()
        self.name_entry1 = ct.CTkEntry(self.addInstance_window, font=ct.CTkFont(size=25, family="Inter"), width=400, textvariable=name_va1r,  placeholder_text="Name", placeholder_text_color="#b3b3b3")
        self.name_entry1.place(x=150, y=70)
        method_var = ct.StringVar()
        method_var.set("Vanilla")
        self.vanilla_versions = []
        self.forge_versions = []
        self.fabric_versions = []
        self.installed_versions = mc.utils.get_installed_versions(mc_dir)
        for version in self.available_versions:
            self.vanilla_versions.append(version["type"] + " " + version["id"])
        for version in self.forge_versions_all:
            self.forge_versions.append(version)
        for version in self.fabric_versions_all:
            self.fabric_versions.append(version["version"])
        version_var = ct.StringVar()
        version_var.set(self.vanilla_versions[0])
        self.chosen_version = str("Vanilla " + self.vanilla_versions[0])
        if self.vanilla_versions[0].startswith("release "):
                self.chosen_version_alone = self.vanilla_versions[0].strip("release ")
        elif self.vanilla_versions[0].startswith("snapshot "):
            self.chosen_version_alone = self.vanilla_versions[0].strip("snapshot ")
        def get_version_method(version):
            if version in self.vanilla_versions:
                return "Vanilla"
            elif version in self.forge_versions:
                return "Forge"
            elif version in self.fabric_versions:
                return "Fabric"
        
        def change_version(var):
            print(var)
            if not var in self.vanilla_versions:
                if not var in self.forge_versions:
                    if not var in self.fabric_versions:
                        msg.CTkMessagebox(title="Error", message="Invalid version selected.", icon="cancel")
                        return
            version_var.set(var)
            self.chosen_version = str(get_version_method(var)+ " " + var)
            if var.startswith("release "):
                self.chosen_version_alone = var.strip("release ")
            elif var.startswith("snapshot "):
                self.chosen_version_alone = var.strip("snapshot ")
            else:
                self.chosen_version_alone = var
            print(get_version_method(var),var)
        self.version_dropdown = ct.CTkComboBox(self.addInstance_window, command=change_version, values=self.vanilla_versions, variable=version_var, font=ct.CTkFont(size=15, family="Inter"), width=200, button_color="#565b5e", bg_color="transparent", button_hover_color="#3c3e41", fg_color="#343638", hover="#3c3e41")
        self.version_dropdown.place(x=270, y=130)
        self.version_dropdown.bind("<Return>", lambda event: change_version(version_var.get()))
        CTkScrollableDropdown(self.version_dropdown, values=self.vanilla_versions, justify="left", frame_corner_radius=5, command=change_version)
        def method_change(var):
            print(var)
            self.version_dropdown.destroy()
            if var == "Vanilla":
                version_var.set(self.vanilla_versions[0])
                self.chosen_version = str("Vanilla " + self.vanilla_versions[0])
                if self.vanilla_versions[0].startswith("release "):
                    self.chosen_version_alone = self.vanilla_versions[0].strip("release ")
                elif self.vanilla_versions[0].startswith("snapshot "):
                    self.chosen_version_alone = self.vanilla_versions[0].strip("snapshot ")
                self.version_dropdown = ct.CTkComboBox(self.addInstance_window, command=change_version, values=self.vanilla_versions, variable=version_var, font=ct.CTkFont(size=15, family="Inter"), width=200, button_color="#565b5e", bg_color="transparent", button_hover_color="#3c3e41", fg_color="#343638", hover="#3c3e41")
                self.version_dropdown.place(x=270, y=130)
                self.version_dropdown.bind("<Return>", lambda event: change_version(version_var.get()))
                CTkScrollableDropdown(self.version_dropdown, values=self.vanilla_versions, justify="left", frame_corner_radius=5, command=change_version)
            elif var == "Forge":
                version_var.set(self.forge_versions[0])
                self.chosen_version = str("Forge " + self.forge_versions[0])
                self.chosen_version_alone = self.forge_versions[0]
                self.version_dropdown = ct.CTkComboBox(self.addInstance_window, command=change_version, values=self.forge_versions, variable=version_var, font=ct.CTkFont(size=15, family="Inter"), width=200, button_color="#565b5e", bg_color="transparent", button_hover_color="#3c3e41", fg_color="#343638", hover="#3c3e41")
                self.version_dropdown.place(x=270, y=130)
                self.version_dropdown.bind("<Return>", lambda event: change_version(version_var.get()))
                CTkScrollableDropdown(self.version_dropdown, values=self.forge_versions, justify="left", frame_corner_radius=5, command=change_version)
            elif var == "Fabric":
                version_var.set(self.fabric_versions[0])
                self.chosen_version = str("Fabric " + self.fabric_versions[0])
                self.chosen_version_alone = self.fabric_versions[0]
                self.version_dropdown = ct.CTkComboBox(self.addInstance_window, command=change_version, values=self.fabric_versions, variable=version_var, font=ct.CTkFont(size=15, family="Inter"),width=200, button_color="#565b5e", bg_color="transparent", button_hover_color="#3c3e41", fg_color="#343638", hover="#3c3e41")
                self.version_dropdown.place(x=270, y=130)
                self.version_dropdown.bind("<Return>", lambda event: change_version(version_var.get()))
                CTkScrollableDropdown(self.version_dropdown, values=self.fabric_versions, justify="left", frame_corner_radius=5, command=change_version)
        self.method_dropdown = ct.CTkOptionMenu(self.addInstance_window,variable=method_var, font=ct.CTkFont(size=15, family="Inter"), values=["Vanilla", "Forge", "Fabric"], width=100, button_color="#565b5e", bg_color="transparent", button_hover_color="#3c3e41", fg_color="#343638", hover="#3c3e41", command=method_change)
        self.method_dropdown.place(x=150, y=130)
        def checkInstalled():
            isinstalled = False
            print(self.chosen_version_alone)
            if method_var.get() == "Vanilla":
                for version in self.installed_versions:
                    if self.chosen_version_alone == version["id"]:
                        isinstalled = True
                        break
                    else:
                        isinstalled = False
            else:
                pass
            if isinstalled == True:
                msg.CTkMessagebox(title="Instance already installed", message="This version is already installed.", icon="info")
            else:
                print("Not installed")
                self.handle_download(self.chosen_version)
        self.install_btn = ct.CTkButton(self.addInstance_window, text="Install", font=ct.CTkFont(size=15, family="Inter"), command=checkInstalled, corner_radius=5, anchor="center", width=60)
        self.install_btn.place(x=490, y=130)
        namevar = self.name_entry1.get()
        
        self.addinstance_btn = ct.CTkButton(self.addInstance_window, text="Add Instance", font=ct.CTkFont(size=20, family="Inter"), command=lambda: self.addinstance_fr(name=self.name_entry1.get(), version=self.chosen_version, icon=self.chosen_icon), corner_radius=5, anchor="center", width=120)
        self.addinstance_btn.place(x=270, y=180)

        
        #CTkScrollableDropdown(self.method_dropdown, values=["Vanilla", "Forge", "Fabric"], justify="left", frame_corner_radius=5, command=method_change)
    def addinstance_fr(self, name, version, icon):
        name = name.lstrip()
        print(name, version, icon)
        if icon == None:
            msg.CTkMessagebox(title="Error", message="Please choose all values.", icon="cancel")
            return
        if name == "":
            msg.CTkMessagebox(title="Error", message="Please choose all values.", icon="cancel")
            return
        if version.startswith("Vanilla"):
            method = "vanilla"
            version = version.partition(" ")[2]
            if version.startswith("release"):
                typee = "release"
                version = version.strip("release ")
            elif version.startswith("snapshot"):
                typee = "snapshot"
                split_string = version.split(' ')
                new_string_list = split_string[1:]
                new_string = ' '.join(new_string_list)
                version = new_string
            
        elif version.startswith("Forge"):
            version = version.partition(" ")[2]
            method = "forge"
            typee = "release"
        elif version.startswith("Fabric"):
            version = version.partition(" ")[2]
            method = "fabric"
            typee = "release"

        with open("launcherProfiles.json", "r") as js_read:
            s = js_read.read()
            s = s.replace('\t','')
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            data = json.loads(s)
        instances = data["all-instances"]
        new_instance = {
            name: [
                {
                    "name": name,
                    "version": version,
                    "method": method,
                    "type": typee,
                    "icon": icon,
                    "timePlayed": 0,
                    "mods": None,
                    "pinned": False
                }
            ]
        }
        instances[0].update(new_instance)
        data["all-instances"] = instances
        with open("launcherProfiles.json", "w") as js_write:
            json.dump(data, js_write, indent=4)
        self.addInstance_window.withdraw()
        msg.CTkMessagebox(title="Instance added", message=f"Instance '{name}' has been added successfully.", icon="info")
        self.refresh_instances()

        

    def choose_inst(self, inst, inst_ver):
        self.play.configure(text=f"Play\n{str(inst)}")
        data["selected-version"] = inst_ver
        data["selected-instance"] = inst
        with open("settings.json", "w") as js_write:
            json.dump(data, js_write, indent=4)
            js_write.close()

    def maximum(self, max_value, value):
        self.max_value[0] = value
    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        self.percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        self.filledLength = int(length * iteration // total)
        self.bar = fill * self.filledLength + '-' * (length - self.filledLength)

        self.install_progress.set(float(self.percent)/100)
        print('\r%s |%s| %s%% %s' % (prefix, self.bar, self.percent, suffix), end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()

    def install_mc_window(self, version):
        self.install_window = ct.CTkToplevel(self)
        self.install_window.title(f"Downloading Minecraft {version}")
        self.install_window.geometry("500x200")
        self.install_window.resizable(False, False)
        self.install_window.configure(bg="#262626")
        def disable_event():
            pass
        self.install_window.protocol("WM_DELETE_WINDOW", disable_event)
        self.install_window.after(200, lambda: self.install_window.iconbitmap("img/icon.ico"))
        self.install_window.grab_set()
        self.install_label = ct.CTkLabel(self.install_window, text=f"Installing Minecraft {version}", font=ct.CTkFont(size=15, family="Inter", weight="bold"), bg_color="transparent")
        self.install_label.place(x=20, y=20)
        self.install_progress = ct.CTkProgressBar(self.install_window, width=400, height=30, corner_radius=5, mode="determinate",progress_color="#1f6aa5")
        self.install_progress.place(x=50, y=100)
        self.cancel_btn = ct.CTkButton(self.install_window, text="Stop Download", font=ct.CTkFont(size=15, family="Inter"), command=self.stop_download, corner_radius=5, anchor="center", width=60)
        self.cancel_btn.place(x=200, y=150)

    def stop_download(self):
        '''restores the minimized original window and cancels the download.'''
        self.install_window.deiconify()
        self.dl_thread.join(timeout=3.0)
        print("Download terminated")
        #raise KeyboardInterrupt
    def handle_download(self, version):
        '''Starts the download thread'''
        self.install_mc_window(version)

        try:
            self.dl_thread = Thread(target=self.install_mc, args=(version,))
            self.dl_thread.start()
        except Exception as e:
            print(e)
    def install_mc(self, version):
        og_version = version
        self.max_value = [0]
        

        self.callback = {
            "setStatus": lambda text: print(text),
            "setProgress": lambda value: self.printProgressBar(value, self.max_value[0]),
            "setMax": lambda value: self.maximum(self.max_value, value)
        }

        if version.startswith("Vanilla"):
            version = version.partition(" ")[2]
            if version.startswith("release"):
                version = version.strip("release ")
            elif version.startswith("snapshot"):
                split_string = version.split(' ')
                new_string_list = split_string[1:]
                new_string = ' '.join(new_string_list)
                version = new_string
            print(f"Installing Minecraft {version}")
            mc.install.install_minecraft_version(version, mc_dir, callback=self.callback)
        elif version.startswith("Forge"):
            version = version.partition(" ")[2]

            if supports_automatic_install(version):
                print(f"Installing Minecraft Forge {version}")
                install_forge_version(version, mc_dir, callback=self.callback)

            else:
                run_forge_installer(version)

        elif version.startswith("Fabric"):
            version = version.partition(" ")[2]
            print(f"Installing Minecraft Fabric {version}")
            install_fabric(version, mc_dir, callback=self.callback)


        self.install_window.destroy()
        msg.CTkMessagebox(title="Installation complete", message=f"Minecraft {og_version} has been installed successfully.", icon="info")
            
            
            


    def runMinecraft(self):
        installed_versions = mc.utils.get_installed_versions(mc_dir)
        selected_ver = data["selected-version"]
        if selected_ver.startswith("vanilla"):
            selected_ver = selected_ver.partition(" ")[2]
            if selected_ver.startswith("release"):
                selected_ver = selected_ver.strip("release ")
            elif selected_ver.startswith("snapshot"):
                split_string = selected_ver.split(' ')
                new_string_list = split_string[1:]
                new_string = ' '.join(new_string_list)
                selected_ver = new_string

        elif selected_ver.startswith("forge"):
            selected_ver = selected_ver.partition(" ")[2]
            if selected_ver.startswith("release"):
                selected_ver = selected_ver.strip("release ")
        elif selected_ver.startswith("fabric"):
            selected_ver = selected_ver.partition(" ")[2]
            if selected_ver.startswith("release"):
                selected_ver = selected_ver.strip("release ")

        for version in installed_versions:
            if selected_ver == version["id"]:
                break
        else:
            msg.CTkMessagebox(title="Error", message="The selected version is not installed.", icon="cancel")
        '''Creates the thread on which minecraft is running'''
        self.t4 = Thread(target=self.launch_mc)
        self.t4.start()

        self.monitor_mc(self.t4)

    def monitor_mc(self, t4):
        '''Monitors the thread on which minecraft is running'''
        if self.t4.is_alive():
            self.after(100, lambda: self.monitor_mc(self.t4))
        else:
            t4.join(timeout=3.0)
            self.deiconify()

    def launch_mc(self):
        '''Runs minecraft with the specified settings'''
        with open("settings.json", "r") as js_read:
            s = js_read.read()
            s = s.replace('\t','')  #Trailing commas in dict cause file read problems, these lines will fix it.
            s = s.replace('\n','')  #Found this on stackoverflow.
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            data = json.loads(s)

        self.login_method = data["User-info"][0]["AUTH_TYPE"]
        self.detected_ver = ""
        self.runtime_ver = data["selected-version"]

        with open("settings.json", "r") as js_read1:
            self.s1 = js_read1.read()
            self.s1 = self.s1.replace('\t','')  #Trailing commas in dict cause file read problems, these lines will fix it.
            self.s1 = self.s1.replace('\n','')  #Found this on stackoverflow.
            self.s1 = self.s1.replace(',}','}')
            self.s1 = self.s1.replace(',]',']')
            self.data1 = json.loads(self.s1)

        self.mc_dir = data["Minecraft-home"]

        self.allocated_ram = self.data1["settings"][0]["allocated_ram"]

        self.modified_ram = self.allocated_ram//1
        self.ram_mb = int(self.modified_ram)

        self.ram_gb = self.allocated_ram//1000
        self.int_ram_gb = int(self.ram_gb)

        self.cpu_count = os.cpu_count()

        self.j1 = [f"-Xmx{int(self.ram_mb)}M", "-Xms128M"]

        data["settings"][0]["jvm-args"] = self.j1

        with open("settings.json", "w") as js_set:
            json.dump(data, js_set, indent=4)
            js_set.close()
        os.chdir(mc_dir)
        if connected == True:
            if self.runtime_ver.startswith("vanilla"):
                if self.login_method == "Microsoft":
                    try:
                        if data["selected-version"] == "vanilla snapshot":
                            self.mc_ver = str(data["selected-version"]).partition(" ")[2]
                        else:
                            self.mc_ver = str(data["selected-version"]).strip("vanilla ")
                        self.detected_ver = ""
                        if self.mc_ver.startswith("release"):
                            self.detected_ver = self.mc_ver.strip("release ")
                        elif self.mc_ver.startswith("snapshot"):
                            self.detected_ver = self.mc_ver.partition(' ')[2]
                        
                        with open("settings.json", "r") as js_read:
                            s = js_read.read()
                            s = s.replace('\t','')
                            s = s.replace('\n','')
                            s = s.replace(',}','}')
                            s = s.replace(',]',']')
                            data = json.loads(s)
                        refresh_token = data["Microsoft-settings"][0]["refresh_token"]
                        self.options = {
                            "username": msaoptions["username"],
                            "uuid": msaoptions["uuid"],
                            "token": msaoptions["token"],
                            "jvmArguments": self.j1,
                            "executablePath": javaPath,
                        }
                        selected_instance = data["selected-instance"]
                        
                        self.withdraw()
                        self.minecraft_command = mc.command.get_minecraft_command(self.detected_ver, self.mc_dir, self.options)
                        print(self.detected_ver)
                        print(f"Launching Minecraft {self.mc_ver}")
                        command = subprocess.Popen(
                            self.minecraft_command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,  # Combine stderr with stdout
                            text=True  # Decode output as text
                        )
                        
                        try:
                            last_line = None
                            log = ""
                            for line in command.stdout:
                                print(line, end='')
                                log += line + "\n"
                                last_line = line

                            minecraft_log = log
                            command.wait()

                        except:
                            pass
                        
                        '''Get crash report if it exists '''
                        if last_line.startswith("#@!@# Game crashed!"):
                            print("Game crashed! Getting crash report...")
                            match = regex.search(r"[A-Za-z]:\\[^\n]+", last_line)
                            if match:
                                crash_report_path = match.group()
                            else:
                                print("Failed to get crash report path")
                                crash_report_path = None
                            with open(crash_report_path, "r", encoding="utf8") as f:
                                crash_report = f.read()
                            self.showErrorWindow(crash_report, minecraft_log)
                        else:
                            pass
                    except mc.exceptions.VersionNotFound as e:
                        msg(title="Error", message=e, icon="cancel")

                elif self.login_method == "ElyBy":
                    self.ely_authenticate()
                    if data["selected-version"] == "vanilla snapshot":
                            self.mc_ver = str(data["selected-version"]).partition(" ")[2]
                    else:
                        self.mc_ver = str(data["selected-version"]).strip("vanilla ")
                    self.detected_ver = ""
                    if self.mc_ver.startswith("release"):
                        self.detected_ver = self.mc_ver.strip("release ")
                    elif self.mc_ver.startswith("snapshot"):
                        self.detected_ver = self.mc_ver.partition(' ')[2]
                    self.j2 = [r"-javaagent:{}\\authlib\\".format(currn_dir) + "" + f"authlib-injector-1.2.5.jar=ely.by", f"-Xmx{int(self.ram_mb)}M", "-Xms128M"]
                    self.options = {
                        "username": data["User-info"][0]["username"],
                        "uuid": data["User-info"][0]["UUID"],
                        "token": "",
                        "jvmArguments": self.j2,
                        "executablePath": javaPath,
                    }
                    self.withdraw()
                    self.minecraft_command = mc.command.get_minecraft_command(self.detected_ver, self.mc_dir, self.options)
                    print(self.detected_ver)
                    print(f"Launching Minecraft {self.mc_ver}")
                    command = subprocess.Popen(
                        self.minecraft_command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,  # Combine stderr with stdout
                        text=True  # Decode output as text
                    )
                    try:
                        last_line = None
                        log = ""
                        for line in command.stdout:
                            print(line, end='')
                            log += line + "\n"
                            last_line = line

                        minecraft_log = log
                        command.wait()
                    except:
                        pass
                    '''Get crash report if it exists '''
                    if last_line.startswith("#@!@# Game crashed!"):
                        print("Game crashed! Getting crash report...")
                        match = regex.search(r"[A-Za-z]:\\[^\n]+", last_line)
                        if match:
                            crash_report_path = match.group()
                        else:
                            print("Failed to get crash report path")
                            crash_report_path = None
                        with open(crash_report_path, "r", encoding="utf8") as f:
                            crash_report = f.read()
                        self.showErrorWindow(crash_report, minecraft_log)
                    else:
                        pass
                
                elif self.login_method == "Offline":
                    if data["selected-version"] == "vanilla snapshot":
                            self.mc_ver = str(data["selected-version"]).partition(" ")[2]
                    else:
                        self.mc_ver = str(data["selected-version"]).strip("vanilla ")
                    self.detected_ver = ""
                    if self.mc_ver.startswith("release"):
                        self.detected_ver = self.mc_ver.strip("release ")
                    elif self.mc_ver.startswith("snapshot"):
                        self.detected_ver = self.mc_ver.partition(' ')[2]
                    self.j2 = [r"-javaagent:{}\\authlib\\".format(currn_dir) + "" + f"authlib-injector-1.2.5.jar=ely.by", f"-Xmx{int(self.ram_mb)}M", "-Xms128M"]
                    self.options = {
                        "username": data["User-info"][0]["username"],
                        "uuid": data["User-info"][0]["UUID"],
                        "token": "",
                        "jvmArguments": self.j1,
                        "executablePath": javaPath,
                    }
                    self.withdraw()
                    self.minecraft_command = mc.command.get_minecraft_command(self.detected_ver, self.mc_dir, self.options)
                    print(self.detected_ver)
                    print(f"Launching Minecraft {self.mc_ver}")
                    command = subprocess.Popen(
                        self.minecraft_command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,  # Combine stderr with stdout
                        text=True  # Decode output as text
                    )
                    try:
                        last_line = None
                        log = ""
                        for line in command.stdout:
                            print(line, end='')
                            log += line + "\n"
                            last_line = line

                        minecraft_log = log
                        command.wait()
                    except:
                        pass
                    '''Get crash report if it exists '''
                    if last_line.startswith("#@!@# Game crashed!"):
                        print("Game crashed! Getting crash report...")
                        match = regex.search(r"[A-Za-z]:\\[^\n]+", last_line)
                        if match:
                            crash_report_path = match.group()
                        else:
                            print("Failed to get crash report path")
                            crash_report_path = None
                        with open(crash_report_path, "r", encoding="utf8") as f:
                            crash_report = f.read()
                        self.showErrorWindow(crash_report, minecraft_log)
                    else:
                        pass

            elif self.runtime_ver.startswith("forge"):
                if self.login_method == "Microsoft":
                    try:
                        self.mc_ver = data["selected-version"].strip("forge release ")
                        parts = self.mc_ver.split('-')
                        self.detected_ver1 = f"{parts[0]}-forge-{parts[1]}"
                        
                        with open("settings.json", "r") as js_read:
                            s = js_read.read()
                            s = s.replace('\t','')
                            s = s.replace('\n','')
                            s = s.replace(',}','}')
                            s = s.replace(',]',']')
                            data = json.loads(s)
                        refresh_token = data["Microsoft-settings"][0]["refresh_token"]
                        self.options = {
                            "username": msaoptions["username"],
                            "uuid": msaoptions["uuid"],
                            "token": msaoptions["token"],
                            "jvmArguments": self.j1,
                            "executablePath": javaPath,
                        }
                        selected_instance = data["selected-instance"]
                        selected_instance = currn_dir + "\\instances\\" + selected_instance + "\\mods"
                        instanceHasMods = False
                        if mods.Manager.doesInstanceHaveMods(selected_instance):
                            instanceHasMods = True
                            mods.Manager.transferModsOnRun(selected_instance, self.mc_dir)
                        else:
                            pass
                        self.withdraw()
                        self.minecraft_command = mc.command.get_minecraft_command(self.detected_ver1, self.mc_dir, self.options)
                        print(self.detected_ver)
                        print(f"Launching Minecraft {self.mc_ver}")
                        command = subprocess.Popen(
                            self.minecraft_command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,  # Combine stderr with stdout
                            text=True  # Decode output as text
                        )
                        try:
                            last_line = None
                            log = ""
                            for line in command.stdout:
                                print(line, end='')
                                log += line + "\n"
                                last_line = line

                            minecraft_log = log
                            command.wait()
                        except:
                            pass
                        if instanceHasMods:
                            mods.Manager.transferFilesBack(selected_instance, self.mc_dir)
                        else:
                            pass
                        '''Get crash report if it exists '''
                        if last_line.startswith("#@!@# Game crashed!"):
                            print("Game crashed! Getting crash report...")
                            match = regex.search(r"[A-Za-z]:\\[^\n]+", last_line)
                            if match:
                                crash_report_path = match.group()
                            else:
                                print("Failed to get crash report path")
                                crash_report_path = None
                            with open(crash_report_path, "r", encoding="utf8") as f:
                                crash_report = f.read()
                            self.showErrorWindow(crash_report, minecraft_log)
                        else:
                            pass
                    except mc.exceptions.VersionNotFound as e:
                        msg(title="Error", message=e, icon="cancel")

                elif self.login_method == "ElyBy":
                    self.ely_authenticate()
                    self.j2 = [r"-javaagent:{}\\authlib\\".format(currn_dir) + "" + f"authlib-injector-1.2.5.jar=ely.by", f"-Xmx{int(self.ram_mb)}M", "-Xms128M"]
                    self.mc_ver = data["selected-version"].strip("forge release ")
                    parts = self.mc_ver.split('-')
                    self.detected_ver1 = f"{parts[0]}-forge-{parts[1]}"
                    self.options = {
                        "username": data["User-info"][0]["username"],
                        "uuid": data["User-info"][0]["UUID"],
                        "token": "",
                        "jvmArguments": self.j2,
                        "executablePath": javaPath,
                    }
                    selected_instance = data["selected-instance"]
                    selected_instance = currn_dir + "\\instances\\" + selected_instance + "\\mods"
                    instanceHasMods = False
                    if mods.Manager.doesInstanceHaveMods(selected_instance):
                        instanceHasMods = True
                        mods.Manager.transferModsOnRun(selected_instance, self.mc_dir)
                    else:
                        pass
                    self.withdraw()
                    self.minecraft_command = mc.command.get_minecraft_command(self.detected_ver1, self.mc_dir, self.options)
                    print(self.detected_ver)
                    print(f"Launching Minecraft {self.mc_ver}")
                    command = subprocess.Popen(
                        self.minecraft_command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,  # Combine stderr with stdout
                        text=True  # Decode output as text
                    )
                    try:
                        last_line = None
                        log = ""
                        for line in command.stdout:
                            print(line, end='')
                            log += line + "\n"
                            last_line = line

                        minecraft_log = log
                        command.wait()
                    except:
                        pass
                    if instanceHasMods:
                        mods.Manager.transferFilesBack(selected_instance, self.mc_dir)
                    else:
                        pass
                    '''Get crash report if it exists '''
                    if last_line.startswith("#@!@# Game crashed!"):
                        print("Game crashed! Getting crash report...")
                        match = regex.search(r"[A-Za-z]:\\[^\n]+", last_line)
                        if match:
                            crash_report_path = match.group()
                        else:
                            print("Failed to get crash report path")
                            crash_report_path = None
                        with open(crash_report_path, "r", encoding="utf8") as f:
                            crash_report = f.read()
                        self.showErrorWindow(crash_report, minecraft_log)
                    else:
                        pass

                elif self.login_method == "Offline":
                    if data["selected-version"] == "vanilla snapshot":
                            self.mc_ver = str(data["selected-version"]).partition(" ")[2]
                    else:
                        self.mc_ver = str(data["selected-version"]).strip("vanilla ")
                    self.detected_ver = ""
                    if self.mc_ver.startswith("release"):
                        self.detected_ver = self.mc_ver.strip("release ")
                    elif self.mc_ver.startswith("snapshot"):
                        self.detected_ver = self.mc_ver.partition(' ')[2]
                    self.j2 = [r"-javaagent:{}\\authlib\\".format(currn_dir) + "" + f"authlib-injector-1.2.5.jar=ely.by", f"-Xmx{int(self.ram_mb)}M", "-Xms128M"]
                    self.options = {
                        "username": data["User-info"][0]["username"],
                        "uuid": data["User-info"][0]["UUID"],
                        "token": "",
                        "jvmArguments": self.j1,
                        "executablePath": javaPath,
                    }
                    self.mc_ver = data["selected-version"].strip("forge release ")
                    parts = self.mc_ver.split('-')
                    self.detected_ver1 = f"{parts[0]}-forge-{parts[1]}"
                    selected_instance = data["selected-instance"]
                    selected_instance = currn_dir + "\\instances\\" + selected_instance + "\\mods"
                    instanceHasMods = False
                    if mods.Manager.doesInstanceHaveMods(selected_instance):
                        instanceHasMods = True
                        mods.Manager.transferModsOnRun(selected_instance, self.mc_dir)
                    else:
                        pass
                    self.withdraw()
                    self.minecraft_command = mc.command.get_minecraft_command(self.detected_ver1, self.mc_dir, self.options)
                    print(self.detected_ver)
                    print(f"Launching Minecraft {self.mc_ver}")
                    command = subprocess.Popen(
                        self.minecraft_command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,  # Combine stderr with stdout
                        text=True  # Decode output as text
                    )
                    try:
                        last_line = None
                        log = ""
                        for line in command.stdout:
                            print(line, end='')
                            log += line + "\n"
                            last_line = line

                        minecraft_log = log
                        command.wait()
                    except:
                        pass
                    if instanceHasMods:
                        mods.Manager.transferFilesBack(selected_instance, self.mc_dir)
                    else:
                        pass
                    '''Get crash report if it exists '''
                    if last_line.startswith("#@!@# Game crashed!"):
                        print("Game crashed! Getting crash report...")
                        match = regex.search(r"[A-Za-z]:\\[^\n]+", last_line)
                        if match:
                            crash_report_path = match.group()
                        else:
                            print("Failed to get crash report path")
                            crash_report_path = None
                        with open(crash_report_path, "r", encoding="utf8") as f:
                            crash_report = f.read()
                        self.showErrorWindow(crash_report, minecraft_log)
                    else:
                        pass

            elif self.runtime_ver.startswith("fabric"):
                self.lv = get_latest_loader_version()
                if self.login_method == "Microsoft":
                    try:
                        self.mc_ver = str(data["selected-version"]).partition(" ")[2]
                        self.detected_ver = ""
                        if self.mc_ver.startswith("release"):
                            self.detected_ver = self.mc_ver.strip("release ")
                        elif self.mc_ver.startswith("snapshot"):
                            self.detected_ver = self.mc_ver.partition(' ')[2]

                        self.v1 = self.detected_ver[:6]
                        self.detected_ver2 = f"fabric-loader-{self.lv}-{self.v1}"
                        
                        with open("settings.json", "r") as js_read:
                            s = js_read.read()
                            s = s.replace('\t','')
                            s = s.replace('\n','')
                            s = s.replace(',}','}')
                            s = s.replace(',]',']')
                            data = json.loads(s)
                        refresh_token = data["Microsoft-settings"][0]["refresh_token"]
                        self.options = {
                            "username": msaoptions["username"],
                            "uuid": msaoptions["uuid"],
                            "token": msaoptions["token"],
                            "jvmArguments": self.j1,
                            "executablePath": javaPath,
                        }
                        selected_instance = str(data["selected-instance"])
                        selected_instance = currn_dir + "\\instances\\" + selected_instance + "\\mods" #A bug that really irritated me so i had to specify this stuff
                        print(selected_instance)
                        if mods.Manager.doesInstanceHaveMods(selected_instance):
                            instanceHasMods = True
                            mods.Manager.transferModsOnRun(selected_instance, self.mc_dir)
                        else:
                            pass
                        self.withdraw()
                        self.minecraft_command = mc.command.get_minecraft_command(self.detected_ver2, self.mc_dir, self.options)
                        print(self.detected_ver)
                        print(f"Launching Minecraft {self.mc_ver}")
                        command = subprocess.Popen(
                            self.minecraft_command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,  # Combine stderr with stdout
                            text=True  # Decode output as text
                        )
                        try:
                            last_line = None
                            log = ""
                            for line in command.stdout:
                                print(line, end='')
                                log += line + "\n"
                                last_line = line

                            minecraft_log = log
                            command.wait()
                        except:
                            pass
                        if instanceHasMods:
                            mods.Manager.transferFilesBack(selected_instance, self.mc_dir)
                        else:
                            pass
                        '''Get crash report if it exists '''
                        if last_line.startswith("#@!@# Game crashed!"):
                            print("Game crashed! Getting crash report...")
                            match = regex.search(r"[A-Za-z]:\\[^\n]+", last_line)
                            if match:
                                crash_report_path = match.group()
                            else:
                                print("Failed to get crash report path")
                                crash_report_path = None
                            with open(crash_report_path, "r", encoding="utf8") as f:
                                crash_report = f.read()
                            self.showErrorWindow(crash_report, minecraft_log)
                        else:
                            pass
                    except mc.exceptions.VersionNotFound as e:
                        msg(title="Error", message=e, icon="cancel")

                elif self.login_method == "ElyBy":
                    self.ely_authenticate()
                    self.j2 = [r"-javaagent:{}\\authlib\\".format(currn_dir) + "" + f"authlib-injector-1.2.5.jar=ely.by", f"-Xmx{int(self.ram_mb)}M", "-Xms128M"]
                    self.mc_ver = str(data["selected-version"]).partition(" ")[2]
                    self.detected_ver = ""
                    if self.mc_ver.startswith("release"):
                        self.detected_ver = self.mc_ver.strip("release ")
                    elif self.mc_ver.startswith("snapshot"):
                        self.detected_ver = self.mc_ver.partition(' ')[2]

                    self.v1 = self.detected_ver[:6]
                    self.detected_ver2 = f"fabric-loader-{self.lv}-{self.v1}"
                    
                    self.options = {
                        "username": data["User-info"][0]["username"],
                        "uuid": data["User-info"][0]["UUID"],
                        "token": "",
                        "jvmArguments": self.j2,
                        "executablePath": javaPath,
                    }
                    selected_instance = data["selected-instance"]
                    selected_instance = currn_dir + "\\instances\\" + selected_instance + "\\mods"
                    instanceHasMods = False
                    if mods.Manager.doesInstanceHaveMods(selected_instance):
                        instanceHasMods = True
                        mods.Manager.transferModsOnRun(selected_instance, self.mc_dir)
                    else:
                        pass
                    self.withdraw()
                    self.minecraft_command = mc.command.get_minecraft_command(self.detected_ver2, self.mc_dir, self.options)
                    print(self.detected_ver)
                    print(f"Launching Minecraft {self.mc_ver}")
                    command = subprocess.Popen(
                        self.minecraft_command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,  # Combine stderr with stdout
                        text=True  # Decode output as text
                    )
                    try:
                        last_line = None
                        log = ""
                        for line in command.stdout:
                            print(line, end='')
                            log += line + "\n"
                            last_line = line

                        minecraft_log = log
                        command.wait()
                    except:
                        pass
                    if instanceHasMods:
                        mods.Manager.transferFilesBack(selected_instance, self.mc_dir)
                    else:
                        pass
                    '''Get crash report if it exists '''
                    if last_line.startswith("#@!@# Game crashed!"):
                        print("Game crashed! Getting crash report...")
                        match = regex.search(r"[A-Za-z]:\\[^\n]+", last_line)
                        if match:
                            crash_report_path = match.group()
                        else:
                            print("Failed to get crash report path")
                            crash_report_path = None
                        with open(crash_report_path, "r", encoding="utf8") as f:
                            crash_report = f.read()
                        self.showErrorWindow(crash_report, minecraft_log)
                    else:
                        pass
                
                elif self.login_method == "Offline":
                    if data["selected-version"] == "vanilla snapshot":
                            self.mc_ver = str(data["selected-version"]).partition(" ")[2]
                    else:
                        self.mc_ver = str(data["selected-version"]).strip("vanilla ")
                    self.detected_ver = ""
                    if self.mc_ver.startswith("release"):
                        self.detected_ver = self.mc_ver.strip("release ")
                    elif self.mc_ver.startswith("snapshot"):
                        self.detected_ver = self.mc_ver.partition(' ')[2]
                    self.j2 = [r"-javaagent:{}\\authlib\\".format(currn_dir) + "" + f"authlib-injector-1.2.5.jar=ely.by", f"-Xmx{int(self.ram_mb)}M", "-Xms128M"]
                    self.options = {
                        "username": data["User-info"][0]["username"],
                        "uuid": data["User-info"][0]["UUID"],
                        "token": "",
                        "jvmArguments": self.j1,
                        "executablePath": javaPath,
                    }
                    self.mc_ver = str(data["selected-version"]).partition(" ")[2]
                    self.detected_ver = ""
                    if self.mc_ver.startswith("release"):
                        self.detected_ver = self.mc_ver.strip("release ")
                    elif self.mc_ver.startswith("snapshot"):
                        self.detected_ver = self.mc_ver.partition(' ')[2]

                    self.v1 = self.detected_ver[:6]
                    self.detected_ver2 = f"fabric-loader-{self.lv}-{self.v1}"
                    selected_instance = data["selected-instance"]
                    selected_instance = currn_dir + "\\instances\\" + selected_instance + "\\mods"
                    instanceHasMods = False
                    if mods.Manager.doesInstanceHaveMods(selected_instance):
                        instanceHasMods = True
                        mods.Manager.transferModsOnRun(selected_instance, self.mc_dir)
                    else:
                        pass
                    self.withdraw()
                    self.minecraft_command = mc.command.get_minecraft_command(self.detected_ver2, self.mc_dir, self.options)
                    print(self.detected_ver)
                    print(f"Launching Minecraft {self.mc_ver}")
                    command = subprocess.Popen(
                        self.minecraft_command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,  # Combine stderr with stdout
                        text=True  # Decode output as text
                    )
                    try:
                        last_line = None
                        log = ""
                        for line in command.stdout:
                            print(line, end='')
                            log += line + "\n"
                            last_line = line

                        minecraft_log = log
                        command.wait()
                    except:
                        pass
                    if instanceHasMods:
                        mods.Manager.transferFilesBack(selected_instance, self.mc_dir)
                    else:
                        pass
                    '''Get crash report if it exists '''
                    if last_line.startswith("#@!@# Game crashed!"):
                        print("Game crashed! Getting crash report...")
                        match = regex.search(r"[A-Za-z]:\\[^\n]+", last_line)
                        if match:
                            crash_report_path = match.group()
                        else:
                            print("Failed to get crash report path")
                            crash_report_path = None
                        with open(crash_report_path, "r", encoding="utf8") as f:
                            crash_report = f.read()
                        self.showErrorWindow(crash_report, minecraft_log)
                    else:
                        pass
        os.chdir(currn_dir)
            
        
    def showErrorWindow(self, crash_report, minecraft_log):
        '''Shows the error window with the crash report'''
        self.error_window = ct.CTkToplevel(self)
        self.error_window.title("Minecraft Crashed!")
        self.error_window.geometry("500x510")
        self.error_window.resizable(False, False)
        self.error_window.configure(bg="#262626")
        self.error_window.after(200, lambda: self.error_window.iconbitmap("img/icon.ico"))
        self.error_window.grab_set()
        
        self.scrollableTextBox = ct.CTkScrollableFrame(self.error_window, corner_radius=10, height=420, width=440, fg_color="#2b2b2b", bg_color="transparent")
        self.scrollableTextBox.place(x=20, y=20)
        
        self.crash_report_text = ct.CTkLabel(self.scrollableTextBox, text=crash_report, text_color="white", font=ct.CTkFont(size=15, family="Inter"), anchor="nw", wraplength=420, justify="left")
        self.crash_report_text.pack(padx=10, pady=10, fill="both", expand=True)
        def hideFullLog():
            self.crash_report_text.configure(text=crash_report)
            self.showFullLog_btn.configure(text="Show Full Log", command=showFullLog)
        def showFullLog():
            self.crash_report_text.configure(text=minecraft_log)
            self.showFullLog_btn.configure(text="Hide Full Log", command=hideFullLog)

        def copyToClipboard(text):
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update()
        self.closeWindow = ct.CTkButton(self.error_window, text="Close", font=ct.CTkFont(size=15, family="Inter"), command=self.error_window.destroy, height=30, width=80, corner_radius=5, anchor="center")
        self.closeWindow.place(x=390, y=470)
        self.showFullLog_btn = ct.CTkButton(self.error_window, text="Show Full Log", font=ct.CTkFont(size=15, family="Inter"), command=showFullLog, height=30, width=120, corner_radius=5, anchor="center")
        self.showFullLog_btn.place(x=250, y=470)
        self.copyLog_btn = ct.CTkButton(self.error_window, text="Copy Log", font=ct.CTkFont(size=15, family="Inter"), command=lambda: self.copyToClipboard(minecraft_log), height=30, width=80, corner_radius=5, anchor="center")
        self.copyLog_btn.place(x=20, y=470)
    def ely_authenticate(self):
        '''Connects to ely.by for user authorization'''

        self.usr = data["User-info"][0]["username"]
        self.pwd = data["User-info"][0]["cracked_password"]
        self.client_token = str(uuid.uuid4())

        self.acc_data ={
            "username": self.usr,
            "password": self.pwd,
            "clientToken" : self.client_token,
            "requestUser" : True
        }


        self.r = requests.get(f"https://authserver.ely.by/api/users/profiles/minecraft/{self.usr}")
        if self.r.status_code == 200:
            print("[ElyBy]", "User found, getting details........")
            self.r1 = requests.post(f"https://authserver.ely.by/auth/authenticate", data=self.acc_data)
            if self.r1.status_code == 200:
                self.accessToken = self.r1.json()["accessToken"]
                self.uid = self.r1.json()["user"]["id"]

                data["User-info"][0]["UUID"] = self.uid
                data["clientToken"] = self.client_token
                data["accessToken"] = self.accessToken

                with open("settings.json", "w") as f:
                    json.dump(data, f, indent=4 )
                    f.close()

                '''with open("user_details.json", "r") as js_read:
                    s = js_read.read()
                    s = s.replace('\t','')  #Trailing commas in dict cause file read problems, these lines will fix it.
                    s = s.replace('\n','')
                    s = s.replace(',}','}')
                    s = s.replace(',]',']')
                    data1 = json.loads(s)
                    print(json.dumps(data1, indent=4))'''

            elif self.r1.status_code == 404:
                msg(title="Error", message=f"Data entered is either incomplete or account is secured with Oauth2. Error code: {self.r1.status_code}", icon="cancel")
                print("Data entered is either incomplete or account is secured with Oauth2")
        elif self.r.status_code == 404:
            print("[ERROR] 404", "User does not exist.")
            msg(title="User not found", message=f"The specified user does not exist. Error code: {self.r.status_code}", icon="cancel")
    
class SplashScreen(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("Argon")
        width_of_window = 500
        height_of_window = 281
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width/2) - (width_of_window/2)
        y_coordinate = (screen_height/2) - (height_of_window/2)
        self.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
        self.resizable(False, False)
        def passs():
            pass
        self.protocol("WM_DELETE_WINDOW", lambda: passs())
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.grab_set()

        self.after(200, lambda: self.iconbitmap("img/icon.ico"))

        splash_num = random.randint(1, 5)
        if splash_num == 1:
            bg_var = "#fdfdfd"
            color_var = "white"
        elif splash_num == 2:
            bg_var = "#fdfdfd"
            color_var = "white"
        elif splash_num == 3:
            bg_var = "#fdfdfd"
            color_var = "white"
        elif splash_num == 4:
            splash_num = 5
            bg_var = "#f1f1f1"
            color_var = "white"
        elif splash_num == 5:
            bg_var = "#f1f1f1"
            color_var = "white"
        self.bg = ct.CTkImage(dark_image=Image.open(f"img/splashes/{splash_num}.png"), light_image=Image.open(f"img/splashes/{splash_num}.png"), size=(500, 281))
        self.bg_label = ct.CTkLabel(self, image=self.bg, text="")
        self.bg_label.place(x=0, y=0)

        self.logo = ct.CTkImage(dark_image=Image.open("img/logo.png"), light_image=Image.open("img/logo.png"), size=(100, 100))
        self.logo_label = ct.CTkLabel(self, image=self.logo, text="", bg_color="#a9a9a9")
        self.logo_label.place(x=40, y=80)
        pywinstyles.set_opacity(self.logo_label, color="#a9a9a9")

        
        self.name_label = ct.CTkLabel(self, text="Argon", font=ct.CTkFont(size=100, family="Inter", weight="bold"), bg_color=bg_var, text_color=color_var)
        self.name_label.place(x=160, y=65)

        pywinstyles.set_opacity(self.name_label, color=bg_var)
        def runArgon():
            app = Argon()
            app.mainloop()
        
        #argon_thread = Thread(target=runArgon, daemon=True)
        #argon_thread.start()

if __name__ == "__main__":
    app = Argon()
    app.mainloop()
