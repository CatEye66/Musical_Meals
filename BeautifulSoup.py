## Beautiful Soup
## Script for converting YouTube links into mp3s
## CatEye66 2023
## Reference: https://www.thepythoncode.com/article/extracting-and-submitting-web-page-forms-in-python

# imports
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import time
import os
import sys
import getopt
from requests_html import HTMLSession
from pprint import pprint
from urllib.parse import urljoin
import webbrowser
import mutagen
from mutagen.easyid3 import EasyID3
import eyed3
from eyed3 import id3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
import chromedriver_autoinstaller 

from selenium.webdriver.firefox.options import Options as FirefoxOptions

#######################################

# Processing arguments
def process_args(instructions):
    # list of command line arguments
    argList = sys.argv[1:]
    
    # Options
    short_options = "hDi:o:ns:"
    
    # Long options
    long_options = ["help", "Download", "input=", "output=", "numbered", "startingNum="]
    
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argList, short_options, long_options)
        
        # checking each argument
        for currentArgument, currentValue in arguments:
    
            if currentArgument in ("-h", "--help"):
                print("\nUsage: python [program name].py -D -i [path to input text] -o [path to output text] -n -s [starting line number]\n")
                print("-D, --Download: Script will download YouTube links as mp3s")
                print("-i, --input: Input text for YouTube links")
                print("-o, --ouput: Output directory for downloaded mp3s")
                print("-n, --numbered: Script will number tracks")
                print("-s, --startingNum: Script will start reading at the specified line number")
            
            elif currentArgument in ("-D", "--Download"):
                instructions["downloadBool"] = True
                print("Downloading YouTube links")
                
            elif currentArgument in ("-i", "--input"):
                instructions["downloadInput"] = currentValue
                print(f"Input file: {currentValue}")
                
            elif currentArgument in ("-o", "--output"):
                instructions["downloadOutput"] = currentValue
                print(f"Output directory: {currentValue}")

            elif currentArgument in ("-n", "--numbered"):
                instructions["numbered"] = True
                print("Numbering tracks")

            elif currentArgument in ("-s", "--startingNum"):
                instructions["starting"] = int(currentArgument)
                print(f"\nStarting number: {currentValue}")
                
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
    
    return instructions

