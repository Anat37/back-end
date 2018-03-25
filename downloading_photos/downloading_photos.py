from bs4 import BeautifulSoup
import requests
import os

tags = [
    "populous",
    "one person",
    "family",
    "friends",
    "Calm",
    "Active",
    "Food",
    "Drinks",
    "Alcohol",
    "Noisy",
    "Quiet",
    "Nature",
    "City",
    "Fragrant",
    "Cinema",
    "Sad",
    "Gloomy",
    "fast",
    "long",
    "free",
    "cheap",
    "expensive",
    "culture",
    "adrenaline"
]

def downloading_photos(tag):
    try:
        os.mkdir("img/{}".format(tag))
    except Exception:
        pass
    url = "https://www.google.ru/search?q={}&newwindow=1&source=lnms&tbm=isch".format(tag)
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    ans = soup.find_all("img")
    for i in range(1, len(ans)):
        img_url = ans[i]["src"]
        img = requests.get(img_url)
        out = open("img/{}/{}.jpg".format(tag, str(i)), "wb")
        out.write(img.content)
        out.close()

try:
    os.mkdir("img")
except Exception:
    pass
for tag in tags:
    downloading_photos(tag)