from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

load_dotenv()



def cleanUpLyrics(lyrics):
    cleanedLyrics = ""
    for line in lyrics.split("\n"):
        line = line.strip()
        line = line.replace("\r", "")
        if(line and
           line is not "\n" and
           len(line.split(" ")) > 1 and
           "[" not in line and
           "(" not in line and
           "~" not in line
        ):
            cleanedLyrics += line + "\n"
    return cleanedLyrics.strip()



artistName = input("What Artist Do You Want to Imitate? ")
if(os.path.isdir(f"./Dataset/{artistName}")):
    print("\nArtist's lyrics exists in the dataset! No need to generate new data, proceed to the model!")
    exit()

os.makedirs(f"./Dataset/{artistName}")
print(f"\nFetching new data for {artistName}...")

artistNameURL = "+".join(artistName.split(" "))
pageHTML = BeautifulSoup(requests.get(os.environ.get("BASE_URL") + f"/i/{artistNameURL}").text, features = "lxml")

for songLink in pageHTML.find_all("div", class_ = "lf-list__row js-sort-table-content-item"):
    songHTML = BeautifulSoup(requests.get(os.environ.get("BASE_URL") + songLink.a.get("href")).text, features = "lxml")
    songName = songHTML.find("a", class_ = "song-page-conthead-link").parent.text.split("\u2013")[-1].replace("Lyrics", "").strip()
    lyrics = songHTML.find(id = "content").text.strip()
    lyrics = cleanUpLyrics(lyrics)
    with open(f"./Dataset/{artistName}/{songName}.txt", mode = "w") as songFile:
        songFile.write(lyrics)
    print(f"{songName} by {artistName} was added to the dataset!")