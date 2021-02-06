
import lyricsgenius
from dotenv import load_dotenv
import os
import json
import requests
from exceptions import ResponseException
load_dotenv() 
GENIUS_ACCESS_TOKEN= os.getenv('GENIUS_ACCESS_TOKEN')
SPOTIFY_USER_ID= os.getenv('SPOTIFY_USER_ID')
SPOTIFY_OAUTH= os.getenv('SPOTIFY_OAUTH')

class SpotifyLyricSearch: 
    def __init__(self):
      
        self.song_info={}

    def find_song(self,lyrics):

        genius= lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
        request = genius.search_songs(lyrics,5)

        if(len(request['hits'])<1):
            print("No songs found :(")
            return None

        for i,hit in enumerate(request['hits']):
            print('{0}: {1}\n'.format(i+1,hit['result']['full_title']))

        i = input("Which number is your song? Press 0 for None: \n")
        if i == '0': 
            print("Not listed...")
            return None

        song_name= request['hits'][int(i)-1]['result']['title']
        artist = request['hits'][int(i)-1]['result']['primary_artist']['name']
        
        self.song_info={
            "title" : song_name,
            "artist": artist,
            "uri": self.get_spotify_uri(song_name,artist)
            
        }
    
    def create_playlist(self):
        """Create A New Playlist"""
        request_body = json.dumps({
            "name": "Lyrical Search",
            "description": "Songs found using the lyrics",
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            SPOTIFY_USER_ID)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(SPOTIFY_OAUTH)
            }
        )
        response_json = response.json()
        # playlist id
        return response_json["id"]
        
    
    def get_spotify_uri(self, song_name, artist):
        """Search For the Song"""
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(SPOTIFY_OAUTH)
            }
        
        )
        print(query)


        response_json = response.json()
        songs = response_json["tracks"]["items"]
    
        # only use the first song
        try:
            uri = songs[0]["uri"]
            return uri
        except:
            return None
            
        
    def add_song(self):
        self.find_song(input("Enter Lyrics"))

 
        uri = self.song_info["uri"]
      
        
        playlist_id = self.create_playlist()

        request_data = json.dumps([uri])
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(SPOTIFY_OAUTH)
            }
        )

        # check for valid response status
        if response.status_code != 201:
            raise ResponseException(response.status_code)

        response_json = response.json()
        return response_json

if __name__ == '__main__':
    sls = SpotifyLyricSearch()
    print('\n')
    sls.add_song()    
    