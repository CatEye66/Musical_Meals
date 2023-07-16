# Musical_Meals

Welcome to the Musical Meals. This is a series of script series for converting songs to YouTube links and mp3 files.

SpottyPie: Extracting Spotify playlists into individual tracks <br>
Sauerkraut: Converting track name and artist into YouTube links <br>
BeautifulSoup: Downloading the YouTube links as mp3 files on your computer <br>

# Requirements
- Run the requirements file to ensure you have the appropriate libaries 
- Ensure you are running Python 3.7 or higher 
- Ensure you have pip installed
>`pip install -r requirements.txt`

# Listing down the music you'd like to convert

- The first step is to populate the _defaultExtractedSpotify.txt_ with the list of music you'd like to convert into YouTube links and mp3s
- You can do this in one of two ways:
    1. Manual Typing 
    2. Spotify Playlist Extraction 

## Manual Typing
- You can type this in _defaultExtractedSpotify.txt_ manually, using the format: <br>
>Song name | Song artist | Optional: Duration 
- Place each song on a separate line

## Spotify Playlist Extraction
- Another option is to extract from a Spotify playlist
- If you are starting with a Spotify playlist, first copy the share link of your playlist from spotify
    - **Ensure it is a public playlist.**
- Next, paste the link into the _defaultSpotifyPlaylist.txt_ file, under the _files_ directory
    - Place each spotify playlist link on a new line in the file if you are extracting from multiple playlists
- Before running the script, be sure to add your Spotify Client ID and Client Secret
    - You can find out how via this guide: https://support.heateor.com/get-spotify-client-id-client-secret/
- Next, run the SpottyPie script, and ensure you are at the Musical_Meals directory 
>`python3 SpottyPie.py -E`
- The script should extract all the spotify tracks into the file _defaultExtractedSpotify.txt_ with the format: <br>
>Song name | Song artist | Duration | Spotify links

# Converting track name and artist into YouTube links

- When you have populated the _defaultExtractedSpotify.txt_ file, the next step is to convert them into YouTube links
- Next, run the Sauerkraut script, and ensure you are at the Musical_Meals directory
- If the duration is available, run: <br>
>`python3 Sauerkraut.py -C -d` <br>
- If the duration is not available, run: <br>
>`python3 Sauerkraut.py -C` <br>
- The script should convert all tracks into YouTube links in the file _defaultYouTubeLinks.txt_
>Song name | Song artist | Optional: Duration | YouTube links

## Troubleshooting
- Once the conversion is complete, check the _defaultYouTubeLinks.txt_ for <br>
> MANUAL REPLACE: <br>
- These are tracks that could not be found correctly on YouTube and need to be manually searched
- Please fix by finding the YouTube link of choice and placing into the error line, and remove the "MANUAL REPLACE: ", so that the final format is:
>Song name | Song artist | Optional: Duration | YouTube links
- Also check the _defaultYouTubeLinks.txt_ file for <br>
> CHECK: <br>
- These are YouTube links taken low down in the list and may not be accurate, and need to be manually checked
- Please fix by checking YouTube link and remove the "CHECK: ", so that the final format is:
>Song name | Song artist | Optional: Duration | YouTube links

# Downloading the YouTube links as mp3 files on your computer 

- Finally, run the BeautifulSoup script to convert the list of YouTube links into mp3 files
- If you would like tracks to be numbered, run: <br>
>`python3 BeautifulSoup.py -D -n` <br>
- If you would not like tracks to be numbered, run: <br>
>`python3 BeautifulSoup.py -D` <br>
- Note that tracks are automatically numbered if detected in a playlist
- The mp3s will be downloaded into the _mp3s_ directory
