from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtCore import QUrl, QLocale
import minecraft_launcher_lib
import json
import sys
import os
from keys import secret, client


redirect = "https://eclient-done.vercel.app/"
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
allocated_ram = data["settings"][0]["allocated_ram"]
jvm_args = data["settings"][0]["jvm-args"]
ramlimiterExceptionBypassed = data["settings"][0]["ramlimiterExceptionBypassed"]
ramlimiterExceptionBypassedSelected = data["settings"][0]["ramlimiterExceptionBypassedSelected"]
verbose = data["settings"][0]["verbose"]
refresh_token = data["Microsoft-settings"][0]["refresh_token"]

class LoginWindow(QWebEngineView):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login to Microsoft Account")

        # Set the path where the refresh token is saved
        self.refresh_token_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "refresh_token.json")

        # Open the login url
        login_url, self.state, self.code_verifier = minecraft_launcher_lib.microsoft_account.get_secure_login_data(client, redirect)
        self.load(QUrl(login_url))

        # Connects a function that is called when the url changed
        self.urlChanged.connect(self.new_url)

        self.show()

    def new_url(self, url: QUrl):
        try:
            # Get the code from the url
            auth_code = minecraft_launcher_lib.microsoft_account.parse_auth_code_url(url.toString(), self.state)
            # Do the login
            account_information = minecraft_launcher_lib.microsoft_account.complete_login(client, secret, redirect, auth_code, self.code_verifier)
            # Show the login information
            data["Microsoft-settings"][0]["refresh_token"] = account_information["refresh_token"]
            data["User-info"][0]["AUTH_TYPE"] = "Microsoft"
            with open("settings.json", "w") as f:
                json.dump(data, f, indent=4 )
                f.close()
            self.show_account_information(account_information)
        except AssertionError:
            print("States do not match!")
        except KeyError:
            print("Url not valid.")

    def show_account_information(self, information_dict):
        information_string = f'Username: {information_dict["name"]}<br>'
        information_string += f'UUID: {information_dict["id"]}<br>'
        information_string += f'Token: {information_dict["access_token"]}<br>'
        print(information_string)
        data["User-info"][0]["username"] = information_dict["name"]
        data["User-info"][0]["UUID"] = information_dict["id"]
        data["accessToken"] = information_dict["access_token"]
        data["Microsoft-settings"][0]["refresh_token"] = information_dict["refresh_token"]
        data["User-info"][0]["AUTH_TYPE"] = "Microsoft"
        with open("settings.json", "w") as f:
            json.dump(data, f, indent=4 )
            f.close()

        message_box = QMessageBox()
        message_box.setWindowTitle("Logged In")
        message_box.setText("You have successfully logged in, {}".format(information_dict["name"]))
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()
        

def Authenticate():
    app = QApplication(sys.argv)
    QWebEngineProfile.defaultProfile().setHttpAcceptLanguage(QLocale.system().name().split("_")[0])
    w = LoginWindow()
    app.exec()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # This line sets the language of the webpage to the system language
    QWebEngineProfile.defaultProfile().setHttpAcceptLanguage(QLocale.system().name().split("_")[0])
    w = LoginWindow()
    sys.exit(app.exec())
