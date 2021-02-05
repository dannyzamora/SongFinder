
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

if __name__ == '__main__':
    sls = SpotifyLyricSearch(input("Enter Lyrics please: "))
    print('\n')
    sls.find_song()
    