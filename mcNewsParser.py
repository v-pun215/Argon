import requests
import xml.etree.ElementTree as ET
def get_news_list():
    url = 'https://rss-bridge.org/bridge01/?action=display&bridge=MinecraftBridge&category=News&format=Atom'
    response = requests.get(url)
    xml_string = response.text

    root = ET.fromstring(xml_string)
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}

    entries = []
    for entry in root.findall('atom:entry', namespace):
        title = entry.find('atom:title', namespace).text
        content = entry.find('atom:content', namespace).text
        link = entry.find("atom:link[@rel='alternate']", namespace).get('href')
        image = entry.find("atom:link[@rel='enclosure']", namespace).get('href')
        
        entries.append({
            'title': title,
            'content': content,
            'link': link,
            'image': image
        })
    return entries