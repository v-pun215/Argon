import sys
import wget
import requests
import minecraft_launcher_lib
import os, json

import shutil
from pathlib import Path


with open("metadata.json", "r") as metadata_file:
    metadata = json.load(metadata_file)

author = metadata.get("author", "")
current_version = metadata.get("version", "")
description = metadata.get("description", "")

def restartArgon():
    os.execv(sys.executable, ['python'] + sys.argv)

def check_for_updates():
    try:
        response = requests.get("https://api.github.com/repos/v-pun215/Argon/releases/latest")
        response.raise_for_status()
        data = response.json()
        latest_release = data["name"]
        latest_release = latest_release.replace("v", "")

        if latest_release >= current_version:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return False

def install_update():
    # Get original directory (script location)
    original_dir = Path.cwd()
    parent_dir = original_dir.parent
    update_dir = parent_dir / "ArgonUpdate"

    # Create ArgonUpdate directory safely
    update_dir.mkdir(exist_ok=True)

    # Move update.zip safely
    update_zip = original_dir / "update.zip"
    if update_zip.exists():
        shutil.move(str(update_zip), str(update_dir / "update.zip"))
    else:
        print("update.zip not found.")
        return

    print("Update downloaded successfully. Extracting files...")

    # Extract archive into the update directory
    shutil.unpack_archive(str(update_dir / "update.zip"), extract_dir=str(update_dir))

    # Copy config files if they exist
    for filename in ["settings.json", "launcherProfiles.json"]:
        src_file = original_dir / filename
        if src_file.exists():
            shutil.copy(str(src_file), str(update_dir / filename))

    print("Update installed successfully in:", update_dir)

    #deletes original directory, changes name of update directory to original directory name
    try:
        shutil.copytree(original_dir, str(update_dir / "argonOLD"))
        shutil.rmtree(original_dir)
        print("Original directory deleted successfully.")
    except Exception as e:
        print(f"Error deleting original directory: {e}")
    try:
        new_dir_name = original_dir.name
        new_dir_path = update_dir.parent / new_dir_name
        update_dir.rename(new_dir_path)
        print("Update directory renamed to original directory name.")
    except Exception as e:
        print(f"Error renaming update directory: {e}")

    # Change working directory to the new directory
    os.chdir(new_dir_path)

def download_update():
    try:
        response = requests.get("https://api.github.com/repos/v-pun215/Argon/releases/latest")
        response.raise_for_status()
        data = response.json()
        download_url = None
        for asset in data["assets"]:
            if asset["name"].endswith(".zip"):
                download_url = asset["browser_download_url"]
                break

        if download_url:
            print("Downloading update...")
            if os.path.exists("update.zip"):
                os.remove("update.zip")
            wget.download(download_url, "update.zip")
            install_update()
        else:
            print("No update found.")
    except Exception as e:
        print(f"Error downloading update: {e}")

