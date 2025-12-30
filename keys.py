import requests

discordClient = "1331607427547660340"
redirectURL = "https://eclient-done.vercel.app/"

def getCurrentBackend():
    try:
        url = "https://argon-auth.vercel.app/backend"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        return None
    except Exception as e:
        return None
