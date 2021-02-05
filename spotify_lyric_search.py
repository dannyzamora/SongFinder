
import lyricsgenius
from dotenv import load_dotenv
import os

load_dotenv() 
GENIUS_ACCESS_TOKEN= os.getenv('GENIUS_ACCESS_TOKEN')

class SpotifyLyricSearch: 
    def __init__(self,lyrics):
        self.lyrics=lyrics
    def find_song(self):
        genius= lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
        request = genius.search_songs(self.lyrics,5)
        for hit in request['hits']:
            print(hit['result']['full_title'],'\n') 

#for hit in request['sections'][0]['hits']:
   # print(hit['result']['title'])# import requests



# url = "http://api.genius.com/search?q=Kendrick%20Lamar"

# payload={}
# headers = {
#   'Authorization': 'Bearer',
#   'Cookie': '__cfduid=d40ec58ce31c0da814768a95202a215ca1612483091'
# }

# response = requests.request("GET", url, headers=headers, data=payload)
# print(response.text)

if __name__ == '__main__':
    #
    sls = SpotifyLyricSearch("my girl")
    sls.find_song()
    