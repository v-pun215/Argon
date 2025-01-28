# work in progress, thinking of implementing this with next update.
'''
requirements:
ytp-dl
mutagen
'''
import os, wget
import urllib.request
import json
import urllib
from mutagen.mp3 import MP3

def downloadYTaudio(url, title=""):
    if url.startswith("https://youtu.be/"):
        VideoID = url[17:]
    elif url.startswith("https://www.youtube.com/watch?v="):
        VideoID = url[32:]
    else:
        print("Invalid URL")
        return

    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        print(data['title'])

        vid_title = data['title']

    if title != "":
        vid_title = title

    if "/" in vid_title or "\" in vid_title" or ":" in vid_title or "*" in vid_title or "?" in vid_title or "<" in vid_title or ">" in vid_title or "|" in vid_title:
        vid_title = vid_title.replace("/", "").replace("\"", "").replace(":", "").replace("*", "").replace("?", "").replace("<", "").replace(">", "").replace("|", "")
    og_dir = os.getcwd()
    os.mkdir(f"{og_dir}\\music\\{vid_title}")
    thumbnail = f"https://img.youtube.com/vi/{VideoID}/0.jpg"
    print("Downloading thumbnail...")
    wget.download(thumbnail, f"music\\{vid_title}\\thumbnail.jpg")

    cmd = f'yt-dlp --extract-audio --audio-format mp3 --output "music\\{vid_title}\\audio.mp3" --ffmpeg-location "music/bin" "https://www.youtube.com/watch?v={VideoID}"'
    print("Downloading audio...")
    os.system(cmd)

    # Making metadata json

    audio = MP3(f"music\\{vid_title}\\audio.mp3")
    duration = audio.info.length

    metadata = {
        "duration": duration,
        "platform": "youtube",
        "author": data['author_name'],
    }
    with open(f"music\\{vid_title}\\metadata.json", "w") as f:
        json.dump(metadata, f)

def deleteMusic(title):
    try:
        os.remove("music\\"+title+"\\audio.mp3")
        os.remove("music\\"+title+"\\thumbnail.jpg")
        os.remove("music\\"+title+"\\metadata.json")
        os.rmdir("music\\"+title)
        return True

    except:
        return False


def listMusic():
    music_list = []
    for i in os.listdir("music"):
        if i != "bin":
            music_list.append(i)

    return music_list
