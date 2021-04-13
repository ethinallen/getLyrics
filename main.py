import lyricsgenius
import time
import sys
import requests
import keys

# fetch a client token from genius api
def getToken():

    data = {
      'client_id': keys.client_id,
      'client_secret': keys.client_secret,
      'grant_type': 'client_credentials'
    }

    response = requests.post('https://api.genius.com/oauth/token', data=data)
    return response.json()['access_token']

# return artist object
def getArtist(artistName):
    genius = lyricsgenius.Genius(getToken())
    genius.verbose = False
    try:
        artist = genius.search_artist(artistName, max_songs=1, sort="title")
        return artist
    except Exception as e:
        print(e)

# return song lyrics as string
def getSongLyrics(artist, songTitle):
    try:
        song = artist.song(songTitle)
        return song
    except Exception as e:
        print(e)

if __name__ == '__main__':
    artistName = sys.argv[1].replace("_", " ")
    songName = sys.argv[2].replace("_", " ")
    artist = getArtist(artistName)
    song = getSongLyrics(artist, songName)
    print(song.lyrics)
    sys.stdout.flush()
