from ..playmakerpy.spotifyapi import *
from ..playmakerpy.spotifyalbums import *
from ..playmakerpy.yt import ytmUploader
from ytmusicapi import YTMusic
import tempfile
import os
import os.path
import json

import datetime
import logging

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    # Temporary file is needed to retrieve the ytm cookie securely and being able to write to a file, while running in azure
    fp = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', suffix=".json", delete=False)
    # add ytm cookie to temp file fp
    formerCookieTxt = addYTMCookieToAuth(os.environ["yt_cookie"], fp)
    fp.seek(0)
    # Initialize a yt uploader for the channel (your account)
    ytm = ytmUploader(os.environ['yt_channel_id'], fp.name)

    fp.close()
    os.unlink(fp.name)

    # Get spotify bearer token obj
    spotifyAccesTokenResp = refreshAcessTokenRespons(os.environ["spotify_client_id"], os.environ["spotify_client_secret"])

    # Delete existing similar named albums on your account
    # Then upload all albums found in spofityalbums.py albumIDs dict
    for albumID in reversed(albumIDs.values()): # Reverse so that albums are in yt account with same order as albumids (recent uploaded)
        spotifyPL = getSpotifyPlaylist(spotifyAccesTokenResp, albumID)
        formattedSpotifyPL = formatSpotifyPlaylist(spotifyPL)
        ytm.uploadSpotifyPlaylist(formattedSpotifyPL)

    logging.info("Albums updated")

def addYTMCookieToAuth(cookie, fp_tmp):
    """Gets the ytm cookie from settings and the file headers_auth.jsom, combines these 2, and writes it to a temporary file to initialize YTMusic() as decribed in doc for ytmusicapi"""
    with open('headers_auth.json') as json_file:
        data = json.load(json_file)
        temp = data['Cookie']
        data['Cookie'] = cookie
        fp_tmp.write(json.dumps(data))
