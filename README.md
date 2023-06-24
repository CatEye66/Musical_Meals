# Musical_Meals

Welcome to the Musical Meals. This is a series of script series for converting songs to YouTube links and mp3 files.

SpottyPie: Extracting Spotify playlists into individual tracks <br>
Sauerkraut: Converting track name and artist into YouTube links <br>
BeautifulSoup: Downloading the YouTube links as mp3 files on your computer <br>

## Requirements
- Run the requirements file to ensure you have the appropriate libaries 
- Ensure you are running Python 3.7 or higher 

## Extracting Spotify PLaylists into individual tracks

- If you are starting with a Spotify playlist, first copy the share link of your playlist from spotify
    - **Ensure it is a public playlist.**
- Next, paste the link into the _defaultSpotifyPlaylist.txt_ file, under the _files_ directory
    - Place each spotify playlist link on a new line in the file if you are extracting from multiple playlists
- Next, run the SpottyPie script, and ensure you are at the Musical_Meals directory 
>`python3 SpottyPie.py -E`
- The script should extract all the spotify tracks into the file _defaultExtractedSpotify.txt_

## Converting track name and artist into YouTube links

- If you have previously run _SpottyPie_, it will generate a list in _defaultExtractedSpotify.txt_ with the format: <br>
>Song name | Song artist | Duration | Spotify links
- You can also choose to type in _defaultExtractedSpotify.txt_ manually, using the format: <br>
>Song name | Song artist | Optional: Duration 
- Next, run the Sauerkraut script, and ensure you are at the Musical_Meals directory
- If the duration is available, run: <br>
>`python3 Sauerkraut.py -C -d` <br>
- If the duration is not available, run: <br>
>`python3 Sauerkraut.py -C` <br>
- The script should convert all tracks into YouTube links in the file _defaultYouTubeLinks.txt_
>Song name | Song artist | Optional: Duration | YouTube links

### Troubleshooting
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

## Downloading the YouTube links as mp3 files on your computer 

- Finally, run the BeautifulSoup script to convert the list of YouTube links into mp3 files
- If you would like tracks to be numbered, run: <br>
>`python3 BeautifulSoup.py -D -n` <br>
- If you would not like tracks to be numbered, run: <br>
>`python3 BeautifulSoup.py -D` <br>
- Note that tracks are automatically numbered if detected in a playlist
- The mp3s will be downloaded into the _mp3s_ directory
