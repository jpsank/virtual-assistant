import time
from datetime import datetime
from dateutil.parser import parse
import json
import math
import random
import webbrowser
import platform
import re
import os
import subprocess
import html
import threading
import pickle
import argparse
from threading import Thread
import readline

import smtplib
import imaplib
import email.parser
import getpass

import requests
from bs4 import BeautifulSoup
if platform.system() == "Windows":
    import winsound

home = os.path.expanduser("~")

primaryCommandPrompt = '>> '
secondaryCommandPrompt = '> '

# <!-- MATH

floatRegexNoPlus = r"-?(?:[0-9]*\.[0-9]+|[0-9]+(?:\.[0-9]*)?)(?:[Ee][+\-][0-9]+)?"
floatRegex = r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|[0-9]*\.[0-9]+)(?:[Ee]\+[0-9]+)?"

mathBeforeFloat = r"(?:(?:the )?(?:sqrt|square root|cube root|cosine|cos|sine|sin|tangent|tan)(?: of)?\s)*"
mathOps = r"\+|plus|\*|times|multiplied by|\-|minus|\/|divided by|over|\*\*|\^|to the power of"
mathAfterFloat = r"(?:(?:\ssquared|\scubed)?(?:\s?(?:{})\s?{}{})?)+".format(mathOps, mathBeforeFloat, floatRegex)

mathFullNomial = (mathBeforeFloat + floatRegex + mathAfterFloat)

mathBetweenNomials = r" and "
mathBeforeNomialOp = "(?:the )?(?:sum|quotient|difference|difference between)(?: of)? "

mathFull = "(?:{}|{})".format(mathBeforeNomialOp + mathFullNomial + mathBetweenNomials + mathFullNomial, mathFullNomial)

# MATH -->

default_contact = {"BDAY": None, "GENDER": None, "NN": None, "FULLNAME": None, "PHONE": None, "EMAILS": []}

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (Klxml.html, like Gecko) Chrome/61.0.3163.100 Safari/537.36 OPR/48.0.2685.39"

currentDir = os.path.dirname(os.path.realpath(__file__))

mtime = os.path.getmtime(currentDir+"/responses.py")
# Load preferences
if os.path.exists(currentDir+"/preferences.json"):
    # print("Fetching preferences...")
    with open(currentDir+"/preferences.json", "r") as f:
        PREFERENCES = json.load(f)
else:
    print("Generating preferences...")
    PREFERENCES = {"contacts":[default_contact], "mtime":mtime, "reminders": [], "musicDir": None}
    if platform.system() == "Darwin":
        PREFERENCES.update({"afplay":False})
    # User initiation
    print("Welcome to virtual-assistant setup, friend")
    CONTACTS = PREFERENCES["contacts"]
    print("Enter your nickname, or hit return and I'll keep calling you 'friend': ")
    CONTACTS[0]["NN"] = input(secondaryCommandPrompt)
    CONTACTS[0]["NN"] = CONTACTS[0]["NN"] if CONTACTS[0]["NN"] != '' else 'friend'
    print("Okay, %s, here's some guidance:" % CONTACTS[0]["NN"])
    print(" - At any time, you can tell me more about yourself and change your contact info")
    print(" - You can also type 'help' if you get hopelessly lost or want to know what I can do")
    PREFERENCES["contacts"] = CONTACTS
    print("Setup complete")

# Load responses
if os.path.exists(currentDir+'/response_data.p') and mtime == float(PREFERENCES["mtime"]):
    # print("Fetching response data...")
    with open(currentDir + '/response_data.p', 'rb') as f:
        RESPONSES = pickle.load(f)
else:
    print("Generating response data...")
    if os.path.exists(currentDir + '/response_data.p'): os.remove(currentDir + '/response_data.p')
    from responses import RESPONSES,offlineMode
    if not offlineMode:
        with open(currentDir + '/response_data.p','wb') as f:
            pickle.dump(RESPONSES,f)
    PREFERENCES["mtime"] = mtime

with open(currentDir+"/preferences.json", "w") as f:
    json.dump(PREFERENCES,f)

CONTACTS = PREFERENCES["contacts"]


def save_preferences():
    with open(currentDir + "/preferences.json", "w") as f:
        json.dump(PREFERENCES, f)

def save_contacts():
    PREFERENCES["contacts"] = CONTACTS
    save_preferences()


def printColumns(data):
    if isinstance(data, dict):
        title_width = max(len(key) for key in data) + 2  # padding
        col_width = max(len(word) for key in data for word in data[key]) + 2  # padding
        for key in data:
            print(key.ljust(title_width),end="")
            print("".join(word.ljust(col_width) for word in data[key]))
    else:
        col_width = max(len(word) for row in data for word in row) + 2  # padding
        for row in data:
            print("".join(word.ljust(col_width) for word in row))


