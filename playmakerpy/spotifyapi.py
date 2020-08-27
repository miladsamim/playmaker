import requests
import base64

def refreshAcessTokenRespons(client_id, client_secret):
    """Get accesstoken for spotify api (no user authorization)"""

    #preparing request
    url = "https://accounts.spotify.com/api/token"
    payload = {'grant_type': 'client_credentials'}

    #sending post request
    r = requests.post(url, data=payload, auth=(client_id, client_secret))

    return r.json()

def getSpotifyPlaylist(accessTokenResponse, albumID = ""):
    """Get spotify playlist obj"""
    accessToken = accessTokenResponse.get('access_token')
    tokenType = accessTokenResponse.get('token_type')
    expiresIn = accessTokenResponse.get('expires_in')

    url = "https://api.spotify.com/v1/playlists/" + albumID
    headers = {'Authorization' : f'Bearer {accessToken}'}

    r = requests.get(url, headers=headers)
    return r.json()


def formatSpotifyPlaylist(spotifyPlaylist):
    """Return an dict with playlist name and array of arrays consisting track name, album name and artists.
    Like {playlistName:"", tracks:[['name','album_name',['artist_name',..]],...)]}"""

    resDictPL = {'playlistName': '', 'tracks':[]}

    resDictPL['playlistName'] = spotifyPlaylist.get('name')

    for trackWrapper in spotifyPlaylist.get('tracks').get('items'): # item can be either playlist track objects or episodes - https://developer.spotify.com/documentation/web-api/reference/object-model/#playlist-object-full
        track = trackWrapper.get('track')
        if track is not None: #avoid Nonetype objects
            if 'album' in track: # only add tracks
                trackName = track.get('name')
                trackAlbumName = track.get('album').get('name')
                trackArtists = [artist.get('name') for artist in track.get('artists')]

                resDictPL['tracks'].append([trackName, trackAlbumName, [trackArtists]])

    return resDictPL
