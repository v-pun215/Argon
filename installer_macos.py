
'''
The installer does these things:
1. lets user choose install location
2. checks if Python is installed, if not, installs it
3. checks if Inter font is installed, if not, installs it
4. checks if Java is installed, if not, installs it
5. downloads the latest release of Argon from a private repository
6. extracts the release zip to the install location
7. installs the dependencies from requirements.txt
8. creates a app shortcut to the main.py file

'''


import customtkinter as ct
import PIL, tkinter
import wget
import zipfile
import requests
from CTkMessagebox import CTkMessagebox
import subprocess, sys, string, random, os
import platform
from pathlib import Path
import psutil
import minecraft_launcher_lib
import threading
import pwd


argonFont = ""

# EXE
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)    


version = "v1.4"



usr_accnt = pwd.getpwuid(os.getuid())[0]
mc_dir = minecraft_launcher_lib.utils.get_minecraft_directory()
svmem = psutil.virtual_memory()
currn_dir = os.getcwd()

# Detect if Java is installed
def is_java_installed():
    try:
        output = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT, universal_newlines=True)
        return "version" in output.lower()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

is_java = is_java_installed()
print(f"Java installed: {is_java}")


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

class ArgonInstaller(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        icon = tkinter.PhotoImage(file=resource_path("img/mac.png"))
        self.iconphoto(False, icon)
        #self.protocol("WM_DELETE_WINDOW", self.ays)
        self.resizable(False, False)
        self.title(f"Argon {version} Installer")
        
        'Page 1'
        self.page1 = ct.CTkFrame(self, corner_radius=0, fg_color="transparent", bg_color="transparent")
        self.page1.place(relwidth=1, relheight=1)
        self.logo = ct.CTkImage(dark_image=PIL.Image.open(resource_path("img/hello.png")), light_image=PIL.Image.open(resource_path("img/hello.png")), size=(120, 120))
        self.logo_label = ct.CTkLabel(self.page1, image=self.logo, text="")
        self.logo_label.place(relx=0.3, rely=0.42, anchor="center")
        heading = ct.CTkLabel(self.page1, text="Welcome!", font=(argonFont, 30, "bold"))
        heading.place(relx=0.55, rely=0.32, anchor="center")
        label = ct.CTkLabel(self.page1, text="This installer will guide you through the installation of Argon.", font=(argonFont, 15), wraplength=350, justify="left")
        label.place(relx=0.44, rely=0.4)

        self.next_button = ct.CTkButton(self.page1, text="Next", command=lambda: self.next_page(2), font=(argonFont, 15), width=80)
        self.next_button.place(relx=0.495, rely=0.55, anchor="center")
        self.cancel_button = ct.CTkButton(self.page1, text="Cancel", command=self.ays, font=(argonFont, 15), width=80)
        self.cancel_button.place(relx=0.63, rely=0.55, anchor="center")

        # below 
        self.v_label = ct.CTkLabel(self.page1, text=f"{version}", font=(argonFont, 15), text_color="#b3b3b3")
        self.v_label.place(x=10, rely=0.955, anchor="w")

        self.author_label = ct.CTkLabel(self.page1, text="Made by v-pun215.", font=(argonFont, 15), text_color="#b3b3b3")
        self.author_label.place(relx=0.89, rely=0.955, anchor="center")

        'Page 2'
        self.page2 = ct.CTkFrame(self, corner_radius=0, fg_color="transparent", bg_color="transparent")

        self.question = ct.CTkLabel(self.page2, text="License Agreement", font=(argonFont, 20, "bold"))
        self.question.place(relx=0.5, rely=0.1, anchor="center")

        self.next_button = ct.CTkButton(self.page2, text="Next", command=lambda: self.next_page(3, agreement=True), font=(argonFont, 15), width=80)
        self.next_button.place(relx=0.425, rely=0.9, anchor="center")
        self.cancel_button = ct.CTkButton(self.page2, text="Back", command=lambda: self.next_page(1), font=(argonFont, 15), width=80)
        self.cancel_button.place(relx=0.575, rely=0.9, anchor="center")
        with open(resource_path("LICENSE"), "r") as f:
            license_text = f.read()
        self.license_text_area = ct.CTkTextbox(self.page2, width=500, height=225, font=(argonFont, 15), text_color="white", wrap="word")
        self.license_text_area.bind("<Key>", lambda e: "break")
        self.license_text_area.insert(ct.INSERT, text=license_text)
        self.license_text_area.place(relx=0.5, rely=0.45, anchor="center")
        self.radio_var = ct.IntVar()
        self.radio_var.set(0)
        self.accept_radio = ct.CTkRadioButton(self.page2, variable=self.radio_var, text="I accept the license.", font=(argonFont, 15), text_color="white" ,value=1)
        self.accept_radio.place(relx=0.5, rely=0.8, anchor="center")

        # below 
        self.v_label = ct.CTkLabel(self.page2, text=f"{version}", font=(argonFont, 15), text_color="#b3b3b3")
        self.v_label.place(x=10, rely=0.955, anchor="w")

        self.author_label = ct.CTkLabel(self.page2, text="Made by v-pun215.", font=(argonFont, 15), text_color="#b3b3b3")
        self.author_label.place(relx=0.89, rely=0.955, anchor="center")

        'Page 3'
        self.page3 = ct.CTkFrame(self, corner_radius=0, fg_color="transparent", bg_color="transparent")
        self.title1 = ct.CTkLabel(self.page3, text="Choose Install Location", font=(argonFont, 20, "bold"))
        self.title1.place(relx=0.5, rely=0.2, anchor="center")

        default_dir = f'/Users/{usr_accnt}/Library/Application Support/Argon'
        self.dir_entry = ct.CTkEntry(self.page3, width=400, height=30, font=(argonFont, 20), text_color="white")
        self.dir_entry.insert(ct.END, default_dir)
        self.dir_entry.place(relx=0.5, rely=0.3, anchor="center")

        self.browse_button = ct.CTkButton(self.page3, text="Browse", command=self.browse, font=(argonFont, 15), width=80)
        self.browse_button.place(relx=0.5, rely=0.4, anchor="center")
        def save_dir():
            install_dir = self.dir_entry.get()
            print(install_dir)
            self.next_page(4)
            install_thread = threading.Thread(target=self.install, args=(install_dir,))
            install_thread.start()
        self.next_button = ct.CTkButton(self.page3, text="Install", command=lambda: save_dir(), font=(argonFont, 15), width=80)
        self.next_button.place(relx=0.425, rely=0.9, anchor="center")
        self.cancel_button = ct.CTkButton(self.page3, text="Back", command=lambda: self.next_page(2), font=(argonFont, 15), width=80)
        self.cancel_button.place(relx=0.575, rely=0.9, anchor="center")

        #below 
        self.v_label = ct.CTkLabel(self.page3, text=f"{version}", font=(argonFont, 15), text_color="#b3b3b3")
        self.v_label.place(x=10, rely=0.955, anchor="w")

        self.author_label = ct.CTkLabel(self.page3, text="Made by v-pun215.", font=(argonFont, 15), text_color="#b3b3b3")
        self.author_label.place(relx=0.89, rely=0.955, anchor="center")

        'Page 4'
        self.page4 = ct.CTkFrame(self, corner_radius=0, fg_color="transparent", bg_color="transparent")
        self.title1 = ct.CTkLabel(self.page4, text="Installing", font=(argonFont, 30, "bold"))
        self.title1.place(relx=0.5, rely=0.2, anchor="center")

        self.progress = ct.CTkProgressBar(self.page4, width=300, height=20, mode="indeterminate", corner_radius=5)
        self.progress.place(relx=0.5, rely=0.4, anchor="center")
        self.progress.start()

        self.status_label = ct.CTkLabel(self.page4, text="Starting Install", font=(argonFont, 15))
        self.status_label.place(relx=0.5, rely=0.48, anchor="center")

        self.cancel_button = ct.CTkButton(self.page4, text="Cancel", command=self.ays, font=(argonFont, 15), width=80)
        self.cancel_button.place(relx=0.5, rely=0.9, anchor="center")

        #below 
        self.v_label = ct.CTkLabel(self.page4, text=f"{version}", font=(argonFont, 15), text_color="#b3b3b3")
        self.v_label.place(x=10, rely=0.955, anchor="w")

        self.author_label = ct.CTkLabel(self.page4, text="Made by v-pun215.", font=(argonFont, 15), text_color="#b3b3b3")
        self.author_label.place(relx=0.89, rely=0.955, anchor="center")

        'Page 5'
        self.page5 = ct.CTkFrame(self, corner_radius=0, fg_color="transparent", bg_color="transparent")
        self.title1 = ct.CTkLabel(self.page5, text="Installation Complete!", font=(argonFont, 30, "bold"))
        self.title1.place(relx=0.5, rely=0.2, anchor="center")

        def exitee():
            self.destroy()
        self.description = ct.CTkLabel(self.page5, text="Argon Installer has finished installing Argon to your computer.", font=(argonFont, 15))
        self.description.place(relx=0.5, rely=0.3, anchor="center")
        self.next_button = ct.CTkButton(self.page5, text="Finish", command=lambda: exitee(), font=(argonFont, 15), width=80)
        self.next_button.place(relx=0.5, rely=0.8, anchor="center")

        #below 
        self.v_label = ct.CTkLabel(self.page5, text=f"{version}", font=(argonFont, 15), text_color="#b3b3b3")
        self.v_label.place(x=10, rely=0.955, anchor="w")

        self.author_label = ct.CTkLabel(self.page5, text="Made by v-pun215.", font=(argonFont, 15), text_color="#b3b3b3")
        self.author_label.place(relx=0.89, rely=0.955, anchor="center")






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
            if argonFont in file.lower() and (".tt" in file or ".ot" in file):
                return True
            
    def check_python_installed(self):
        try:
            output = subprocess.check_output(["python3", "--version"], stderr=subprocess.STDOUT, universal_newlines=True)
            version = output.split()[1]
            major_version = int(version.split('.')[0])
            return major_version >= 3 and major_version <= 10
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
        
    def mount_dmg(self, dmg_path):
        try:
            result = subprocess.run(
                ["hdiutil", "attach", dmg_path],
                capture_output=True,
                text=True,
                check=True
            )
            print("DMG mounted successfully.")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Failed to mount DMG.")
            print(e.stderr)


    def install(self, install_dir):
        print(install_dir)
        
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)
        
        os.chdir(install_dir)
        # Check Java Installation
        if not is_java:
            CTkMessagebox(title="Java not found", message="Java is not installed on your Mac. Please install Java 21 to continue.", icon="cancel")
            self.destroy()
            return
        # Python
        if not self.check_python_installed():
            message = CTkMessagebox(title="Python not found", message="Python is not installed on your Mac. Please install Python 3.10 or higher to continue.", icon="cancel")
            self.destroy()
            return
            

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
        os.system(f"pip3 install -r requirements.txt")

        # Add a file in the root directory to store the install location
        os.chdir(f"/users/{usr_accnt}")
        with open(".ArgonProfile", "w") as f:
            f.write(f"{install_dir}")

        # Create a shortcut to the main.py file
        os.chdir(install_dir)
        if version >= "v1.4":
            wget.download(url="https://argon-release.vercel.app/macos/Argon.dmg", out="Argon.dmg")
            self.mount_dmg("Argon.dmg")

        self.progress.stop()
        self.next_page(5)



app = ArgonInstaller()
app.mainloop()