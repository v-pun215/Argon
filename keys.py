import urllib.request

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
    else:
        break

client = line1
secret = line2
redirectURL = "https://eclient-done.vercel.app/"