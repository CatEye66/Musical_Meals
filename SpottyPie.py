## Spotty Pie 
## Script for extracting spotify links from spotify playlists
## CatEye66 2023

# imports
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import getopt
import math

#######################################

# Processing arguments
def process_args(instructions):
    # list of command line arguments
    argList = sys.argv[1:]
    
    # Options
    short_options = "hEi:o:"
    
    # Long options
    long_options = ["help", "Extract", "input=", "output="]
    
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argList, short_options, long_options)
        
        # checking each argument
        for currentArgument, currentValue in arguments:
    
            if currentArgument in ("-h", "--help"):
                print("\nUsage: python [program name].py -E -i [path to input text] -o [path to output text]\n")
                print("-E, --Extract: Script will pull out all spotify song links from spotify playlist link")
                print("-i, --input: Input text for spotify playlists")
                print("-o, --ouput: Output text for spotify song links")
            
            elif currentArgument in ("-E", "--Extract"):
                instructions["extractBool"] = True
                print("Extracting spotify links")
                
            elif currentArgument in ("-i", "--input"):
                instructions["extractInput"] = currentValue
                print(f"Input file: {currentValue}")
                
            elif currentArgument in ("-o", "--output"):
                instructions["extractOutput"] = currentValue
                print(f"EOutput file: {currentValue}")
                
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
    
    return instructions

# Extracting spotify links from spotify playlist
def extract(playlist_link, instructions):

    #Authentication - without user
    cid = #
    secret = #
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    # playlist tracks extract
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    #track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

    # playlist name extract
    results = sp.user_playlist(user=None, playlist_id=playlist_URI, fields="name")
    playlist_name = results["name"]

    # extract urls 
    with open(instructions["extractOutput"],'a', encoding="utf-8") as file:
        # set up playlist name
        file.write(f"Playlist: {playlist_name}\n")
        print(f"\nPlaylist found... {playlist_name}")

        # set up tracks 
        for track in sp.playlist_tracks(playlist_URI)["items"]:
            #print(track) # will print all info on everything in playlist
            track_uri = str(track['track']['uri'])
            track_uri = track_uri.split(':')[2]
            track_url = f"https://open.spotify.com/track/{track_uri}"
            #print(track_uri)
            track_name = track["track"]["name"]
            artist_name = track["track"]["artists"][0]["name"]
            minutes = (track['track']['duration_ms'])/60000
            duration = f'{math.floor(minutes)}:{str(math.floor((minutes % 1) * 60)).zfill(2)}'
            #print(track_name, artist_name, duration)
            file.write(f"{track_name} | {artist_name} | {duration} | {track_url}\n")
            print(f"Link extracted... {track_name} | {artist_name} | {duration} | {track_url}")
        file.write("\n")

# Main
if __name__=='__main__':
    # welcome
    print("\n== Welcome to Spotty Pie ==") 

    # set up variables
    instructions = {
        "extractBool": False,
        "extractInput": ".\\files\\defaultSpotifyPlaylist.txt",
        "extractOutput": ".\\files\\defaultExtractedSpotify.txt"
    }

    # get args
    instructions = process_args(instructions)
                
    # EXTRACTION
    if instructions["extractBool"]:
        with open(instructions["extractInput"]) as file:

            for line in file:
                rline = line.rstrip()

                # skip if empty
                if rline == "":
                    continue

                # run extract
                extract(rline, instructions)

    # NO FLAG
    else:
        print("\nNo flag given. Exiting...\n")