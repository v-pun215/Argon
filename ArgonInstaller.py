# This file is meant to be packaged using Pyinstaller, hence all the nuances.

'''
The installer does these things:
1. lets user choose install location
2. checks if Python is installed, if not, installs it
3. checks if Inter font is installed, if not, installs it
4. checks if Java is installed, if not, installs it
5. downloads the latest release of Argon from a private repository
6. extracts the release zip to the install location
7. installs the dependencies from requirements.txt
8. creates a desktop shortcut to the main.py file

'''

import os
import subprocess
import wget
import sys
import ctypes
import subprocess
import customtkinter as ct
import ctypes, PIL
import wget
import zipfile
import winshell
import requests
from CTkMessagebox import CTkMessagebox
import subprocess, sys, string, random, os
import platform
from pathlib import Path
import psutil
import minecraft_launcher_lib
import threading
import pythoncom
try:
    import pyi_splash
    pyi_splash.close()
except ModuleNotFoundError:
    pass
# your code..........


# EXE
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)    


version = "v1.4"



usr_accnt = str(Path.home()).replace("\\", "/").split("/")[-1]
mc_dir = minecraft_launcher_lib.utils.get_minecraft_directory()
svmem = psutil.virtual_memory()
currn_dir = os.getcwd()
java_home = os.getenv("JAVA_HOME")+r"\\bin\\java.exe"
java_home = java_home.replace("\\", "/")
global isJava
isJava = True
try: 
    java_loc = os.getenv('JAVA_HOME').replace("\\", "/")+str(r"\\bin\\java.exe")
