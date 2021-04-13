import lyricsgenius
import time

genius = lyricsgenius.Genius()

def getArtist(artistName):
    try:
        artist = genius.search_artist(artistName, max_songs=1, sort="title")
        return artist
    except Exception as e:
        print(e)


def getSongLyrics(artist, songTitle):
    try:
        song = artist.song(songTitle)
        return song
    except Exception as e:
        print(e)

if __name__ == '__main__':
    t = time.time()
    artist = getArtist('the avett brothers')
    song = getSongLyrics(artist, 'around the world')
    print(song.lyrics)
    print('\n\nIt took:\t{} seconds'.format(time.time() - t))
