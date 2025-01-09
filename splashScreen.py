
# Import module
from customtkinter import *
import ctypes
from PIL import Image
# Create object

def centerWindow(width, height, root):  # Return 4 values needed to center Window
    screen_width = root.winfo_screenwidth()  # Width of the screen
    screen_height = root.winfo_screenheight() # Height of the screen     
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    return int(x), int(y)
root = CTk()

# Adjust size
width_of_window = 427
height_of_window = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width/2)-(width_of_window/2)
y_coordinate = (screen_height/2)-(height_of_window/2)
root.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
# Use overrideredirect() method
root.resizable(False, False)
myappid = u'vpun215.argon.release.2.0' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Set title
logo_image = CTkImage(light_image=Image.open("img/logo.png"), dark_image=Image.open("img/logo.png"))
logo_label = CTkLabel(root, text="", font=("Inter", 50, "bold"), image=logo_image)
logo_label.place(relx=0.3, rely=0.1, anchor="center")
title_label = CTkLabel(root, text="Argon", font=("Inter", 50, "bold"))
title_label.place(relx=0.7, rely=0.1, anchor="center")
# Execute tkinter

root.after(10000, root.destroy)
root.mainloop()