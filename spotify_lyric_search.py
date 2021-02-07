#
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
        self.songs_info={}

    def find_song(self,lyrics):

        genius= lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
        request = genius.search_songs(lyrics,5)

        if(len(request['hits'])<1):
            print("No songs found :(")
            return None

        for i,hit in enumerate(request['hits']):
            print('{0}: {1}\n'.format(i+1,hit['result']['full_title']))

        i = input("Which number is your song? Press 0 for None: ")
        if i == '0': 
            print("Not listed...")
            return None

        song_name= request['hits'][int(i)-1]['result']['title']
        artist = request['hits'][int(i)-1]['result']['primary_artist']['name']
        
        self.songs_info[song_name]={
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
        #New Spotify Token is needed for status code 401
        if response.status_code != 200:
            raise ResponseException(response.status_code,response.reason)


        response_json = response.json()
        songs = response_json["tracks"]["items"]
    
        # only use the first song
        try:
            uri = songs[0]["uri"]
            return uri
        except:
            print(f"Couldn't find {song_name} by {artist}")
            return None
            
        
    def add_songs(self):

        while True:
            q= input("Enter Lyrics, or type \"quit()\" to stop searching: ") 
            if(q=="quit()"): break

            self.find_song(q)
        

        uris= [song["uri"] for _,song in self.songs_info.items() if song["uri"]!=None]
        

        playlist_id = self.create_playlist()

        request_data = json.dumps(uris)
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
            raise ResponseException(response.status_code,response.reason)

        response_json = response.json()
        return response_json

if __name__ == '__main__':
    sls = SpotifyLyricSearch()
    sls.add_songs()    