except:

    print("Java is not installed, or it is not installed to the PATH (system environment variable). Please (re)install Java and try again.")
    isJava = False
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
class ArgonInstaller(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.wm_iconbitmap(resource_path("img\\icon.ico"))
        #self.protocol("WM_DELETE_WINDOW", self.ays)
        self.resizable(False, False)
        self.title(f"Argon {version} Installer")
        'Page 1'
        if not isJava:
            response = CTkMessagebox(title="Error", message="Java is not installed, or it is not installed to the PATH (system environment variable). Would you like to download, install and Java to your PATH?", icon="cancel", option_2="Exit", option_1="Install Java Automatically")
            if response.get() == "Install Java Automatically":
                self.javaInstall()
            else:
                self.destroy()
                sys.exit(0)
        self.page1 = ct.CTkFrame(self, corner_radius=0, fg_color="transparent", bg_color="transparent")
        self.page1.place(relwidth=1, relheight=1)
        self.logo = ct.CTkImage(dark_image=PIL.Image.open(resource_path("img/hello.png")), light_image=PIL.Image.open(resource_path("img/hello.png")), size=(120, 120))
        self.logo_label = ct.CTkLabel(self.page1, image=self.logo, text="")
        self.logo_label.place(relx=0.3, rely=0.42, anchor="center")
        heading = ct.CTkLabel(self.page1, text="Welcome!", font=("inter", 30, "bold"))
        heading.place(relx=0.55, rely=0.32, anchor="center")
        label = ct.CTkLabel(self.page1, text="This installer will guide you through the installation of Argon.", font=("Inter", 15), wraplength=350, justify="left")
        label.place(relx=0.44, rely=0.4)

        self.next_button = ct.CTkButton(self.page1, text="Next", command=lambda: self.next_page(2), font=("Inter", 15), width=80)
        self.next_button.place(relx=0.495, rely=0.55, anchor="center")
        self.cancel_button = ct.CTkButton(self.page1, text="Cancel", command=self.ays, font=("Inter", 15), width=80)
        self.cancel_button.place(relx=0.63, rely=0.55, anchor="center")

        # below 
        self.v_label = ct.CTkLabel(self.page1, text=f"{version}", font=("Inter", 15), text_color="#b3b3b3")
        self.v_label.place(x=10, rely=0.955, anchor="w")

        self.author_label = ct.CTkLabel(self.page1, text="Made by v-pun215.", font=("Inter", 15), text_color="#b3b3b3")
        self.author_label.place(relx=0.89, rely=0.955, anchor="center")

        'Page 2'
        self.page2 = ct.CTkFrame(self, corner_radius=0, fg_color="transparent", bg_color="transparent")

        self.question = ct.CTkLabel(self.page2, text="License Agreement", font=("Inter", 20, "bold"))
        self.question.place(relx=0.5, rely=0.1, anchor="center")

        self.next_button = ct.CTkButton(self.page2, text="Next", command=lambda: self.next_page(3, agreement=True), font=("Inter", 15), width=80)
        self.next_button.place(relx=0.425, rely=0.9, anchor="center")
        self.cancel_button = ct.CTkButton(self.page2, text="Back", command=lambda: self.next_page(1), font=("Inter", 15), width=80)
        self.cancel_button.place(relx=0.575, rely=0.9, anchor="center")
        with open(resource_path("LICENSE"), "r") as f:
            license_text = f.read()
        self.license_text_area = ct.CTkTextbox(self.page2, width=500, height=225, font=("Inter", 15), text_color="white", wrap="word")
        self.license_text_area.bind("<Key>", lambda e: "break")
        self.license_text_area.insert(ct.INSERT, text=license_text)
        self.license_text_area.place(relx=0.5, rely=0.45, anchor="center")
        self.radio_var = ct.IntVar()
        self.radio_var.set(0)
        self.accept_radio = ct.CTkRadioButton(self.page2, variable=self.radio_var, text="I accept the license.", font=("Inter", 15), text_color="white" ,value=1)
        self.accept_radio.place(relx=0.5, rely=0.8, anchor="center")

        # below 
        self.v_label = ct.CTkLabel(self.page2, text=f"{version}", font=("Inter", 15), text_color="#b3b3b3")
        self.v_label.place(x=10, rely=0.955, anchor="w")

        self.author_label = ct.CTkLabel(self.page2, text="Made by v-pun215.", font=("Inter", 15), text_color="#b3b3b3")
        self.author_label.place(relx=0.89, rely=0.955, anchor="center")

        'Page 3'
        self.page3 = ct.CTkFrame(self, corner_radius=0, fg_color="transparent", bg_color="transparent")
        self.title1 = ct.CTkLabel(self.page3, text="Choose Install Location", font=("Inter", 20, "bold"))
        self.title1.place(relx=0.5, rely=0.2, anchor="center")

        default_dir = "C:/Users/"+usr_accnt+"/AppData/Roaming/Argon"
        self.dir_entry = ct.CTkEntry(self.page3, width=400, height=30, font=("Inter", 20), text_color="white")
        self.dir_entry.insert(ct.END, default_dir)
        self.dir_entry.place(relx=0.5, rely=0.3, anchor="center")

        self.browse_button = ct.CTkButton(self.page3, text="Browse", command=self.browse, font=("Inter", 15), width=80)
        self.browse_button.place(relx=0.5, rely=0.4, anchor="center")
        def save_dir():
            install_dir = self.dir_entry.get()
            print(install_dir)
            self.next_page(4)
            install_thread = threading.Thread(target=self.install, args=(install_dir,))
            install_thread.start()
        self.next_button = ct.CTkButton(self.page3, text="Install", command=lambda: save_dir(), font=("Inter", 15), width=80)
        self.next_button.place(relx=0.425, rely=0.9, anchor="center")
        self.cancel_button = ct.CTkButton(self.page3, text="Back", command=lambda: self.next_page(2), font=("Inter", 15), width=80)
        self.cancel_button.place(relx=0.575, rely=0.9, anchor="center")

        #below 
        self.v_label = ct.CTkLabel(self.page3, text=f"{version}", font=("Inter", 15), text_color="#b3b3b3")
        self.v_label.place(x=10, rely=0.955, anchor="w")

        self.author_label = ct.CTkLabel(self.page3, text="Made by v-pun215.", font=("Inter", 15), text_color="#b3b3b3")
        self.author_label.place(relx=0.89, rely=0.955, anchor="center")

        'Page 4'
        self.page4 = ct.CTkFrame(self, corner_radius=0, fg_color="transparent", bg_color="transparent")
        self.title1 = ct.CTkLabel(self.page4, text="Installing", font=("Inter", 30, "bold"))
        self.title1.place(relx=0.5, rely=0.2, anchor="center")

        self.progress = ct.CTkProgressBar(self.page4, width=300, height=20, mode="indeterminate", corner_radius=5)
        self.progress.place(relx=0.5, rely=0.4, anchor="center")
        self.progress.start()

        self.status_label = ct.CTkLabel(self.page4, text="Starting Install", font=("Inter", 15))
        self.status_label.place(relx=0.5, rely=0.48, anchor="center")

        self.cancel_button = ct.CTkButton(self.page4, text="Cancel", command=self.ays, font=("Inter", 15), width=80)
        self.cancel_button.place(relx=0.5, rely=0.9, anchor="center")

        #below 
        self.v_label = ct.CTkLabel(self.page4, text=f"{version}", font=("Inter", 15), text_color="#b3b3b3")
        self.v_label.place(x=10, rely=0.955, anchor="w")

        self.author_label = ct.CTkLabel(self.page4, text="Made by v-pun215.", font=("Inter", 15), text_color="#b3b3b3")
        self.author_label.place(relx=0.89, rely=0.955, anchor="center")

        'Page 5'
        self.page5 = ct.CTkFrame(self, corner_radius=0, fg_color="transparent", bg_color="transparent")
        self.title1 = ct.CTkLabel(self.page5, text="Installation Complete!", font=("Inter", 30, "bold"))
        self.title1.place(relx=0.5, rely=0.2, anchor="center")

        def exitee():
            self.destroy()
        self.description = ct.CTkLabel(self.page5, text="Argon Installer has finished installing Argon to your computer.", font=("Inter", 15))
        self.description.place(relx=0.5, rely=0.3, anchor="center")
        self.next_button = ct.CTkButton(self.page5, text="Finish", command=lambda: exitee(), font=("Inter", 15), width=80)
        self.next_button.place(relx=0.5, rely=0.8, anchor="center")

        #below 
        self.v_label = ct.CTkLabel(self.page5, text=f"{version}", font=("Inter", 15), text_color="#b3b3b3")
        self.v_label.place(x=10, rely=0.955, anchor="w")

        self.author_label = ct.CTkLabel(self.page5, text="Made by v-pun215.", font=("Inter", 15), text_color="#b3b3b3")
        self.author_label.place(relx=0.89, rely=0.955, anchor="center")

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    def javaInstall(self):
        if not self.is_admin():
            # Re-run the script with admin rights
            print("Requesting admin privileges...")
            script = sys.executable
            params = ' '.join([f'"{arg}"' for arg in sys.argv])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", script, params, None, 1)
            sys.exit()

        print("Running as admin.")
        # Configuration

        msi_url = "https://download.bell-sw.com/java/21.0.7+9/bellsoft-jdk21.0.7+9-windows-amd64.msi"
        msi_file = "bellsoft-jdk21.msi"
        install_dir = "C:\\Java\\BellSoft\\jdk-21"

        # Step 1: Download the MSI installer
        print("Downloading BellSoft JDK 21...")
        wget.download(msi_url, msi_file)
        print("\nDownload complete.")

        msi_file = "bellsoft-jdk21.msi"
        install_dir = "C:\\Java\\BellSoft\\jdk-21"
        # Step 2: Install silently using msiexec
        print("Installing Java 21 silently...")
        install_cmd = [
            "msiexec", "/i", msi_file,
            "/qn",  # quiet mode: no UI
            f"INSTALLDIR={install_dir}"
        ]
        subprocess.run(install_cmd, check=True)

        # Optional: delete the MSI installer
        os.remove(msi_file)

        print(f"Java 21 installed successfully in {install_dir}")
        CTkMessagebox(title="Success", message="Java 21 has been installed successfully.", icon="check")
        self.next_page(1)




    def browse(self):
        self.dir_entry.delete(0, ct.END)
        self.dir_entry.insert(ct.END, ct.filedialog.askdirectory())
        print(self.dir_entry.get())

    
    def ays(self):
        hello = CTkMessagebox(title="Exit", message="Are you sure you want to exit?", options=["Yes", "No"], icon="warning")
        response = hello.get()
        if response == "Yes":
            self.destroy()
        else:
            print("no")
            pass

    def next_page(self, page_num, agreement=False):
        
        if agreement == False:
            if page_num == 1:
                self.page1.place_forget()
                self.page2.place_forget()
                self.page3.place_forget()
                self.page1.place(relwidth=1, relheight=1)

            elif page_num == 2:
                self.page1.place_forget()
                self.page2.place_forget()
                self.page3.place_forget()
                self.page2.place(relwidth=1, relheight=1)

            elif page_num == 3:
                self.page1.place_forget()
                self.page2.place_forget()
                self.page3.place_forget()
                self.page3.place(relwidth=1, relheight=1)

            elif page_num == 4:
                self.page1.place_forget()
                self.page2.place_forget()
                self.page3.place_forget()
                self.page4.place(relwidth=1, relheight=1)

            elif page_num == 5:
                self.page1.place_forget()
                self.page2.place_forget()
                self.page3.place_forget()
                self.page4.place_forget()
                self.page5.place(relwidth=1, relheight=1)
        else:
            if self.radio_var.get() == 1:
                if page_num == 1:
                    self.page1.place_forget()
                    self.page2.place_forget()
                    self.page3.place_forget()
                    self.page1.place(relwidth=1, relheight=1)

                elif page_num == 2:
                    self.page1.place_forget()
                    self.page2.place_forget()
                    self.page3.place_forget()
                    self.page2.place(relwidth=1, relheight=1)

                elif page_num == 3:
                    self.page1.place_forget()
                    self.page2.place_forget()
                    self.page3.place_forget()
                    self.page3.place(relwidth=1, relheight=1)
            else:
                CTkMessagebox(title="Error", message="Please accept the license agreement to continue.", icon="cancel")

    
    def check_font_installed(self):
        file_list = os.listdir("C:/Windows/Fonts")

        for file in file_list:
            if "inter" in file.lower() and (".tt" in file or ".ot" in file):
                return True
            
    def check_python_installed(self):
        path = os.environ["PATH"]
        path = path.split(";")
        for folder in path:
            if "python" in folder.lower():
                return True

    def install(self, install_dir):
        print(install_dir)
        
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)
        
        os.chdir(install_dir)
        # Python
        if not self.check_python_installed():
            self.status_label.configure(text="Downloading Python 3.13.2")
            wget.download(url="https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe")
            os.system("python-3.13.2-amd64.exe")
            os.remove("python-3.13.2-amd64.exe")


        # Download release from private repository of releases (zips)
        self.status_label.configure(text="Downloading Argon...")
        wget.download(url=f"https://argon-release.vercel.app/zips/Argon-{version}.zip")
        
        self.status_label.configure(text="Extracting Argon zip")
        # Extract it
        with zipfile.ZipFile(f"Argon-{version}.zip", "r") as zip_ref:
            zip_ref.extractall(install_dir)

        os.remove(f"Argon-{version}.zip")

        # Install dependencies
        self.status_label.configure(text="Installing Python dependencies")
        os.system(f"pip install -r requirements.txt")

        # Install Inter font
        if not self.check_font_installed() == True:
            self.status_label.configure(text="Downloading and installing fonts")
            os.mkdir("fonts")
            os.chdir("fonts")
            wget.download("https://argon-release.vercel.app/windows/ArgonInstaller.exe") # Downloads FontReg (renamed ArgonInstaller because why not)
            wget.download("https://argon-release.vercel.app/fonts/Inter.ttc") # Downloads Inter font (ttc)
            os.system("ArgonInstaller /copy")


        # Create Desktop Shortcut
        pythoncom.CoInitialize()
        os.chdir(install_dir)
        link_filepath = os.path.join(winshell.desktop(), "Argon.lnk")

        with winshell.shortcut(link_filepath) as link:
            link.path = f"{install_dir}/main.py"
            link.description = "Launches Argon."
            link.icon_location = (f"{install_dir}/img/icon.ico", 0)
            link.working_directory = install_dir

        # Create Start Menu Shortcut
        link_filepath = os.path.join(winshell.start_menu(), "Argon.lnk")

        with winshell.shortcut(link_filepath) as link:
            link.path = f"{install_dir}/main.py"
            link.description = "Launches Argon."
            link.icon_location = (f"{install_dir}/img/icon.ico", 0)
            link.working_directory = install_dir

        
        
        self.progress.stop()
        self.next_page(5)



app = ArgonInstaller()
app.mainloop()
