from xml.dom.minidom import parse
import xml.dom.minidom, os, subprocess
import requests, json
mcNewsHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
def get_json_file():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    try:
        response = requests.get('https://launchercontent.mojang.com/news.json', headers=headers)
        if response.status_code == 200:
            with open ("mcNewsletter.json", "wb") as f:
                f.write(response.content)
                f.close()

            with open("mcNewsletter.json", "r") as f:
                news = f.read()

            news = news.replace('â€™',"'")

            with open("mcNewsletter.json", "w") as f:
                f.write(news)
                f.close()
        else:
            print("Minecraft News is down :(")
    except Exception as e:
        print("Unable to fetch MC News.")
        print(e)
