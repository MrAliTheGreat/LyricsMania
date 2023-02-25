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
songLinksContainer = pageHTML.find("div", class_ = "lf-list__container js-sort-table-container")

for songLink in songLinksContainer.find_all("div", class_ = "lf-list__row js-sort-table-content-item"):
    songName = songLink.a.text.encode("ascii", "ignore").decode("utf-8").replace("Lyrics", "").replace("?", "").strip()

    songHTML = BeautifulSoup(requests.get(os.environ.get("BASE_URL") + songLink.a.get("href")).text, features = "lxml")

    lyrics = songHTML.find(id = "content").text.encode("ascii", "ignore").decode("utf-8").strip()
    lyrics = cleanUpLyrics(lyrics)

    with open(f"./Dataset/{artistName}/{songName}.txt", mode = "w") as songFile:
        songFile.write(lyrics)
    print(f"{songName} by {artistName} was added to the dataset!")