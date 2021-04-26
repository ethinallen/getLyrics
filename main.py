import time
import sys

import boto3
import lyricsgenius
import requests
import csv

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

def checkExist(artist, song, dynamodb=None):
    song_id = artistName + songName
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id=keys.access_key_id, aws_secret_access_key=keys.access_key, region_name=keys.region)

    table = dynamodb.Table('lyrics')
    response = table.get_item(
       Key={
            'song_id': song_id}
    )
    print(response)
    try:
        return response['Item']
    except:
        return None

def put_lyrics(song, lyrics, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id=keys.access_key_id, aws_secret_access_key=keys.access_key, region_name=keys.region)

    table = dynamodb.Table('lyrics')
    response = table.put_item(
       Item={
            'song_id': song,
            'lyrics' : lyrics
            }
    )

    return response

def translate(lyrics):
    translate = boto3.client(service_name='translate', aws_access_key_id=keys.access_key_id, aws_secret_access_key=keys.access_key, region_name=keys.region, use_ssl=True)
    result = translate.translate_text(Text=lyrics, SourceLanguageCode="auto", TargetLanguageCode="en")
    return result

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

    nativeKey = artistName + songName
    lyrics = checkExist(artistName, songName)

    if lyrics:
        print(lyrics['lyrics'])

    else:
        artist = getArtist(artistName)
        song = getSongLyrics(artist, songName)



        key = artistName + songName

        print(song.lyrics)
        # translation = translate(song.lyrics)
        # print(translation.get('TranslatedText'))

        # nativeKey = artistName + songName + translation.get('SourceLanguageCode')
        # enKey = artistName + songName + translation.get('TargetLanguageCode')
        put_lyrics(key, song.lyrics)
        # put_lyrics(enKey, translation.get('TranslatedText'))

    sys.stdout.flush()
