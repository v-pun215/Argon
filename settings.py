import os
import sys
import json
import platform
import psutil, getpass
import subprocess, minecraft_launcher_lib
currn_dir = os.getcwd()
usr_accnt = getpass.getuser()
mc_dir = minecraft_launcher_lib.utils.get_minecraft_directory()
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

svmem = psutil.virtual_memory()

try: 
    java_loc = os.getenv('JAVA_HOME').replace("\\", "/")+str("bin")
except AttributeError:
    print("Java is not installed, or it is not installed to the PATH (system environment variable). Please (re)install Java and try again.")
    os.system("pause")
    sys.exit()
settings = {
            "accessToken": None,
            "clientToken": None,
            "User-info" : [
                {
                    "username": None,
                    "AUTH_TYPE": None,
                    "UUID": None,
                    "cracked_password": None,
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
            "selected-version": None,
            "settings" : [
                {
                    "allocated_ram" : 3000,
                    "jvm-args": None,
                    "executablePath": java_loc,
                    "ramlimiterExceptionBypassed": False,
                    "ramlimiterExceptionBypassedSelected": False,
                    "verbose": False
                }
            ]
}
pinned_icons = {
                "pinned-icons" : [
                    {
                        "pinned1": None,
                        "pinned2": None,
                        "pinned3": None,
                        "pinned4": None,
                        "pinned5": None,
                        "pinned6": None,
                        "pinned7": None,
                        "pinned8": None,
                        "pinned9": None,
                    }
                ],
                "pinned-instances" : [
                    {
                        "pinned1": None,
                        "pinned2": None,
                        "pinned3": None,
                        "pinned4": None,
                        "pinned5": None,
                        "pinned6": None,
                        "pinned7": None,
                        "pinned8": None,
                        "pinned9": None,
                    }
                ],
                "icons" : [
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
                        "icon17": None,
                    }
                ],
                "all-instances" : [
                    {
                        
                    }
                ]
}
if not os.path.exists(r"{}/settings.json".format(currn_dir)):
    print("Settings file not found, creating one...")
    with open("settings.json", "w") as js_set:
        json.dump(settings, js_set, indent=4)
        js_set.close()
    first = True
else:
    pass
if not os.path.exists(r"{}/launcherProfiles.json".format(currn_dir)):
    print("Pinned icons file not found, creating one...")
    with open("launcherProfiles.json", "w") as js_set:
        json.dump(pinned_icons, js_set, indent=4)
        js_set.close()
    first = True
with open("settings.json", "r") as js_read:
    s = js_read.read()
    s = s.replace('\t','')  #Trailing commas in dict cause file read problems, these lines will fix it.
    s = s.replace('\n','')  #Found this on stackoverflow.
    s = s.replace(',}','}')
    s = s.replace(',]',']')
    data = json.loads(s)
    #print(json.dumps(data, indent=4,))

verbose = data["settings"][0]["verbose"]
def open1():
    CREATE_NO_WINDOW = 0x08000000
    subprocess.call("python main.py", creationflags=CREATE_NO_WINDOW)
if verbose == False:
    open1()
else:
    subprocess.call("python main.py")