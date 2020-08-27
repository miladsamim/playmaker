from ytmusicapi import YTMusic
from .spotifyalbums import *

class ytmUploader:
    """class to use ytmusicapi (https://github.com/sigma67/ytmusicapi) to upload spotifyplaylists"""

    def __init__(self, yt_channel_id, auth_filepath='headers_auth.json'):
        self.ytmusic = YTMusic(auth_filepath)
        self.yt_channel_id = yt_channel_id

    def uploadSpotifyPlaylist(self, spotifyPL):

        plTitle = spotifyPL.get('playlistName')

        print(f"Retrieving songs for album {plTitle}")
        formerPlaylistID = self.getPlaylistID(plTitle)

        # convert Spotify songs to ytmusic video ids
        # Has to be done regardless, to update if exists
        videoIDs = self.ytVideoIDs(spotifyPL)

        if formerPlaylistID:
            # Delete first
            print(f"Deleting: {plTitle}")
            self.ytmusic.delete_playlist(formerPlaylistID)

        # Create playlist
        print(f"Creating: {plTitle}")
        plID = self.ytmusic.create_playlist(title=plTitle, description=f"{plTitle} from Spotify - magic from playmaker script", privacy_status="PUBLIC", video_ids=list(videoIDs))


    def ytVideoIDs(self, spotifyPL):

        ids = []
        """
        plTitle = spotifyPL.get('playlistName')
        if plTitle == 'RapCaviar':
            return rapCaviarIDs
        elif plTitle == 'Most Necessary':
            return mostNecessaryIDs
        elif plTitle == 'Get Turnt':
            return getTurntIDs
            """
        for song in spotifyPL.get('tracks'):
            songname = song[0]
            ytSongs = self.ytmusic.search(songname, "songs")
            if ytSongs:
                topMatchingSong = ytSongs[0]
                ids.append(topMatchingSong.get('videoId'))

        return ids


    def getPlaylistID(self, plTitle):

        userInfo = self.ytmusic.get_user(self.yt_channel_id)

        if 'playlists' in userInfo:
            for song in userInfo.get('playlists').get('results'):
                if song["title"] == plTitle:
                    return song["playlistId"]

        return ""
