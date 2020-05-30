import spotipy
import sys
import spotipy.util as util
from datetime import datetime

from spotipy.oauth2 import SpotifyClientCredentials
def print_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        print(
            "Track: %d Artist: %32.32s Track Name: %s ID: %s" %
            (i + 1 , track['artists'][0]['name'], track['name'],track['id']))

def tracks_to_file(results):
    date = datetime.now().strftime('%Y-%m-%d')
    print(date)
    f = open("on-repeat-{}.txt".format(date),"a")
    for i, item in enumerate(results['items']):
        track = item['track']
        f.write(
            "Track: %d Artist: %32.32s Track Name: %s ID: %s \n" %
            (i + 1 , track['artists'][0]['name'], track['name'],track['id']))
        

   


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Whoops, need your username!")
        print("usage: python user_playlists_contents.py [username]")
        sys.exit()

    token = util.prompt_for_user_token(username)

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['name'] == 'On Repeat':
                results = sp.playlist(playlist['id'], fields="tracks,next")
                
                tracks = results['tracks']
                print_tracks(tracks)
                tracks_to_file(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    print_tracks(tracks)
                    tracks_to_file(tracks)
                 
    else:
        print("Can't get token for", username)