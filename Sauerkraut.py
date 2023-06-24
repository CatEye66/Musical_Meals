## Sauerkraut
## Script for converting name and artist into formatted YouTube links
## CatEye66 2023

# imports
import re
import time
import datetime 
import os
import sys
from fuzzysearch import find_near_matches
import getopt
import regex

import requests
from bs4 import BeautifulSoup
import urllib.request
from requests_html import HTMLSession
from pprint import pprint
from urllib.parse import urljoin
import webbrowser
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions


#######################################

# Processing arguments
def process_args(instructions):
    # list of command line arguments
    argList = sys.argv[1:]
    
    # Options
    short_options = "hCdi:o:"
    
    # Long options
    long_options = ["help", "Convert", "duration=", "input=", "output="]
    
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argList, short_options, long_options)
        
        # checking each argument
        for currentArgument, currentValue in arguments:
    
            if currentArgument in ("-h", "--help"):
                print("\nUsage: python [program name].py -C -i [path to input text] -o [path to output text]\n")
                print("-C, --Convert: Script will convert the given name and artist in the formatted text file into Youtube links")
                print("-d, --duration: The file includes song duration")
                print("-i, --input: Input text for the name and artist")
                print("-o, --ouput: Output text for formatted Youtube links")
            
            elif currentArgument in ("-C", "--Convert"):
                instructions["convertBool"] = True
                print("Converting given songs")

            elif currentArgument in ("-d", "--duration"):
                instructions["convertDuration"] = True
                print("Duration given")
                
            elif currentArgument in ("-i", "--input"):
                instructions["convertInput"] = currentValue
                print(f"Input file: {currentValue}")
                
            elif currentArgument in ("-o", "--output"):
                instructions["convertOutput"] = currentValue
                print(f"EOutput file: {currentValue}")
                
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
    
    return instructions

