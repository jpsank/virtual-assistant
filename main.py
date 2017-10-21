import time
from datetime import datetime
from dateutil.parser import parse
import json
import math
import random
import webbrowser
import platform
if platform.system() == "Windows":
    import winsound
import re
import os
from responses import RESPONSES

import requests
from lxml import html
from enchant.checker import SpellChecker


SPELL_CHECK = False


spellchecker = SpellChecker("en_US")


primaryCommandPrompt = '>> '
secondaryCommandPrompt = '> '

if os.path.exists('contacts.json'):
    with open('contacts.json','r') as f:
        CONTACTS = json.load(f)
else:
    print("Welcome to virtual-assistant setup, friend")
    CONTACTS = [{"BDAY": None, "GENDER": None, "NN": None, "FULLNAME": None, "EMAIL": None, "PHONE": None}]
    time.sleep(1)
    print("Enter your nickname, or hit return and I'll keep calling you 'friend': ")
    CONTACTS[0]["NN"] = input(primaryCommandPrompt)
    CONTACTS[0]["NN"] = CONTACTS[0]["NN"] if CONTACTS[0]["NN"] != '' else 'friend'
    time.sleep(1)
    print("Okay, %s, here's some guidance:" % CONTACTS[0]["NN"])
    time.sleep(2)
    print(" - At any time, you can tell me more about yourself and change your contact info")
    time.sleep(2)
    print(" - You can also ask me for help if you get hopelessly lost")
    with open('contacts.json', 'w') as f:
        json.dump(CONTACTS, f)
    time.sleep(1)
    print("Setup complete")
    print()
    time.sleep(1)
    print("Now talk to me!")


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
    def __init__(self):
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
            print("Sorry, I can only sing on Windows Computers")

    def thesaurus(self,word):
        url = "http://www.thesaurus.com/browse/%s" % word
        page = requests.get(url)
        tree = html.fromstring(page.content)
        syns = tree.xpath('//div[@class="relevancy-list"]/ul/li/a/span[@class="text"]')
        if syns:
            return ', '.join([d.text_content() for d in syns])
        return random.choice(["Never heard of it", "A %s?" % word])

    def weatherHourly(self,*keys):
        r = requests.get("https://www.wunderground.com/hourly/{}/{}/{}".format(*self.locationData("region_code","city","zip_code")))
        page = html.fromstring(r.content)
        rows = page.xpath("//table[@id='hourly-forecast-table']/tbody/tr")
        if rows:
            headers = ["Time","Conditions","Temp.","Feels Like","Precip","Amount","Cloud Cover","Dew Point","Humidity","Wind","Pressure"]
            result = [[h for h in headers if not (keys and h not in keys)]]
            for row in rows:
                data = row.xpath('./td')
                if data:
                    for i,d in enumerate(data):
                        if not (keys and headers[i] not in keys):
                            text = data[i].xpath('.//span//text()[not(ancestor::*[contains(@class,"show-for-small-only")])]')
                            data[i] = ' '.join(''.join(text).split())
                    result.append(data)
            return result

    def weatherCurrent(self,*keys):
        r = requests.get("https://www.wunderground.com/hourly/{}/{}/{}".format(*self.locationData("region_code", "city", "zip_code")))
        page = html.fromstring(r.content)
        rows = page.xpath("//table[@id='hourly-forecast-table']/tbody/tr")
        if rows:
            headers = ["Time", "Conditions", "Temp.", "Feels Like", "Precip", "Amount", "Cloud Cover", "Dew Point",
                       "Humidity", "Wind", "Pressure"]
            row = rows[0]
            result = {}
            cells = row.xpath('./td')
            if cells:
                for i, d in enumerate(cells):
                    if not (keys and headers[i] not in keys):
                        text = cells[i].xpath('.//span//text()[not(ancestor::*[contains(@class,"show-for-small-only")])]')
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
        tree = html.fromstring(page.content)
        defsets = tree.xpath('//div[@class="def-content"]')
        if defsets:
            defs = [' '.join(d.text_content().replace('\n','').replace('\r','').split()) for d in defsets]
            if index is not None:
                return defs[index]
            else:
                return defs

    def getDefinition(self,word):
        d = self.define(word,0)
        if d:
            return "%s: %s" % (word,d)
        else:
            return "%s (did you mean %s?)" % (random.choice(["Never heard of it", "A %s?" % word]),self.spellcheckSuggest(word))

    def spellcheckSuggest(self,word):
        return ', '.join(spellchecker.suggest(word))

    def usedInASentence(self,word):
        url = "http://www.dictionary.com/browse/%s" % word
        page = requests.get(url)
        tree = html.fromstring(page.content)
        defsets = tree.xpath('//p[@class="partner-example-text"]')
        if defsets:
            defs = [' '.join(d.text_content().split()) for d in defsets]
            return defs
        return random.choice(["Never heard of it", "A %s?" % word])

    def basicMath(self,mathstr):
        signs = {
            "+":["plus"],
            "-":["minus"],
            "/":["over","divided by"],
            "*":["times","multiplied by"],
            "**": ["to the power of", "to the", "\^"]
        }
        for s in signs:
            pattern = re.compile("\d+(\s*(?:%s)\s*)\d+" % '|'.join(signs[s]))
            for m in re.finditer(pattern,mathstr):
                match = m.group(1)
                mathstr = mathstr.replace(match,s)
        try:
            return mathstr, eval(mathstr)
        except NameError:
            return mathstr

    def moviesNearMe(self):
        url = 'https://www.google.com/search?q=movies%20near%20me'
        page = requests.get(url)
        tree = html.fromstring(page.content)
        movies = tree.xpath('//div[@class="_Nxj"]')
        if movies:
            result = []
            for m in movies:
                title = m.xpath('./div/a[@class="fl _yxj"]')
                if title: title = title[0].text_content()
                genre = m.xpath('./span[@class="_Bxj"]')
                if genre: genre = genre[0].text_content()
                if title and genre:
                    result.append('%s (%s)' % (title,genre))
            if result:
                return result

    def movieShowTimes(self,movie):
        url = "https://www.google.com/search?q=showtimes+for+%s" % movie
        page = requests.get(url)
        tree = html.fromstring(page.content)
        name = tree.xpath('//div[@class="_Kxj"]/span/span')
        if name:
            rows = tree.xpath('//table[@class="_W5j _Axj"]/tbody/tr')
            showtimes = {}
            for i in range(0,len(rows),3):
                title = rows[i].text_content()
                times = rows[i+1].xpath('.//div[@class="_wxj"]')
                if title and times:
                    showtimes[title] = [t.text_content() for t in times]
            if showtimes:
                return name[0].text_content(), showtimes

    def runTerminal(self, command):
        try:
            os.system(command)
        except Exception as e:
            return e

    def wikiPageScrape(self, page):
        tree = html.fromstring(page.content)
        desc = tree.xpath('//div[@class="mw-parser-output"]/p')
        if desc:
            result = desc[0].text_content()
            return result

    def wikiLookup(self,topic):
        url = "https://en.wikipedia.org/wiki/?search=%s" % topic
        page = requests.get(url)
        if '?search' in page.url:
            tree = html.fromstring(page.content)
            searches = tree.xpath('//div[@class="mw-search-result-heading"]/a')
            if searches:
                prompt = self.promptD("Choose the number of the article you want to open:\n%s" % '\n'.join(
                    ["%s. %s" % (i, s.text_content()) for i, s in enumerate(searches)]))
                while prompt[0] >= len(searches):
                    prompt = self.promptD("Choose a number between 0 and %s" % str(len(searches)-1))
                page = requests.get("https://en.wikipedia.org%s" % searches[prompt[0]].get('href'))
                return self.wikiPageScrape(page)
            else:
                return
        else:
            return self.wikiPageScrape(requests.get(page.url))

    def whatIsLookup(self,what):
        if self.promptYN("Check my sources for %s?" %what):
            d = self.define(what)
            if d:
                return "%s: %s" %(what,d[0])

            wiki = self.wikiLookup(what)
            if wiki:
                return wiki
        else:
            return "If you say so"

    def redditSearchScrape(self, topic):
        url = "https://www.reddit.com/search?q=%s" % topic
        try:
            page = requests.get(url,headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.55'})
        except ConnectionError:
            return
        tree = html.fromstring(page.content)
        results = tree.xpath('//div[contains(@class, "search-result-link")]//a[contains(@class, "search-title")]')
        if results:
            return results

    def redditLookup(self,topic):
        searches = self.redditSearchScrape(topic)
        if searches:
            prompt = self.promptD("Which number post to open?\n%s" % '\n'.join(["%s. %s" % (i,s.text_content()) for i,s in enumerate(searches)]))
            p = prompt[0]
            webbrowser.open(searches[p].get('href'))
            return random.choice(["Opening reddit post","Opening '%s'" % searches[p].text_content()])
        else:
            return

    def xkcdComic(self,number=None):
        if number is None:
            webbrowser.open("https://c.xkcd.com/random/comic/")
        else:
            webbrowser.open("https://xkcd.com/%s" % number)

    def openSomething(self,thing):
        if os.path.exists(thing):
            if self.promptYN('Open file %s? ' % thing):
                try:
                    print("Opening %s..." % thing)
                    os.startfile(thing)
                except:
                    print('Unable to open file')
        else:
            if self.promptYN('Open website %s? ' % thing):
                try:
                    print("Opening %s..." % thing)
                    if thing.startswith('http'):
                        webbrowser.open(thing)
                    else:
                        webbrowser.open("https://%s" % thing)
                except:
                    print("Unable to open %s" % thing)

    def googleIt(self,search):
        webbrowser.open("https://www.google.com/search?q=%s" % search)
        return random.choice(["googling %s" % search,"searching for %s" % search, "accessing interwebs", "okay, NN, I'll google that"])

    def addContact(self,name=None):
        if name is None:
            name = self.promptANY("What is the contact's name?")
        if self.promptYN("Add contact '%s'?" % name):
            CONTACTS.append({"BDAY": None, "GENDER": None, "NN": name, "FULLNAME": None, "EMAIL": None, "PHONE": None})
            with open('contacts.json', 'w') as f:
                json.dump(CONTACTS, f)
            return "Added %s as a contact" % name
        else:
            return "Cancelling..."

    def removeContact(self, tag=None):
        if tag is None:
            tag = self.promptANY("Which contact to remove?")
        contactIndex = self.parseContactString(tag)
        if self.promptYN("Are you sure you want to remove contact '%s'?" % CONTACTS[contactIndex]["NN"]):
            del CONTACTS[contactIndex]
            with open('contacts.json', 'w') as f:
                json.dump(CONTACTS, f)
            return "Removed %s from your contacts" % tag
        else:
            return "Cancelling..."

    def personLookup(self,name):
        index = self.parseContactString(name)
        if isinstance(index,int):
            if self.promptYN("Show %s's contact info?" % CONTACTS[index]["NN"]):
                self.showContactInfo(index)
            else:
                print("Okay then")
            return

        if self.promptYN("Search Wikipedia for %s?" %name):
            wiki = self.wikiLookup(name)
            if wiki is not None:
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
                for i, c in enumerate(CONTACTS):
                    if tag in c["NN"].lower() \
                            or c["NN"].lower() in tag \
                            or (c["FULLNAME"] is not None and any(n.lower() in c["FULLNAME"].split() for n in tag.split())):
                        prompts = ["Are you referring to your contact NN?","You mean your contact NN?","Are you talking about your contact NN?"]
                        if self.promptYN(random.choice(prompts).replace("NN",c["NN"])):
                            return i
        elif isinstance(tag, int):
            return tag

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
        if isinstance(contactNum,int) and key in CONTACTS[contactNum]:
            if contactNum == 0:
                responses = {
                    "NN": ["Your name is NN, NN", "I thought you would know your own name, NN",
                           "I call you NN, but we all know what people call you behind your back"],
                    "BDAY": ["You were born on BDAY, NN"],
                    "FULLNAME": ["Your full name is FULLNAME, NN", "I thought you would know your own full name, NN"],
                    "GENDER": ["You're GENDER, NN", "You should know this, NN"],
                    "EMAIL": ["Your email is EMAIL, NN"],
                    "PHONE": ["Your phone number is PHONE, NN"]
                }
            else:
                responses = {
                    "NN": ["NN's name is NN", "I have a feeling you already know it",
                           "NN's name is - you guessed it - NN"],
                    "BDAY": ["NN was born on BDAY","NN's birthday is BDAY"],
                    "FULLNAME": ["NN's full name is FULLNAME"],
                    "GENDER": ["NN is GENDER", "Apparently, NN is GENDER"],
                    "EMAIL": ["NN's email is EMAIL"],
                    "PHONE": ["NN's phone number is PHONE"]
                }
            if key in responses:
                choice = random.choice(responses[key])
                for r in responses:
                    if CONTACTS[contactNum][r] is not None:
                        choice = choice.replace(r,CONTACTS[contactNum][r])
                return choice
        fail = ["I don't know who that is", "Who's that?"]
        return random.choice(fail)

    def changeContactInfo(self,contact,key,newValue):
        contactNum = self.parseContactString(contact)
        fail = ["Unable to find contact %s" % contact]
        if isinstance(contactNum,int) and key in CONTACTS[contactNum]:
            original = "UNKNOWN" if CONTACTS[contactNum][key] is None else CONTACTS[contactNum][key]
            name = "you" if contactNum == 0 else CONTACTS[contactNum]["NN"]
            possessive = "your" if contactNum == 0 else "%s's" % CONTACTS[contactNum]["NN"].capitalize()
            if key == "BDAY":
                try:
                    newValue = parse(newValue).strftime('%m/%d/%Y')
                except ValueError:
                    return "Could not parse the date of birth entered"
                if self.promptYN('Change %s birth date to %s? ' % (possessive,newValue)):
                    self.changeContact(contactNum,{key: newValue})
                    return "%s birthday is now %s" % (possessive.capitalize(),CONTACTS[contactNum][key])
                else:
                    return "Leaving %s birthday as %s" % (possessive,original)
            elif key == "NN":
                if self.promptYN('Change %s nickname to %s? ' % (possessive,newValue)):
                    self.changeContact(contactNum,{key: newValue})
                    return "I will call %s '%s' from now on" % (name,CONTACTS[contactNum][key])
                else:
                    return "%s name will be left as '%s'" % (possessive.capitalize(),original)
            elif key == "FULLNAME":
                if self.promptYN('Change %s full name to %s? ' % (possessive,newValue)):
                    self.changeContact(contactNum,{key: newValue})
                    return "%s full name is now %s" % (possessive.capitalize(),CONTACTS[contactNum][key])
                else:
                    return "%s full name will be left as '%s'" % (possessive.capitalize(),original)
            elif key == "GENDER":
                if self.promptYN('Change %s gender to %s? ' % (possessive,newValue)):
                    self.changeContact(contactNum,{key: newValue})
                    return "%s gender has been changed to %s" % (possessive.capitalize(),CONTACTS[contactNum][key])
                else:
                    return "%s gender will be left as '%s'" % (possessive.capitalize(),original)
            elif key == "EMAIL":
                if self.promptYN('Change %s email to %s? ' % (possessive,newValue)):
                    self.changeContact(contactNum,{key: newValue})
                    return "%s email is now %s" % (possessive.capitalize(),CONTACTS[contactNum][key])
                else:
                    return "%s email will be left as '%s'" % (possessive.capitalize(),original)
            elif key == "PHONE":
                if self.promptYN('Change %s phone number to %s? ' % (possessive,newValue)):
                    self.changeContact(contactNum,{key: newValue})
                    return '%s phone number is now %s' % (possessive.capitalize(),CONTACTS[contactNum][key])
                else:
                    return "%s phone number will be left as '%s'" % (possessive.capitalize(),original)
        return random.choice(fail)

    def changeContact(self,contactNum,update):
        CONTACTS[contactNum].update(update)
        with open('contacts.json', 'w') as f:
            json.dump(CONTACTS,f)

    def promptANY(self,prompt):
        print(random.choice(prompt) if isinstance(prompt, list) else prompt)
        answer = input(secondaryCommandPrompt)
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

    def promptD(self,prompt,failsafe="Pick a number"):
        print(random.choice(prompt) if isinstance(prompt,list) else prompt)
        answer = input(secondaryCommandPrompt).lower()
        result = []
        for m in re.findall("[+-]?\d+",answer):
            result.append(int(m))
        if result:
            return result
        else:
            return self.promptD(failsafe,failsafe)


class JERF:
    def __init__(self):
        self.match = None
        self.text = None
        self.toolBox = toolBox()

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

        noAnd = ['between','from']

        pattern = re.compile("(?<=[a-zA-Z])+(-)(?=[a-zA-Z])+")
        textnum = re.sub(pattern, ' ', textnum)

        pattern = re.compile("(?!\s)(-)(?!\s)")
        textnum = re.sub(pattern,' - ',textnum)

        current = result = 0
        stringlist = []
        onnumber = False
        for word in textnum.split():
            if word in numwords and not (word == 'and' and stringlist[-1] in noAnd):
                scale, increment = numwords[word]
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
            elif word.isdigit():
                scale, increment = 1,int(word)
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
            else:
                if onnumber:
                    stringlist.append(repr(result + current))
                stringlist.append(word)
                result = current = 0
                onnumber = False

        if onnumber:
            stringlist.append(repr(result + current))

        return ' '.join(stringlist)

    def spellcheck(self,text):
        spellchecker.set_text(text)
        for err in spellchecker:
            err.replace(err.suggest()[0] if err.suggest() else err)
        return spellchecker.get_text().lower()

    def contractify(self,text):
        dictionary = {
            " was":"'s",
            " is":"'s",
            " were":"'re",
            " are":"'re",
            " did":"'d"
        }
        regex = r"(\w+)(%s) " % "|".join([d for d in dictionary])
        for m in re.finditer(regex,text):
            text = text.replace(m.group(0),"%s%s " % (m.group(1),dictionary[m.group(2)]))
        return text

    def evaluate(self,text):
        regex = re.compile(r"<eval>(.+?)</eval>",re.DOTALL)
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
            text = text.replace(r,replaces[r] if replaces[r] is not None else 'UNKNOWN')
        return text

    def process_reply(self,text_blueprint):
        if isinstance(text_blueprint, tuple):
            return [self.process_reply(part) for part in text_blueprint]
        elif isinstance(text_blueprint, list):
            return self.process_reply(random.choice(text_blueprint))
        return text_blueprint

    def reply(self,text):
        text = self.text2num(self.contractify(self.spellcheck(text.lower()) if SPELL_CHECK else text.lower()))
        self.text = text
        for r in RESPONSES:
            self.match = None
            for choice in r["input"]:
                self.match = re.match(choice,text)
                if self.match is not None:
                    rep = ''.join(self.process_reply(r["reply"]))
                    return self.replaceify(self.evaluate(rep))
        return 'say what'


assistant = JERF()

while True:
    text = input(primaryCommandPrompt)
    rep = assistant.reply(text)
    if rep is not '': print(rep)
