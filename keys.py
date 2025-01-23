import urllib.request
# You are not allowed to use these keys. It is illegal to use them without permission.
c = 0
file_url = "https://argon-keys.vercel.app/keys.txt"
line1 = line2 = line3 = ""

for line in urllib.request.urlopen(file_url):
    if c == 0:
        line1 = line.decode('utf-8').strip()
        c = 1
    elif c == 1:
        line2 = line.decode('utf-8').strip()
        c = 2
    elif c ==2:
        line3 = line.decode('utf-8').strip()
        c = 3
    else:
        break

client = line1
secret = line2
discordClient = line3
redirectURL = "https://eclient-done.vercel.app/"