class toolBox:
    def __init__(self, single):
        self.single=single
        return

    def sing(self):
        if platform.system() == "Windows":
            beatlength = 300
            m = random.randint(3,5)
            rand = random.randint(0,1)
            if rand == 0:
                winsound.Beep(200*m,beatlength)
                winsound.Beep(300 * m, beatlength)
                winsound.Beep(400 * m, beatlength)
                winsound.Beep(500 * m, beatlength)
                time.sleep(.5)
                winsound.Beep(300 * m, beatlength)
                winsound.Beep(400 * m, beatlength)
                winsound.Beep(500 * m, beatlength)
                time.sleep(.5)
                winsound.Beep(400 * m, beatlength)
                winsound.Beep(500 * m, beatlength)
                winsound.Beep(600 * m, beatlength)
                time.sleep(.5)
                winsound.Beep(400 * m, beatlength)
                winsound.Beep(300 * m, beatlength)
                winsound.Beep(100 * m, beatlength*2)
            elif rand == 1:
                winsound.Beep(200*m, beatlength)
                winsound.Beep(300*m, beatlength)
                winsound.Beep(400*m, beatlength)
                winsound.Beep(500*m, beatlength)
                winsound.Beep(400*m, beatlength)
                winsound.Beep(300*m, beatlength)
                winsound.Beep(200*m, beatlength)
                winsound.Beep(200*m, beatlength)
                winsound.Beep(300*m, beatlength)
                winsound.Beep(400*m, int(beatlength * 2))
        else:
            print("Sorry, I can only sing on Windows computers")

    def tellAJoke(self):
        r = requests.get("https://www.reddit.com/r/cleanjokes.json?t=month&limit=100",headers={"user-agent":userAgent})
        j = r.json()
        jokes = ["{}\n{}".format(i["data"]["title"],i["data"]["selftext"]) for i in j["data"]["children"]]
        return random.choice(jokes)

    def insultMe(self):
        part1 = ["unable","bunch-backed","loathsome","cream-faced","elvish-mark’d","foul","sodden-witted","dried",
                 "ill-roasted"]
        part2 = ["pretzel nugget","egg","biscuit","worm","toad","mountain goat","deformity","fiend"]

        stem = ["You {}!",
                "You are a {}!",
                "You're a {}!",
                "Away, you {}!",
                "Thou {}!",
                "Go, you {}!"]

        extra = ["Thou hast no more brain than I have in mine elbows!",
                 "There’s no more faith in thee than in a stewed prune.",
                 "The tartness of thy face sours ripe grapes.",
                 "More of your conversation would infect my brain.",
                 "I am sick when I do look on thee!",
                 "If only thou wert clean enough to spit upon!",
                 "I’ll tickle your catastrophe!",
                 "Your brain is as dry as the remainder biscuit after voyage.",
                 "You are not worth the dust which the rude wind blows in your face.",
                 "You are as a candle, the better part burnt out."]

        full = random.choice(stem).format(random.choice(part1) + " " + random.choice(part2))
        if random.random() < .5:
            full += " " + random.choice(extra)
        return full

    def checkPalindrome(self,word):
        if word[::-1] == word:
            return True
        return False

    def doCheckPalindrome(self,word):
        if self.checkPalindrome(word):
            return "'%s' is indeed a palindrome" % word
        else:
            return "'%s' is not a palindrome" % word

    def thesaurus(self,word):
        url = "http://www.thesaurus.com/browse/%s" % word
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        syns = soup.select('ul.css-97poog.er7jav80 > li > span.css-1s00u8u.e1s2bo4t2 > a')
        if syns:
            return [s.text for s in syns]

    def getSynonyms(self,word):
        word = re.sub("\?","",word)
        synonyms = self.thesaurus(word)
        if synonyms:
            string = ', '.join(synonyms)
            choices = ["Here's some synonyms for %s:" % word,
                       "Other words for %s:" % word]
            return "%s %s" % (random.choice(choices),string)
        else:
            return random.choice(["Never heard of it", "I could not find any synonyms for %s, NN" % word])

    def weatherHourly(self,*keys):
        r = requests.get("https://www.wunderground.com/hourly/{}/{}/{}".format(*self.locationData("region_code","city","zip_code")))
        page = BeautifulSoup(r.text,"html.parser")
        rows = page.select("table#hourly-forecast-table > tbody > tr")
        if rows:
            headers = ["Time","Conditions","Temp.","Feels Like","Precip","Amount","Cloud Cover","Dew Point","Humidity","Wind","Pressure"]
            result = [[h for h in headers if not (keys and h not in keys)]]
            for row in rows:
                data = row.select('td')
                if data:
                    for i,d in enumerate(data):
                        if not (keys and headers[i] not in keys):
                            spans = data[i].select('span')
                            text = []
                            if len(spans) > 1:
                                for s in spans:
                                    if not s.has_attr("class") or not "show-for-small-only" in s["class"]:
                                        text.append(s.find(text=True))
                            else:
                                text.append(spans[0].find(text=True))
                            data[i] = ' '.join(''.join(text).split())
                    result.append(data)
            return result

    def weatherCurrent(self,*keys):
        r = requests.get("https://www.wunderground.com/hourly/{}/{}/{}".format(*self.locationData("region_code", "city", "zip_code")))
        page = BeautifulSoup(r.text,"html.parser")
        rows = page.select("table#hourly-forecast-table tbody tr")
        if rows:
            headers = ["Time", "Conditions", "Temp.", "Feels Like", "Precip", "Amount", "Cloud Cover", "Dew Point",
                       "Humidity", "Wind", "Pressure"]
            row = rows[0]
            result = {}
            cells = row.select('td')
            if cells:
                for i, d in enumerate(cells):
                    if not (keys and headers[i] not in keys):
                        spans = cells[i].select('span')
                        text = []
                        if len(spans) > 1:
                            for s in spans:
                                if not s.has_attr("class") or not "show-for-small-only" in s["class"]:
                                    text.append(s.find(text=True))
                        else:
                            text.append(spans[0].find(text=True))
                        cells[i] = ' '.join(''.join(text).split())
                        result[headers[i]] = cells[i]
            return result

    def weatherPrint(self,key=None):
        if key is not None:
            weather = self.weatherCurrent("Time",key)
            weather = [weather["Time"],weather[key]]
            print("The {} for {} is {}".format(key,*weather))
        else:
            print("Here's today's hourly forecast:")
            printColumns(self.weatherHourly())

    def locationData(self,*keys):
        url = 'http://freegeoip.net/json'
        r = requests.get(url)
        j = json.loads(r.text)
        return [j[k] if k in j else None for k in keys]

    def whereAmI(self):
        city, region = self.locationData('city','region_name')
        loc = ("" if city is "" else city+", ") + region
        return random.choice(["you're in ","your location is "])+loc+random.choice([", NN",""])

    def googleMapSearch(self,search):
        search = re.sub(r"\?+\Z", "", search)
        if self.promptYN(random.choice(['Find "%s" on Google Maps? ' % search, 'Search for "%s" on Google Maps? ' % search])):
            webbrowser.open(self.locationURL(search))
            return random.choice(["Searching %s on Google Maps..." % search, "Exploring the world in search of %s..." % search])
        else:
            return random.choice(["Ok then","If you say so"])

    def directionsURL(self,to,fro=None):
        if fro is None:
            return 'https://www.google.com/maps/dir/?api=1&destination=%s' % to
        else:
            return 'https://www.google.com/maps/dir/?api=1&origin=%s&destination=%s' % (fro,to)

    def locationURL(self,place):
        return 'https://www.google.com/maps/search/?api=1&query=%s' %place

    def define(self,word,index=None):
        url = "http://www.dictionary.com/browse/%s" % word
        page = requests.get(url)
        soup = BeautifulSoup(page.text,"html.parser")
        defsets = soup.select('section.css-1sdcacc.e10vl5dg0 ol li span.css-4x41l7.e10vl5dg6')
        if defsets:
            defs = [' '.join(d.text.replace('\n','').replace('\r','').split()) for d in defsets]
            if index is not None:
                return defs[index]
            else:
                return defs

    def getDefinition(self,word):
        d = self.define(word,0)
        if d:
            return "%s: %s" % (word,d)
        else:
            return "Sorry, I don't know that word."

    def battery(self):
        if platform.system() == "Darwin":
            subprocess.call(["pmset", "-g", "batt"])
        elif platform.system() == "Linux":
            os.system("upower -i $(upower -e | grep BAT) | grep --color=never -E \"state|to\ full|to\ empty|percentage\"")

    def translate(self, text, src="en", dest="zh-TW"):
        url = "https://www.translate.com/translator/ajax_translate"
        headers = {"user-agent": userAgent}
        data = {"text_to_translate": text,
                "source_lang": src,
                "translated_lang": dest,
                "use_cache_only": "false"}
        page = requests.post(url, data=data, headers=headers)
        j = json.loads(page.text)
        if j["translation_id"] != 0:
            return html.unescape(j["translated_text"]).encode('utf-8')

    def translateTo(self,text,dest,src="auto detect"):
        LANGUAGES = {'malayalam': 'ml', 'telugu': 'te', 'armenian': 'hy', 'finnish': 'fi', 'urdu': 'ur', 'thai': 'th', 'georgian': 'ka', 'lao': 'lo', 'scots gaelic': 'gd', 'lithuanian': 'lt', 'italian': 'it', 'hmong daw': 'mww', 'auto detect': 'auto_detect', 'belarusian': 'be', 'hebrew': 'iw', 'sesotho': 'st', 'estonian': 'et', 'czech': 'cs', 'basque': 'eu', 'russian': 'ru', 'luxembourgish': 'lb', 'filipino': 'tl', 'welsh': 'cy', 'korean': 'ko', 'sindhi': 'sd', 'persian': 'fa', 'german': 'de', 'samoan': 'sm', 'icelandic': 'is', 'maltese': 'mt', 'somali': 'so', 'malay': 'ms', 'indonesian': 'id', 'spanish': 'es', 'latin': 'la', 'hindi': 'hi', 'hungarian': 'hu', 'danish': 'da', 'xhosa': 'xh', 'sundanese': 'su', 'uzbek': 'uz', 'ukrainian': 'uk', 'slovak': 'sk', 'kannada': 'kn', 'hmong': 'hmn', 'yucatec maya': 'yua', 'afrikaans': 'af', 'albanian': 'sq', 'vietnamese': 'vi', 'croatian': 'hr', 'galician': 'gl', 'bengali': 'bn', 'zulu': 'zu', 'nepali': 'ne', 'slovenian': 'sl', 'cebuano': 'ceb', 'shona': 'sn', 'tamil': 'ta', 'portuguese': 'pt', 'chichewa': 'ny', 'french': 'fr', 'greek': 'el', 'kazakh': 'kk', 'mongolian': 'mn', 'sinhala': 'si', 'tajik': 'tg', 'polish': 'pl', 'malagasy': 'mg', 'chinese (simplified)': 'zh', 'pashto': 'ps', 'marathi': 'mr', 'kyrgyz': 'ky', 'arabic': 'ar', 'hawaiian': 'haw', 'latvian': 'lv', 'igbo': 'ig', 'yiddish': 'yi', 'kurdish': 'ku', 'khmer': 'km', 'punjabi': 'pa', 'esperanto': 'eo', 'javanese': 'jw', 'serbian (latin)': 'sr-La', 'hausa': 'ha', 'amharic': 'am', 'bosnian (latin)': 'bs', 'japanese': 'ja', 'burmese': 'my', 'bulgarian': 'bg', 'turkish': 'tr', 'klingon': 'tlh', 'irish': 'ga', 'catalan': 'ca', 'gujarati': 'gu', 'macedonian': 'mk', 'chinese (traditional)': 'zh-TW', 'maori': 'mi', 'dutch': 'nl', 'frisian': 'fy', 'swedish': 'sv', 'norwegian': 'no', 'english': 'en', 'haitian creole': 'ht', 'swahili': 'sw', 'yoruba': 'yo', 'romanian': 'ro', 'azerbaijani': 'az', 'serbian (cyrillic)': 'sr'}
        if src in LANGUAGES and dest in LANGUAGES:
            translation = self.translate(text,LANGUAGES[src],LANGUAGES[dest])
            if translation is not None:
                return '"%s" in %s: "%s"' % (text, dest, translation.decode())
            else:
                return random.choice(["Could not translate","Translation failed","Failed to translate"])

    def exampleSentences(self,word):
        url = "http://www.dictionary.com/browse/%s" % word
        page = requests.get(url)
        soup = BeautifulSoup(page.text,"html.parser")
        defsets = soup.select('p.partner-example-text')
        if defsets:
            defs = [' '.join(d.text.split()) for d in defsets]
            return defs

    def usedInASentence(self,word):
        examples = self.exampleSentences(word)
        if examples:
            stem = random.choice(["example sentence for %s:" % word, "sentences with %s:" % word])
            return "%s %s" % (stem,random.choice(examples))
        else:
            return random.choice(["Never heard of it", "I could not find sentences for %s, NN" % word])

    def basicMath(self,mathstr):

        andfunctions = {
            r"(\1)+(\2)": ["sum of ","sum "],
            r"(\1)-(\2)": ["difference of ", "difference between ","difference "],
            r"(\1)/(\2)": ["quotient of ","quotient "]
        }
        for f in andfunctions:
            while any(i in mathstr for i in andfunctions[f]):
                mathstr = re.sub(r"(?:the )?(?:{0})({1}){2}({1})(?=[)(])?".format("|".join(andfunctions[f]), mathFullNomial,mathBetweenNomials), f, mathstr)

        signs = {
            "+": ["\s(plus)\s"],
            "-": ["\s(minus)\s"],
            "/": ["\s(over)\s","\s(divided by)\s"],
            "*": ["\s(times)\s","\s(multiplied by)\s"],
            "**": ["\s(to the power of)\s", "\s(to the)\s", "\s(\^)\s"],
            "**2": [r"\s(squared)\b"],
            "**3": [r"\s(cubed)\b"]
        }
        for s in signs:
            mathstr = re.sub("|".join(signs[s]),s,mathstr)

        functions = {
            r"math.cos(\2)": ["cosine of ", "cosine ", "cos of ", "cos "],
            r"math.sin(\2)": ["sine of ", "sine ", "sin of ", "sin "],
            r"math.tan(\2)": ["tangent of ", "tangent ", "tan of ", "tan "],
            r"math.sqrt(\2)": ["square root of ", "square root ", "sqrt of ", "sqrt "],
            r"(\2)**(1/3)": ["cube root of ", "cube root ", "cbrt of ", "cbrt "]
        }
        for f in functions:
            while any(i in mathstr for i in functions[f]):
                mathstr = re.sub(r"(?:the )?({})({})(?=[)(])?".format("|".join(functions[f]),mathFullNomial),f,mathstr)

        try:
            return mathstr, eval(mathstr)
        except NameError:
            return mathstr
        except OverflowError as e:
            return mathstr, e.args[1]

    def moviesNearMe(self):
        url = 'https://www.google.com/search?q=movies%20near%20me'
        page = requests.get(url)
        soup = BeautifulSoup(page.text,"html.parser")
        movies = soup.select('div._Nxj')
        if movies:
            result = []
            for m in movies:
                title = m.select('div a.fl._yxj')
                if title: title = title[0].text
                genre = m.select('span._Bxj')
                if genre: genre = genre[0].text
                if title and genre:
                    result.append('%s (%s)' % (title,genre))
            if result:
                return result

    def getMoviesNearMe(self):
        movies = self.moviesNearMe()
        if movies:
            print('Here are some movies at local theaters:')
            print('\n'.join(movies))
        else:
            print('Failed to find movies')

    def movieShowTimes(self,movie):
        url = "https://www.google.com/search?q=showtimes+for+%s" % movie
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        name = soup.select('div._Kxj span span')
        if name:
            showtimes = {}
            rows = soup.select('table._W5j._Axj tbody tr')
            nrows = []
            last = 0
            for i in range(0, len(rows)):
                if len(rows[i].select("div._U5j")) == 1:
                    nrows.append(rows[last:i])
                    last = i+1
            for r in nrows:
                title = r[0].text
                times = r[1].select('div._wxj')
                if title and times:
                    showtimes[title] = [t.text for t in times]
            if showtimes:
                return name[0].text, showtimes

    def getMovieTimes(self,movie=None):
        if movie is None:
            movie = self.promptANY("Showtimes for what movie?")
        showtimes = self.movieShowTimes(movie)
        if showtimes:
            print('Here are the showtimes for "%s":' % showtimes[0])
            printColumns(showtimes[1])
        else:
            print('Failed to find showtimes')

    def musicControlMac(self, cmd):
        if len(str(subprocess.call(["pgrep","iTunes"])))>0:
            if cmd == "play":
                os.system("osascript -e 'tell Application \"iTunes\" to play'")
            elif cmd == "pause":
                os.system("osascript -e 'tell Application \"iTunes\" to pause'")
            elif cmd == "next":
                os.system("osascript -e 'tell Application \"iTunes\" to play next track'")
            elif cmd == "previous":
                os.system("osascript -e 'tell Application \"iTunes\" to play previous track'")

    def musicControl(self, cmd):
        if cmd == "pause" and platform.system() == "Darwin":
            if PREFERENCES["afplay"] is not False:
                subprocess.call(["kill", str(PREFERENCES["afplay"])])
                PREFERENCES["afplay"] = False
                save_preferences()
                return "Music set to pause"

        if platform.system() == "Linux":
            os.system("rhythmbox-client --{}".format(cmd))
        elif platform.system() == "Darwin":
            self.musicControlMac(cmd)
        else:
            return "Sorry, music control isn't supported for you yet."
        if cmd == "play":
            return "Music set to play"
        elif cmd == "pause":
            return "Music set to pause"
        elif cmd == "next":
            return "Playing next track"
        elif cmd == "previous":
            return "Playing previous track"

    def getCurrentSong(self):
        if platform.system() == "Linux":
            title = subprocess.Popen(["rhythmbox-client", "--print-playing"],
                                     stdout=subprocess.PIPE).stdout.read().decode().strip()
            return "{}".format(title)
        else:
            return "Sorry, your platform doesn't support this feature"

    def browseMusic(self, song):
        if PREFERENCES["musicDir"] is None:
            musicDir = self.promptANY("Please enter the location of your music directory (return to cancel, type 'browse' to browse)")
            if musicDir == "browse":
                import tkinter as tk
                from tkinter import filedialog

                root = tk.Tk()
                root.withdraw()

                musicDir = filedialog.askopenfilename()
                root.quit()
            else:
                musicDir = musicDir.replace("~", home)
            if musicDir is "":
                return "Cancelled"
            PREFERENCES["musicDir"] = musicDir
            save_preferences()
        musicDir = PREFERENCES["musicDir"]
        songs = []
        for root, dirs, files in os.walk(musicDir):
            for name in files:
                if name.endswith("mp3"):
                    songs.append(root+"/"+name)
        for s in songs:
            if song.lower() in s.lower():
                if platform.system() == "Darwin":
                    Thread(target=self.playSongMac, args=(s,)).start()
                    return "Now playing {}".format(s.split("/")[-1].split(".")[0])
                elif platform.system() == "Linux":
                    subprocess.call(["rhythmbox-client","--play-uri={}".format(s)])
                    return "Now playing "+self.getCurrentSong()
                else:
                    return "Sorry, your platform isn't supported yet"

    def playSongMac(self, song):
        self.musicControl("pause")
        p = subprocess.Popen(["afplay", song])
        PREFERENCES["afplay"] = p.pid
        save_preferences()

        if self.single:
            exit(0)
        while self.processCheck(p) and PREFERENCES["afplay"]:
            time.sleep(0.5)
        try:
            p.kill()
        except:
            os.system("kill {}".format(PREFERENCES["afplay"]))

    def processCheck(self, process):
        if process.returncode is None:
            return True
        return False

    def volumeControl(self, volume):
        if not re.match("(\d+(\.\d+|))",volume) or float(volume) > 100 or float(volume) < 0:
            return "Invalid volume input. Please set volume to a number between 0 and 100."
        volume = float(volume)
        # TODO Linux needs testing
        if platform.system() == "Linux":
            os.system("amixer set Master {}%".format(volume))
        elif platform.system() == "Darwin":
            os.system("osascript -e 'set Volume {}'".format(int(volume/10)))
        else:
            return "Sorry, your platform isn't supported for volume control."
        return random.choice(["Volume set to %s" % volume,"I set your volume to %s" % volume])

    def runTerminal(self, command):
        try:
            os.system(command)
        except Exception as e:
            return e

    def terminalMode(self):
        print("Welcome to Terminal Mode! Type 'exit' to leave")
        while True:
            cmd = input(">>> ")
            if cmd == "exit":
                print("Bye Bye!")
                break
            elif platform.system() != "Windows" and cmd == "sudo rm -rf /":
                print("DON'T WIPE YOUR COMPUTER!")
                exec("screw you")
            else:
                os.system(cmd)

    def shunMode(self):
        print("Entering shun mode... beg for forgiveness required")
        done = False
        while not done:
            s = input(primaryCommandPrompt)
            for e in [".*please",".*sorry"]:
                if re.match(e,s):
                    done = True
                    break
            if done:
                print(random.choice(['So you came crawling back', 'There. I hope you have learned your lesson']))
            else:
                print("...")
        print("Shun mode deactivated")

    def sleep(self, cmd):
        if self.promptYN("Are you sure you would like to %s your system? (y/n)" % cmd):
            if platform.system() == "Linux":
                if cmd == "sleep" or cmd == "suspend":
                    os.system("systemctl suspend")
                elif cmd == "shutdown":
                    os.system("shutdown")
                elif cmd == "reboot":
                    os.system("reboot")
            elif platform.system() == "Darwin":
                if cmd == "sleep" or cmd == "suspend":
                    os.system("pmset sleepnow")
                else:
                    return "Sorry, your platform isn't supported yet"
            elif platform.system() == "Windows":
                if cmd == 'sleep' or cmd == 'suspend':
                    os.system(r"%windir%\System32\rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                elif cmd == 'shutdown':
                    os.system(r"%windir%\System32\shutdown.exe -s")
                elif cmd == 'reboot':
                    os.system("%windir%\System32\shutdown.exe -r")
            else:
                return "Sorry, your platform isn't supported yet"
        else:
            return "Canceled"

    def wikiPageScrape(self, page, paragraphs=1):
        soup = BeautifulSoup(page.text, "html.parser")
        desc = soup.select('div.mw-parser-output > p')
        if desc:
            if paragraphs == 1:
                result = desc[0].text
                if "may refer to:" in result:
                    ul = soup.select("div.mw-parser-output > ul")
                    result = "%s %s" % (result,ul[0].text)
                return result
            else:
                result = [d.text for d in desc]
                return result[:paragraphs]

    def wikiLookup(self,topic):
        url = "https://en.wikipedia.org/wiki/?search=%s" % topic
        page = requests.get(url)
        if '?search' in page.url:
            soup = BeautifulSoup(page.text,"html.parser")
            searches = soup.select('div.mw-search-result-heading a')
            if searches:
                prompt = self.promptLIST([s.text for s in searches],
                                         "Choose the number of the article you want to view: (or type 'cancel')",
                                         "Choose a number between 0 and %s (or 'cancel')" % str(len(searches)-1),
                                         "cancel")
                if prompt is False:
                    return False
                page = requests.get("https://en.wikipedia.org%s" % searches[prompt].get('href'))
                return self.wikiPageScrape(page)
            else:
                return None
        else:
            return self.wikiPageScrape(requests.get(page.url))

    def wikiLookupRespond(self,topic):
        wiki = self.wikiLookup(topic)
        if wiki is None:
            return "No Wikipedia articles found"
        elif wiki is False:
            return "Canceled"
        else:
            return wiki

    def whatIsLookup(self,what):
        what = re.sub(r"\?+\Z", "", what)
        if self.promptYN("Check my sources for %s?" %what):
            d = self.define(what)
            if d:
                return "%s: %s" %(what,d[0])

            wiki = self.wikiLookupRespond(what)
            return wiki
        else:
            return "If you say so"

    def wikiTableScrape(self,url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text,"html.parser")
        rows = soup.select("table.wikitable tr")
        links = []
        for r in rows:
            cells = r.find_all(["th","td"])
            for c in cells:
                a = c.find("a")
                if a:
                    links.append(a)
        return links

    def wikiDecadeFind(self, query):
        links = self.wikiTableScrape("https://en.wikipedia.org/wiki/List_of_decades")
        choices = {}
        for l in links:
            if query in l.text:
                choices[l.text] = "https://en.wikipedia.org" + l["href"]
        if len(choices) < 1:
            return random.choice(["Couldn't find requested time period"])
        keys = list(choices.keys())
        index = 0
        if len(choices) > 1:
            index = self.promptLIST(keys,
                                     "Choose the number of the article you want to view: (or type 'cancel' to cancel)",
                                     "Choose a number between 0 and %s (or 'cancel' to cancel)" % str(len(choices)-1),
                                     "cancel")
            if index is False:
                return "Cancelled"
        page = requests.get(choices[keys[index]])
        result = self.wikiPageScrape(page,2)
        return '\n'.join(result)

    def searchAmazon(self,search):
        url = "https://www.amazon.com/s?keywords=%s" % search
        headers = {"User-Agent":  userAgent}
        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        data = []
        results = soup.select("li.s-result-item.celwidget")
        if results:
            for result in results:
                title = result.select("a.s-access-detail-page")
                price = result.select("span.sx-price")
                if title and price:
                    pricetext = price[0].text.split()
                    pricetext = "%s%s.%s" % (pricetext[0],pricetext[1],pricetext[2])
                    data.append({"title":title[0].text,"price":pricetext,"link":title[0]["href"]})
        return data

    def getSearchAmazon(self,search=None):
        if search is None:
            search = self.promptANY("What would you like to shop for? ")
        data = self.searchAmazon(search)
        if not data:
            return random.choice(["No items found!", "I could not find any items, NN"])
        prompt = self.promptLIST(["%s %s" % (i["title"], i["price"]) for i in data],
                                 "Choose the number result you want to open: (or type 'cancel' to return)",
                                 "Pick a number between 0 and %s" % str(len(data)-1), cancel="cancel")
        if prompt is False:
            return "Cancelled"
        else:
            if data[prompt]["link"].startswith("/"):
                data[prompt]["link"] = "https://www.amazon.com"+data[prompt]["link"]
            print("Opening %s..." % (data[prompt]["link"]))
            webbrowser.open(data[prompt]["link"])

    def redditSearchScrape(self, topic):
        url = "https://www.reddit.com/search?q=%s" % topic
        try:
            page = requests.get(url,headers={'user-agent': userAgent})
        except Exception:
            return False
        soup = BeautifulSoup(page.text,"html.parser")
        results = soup.select('div.search-result-link a.search-title')
        if results:
            return results

    def redditLookup(self,topic=None):
        if topic is None:
            topic = self.promptANY(["Search Reddit for what?","What do I search for?"])
        searches = self.redditSearchScrape(topic)
        if searches:
            prompt = self.promptD("Which number post to open? (or type 'cancel' to return)\n%s" % '\n'.join(["%s. %s" % (i,s.text) for i,s in enumerate(searches)]),cancel="cancel")
            if prompt:
                p = prompt[0]
                webbrowser.open(searches[p].get('href'))
                return random.choice(["Opening reddit post","Opening '%s'" % searches[p].text])
            else:
                return "Cancelled"
        elif searches is False:
            return random.choice(["Error searching for reddit posts","I could not open reddit, NN"])
        else:
            return random.choice(["No Reddit posts found!","I could not find any reddit posts, NN"])

    def xkcdComic(self,number=None):
        if number is None:
            webbrowser.open("https://c.xkcd.com/random/comic/")
            return random.choice(["Here's a random xkcd comic","Here you go"])
        else:
            webbrowser.open("https://xkcd.com/%s" % number)
            return random.choice(["Here's comic number %s" % number,"Opening comic number %s..." % number])

    def getHelp(self,key=None):
        with open(currentDir+"/help.json", "r") as f:
            helpData = json.load(f)
        if key is None:
            print("Here's what I can do:")
            colspan = len(max(helpData,key=lambda k: len(k)))
            for term, descrip in helpData.items():
                print("{} - {}".format(term+" "*(colspan-len(term)), descrip))
        elif key in helpData:
            print("{}: {}".format(key, helpData[key]))
        else:
            print("No help entry for '{}'".format(key))

    def sendEmail(self, from_addr, to_addr_list, cc_addr_list, subject, message, login, password, smtpserver='smtp.gmail.com:587'):
        header = 'From: %s\nTo: %s\nCc: %s\nSubject: %s\n' % (from_addr,', '.join(to_addr_list),', '.join(cc_addr_list),subject)
        message = header + message

        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login, password)
        problems = server.sendmail(from_addr, to_addr_list, message)
        server.quit()
        return problems

    def doSendMail(self,to=None):
        emails = CONTACTS[0]["EMAILS"]
        if emails:
            if len(emails) == 1:
                from_addr = emails[0]
            else:
                prompt = self.promptLIST(emails, "Choose the from address (or 'cancel')", cancel="cancel")
                if prompt is False:
                    return "Cancelled"
                else:
                    from_addr = emails[prompt]
        else:
            prompt = self.promptANY("From address: ")
            if re.match("(.+)@(.+)\.(.+)", prompt) is None:
                return "Email address '%s' invalid. Cancelled" % prompt
            from_addr = prompt

        if to is None:
            to = input("To whom? ")
        index = self.parseContactString(to)
        if index is not False and index is not None:
            if self.promptYN("Mail to your contact %s's email?" % CONTACTS[index]["NN"]):
                if CONTACTS[index]["EMAILS"]:
                    if len(CONTACTS[index]["EMAILS"]) > 1:
                        prompt = self.promptLIST(CONTACTS[index]["EMAILS"],
                                                 "Which of %s's emails? (or 'cancel')" % CONTACTS[index]["NN"],
                                                 cancel="cancel")
                        if prompt is False:
                            return "Cancelled"
                        else:
                            to = CONTACTS[index]["EMAILS"][prompt]
                    else:
                        to = CONTACTS[index]["EMAILS"][0]
                else:
                    print("You have not set any emails for %s" % CONTACTS[index]["NN"])
        if re.match("(.+)@(.+)\.(.+)",to) is None:
            return "Email address '%s' invalid. Cancelled" % to

        password = getpass.getpass("Login to your email %s. Password: " % from_addr)
        print("MESSAGE")
        print("From: %s" % from_addr)
        print("To: %s" % to)
        subject = input("Subject: ")
        message = input("Message: ")
        if self.promptYN("Send email?"):
            self.sendEmail(from_addr=from_addr,
                           to_addr_list=[to],
                           cc_addr_list=[],
                           subject=subject,
                           message=message,
                           login=from_addr,
                           password=password)
            print("Email sent.")
        else:
            return "Cancelled"

    def checkMail(self,username,password):
        M = imaplib.IMAP4_SSL("imap.gmail.com")
        try:
            M.login(username,password)
        except Exception as e:
            if "[AUTHENTICATIONFAILED]" in str(e):
                return None
            else:
                raise e
        M.select(readonly=True)
        messages = []
        typ, data = M.search(None, '(UNSEEN)')
        for num in data[0].split():
            typ, data = M.fetch(num, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    email_parser = email.parser.BytesFeedParser()
                    email_parser.feed(response_part[1])
                    msg = email_parser.close()
                    messages.append({"HEADERS":{header.upper(): msg[header] for header in ['to', 'from', "subject"]}})
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            ctype = part.get_content_type()
                            cdispo = str(part.get('Content-Disposition'))
                            if ctype == 'text/plain' and 'attachment' not in cdispo:
                                body = part.get_payload(decode=True)
                                break
                    else:
                        body = msg.get_payload(decode=True)
                    messages[-1].update({"BODY": body.decode()})

        M.close()
        M.logout()
        return messages

    def doCheckMail(self):
        emails = CONTACTS[0]["EMAILS"]
        if emails:
            if len(emails) == 1:
                username = emails[0]
            else:
                prompt = self.promptLIST(emails, "Choose the address to check (or 'cancel')", cancel="cancel")
                if prompt is False:
                    return "Cancelled"
                else:
                    username = emails[prompt]
        else:
            prompt = self.promptANY("Email address: ")
            if re.match("(.+)@(.+)\.(.+)",prompt) is None:
                return "Email address '%s' invalid. Cancelled" % prompt
            username = prompt
        password = getpass.getpass("Login to %s. Password: " % username)
        messages = self.checkMail(username,password)
        if messages is not None:
            if messages:
                print("UNREAD MESSAGES (%s)" % len(messages))
                i = 0
                for m in messages:
                    print("---------------")
                    for l in m["HEADERS"]:
                        print("%s: %s" % (l.title(), m["HEADERS"][l]))
                    print()
                    body = m["BODY"]
                    body = re.sub(r"[\n\r]+","\n  ",body)
                    if len(body) > 1000:
                        body = body[:1000]+"..."
                    print("  "+body)
                    print()
                    i += 1
                    if i % 5 == 0:
                        print("---------------")
                        if not self.promptYN("%s messages remaining. See more? " % (len(messages)-i)):
                            return "Exited mail"
            else:
                return random.choice(["No unread mail","You've read all the messages in your inbox",
                                      "I could not find any unread mail"])
        else:
            return "Invalid credentials, cancelled"

    def appCheck(self, thing):
        opSys = platform.system()
        if opSys == "Linux":
            for path in ["/usr/share/applications/", "{}/.local/share/applications/".format(home)]:
                if os.path.isfile("{}{}.desktop".format(path,thing)):
                    return thing
                elif len(thing.split(" ")) == 1:
                    for file in os.listdir(path):
                        if "-" in file:
                            for i in file.split("-"):
                                if i.replace(".desktop","") == thing:
                                    return file.replace(".desktop","")
            else:
                if len(thing.split(" ")) > 1:
                    return self.appCheck("-".join(thing.split(" ")))
        elif opSys == "Darwin":
            if os.path.exists("/Applications/{}.app".format(thing)):
                return thing
            if len(thing.split(" "))==1:
                for i in thing.split(" "):
                    for x in os.listdir("/Applications"):
                        for z in x.split(" "):
                            if z.lower().replace(".app","") == i:
                                return x
            return None
        elif opSys == "Windows":
            for app in os.listdir(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"):
                fullpath = os.path.join("C:\ProgramData\Microsoft\Windows\Start Menu\Programs",app)
                if os.path.isdir(fullpath):
                    for app2 in os.listdir(fullpath):
                        if thing == os.path.splitext(app2)[0].lower():
                            return os.path.join(fullpath,app2)
                else:
                    if thing in os.path.splitext(app)[0].lower():
                        return fullpath
        return None

    def openSomething(self,thing):
        if os.path.exists(r'"%s"' % thing):
            if self.promptYN('Open file %s? ' % thing):
                try:
                    print("Opening %s..." % thing)
                    os.startfile(thing)
                except:
                    print('Unable to open file')
        else:
            appcheck = self.appCheck(thing)
            if appcheck is not None:
                opSys = platform.system()
                if opSys == "Linux":
                    threading.Thread(target=lambda: subprocess.call(["gtk-launch",appcheck], stdout=subprocess.DEVNULL)).start()
                elif opSys == "Windows":
                    subprocess.Popen('"%s"' % appcheck,shell=True)
                elif opSys == "Darwin":
                    threading.Thread(target=lambda: subprocess.call(["/usr/bin/open", "-a", appcheck])).start()

                print("Attempting to open {}".format(appcheck))
            else:
                url = thing
                if '.' not in url:
                    url = "%s.com" % url
                if not url.startswith('http'):
                    url = "https://%s" % url
                if self.promptYN('Open website %s? ' % url):
                    try:
                        print("Opening %s..." % url)
                        webbrowser.open(url)
                    except:
                        print("Unable to open %s" % url)
                else:
                    print("Cancelled")

    def googleIt(self,search=None):
        if search is None:
            search = self.promptANY("Search the web for what?")
        webbrowser.open("https://www.google.com/search?q=%s" % search)
        return random.choice(["googling %s" % search,"searching for %s" % search, "accessing interwebs", "okay, NN, I'll google that"])

    def shouldIGoogleIt(self,search):
        if self.promptYN(random.choice(['Should I search the web for "%s"?' % search, 'Do web search for "%s"? ' % search])):
            return self.googleIt(search)
        else:
            return random.choice(["Ok then", "If you say so"])

    def duckIt(self, search=None):
        if search is None:
            search = self.promptANY("Search the web for what?")
        webbrowser.open("https://duckduckgo.com/?q={}".format(search))
        return random.choice(["Searching Duck Duck Go for {}".format(search), "Ducking it!", "Searching for {}".format(search)])

    def getReminderDate(self,reminder):
        patterns = [r"\s?(?:at |on )?(?:!in )((\d{1,2}(:\d{2})?) ?(pm|am|))",
                    r"next (?:week|month)",
                    r"(?:january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sept|october|oct|november|nov|december|dec)(?:\d{1,2}(?:, \d{4})?)?",
                    r"(?:teatime|midnight|noon)",
                    r"(?:monday|mon|tuesday|tues|wednesday|wed|thursday|thurs|friday|fri|saturday|sat|sunday|sun)",
                    r"in (\d+ (?:minute|hour|day|week|month|year)s?)"]
        timeday = None
        timedate = None
        if re.search(patterns[0], reminder):
            m = re.search(patterns[0], reminder)
            # hrs, mins = m.group(1).split(":")
            # hrs, mins = int(hrs), int(mins)
            # timeday = "{:02}:{:02}".format(hrs,mins)
            timeday = m.group(1)
        elif re.search(patterns[3], reminder):
            m = re.search(patterns[3], reminder)
            if m.group(0) == "teatime":
                timeday = "04:00 pm"
            elif m.group(0) == "midnight":
                timeday = "12:00 am"
            elif m.group(0) == "noon":
                timeday = "12:00 pm"
        if re.search(patterns[1], reminder):
            m = re.search(patterns[1], reminder)
            timedate = m.group(0)
        elif re.search(patterns[2], reminder):
            m = re.search(patterns[2], reminder)
            timedate = m.group(0)
        elif re.search(patterns[4], reminder):
            m = re.search(patterns[4], reminder)
            timedate = m.group(0)
        elif re.search(patterns[5], reminder):
            m = re.search(patterns[5], reminder)
            timedate = "now + " + m.group(1)
        if timeday is None and timedate is None:
            prompt = self.promptANY("When should I remind you? (or 'cancel') ", cancel="cancel")
            return self.getReminderDate(prompt)
        result = []
        if timeday is not None: result.append(timeday)
        if timedate is not None: result.append(timedate)
        for p in patterns:
            reminder = re.sub(p,"",reminder)
        return result, reminder

    def getReminderDatePAM(self,reminder):
        rdate, reminder = self.getReminderDate(reminder)
        if rdate:
            if not rdate[0].endswith("pm") and not rdate[0].endswith("am") and (":" in rdate[0] or rdate[0].isdigit()):
                if ":" in rdate[0]:
                    hrs, mins = rdate[0].split(":")
                    hrs, mins = int(hrs), int(mins)
                elif rdate[0].isdigit():
                    hrs, mins = int(rdate[0]),0
                # rdate[0] = "{:02}:{:02}".format(hrs, mins)
                if hrs <= 12:
                    currenthr = datetime.today().hour
                    if currenthr > 12:
                        choice = "pm"
                    else:
                        choice = "am"
                    if self.promptYN(random.choice(["Is that {:02}:{:02} {}? y/n ".format(hrs, mins, choice.upper()),
                                                    "Do you mean {:02}:{:02} {}? y/n ".format(hrs, mins, choice.upper())])):
                        rdate[0] += choice
                    else:
                        rdate[0] += "am" if choice == "pm" else "pm"
            rdate = ' '.join(rdate)
        return rdate, reminder

    def checkForAtRun(self):
        p = subprocess.Popen('launchctl list | grep "com.apple.atrun"', stdout=subprocess.PIPE, shell=True)
        output = p.stdout.read()
        print("OUTPUT",output)
        return False if output == "" else True

    def addReminder(self,reminder=None):
        # sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.atrun.plist

        if reminder is None:
            reminder = self.promptANY("What should I add to your reminders? ")
        if self.promptYN("Add '%s' to your reminders? " % reminder):
            PREFERENCES["reminders"].append([reminder,None])
            save_preferences()
            print("I've added that to your reminders")
            if platform.system() == "Darwin":
                if self.checkForAtRun():
                    if self.promptYN("Should I also make a scheduled popup for that? "):
                        rdate, reminder = self.getReminderDatePAM(reminder)
                        if rdate:
                            command = '''osascript -e 'tell app "System Events" to display dialog "{}" with title "Reminder from Virtual Assistant"' '''.format(reminder)
                            with open("tmp.sh","w") as f:
                                f.write(command)
                            fullc = '''at -f tmp.sh %s 2>&1 | awk '/job/ {print $2}' ''' % rdate
                            p = subprocess.Popen(fullc, stdout=subprocess.PIPE, shell=True)
                            job = int(p.stdout.read().strip())
                            os.remove("tmp.sh")

                            PREFERENCES["reminders"][-1][1] = job
                            save_preferences()
                            print(random.choice(["Okay. I scheduled to remind you at {} (job {})".format(rdate,job)]))
                    else:
                        print(random.choice(["Okay, I won't make a popup reminder."]))
                else:
                    print('Tip: to allow for scheduled reminders, run:')
                    print('    sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.atrun.plist')
        else:
            print("I won't add that to your reminders")

    def removeReminder(self,index=None):
        if len(PREFERENCES["reminders"]) == 0:
            return "No reminders to remove"
        if index is not None:
            index = int(index)
            if not 0 <= index < len(PREFERENCES["reminders"]):
                return "You do not have that many reminders"
        else:
            index = self.promptLIST(PREFERENCES["reminders"],"Which reminder to remove? (or 'cancel')",cancel="cancel")
            if index is False:
                return "Cancelled"
        reminder,job = PREFERENCES["reminders"][index]
        if self.promptYN("Remove '%s' from your reminders? " % reminder):
            del PREFERENCES["reminders"][index]
            save_preferences()
            print("I've deleted your reminder '%s'" % reminder)
            if job is not None and self.promptYN("Also delete the scheduled popup for this reminder? "):
                os.system("atrm %s" % job)
                print("deleted job {}".format(job))
        else:
            print("Okay, I won't remove that reminder")

    def removeAllReminders(self):
        if self.promptYN("Remove all reminders? "):
            jobs = [str(r[1]) for r in PREFERENCES["reminders"] if r[1] is not None]
            if jobs:
                os.system("atrm {}".format(' '.join(jobs)))
                print("deleted {} {}".format("jobs" if len(jobs) > 1 else "job", ', '.join(jobs)))
            PREFERENCES["reminders"] = []
            save_preferences()
            return "I've deleted all your reminders"
        else:
            return "Okay, I won't remove your reminders"

    def listReminders(self):
        if PREFERENCES["reminders"]:
            print("Here are your reminders:")
            for i,r in enumerate(PREFERENCES["reminders"]):
                print(("%s. %s" % (i, r[0]))+(" ({})".format(r[1]) if r[1] is not None else ""))
        else:
            return "You have no reminders, NN"

    def personLookup(self,name):
        name = re.sub(r"\?+\Z","",name)
        index = self.parseContactString(name)
        if index is not False and index is not None:
            if self.promptYN("Show %s's contact info?" % CONTACTS[index]["NN"]):
                self.showContactInfo(index)
            else:
                print("Okay then")
            return

        if self.promptYN("Search Wikipedia for %s?" %name):
            wiki = self.wikiLookupRespond(name)
            return wiki

        return random.choice(["Never heard of them"])

    def parseContactString(self, tag):
        if isinstance(tag, str):
            tag = tag.lower()
            if tag in ['my', 'me', 'i']:
                return 0
            else:
                if tag.endswith("'s"):
                    tag = tag[:-2]
                result = None
                for i, c in enumerate(CONTACTS):
                    if tag in c["NN"].lower() \
                            or c["NN"].lower() in tag \
                            or (c["FULLNAME"] is not None and any(n.lower() in c["FULLNAME"].split() for n in tag.split())):
                        prompts = ["Are you referring to your contact NN?","You mean your contact NN?",
                                   "Are you talking about your contact NN?"]
                        if self.promptYN(random.choice(prompts).replace("NN",c["NN"])):
                            return i
                        else:
                            result = False
                return result
        elif isinstance(tag, int):
            return tag

    def addContact(self,name=None):
        if name is None:
            name = self.promptANY("What is the contact's name?")
        if self.promptYN("Add contact '%s'?" % name):
            con = default_contact.copy()
            con["NN"] = name
            CONTACTS.append(con)
            save_contacts()
            return random.choice(["Added %s as a contact" % name, "I've added your contact %s" % name,
                                  "%s has been added as a contact" % name])
        else:
            return "Cancelled"

    def removeContact(self, name=None):
        if name is None:
            name = self.promptANY("Which contact to remove?")
        contactIndex = self.parseContactString(name)
        name = CONTACTS[contactIndex]["NN"]
        if contactIndex is False:
            return random.choice(["No other contacts named '%s'" % name,"Cancelled"])
        elif contactIndex is None:
            return random.choice(["No contact named '%s'" % name,"I could not find any contact named '%s'" % name,
                                  "I couldn't find the contact you were looking for, NN"])
        elif contactIndex == 0:
            return "You can't remove yourself, NN!"
        else:
            if self.promptYN("Are you sure you want to remove contact '%s'?" % CONTACTS[contactIndex]["NN"]):
                del CONTACTS[contactIndex]
                save_contacts()
                return random.choice(["Removed %s from your contacts, NN" % name,"Your contact %s has been removed, NN" % name,
                                      "Contact %s has been deleted, NN" % name])
            else:
                return "Cancelled"

    def showContactInfo(self, contact):
        contactNum = self.parseContactString(contact)
        if isinstance(contactNum,int):
            for k in CONTACTS[contactNum]:
                print("%s: %s" % (k,CONTACTS[contactNum][k]))
        else:
            print("Failed to find contact")

    def contactList(self):
        return [c["NN"] for c in CONTACTS]

    def checkContactInfo(self,contact,key):
        contactNum = self.parseContactString(contact)
        if isinstance(contactNum,int):
            if contactNum == 0:
                responses = {
                    "NN": ["Your name is NN, NN", "I thought you would know your own name, NN",
                           "I call you NN, but we all know what people call you behind your back"],
                    "BDAY": ["You were born on BDAY, NN"],
                    "FULLNAME": ["Your full name is FULLNAME, NN", "I thought you would know your own full name, NN"],
                    "GENDER": ["You're GENDER, NN", "You should know this, NN"],
                    "PHONE": ["Your phone number is PHONE, NN"],
                    "EMAILS": [["You have not set any emails, NN"], ["Your only email is EMAILS, NN"],
                               ["Your emails are EMAILS, NN"]]
                }
            else:
                responses = {
                    "NN": ["NN's name is NN", "I have a feeling you already know it",
                           "NN's name is - you guessed it - NN"],
                    "BDAY": ["NN was born on BDAY", "NN's birthday is BDAY"],
                    "FULLNAME": ["NN's full name is FULLNAME"],
                    "GENDER": ["NN is GENDER", "Apparently, NN is GENDER"],
                    "PHONE": ["NN's phone number is PHONE"],
                    "EMAILS": [["You have not set any emails for NN"], ["NN's only email is EMAILS"],
                               ["NN's emails are EMAILS"]]
                }
            if key in responses:
                if isinstance(CONTACTS[contactNum][key],list):
                    length = len(CONTACTS[contactNum][key])
                    i = 0 if length == 0 else 1 if length == 1 else 2
                    choice = random.choice(responses[key][i])
                else:
                    choice = random.choice(responses[key])
                for r in responses:
                    new = CONTACTS[contactNum][r]
                    new = ", ".join(new) if isinstance(new,list) else "UNSPECIFIED" if new is None else new
                    choice = choice.replace(r,new)
                return choice
        fail = ["I don't know who that is", "Who's that?"]
        return random.choice(fail)

    def changeContactInfoSTR(self,contact,key,newValue):
        contactNum = self.parseContactString(contact)
        fail = ["Unable to find contact %s" % contact]
        if isinstance(contactNum,int):
            if key in CONTACTS[contactNum]:
                original = "UNSPECIFIED" if CONTACTS[contactNum][key] is None else CONTACTS[contactNum][key]
                name = "you" if contactNum == 0 else CONTACTS[contactNum]["NN"]
                possessive = "your" if contactNum == 0 else "%s's" % CONTACTS[contactNum]["NN"].capitalize()
                if key == "BDAY":
                    try:
                        newValue = parse(newValue).strftime('%m/%d/%Y')
                    except ValueError:
                        return "Could not parse the date of birth entered"
                    if self.promptYN('Change %s birth date to %s? ' % (possessive,newValue)):
                        self.changeContactSTR(contactNum, {key: newValue})
                        return "%s birthday is now %s" % (possessive.capitalize(),CONTACTS[contactNum][key])
                    else:
                        return "Leaving %s birthday as %s" % (possessive,original)
                elif key == "NN":
                    if self.promptYN('Change %s nickname to %s? ' % (possessive,newValue)):
                        self.changeContactSTR(contactNum, {key: newValue})
                        return "I will call %s '%s' from now on" % (name,CONTACTS[contactNum][key])
                    else:
                        return "%s name will be left as '%s'" % (possessive.capitalize(),original)
                elif key == "FULLNAME":
                    if self.promptYN('Change %s full name to %s? ' % (possessive,newValue)):
                        self.changeContactSTR(contactNum, {key: newValue})
                        return "%s full name is now %s" % (possessive.capitalize(),CONTACTS[contactNum][key])
                    else:
                        return "%s full name will be left as '%s'" % (possessive.capitalize(),original)
                elif key == "GENDER":
                    if self.promptYN('Change %s gender to %s? ' % (possessive,newValue)):
                        self.changeContactSTR(contactNum, {key: newValue})
                        return "%s gender has been changed to %s" % (possessive.capitalize(),CONTACTS[contactNum][key])
                    else:
                        return "%s gender will be left as '%s'" % (possessive.capitalize(),original)
                elif key == "PHONE":
                    if "-" in newValue or " " in newValue:
                        newValue = re.sub('[^0-9]+', '', newValue)
                    if self.promptYN('Change %s phone number to %s? ' % (possessive,newValue)):
                        self.changeContactSTR(contactNum, {key: newValue})
                        return '%s phone number is now %s' % (possessive.capitalize(),CONTACTS[contactNum][key])
                    else:
                        return "%s phone number will be left as '%s'" % (possessive.capitalize(),original)
        return random.choice(fail)

    def changeContactInfoLIST(self, contact, key, action, item=None):
        contactNum = self.parseContactString(contact)
        if isinstance(contactNum, int):
            if key in CONTACTS[contactNum]:
                if item is None:
                    if action is 'remove':
                        if len(CONTACTS[contactNum][key]) == 0:
                            return "No items to remove"
                        elif len(CONTACTS[contactNum][key]) == 1:
                            item = CONTACTS[contactNum][key][0]
                        else:
                            prompt = self.promptLIST(CONTACTS[contactNum][key],"Which item to remove? (or 'cancel') ", cancel="cancel")
                            if prompt is False:
                                return "Cancelled"
                            else:
                                item = CONTACTS[contactNum][key][prompt]
                    elif action is 'add':
                        item = self.promptANY("Enter new item:", cancel="cancel")
                        if item is False:
                            return "Cancelled"
                    elif action is 'update':
                        item = self.promptANY("What should I set it as?", cancel="cancel")
                        if item is False:
                            return "Cancelled"
                else:
                    if action is 'remove':
                        if item not in CONTACTS[contactNum][key]:
                            return "Item to remove not found. Cancelled"
                original = CONTACTS[contactNum][key]
                name = "you" if contactNum == 0 else CONTACTS[contactNum]["NN"]
                possessive = "your" if contactNum == 0 else "%s's" % CONTACTS[contactNum]["NN"].capitalize()
                if key == "EMAILS":
                    if action != 'remove' and re.match("(.+)@(.+)\.(.+)", item) is None:
                        return "Email address '%s' invalid. Cancelled" % item
                    else:
                        item = re.sub(r"[?!]+\Z","",item)
                    if self.promptYN('%s %s email %s? ' % (action.capitalize(), possessive, item)):
                        if action == "remove":
                            self.changeContactLIST(contactNum, remove={key: item})
                        elif action == "add":
                            self.changeContactLIST(contactNum, add={key: item})
                        elif action == "update":
                            self.changeContactLIST(contactNum, update={key: [item]})
                        if len(CONTACTS[contactNum][key]) > 1:
                            return '%s emails are now %s' % (possessive.capitalize(),', '.join(CONTACTS[contactNum][key]))
                        elif len(CONTACTS[contactNum][key]) == 1:
                            return '%s email is now %s' % (possessive.capitalize(), CONTACTS[contactNum][key][0])
                        else:
                            return '%s email has been removed' % (possessive.capitalize())
                    else:
                        if len(CONTACTS[contactNum][key]) > 1:
                            return "%s emails will be left as %s" % (possessive.capitalize(),', '.join(original))
                        elif len(CONTACTS[contactNum][key]) == 1:
                            return '%s email will remain %s' % (possessive.capitalize(),original[0])
                        else:
                            return '%s will remain without email' % (name.capitalize())

        return random.choice(["Unable to find contact %s" % contact])

    def changeContactSTR(self, contactNum, update):
        CONTACTS[contactNum].update(update)
        save_contacts()

    def changeContactLIST(self, contactNum, add={}, remove={}, update={}):
        if update:
            CONTACTS[contactNum].update(update)
        if remove:
            for key in remove:
                CONTACTS[contactNum][key].remove(remove[key])
        if add:
            for key in add:
                CONTACTS[contactNum][key].append(add[key])
        save_contacts()

    def promptANY(self,prompt,password=False,cancel=None):
        print(random.choice(prompt) if isinstance(prompt, list) else prompt)
        answer = input(secondaryCommandPrompt)
        if cancel is not None and re.match(cancel,answer):
            return False
        return answer

    def promptYN(self,prompt,failsafe="Yes or no?",y="y",n="n"):
        print(random.choice(prompt) if isinstance(prompt,list) else prompt)
        answer = input(secondaryCommandPrompt).lower()
        if re.match(y,answer):
            return True
        elif re.match(n,answer):
            return False
        else:
            return self.promptYN(failsafe,failsafe,y,n)

    def promptD(self,prompt,failsafe="Pick a number",cancel=None):
        print(random.choice(prompt) if isinstance(prompt,list) else prompt)
        answer = input(secondaryCommandPrompt).lower()
        if cancel is not None and re.match(cancel,answer):
            return False
        result = []
        for m in re.findall("[+-]?\d+",answer):
            result.append(int(m))
        if result:
            return result
        else:
            return self.promptD(failsafe,failsafe,cancel=cancel)

    def promptLIST(self,list,prompt,failsafe="Pick a number",cancel=None):
        prompt = self.promptD("%s\n%s" % (prompt, '\n'.join(["%s. %s" % (i, s) for i, s in enumerate(list)])),failsafe,cancel=cancel)
        if prompt is False:
            return False
        while prompt[0] >= len(list) or prompt[0] < 0:
            prompt = self.promptD(failsafe,failsafe, cancel=cancel)
            if prompt is False:
                return False
        return prompt[0]


class VirtAssistant:
    def __init__(self, single=False):
        self.match = None
        self.text = None
        self.toolBox = toolBox(single)

    def float_to_str(self,f):
        s = str(f)
        if s.endswith(".0"): s = s[:-2]
        return s

    def text2num(self, textnum, numwords={}):
        if not numwords:
            units = [
                "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen",
            ]
            tens = ["", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
            scales = ["hundred", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion",
                      "sextillion", "septillion","octillion","nonillion","decillion"]

            numwords["and"] = (1, 0)
            for idx, word in enumerate(units):   numwords[word] = (1, idx)
            for idx, word in enumerate(tens):    numwords[word] = (1, idx * 10)
            for idx, word in enumerate(scales):  numwords[word] = (10 ** (idx * 3 or 2), 0)

        # noAnd = ['between','from']

        # pattern = re.compile("(?<=[a-zA-Z])+(-)(?=[a-zA-Z])+")
        # textnum = re.sub(pattern, ' ', textnum)

        # pattern = re.compile("(?!\s)(-)(?!\s)")
        # textnum = re.sub(pattern,' - ',textnum)

        current = result = 0
        stringlist = []
        onnumber = False
        puncs = '|'.join([r"\%s\s?" % p for p in ".,!?;)(@:;"])
        symbols = "|".join(["\{0}+\s?".format(s) for s in "*/+"])
        symbols += r"|\-+\s|(?<=\d)\-+(?=\d)"
        timeRe = r"\d{1,2}:\d{2}"
        split = re.findall(r"({}\s?|{}\s?|{}|{}|\w+['.]?\w*\s?)".format(timeRe,floatRegexNoPlus,puncs,symbols),textnum)

        class Word:
            def __init__(self,origw):
                self.origw = origw
                self.w = self.origw.strip()
                self.ext = ""

        split = [Word(w) for w in split]
        for i,word in enumerate(split):
            if word.w in numwords and not word.w == "and":
                if numwords[word.w][0] == 1 or (numwords[word.w][0] > 1 and i-1 >= 0 and split[i-1].ext in "ni"):
                    ext = "n"
                else:
                    ext = "w"
            elif word == "and":
                if (i-1 >= 0 and split[i-1].ext == "n") and \
                        (i+1 < len(split) and split[i+1].w in numwords) and \
                        (numwords[split[i+1].w][0] < numwords[split[i-1].w][0]):
                    ext = "a"
                else:
                    ext = "w"
            elif ":" not in word.w and (word.w.isdigit() or re.match(floatRegex,word.w)):
                ext = "i"
            else:
                ext = "w"
            split[i].ext = ext

        for i,word in enumerate(split):
            if word.ext in "nai":
                if word.ext == "i":
                    scale, increment = 1, float(word.w)
                else:
                    scale, increment = numwords[word.w]

                lastscale, lastinc = None, None
                if i-1 >= 0 and split[i-1].ext in "ni":
                    if split[i-1].ext == "i":
                        lastscale, lastinc = 1,float(split[i-1].w)
                    else:
                        lastscale, lastinc = numwords[split[i-1].w]

                if lastinc and lastscale and lastinc < 20 and increment < 20 and lastscale == scale == 1:
                    stringlist.append(self.float_to_str(current) + (" " if word.origw.endswith(" ") else ""))
                    current = increment
                else:
                    current = current * scale + increment
                    if scale > 100:
                        result += current
                        current = 0
                onnumber = True
            elif word.ext == "w":
                if onnumber:
                    stringlist.append(self.float_to_str(result + current) + (" " if split[i-1].origw.endswith(" ") else ""))
                stringlist.append(word.origw)
                result = current = 0
                onnumber = False

        if onnumber:
            stringlist.append(self.float_to_str(result + current))

        return ''.join(stringlist)

    def contractify(self,text):
        dictionary = {
            " was":  "'s",
            " is":   "'s",
            " were": "'re",
            " are":  "'re",
            " did":  "'d"
        }
        regex = r"(\w+)(%s) " % "|".join([d for d in dictionary])
        for m in re.finditer(regex,text):
            text = text.replace(m.group(0),"%s%s " % (m.group(1),dictionary[m.group(2)]))
        return text

    def evaluate(self,text):
        regex = re.compile(r"\${(.+?)}",re.DOTALL)
        for m in re.finditer(regex,text):
            result = eval(m.group(1))
            text = text.replace(m.group(0),result if isinstance(result,str) else '')
        regex = re.compile(r"<exec>(.+?)</exec>",re.DOTALL)
        for m in re.finditer(regex, text):
            result = exec(m.group(1))
            text = text.replace(m.group(0),result if isinstance(result,str) else '')
        return text

    def replaceify(self,text):
        replaces = CONTACTS[0]
        for r in replaces:
            new = ', '.join(replaces[r]) if isinstance(replaces[r],list) else replaces[r] if replaces[r] is not None else 'UNSPECIFIED'
            text = text.replace(r, new)
        return text

    def process_reply(self,text_blueprint):
        if isinstance(text_blueprint, tuple):
            return [self.process_reply(part) for part in text_blueprint]
        elif isinstance(text_blueprint, list):
            return self.process_reply(random.choice(text_blueprint))
        return text_blueprint

    def reply(self,text,oneline=False):
        text = self.text2num(self.contractify(text))
        if " and " in text and oneline:
            texts = text.split(" and ")
            replies = []
            for t in texts:
                self.text = t
                replies.append(self.reply(t))
            return "\n".join(replies)
        for r in RESPONSES:
            self.match = None
            for choice in r["input"]:
                self.match = re.match(choice,text,re.IGNORECASE)
                if self.match is not None:
                    print(choice)
                    print(self.match)
                    try:
                        rep = ''.join(self.process_reply(r["reply"]))
                        return self.replaceify(self.evaluate(rep))
                    except requests.exceptions.ConnectionError:
                        string = random.choice(["Offline, connection failed","It looks like you're offline, NN",
                                                "I could not connect to the interwebs, NN","Connection failed"])
                        return self.replaceify(string)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", nargs='*', type=str, default="", help="Run a single command instead of a session.")
    args = parser.parse_args()

    args.cmd = " ".join(args.cmd)

    if len(args.cmd) > 0:
        assistant = VirtAssistant(single=True)
        rep = assistant.reply(args.cmd, oneline=True)
        if rep is not '': print(rep)
    else:
        assistant = VirtAssistant()
        while True:
            text = input(primaryCommandPrompt)
            rep = assistant.reply(text)
            if rep is not '': print(rep)