# Convert video link to mp3
def convert(name, artist, url_payload, track, instructions, session):
    # set up
    if instructions["numbered"]:
        ntrack = str(track).zfill(2)
        filename = f"{ntrack} - {name} - {artist}.mp3"
    else:
        filename = f"{name} - {artist}.mp3"

    print(f"-- Now Working On: {name} --")
    print(f"Trying download...")

    # set up web driver
    error = 0
    attempt = 0
    while attempt < 5: 
        try:
            error = 0
            
            ## web driver for chrome 
            opt = ChromeOptions()
            #opt.add_argument("-incognito")
            #opt.add_argument('--headless') # chrome does not visibly launch
            #opt.add_argument("--disable-blink-features=AutomationControlled") # Adding argument to disable the AutomationControlled flag 
            #opt.add_experimental_option("excludeSwitches", ["enable-automation"]) # Exclude the collection of enable-automation switches 
            #opt.add_experimental_option("useAutomationExtension", False) # Turn-off userAutomationExtension 
            driver = webdriver.Chrome(options=opt)
            driver.maximize_window()
            wait = WebDriverWait(driver, 3)

            ## launch firefox
            #opt = FirefoxOptions()
            #opt.set_preference("browser.privatebrowsing.autostart", True)
            #opt.add_argument('-headless') # firefox does not visibly launch
            #driver = webdriver.Firefox(options=opt)
            #driver.maximize_window()
            #wait = WebDriverWait(driver, 3)
            
            driver.get(instructions["url"])

            inputElement = WebDriverWait(driver, timeout=20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="txtUrl"]')))
            start = WebDriverWait(driver, timeout=20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnSubmit"]')))
            inputElement.send_keys(url_payload)        
            start.click()

            convert = WebDriverWait(driver, timeout=20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn192"]')))
            convert.click()

            download = WebDriverWait(driver, timeout=20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section[1]/div/div[2]/div[2]/div/div[2]/div/div[3]/table/tbody/tr[2]/td[3]/button/a')))
            download = download.get_attribute('href')
            print(f'Download link: {download}')

            driver.quit()
        
        except Exception as e:      
            error = -1
            print(f"Failed search for {name}, retrying attempt {attempt + 1} of 5...")
            attempt += 1
            continue

        break

    if error == -1:
        return error

    attempt = 0
    error = 0
    while attempt < 5:
        try:
            error = 0
            print('Accessing download link...')
            res = session.get(download, allow_redirects=True)
            print(f"Content Type: {res.headers.get('content-type')}")
            open(f'{instructions["songPath"]}\\{filename}', 'wb').write(res.content)
            print(f"Downloaded {filename}!")

        except Exception as e:      
            error = -1
            print(f"Failed download for {name}, retrying attempt {attempt + 1} of 5...")
            attempt += 1
            continue

        break

    if error == -1:
        return error

    return filename


# edit the mp3 metadata
def edit_metadata(filename, name, artist, track, playlist, instructions):
    path = f'{instructions["songPath"]}\\{filename}'
    tag = id3.Tag()
    tag.parse(path)
    tag.title = name
    tag.artist = artist
    tag.track_num = str(track).zfill(2)
    tag.album = playlist
    tag.save()

    print("Metadata complete... {} - {} - {} - {}".format(track, tag.title, tag.artist, tag.album))

# Iterate over video link file, and edit metadata of downloaded file
def eyed3(instructions):
    # set up track no
    if instructions["starting"] >= 0:
        track = instructions["starting"]
    else:
        track = 1
    playlist = ""

    # open file
    with open(instructions["downloadInput"], encoding='utf-8') as file:

    # run inject for every line of file
        for line in file:

            rline = line.rstrip()

            # skip if it does not match formatting 
            if rline == "":
                continue

            # find playlist
            if "Playlist: " in rline:
                #set up value
                playlist = rline.split(': ')[1]
                playlist = re.sub('[\\/:*?"<>\|]','',playlist)
                # set up track no
                if instructions["starting"] >= 0:
                    track = instructions["starting"]
                else:
                    track = 1
                instructions["numbered"] = True

                # set up directory
                if not os.path.exists(f'{instructions["downloadOutput"]}\\{playlist}'):
                    os.makedirs(f'{instructions["downloadOutput"]}\\{playlist}')
                    print("New Playlist created... {}".format(playlist)) 
                else:
                    print("Resuming Playlist... {}".format(playlist))
                instructions["songPath"] = f'{instructions["downloadOutput"]}\\{playlist}'

                continue

            # skip if it does not match formatting 
            pattern = ".* \| .* \| .*"
            if not re.search(pattern, rline) or '\\' in rline:
                print(f'Skipped... {rline}')
                continue
            
            # extract info
            name = rline.split(' | ')[0]
            artist = rline.split(' | ')[1]
            video_url = rline.split(' | ')[-1]

            # skip if it does not match formatting 
            pattern = "https://.*"
            if not re.search(pattern, video_url):
                print(f'Skipped... {rline}')
                track += 1
                continue

            #print(name, artist, str(track).zfill(2), instructions["numbered"], playlist)
            
            # run
            session = HTMLSession()
            filename = convert(name, artist, video_url, track, instructions, session)

            if filename == -1:
                track += 1
                continue
            else:
                edit_metadata(filename, name, artist, track, playlist, instructions)

            # iterate 
            track += 1

# main
if __name__=='__main__':
    # welcome
    print("\n== Welcome to Beautiful Soup ==") 

    # set up variables
    instructions = {
        "downloadBool": False,
        "downloadInput": ".\\files\\defaultYouTubeLinks.txt",
        "downloadOutput": ".\\mp3s",
        "songPath": ".\\mp3s",
        "numbered": False,
        "starting": -1,
        "url": "https://en.y2mate.is/307/youtube-to-mp3.html",
        "response": ".\\process\\response_beautifulsoup.txt"  
    }

    # get args
    instructions = process_args(instructions)
                
    # CONVERSION
    if instructions["downloadBool"]:
        # GO!
        eyed3(instructions)

    # NO FLAG
    else:
        print("\nNo flag given. Exiting...\n")
    
