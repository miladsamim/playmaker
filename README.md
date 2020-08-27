# playmaker

## Briefly
Uploads specified Spotify albums as playlists to your Youtube music account.

Is an Azure function app (python), which using a timer trigger function to publish Spotify albums specified in \playmakerpy\spotifyalbums.py to your Youtube music account specified by the channel_id in local.settings.json (private/specify your own).

When published to the azure cloud (as a function app) the function "timer" runs everyday at 5 am (UTC) specified by the CRON expression in  \timer\function.json. This is to ensure your albums are updated automactically daily to stay up to date.

## Requirements for local use
- Python version 3.8
- Python modules in requirements.txt (recommended to make a virtual python environment)
- Azure tools (easier to follow here: [link](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-azure-function-azure-cli?tabs=bash%2Cbrowser&pivots=programming-language-python))
  - Azure CLI 2.4 or later
  - Azure functions core tools 3.x
- Azure storage simulator [get here] (https://docs.microsoft.com/en-us/azure/storage/common/storage-use-emulator) (needed to run Timer trigger functions locally)

## How to run locally
1. Make sure you the local.settings.json file is filled with proper values
   - "AzureWebJobsStorage": "UseDevelopmentStorage=true" (has to be development storage)
   - "spotify_client_id" has to be your client_id from Spotify [get here](https://developer.spotify.com/)
   - "spotify_client_secret" has to be your client_secret from Spotify [get here](https://developer.spotify.com/)
   - "yt_channel_id" has to be your yt music channel id, browse to your own channel on music.youtube.com and take id from url
   - "yt_cookie" paste your youtube cookie, has to be retrievied as exlplained in the documentation for py package ytmusicapi ([ytmusicapi doc](https://ytmusicapi.readthedocs.io/en/latest/setup.html))
2. Make sure your azure storage simulator is running
3. Make sure your python virtual environment with requirements.txt is activated
3. In PowerShell(any terminal with needed tools) navigate to root of the function app
4. Execute command ```func start``` to start the function app
5. Instead of waiting for it to run at 5 am (UTC) as specified by the CRON expression, call it with this curl command ```curl -X Post -H "Content-Type:application/json" --data {} http://localhost:7071/admin/functions/timer -v```

## How to publish to azure
1. Create a function app python 3.8 in azure (through portal.azure.com or az cli)
2. When deploying you have to ensure you use the correct storage connection string (refer to this [guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#local-settings-file))
3. (navigate to function app root, have to be signed in ```az login```) Publish with ```func azure functionapp publish <the azure function app name> --publish-local-settings -i --overwrite-settings -y``` (publish local settings is needed store all our yt and Spotify credentials in the azure functionapp securely)
4. Refer to this guide for triggering deployed azure functions [link](https://kevsoft.net/2020/02/20/testing-timer-triggers-in-azure-functions.html)
 