# Search for the name and artist
def convert(rline, instructions):
    # set up variables
    targetURL = "https://www.youtube.com/results?search_query="
    array = rline.split(' | ')
    #print(array)
    song = array[0]
    artist = array[1]
    if instructions["convertDuration"] and len(array) > 2:
        duration = array[2]
        actualMinutes, actualSeconds = re.split(r':', duration)
    search = quote(f'{song} {artist} audio')
    searchURL = f'{targetURL}{search}'
    print(f'Searching for {rline}')

    # set up the web driver
    error = False
    sus = 0
    attempt = 0
    while attempt < 5:
        try:
            error = False
            ## launch chrome with incognito and extension
            #opt = ChromeOptions()
            #opt.add_argument("-incognito")
            #opt.headless = True # chrome does not visibly launch
            #path_to_extension = 'C:\\Users\\Han\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\gighmmpiobklfepjocnamgkkbiglidom\\5.7.0_0'
            #opt.addExtensions(path_to_extension)
            #driver = webdriver.Chrome(options=opt)
            #driver.create_options()

            ## launch firefox with incognito
            opt = FirefoxOptions()
            opt.set_preference("browser.privatebrowsing.autostart", True)
            opt.add_argument('-headless') # firefox does not visibly launch
            driver = webdriver.Firefox(options=opt)
            wait = WebDriverWait(driver, 3)
            
            driver.get(searchURL)
            links = WebDriverWait(driver, timeout=20).until(EC.presence_of_all_elements_located((By.ID, "video-title")))

            # check it is the correct video
            found = False
            for link in links:
                print(f'Aria Label: {link.get_attribute("aria-label")}')
                capture = link.get_attribute("aria-label")
                
                # skip ads
                if capture is None:
                    continue

                if instructions["convertDuration"]:
                    durFail = False
                    
                    minutesSearch = re.findall(r'(\d+) minutes?', capture) 
                    minutes = 0 if len(minutesSearch) == 0 else int(minutesSearch[0])
                    secondsSearch = re.findall(r'(\d+) seconds?', capture)
                    seconds = 0 if len(secondsSearch) == 0 else int(secondsSearch[0])
                    hoursSearch = re.findall(r'(\d+) hours?', capture)
                    hours = 0 if len(hoursSearch) == 0 else int(hoursSearch[0])
                    videoDuration = seconds + minutes * 60 + hours * 60 * 60
                    actualDuration = int(actualSeconds) + int(actualMinutes) * 60
                    print(f'Video Duration: {videoDuration}, Actual Duration: {actualDuration}')

                    if not abs(videoDuration - actualDuration) < actualDuration * 0.02:
                        durFail = True

                    #except:
                    #    print(f"Could not locate video duration for {link.get_attribute('aria-label')}")

                #print(find_near_matches(str(song), capture, max_l_dist=4))
                print(f'Song Name matches: {len(find_near_matches(str(song), capture, max_l_dist=2))}')
                #print(find_near_matches(str(artist), capture, max_l_dist=4))
                print(f'Artist name matches: {len(find_near_matches(str(artist), capture, max_l_dist=2))}')

                if len(find_near_matches(str(song), capture, max_l_dist=2)) and len(find_near_matches(str(artist), capture, max_l_dist=2)) and durFail is False: 
                    youtube_link = link.get_attribute("href")
                    youtube_link = youtube_link.split('&', 1)[0]
                    found = True
                    print(f'Found YouTube link: {youtube_link}')
                    break
                else:
                    print("Match not found, moving on...")
                    sus += 1
            
            if found is False:
                error = True

            driver.quit()

        except Exception as e:
            driver.quit()      
            error = True
            print(f"Failed search for {song}, retrying attempt {attempt + 1} of 5...")
            attempt += 1
            continue

        break

    # catch errors
    if error is True:
        print(f"Error for {rline}")

        with open(instructions["convertOutput"],'a', encoding="utf-8") as file:
            file.write(f"MANUAL REPLACE: {rline}\n")
            print(f"MANUAL REPLACE: {rline}\n")

        return

    # write into file for translation
    with open(instructions["convertOutput"],'a', encoding="utf-8") as file:
        if sus >= 2:
            file.write(f'CHECK: {rline} | {youtube_link}\n')
            print(f'Written: CHECK: {rline} | {youtube_link}\n')
        else:
            file.write(f'{rline} | {youtube_link}\n')
            print(f'Written: {rline} | {youtube_link}\n')


# Writing the playlist name at the top
def write_name(playlist):
    with open(instructions["convertOutput"],'a', encoding="utf-8") as file:
        if os.stat(instructions["convertOutput"]).st_size != 0:
            file.write("\n")
        file.write(f"Playlist: {playlist}\n")

# Main
if __name__=='__main__':
    # welcome
    print("\n== Welcome to Sauerkraut ==") 

    # set up variables
    instructions = {
        "convertBool": False,
        "convertDuration": False,
        "convertInput": ".\\files\\defaultExtractedSpotify.txt",
        "convertOutput": ".\\files\\defaultYouTubeLinks.txt",
        "response": ".\\process\\response_sauerkraut.txt" 
    }

    # get args
    instructions = process_args(instructions)
                
    # CONVERSION
    if instructions["convertBool"]:
        # open file
        with open(instructions["convertInput"], encoding="utf-8") as file:
            
            for line in file:

                rline = line.rstrip()

                # skip if empty
                if rline == "":
                    continue

                # playlist name
                if "Playlist: " in rline:
                    #set up value
                    playlist = rline.split(': ')[1]
                    print(f'Now working on: {playlist}')
                    write_name(playlist)
                    continue

                # run convert
                pattern = ".* \| .* \| .*"
                if instructions["convertDuration"]:
                    pattern = ".* \| .* \| \d:\d\d .*"

                if re.search(pattern, rline):
                    search = ' | '.join(rline.split(' | ')[0:-1])
                    convert(search, instructions)
                
                if not re.search(pattern, rline) or '\\' in rline :
                    print(f'Skipped... {rline}')
                    continue

            # finish writing 
            print("Finished conversion")

    # NO FLAG
    else:
        print("\nNo flag given. Exiting...\n")