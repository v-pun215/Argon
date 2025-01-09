from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import base64
import os
from PIL import Image
import json
def render_skin(skinPath):
    with open("settings.json", "r") as js_read:
        s = js_read.read()
        s = s.replace('\t','')  #Trailing commas in dict cause file read problems, these lines will fix it.
        s = s.replace('\n','')  #Found this on stackoverflow.
        s = s.replace(',}','}')
        s = s.replace(',]',']')
        data = json.loads(s)
        #print(json.dumps(data, indent=4,))

    username = data["User-info"][0]["username"]

    currn_dir = os.getcwd().replace("\\", "/")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://mchorse.github.io/mchead/")
    time.sleep(2)
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(f"{currn_dir}/{skinPath}")
    time.sleep(1)
    y = driver.find_element(By.NAME, "y")
    y.clear()
    y.send_keys("43")
    y.send_keys(Keys.RETURN)
    x = driver.find_element(By.NAME, "x")
    x.clear()
    x.send_keys("20")
    x.send_keys(Keys.RETURN)
    time.sleep(1)
    img = driver.find_element(By.ID, "output")
    render = img.get_attribute("src")
    driver.close()
    decodedData = base64.b64decode((render.removeprefix("data:image/png;base64,")))
  
    # Write Image from Base64 File
    imgFile = open(f'img/user/uncropped.png', 'wb')
    imgFile.write(decodedData)
    imgFile.close()

    # Crop the image
    img = Image.open(f"img/user/uncropped.png")
    width, height = img.size

    left = 30
    top = 100
    right = 220
    bottom = 3 * height / 5

    im1 = img.crop((left, top+25, right, bottom))
    newsize = (144, 138)
    im1 = im1.resize(newsize)
    im1.save(f"img/user/ely-{username}.png")
    os.remove("img/user/uncropped.png")

def render_iso_skin(skinPath):
    with open("settings.json", "r") as js_read:
        s = js_read.read()
        s = s.replace('\t','')  #Trailing commas in dict cause file read problems, these lines will fix it.
        s = s.replace('\n','')  #Found this on stackoverflow.
        s = s.replace(',}','}')
        s = s.replace(',]',']')
        data = json.loads(s)
        #print(json.dumps(data, indent=4,))

    username = data["User-info"][0]["username"]

    currn_dir = os.getcwd().replace("\\", "/")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://mchorse.github.io/mchead/")
    time.sleep(2)
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(f"{currn_dir}/{skinPath}")
    body_checkbox = driver.find_element(By.NAME, "head")
    body_checkbox.click()
    time.sleep(1)
    y = driver.find_element(By.NAME, "y")
    y.clear()
    y.send_keys("43")
    y.send_keys(Keys.RETURN)
    x = driver.find_element(By.NAME, "x")
    x.clear()
    x.send_keys("20")
    x.send_keys(Keys.RETURN)
    time.sleep(1)
    img = driver.find_element(By.ID, "output")
    render = img.get_attribute("src")
    driver.close()
    decodedData = base64.b64decode((render.removeprefix("data:image/png;base64,")))
  
    # Write Image from Base64 File
    imgFile = open(f'img/user/ely-{username}-skin.png', 'wb')
    imgFile.write(decodedData)
    imgFile.close()
