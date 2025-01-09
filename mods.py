import requests, json, wget,os
import shutil
class Modrinth:
    def search_homePage():
        url = f"https://api.modrinth.com/v2/search"
        response = requests.get(url)
        data = json.loads(response.text)
        return data["hits"]
    def search(name):
        name = name.replace(" ", "%20")
        url = f"https://api.modrinth.com/v2/search?query={name}"
        response = requests.get(url)
        data = json.loads(response.text)
        return data["hits"]

    def downloadLatestVersion(slug, mc_ver, dir, mod_loader):
        global url2download, filename, filepath
        url = f"https://api.modrinth.com/v2/project/{slug}/version"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for version in data:
                if mod_loader in version["loaders"]:
                    if mc_ver in version["game_versions"]:
                        url2download = version["files"][0]["url"]
                        filename = version["files"][0]["filename"]
        else:
            raise Exception(f"Error: {response.status_code}")
        try:
            if not os.path.exists(f"{dir}{filename}"):
                if url2download:
                    response = requests.get(url2download)
                    if response.status_code == 200:
                        if os.path.exists(dir) == False:
                            os.mkdir(dir)
                        filepath = f"{dir}{filename}"
                        with open(filepath, 'wb') as file:
                            file.write(response.content)
                        print('File downloaded successfully')
                    else:
                        raise Exception(f"Error: {response.status_code}")
            else:
                print("File already exists.")
                raise Exception("Mod is already added. Go to the file directory tab to see more.")
                
        except Exception as e:
            raise Exception(e)
            

        

    def checkmcversupported(slug, mc_ver):
        url = f"https://api.modrinth.com/v2/project/{slug}/version"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for version in data:
                if mc_ver in version["game_versions"]:
                    return True
        else:
            return f"Error: {response.status_code}"
        return False
    
class Manager:
    def doesInstanceHaveMods(instance_name):
        dir = f"instances/{instance_name}/mods"
        has_jar_files = any(f.endswith('.jar') for f in os.listdir(dir))
        if has_jar_files:
            return True
        else:
            return False
        
    def transferModsOnRun(instance_name, mc_dir):
        dir = f"instances/{instance_name}/mods"
        mc_dir = mc_dir + "/mods"
        for file_name in os.listdir(dir):
            if file_name.endswith('.jar'):
                source_file = os.path.join(dir, file_name)
                destination_file = os.path.join(mc_dir, file_name)
                shutil.move(source_file, destination_file)
        print("Mods transferred successfully.")

    def transferFilesBack(instance_name, mc_dir):
        dir = f"instances/{instance_name}/mods"
        mc_dir = mc_dir + "/mods"
        for file_name in os.listdir(mc_dir):
            if file_name.endswith('.jar'):
                source_file = os.path.join(mc_dir, file_name)
                destination_file = os.path.join(dir, file_name)
                shutil.move(source_file, destination_file)
        print("Mods transferred back successfully.")

        
        
if __name__ == "__main__":
    print(Modrinth.downloadLatestVersion(slug="sodium", mc_ver="1.21", dir="instances/", mod_loader="fabric"))