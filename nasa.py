import requests
import json


class NasaCrawler:

    def __init__(self, url):
        self.content = {}
        self.items = []
        self.media_contents = []
        self.content = self.get_response(url)
        self.load_items(self.content)

    def get_response(self, url):
        response = requests.get(url, headers={'User-agent': 'my-user-agent'})
        return json.loads(response.content)

    def load_items(self, content):
        for item in content["collection"]["items"]:
            self.items.append(item)

    def load_media_content(self, amount):
        for i in range(amount):
            name = self.items[i]["data"][0]["title"]
            media_collection = self.get_response(self.items[i]["href"])
            self.media_contents.append((name, media_collection[0]))

    def check_items_media_formats(self, formats):

        only_defined_format = True
        for item in self.items:
            if not only_defined_format:
                break
            media_collection = self.get_response(item["href"])
            for url in media_collection:
                if not only_defined_format:
                    break
                suffix = url.split(".")[-1]
                if suffix not in formats:
                    only_defined_format = False
                    different_format = url

        if only_defined_format:
            True
        else:
            False

# Image check


url = "https://images-api.nasa.gov/search?year_start=2018&year_end=2018&q=surface%20of%20Mars&media_type=image"

nasaCrawler = NasaCrawler(url)
nasaCrawler.load_media_content(5)

print("THIS IS LIST OF TOP 5 NASA PICTURES FROM MARS:")
for i in range(5):
    print(str(i + 1) + ") " +
          nasaCrawler.media_contents[i][0] + " " + nasaCrawler.media_contents[i][1])

# Video check

video_formats = ("3gp", "3g2", "asf", "wmv", "avi", "divx", "evo", "f4v", "flv", "mkv", "mk3d", "mp4", "mpg",
                 "mpeg", "m2p", "ps", "ts", "m2ts", "mxf", "ogg", "ogv", "ogx", "mov", "qt", "rmvb", "vob", "webm")

url = "https://images-api.nasa.gov/search?year_start=2018&year_end=2018&media_type=video&keywords=Mars"

nasaCrawler = NasaCrawler(url)

print("NOW FOR VIDEO CHECK:")
only_defined_format = nasaCrawler.check_items_media_formats(video_formats)

if only_defined_format:
    print("Result contains only links to videos.")
else:
    print("Result does not contain only links to videos.")
