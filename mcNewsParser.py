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
        link_el = entry.find("atom:link[@rel='alternate']", namespace)
        link = link_el.get('href') if link_el is not None else ''

        image_el = entry.find("atom:link[@rel='enclosure']", namespace)
        image = image_el.get('href') if image_el is not None else None

        entries.append({
            'title': title,
            'content': content,
            'link': link,
            'image': image
        })
    return entries