import requests
from libauth.libauth import Auth
from libdb.libdb import Db

from moon import Moon
from rainfall import Rainfall, RainfallPossibility
from sun import Sun
from swell import Swell
from temperature import Temperature
from tide import Tide
from wind import Wind

TYPES = {
    "moon":{"pre-uri":"moonphases", "creator":Moon},
    "rain":{"pre-uri":"rainfall", "creator":Rainfall},
    "rain_possibility":{"pre-uri":"rainfall", "creator":RainfallPossibility},
    "sun":{"pre-uri":"sunrisesunset", "creator":Sun},
    "swell":{"pre-uri":"swell", "creator":Swell},
    "temperature":{"pre-uri":"www", "creator":Temperature},
    "tide":{"pre-uri":"tides", "creator":Tide},
    "wind":{"pre-uri":"wind", "creator":Wind},
}

REGIONS = {
    "wollongong":"illawarra/coal-cliff-harbour",
    "sydney":"sydney/south-head",
    "central coast":"central-coast/lighthouse-beach",
    "newcastle":"hunter/bar-beach",
}

def url_get(type, region):
    return f"https://{type}.willyweather.com.au/nsw/{region}.html"

def html_get(type, region):
    url = url_get(type, region)
    response = requests.get(url)
    return response.content.decode("utf-8")

def export():
    auth = Auth()
    db = Db(auth.database_host(), auth.database_user(), auth.database_password(), "fishing")
    for region in REGIONS:
        for type in TYPES:
            html = html_get(TYPES[type]["pre-uri"], REGIONS[region])
            object = TYPES[type]["creator"](html)
            object.export(db, region)

def swell_sample_html():
    html = html_get(TYPES['swell']["pre-uri"], REGIONS['sydney'])
    print(html)

if __name__ == "__main__":
    export()
    # swell_sample_html()
