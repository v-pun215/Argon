# This is a WIP, not working as of now

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

version = "v1.0-stable"



usr_accnt = str(Path.home()).replace("\\", "/").split("/")[-1]
mc_dir = minecraft_launcher_lib.utils.get_minecraft_directory()
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

ct.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ct.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
myappid = u'vpun215.argon.release.1.0' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
class WelcomeToArgon(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.wm_iconbitmap("img/icon.ico")
        self.resizable(False, False)
        self.title("Argon Setup")
        
        heading = ct.CTkLabel(self, text="Welcome to the Argon Installer", font=("inter", 30))
        heading.place(x=10, y=10)
        label = ct.CTkLabel(self, text="This installer will guide you through the installation of Argon.", font=("Inter", 15))
        label.place(x=10, y=70)



    



app = WelcomeToArgon()
app.mainloop()