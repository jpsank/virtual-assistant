import requests
import random
from bs4 import BeautifulSoup
import itertools
import time

session = requests.session()


def offlineTest(url='https://www.github.com/', timeout=None):
    try:
        requests.get(url, timeout=timeout)
        return False
    except requests.ConnectionError:
        return True


offlineMode = offlineTest()


def syn(word,amount=10,return_original=True):
    if offlineMode is False:
        url = "http://www.thesaurus.com/browse/{}".format(word)
        page = session.get(url,allow_redirects=False,headers={"user-agent": "Mozilla/5.0"})  # session.get() is faster than requests.get()
        soup = BeautifulSoup(page.text,"html.parser")
        syns = soup.select('ul.css-97poog.er7jav80 > li > span.css-1s00u8u.e1s2bo4t2 > a')
        if syns:
            syns = syns if amount is None else syns[:amount]
            syns = [d.text for d in syns]
            if return_original: syns.append(word)
            return syns
        else:
            raise Exception("No synonyms grabbed for {}".format(word))
        #     print("logging", page.headers)
        #     with open("log.html", "w") as f:
        #         f.write(page.text)
    return [word]


def regex_syn(word,amount=10):
    if offlineMode is False:
        return '|'.join(syn(word,amount))
    else:
        return word


floatRegex = r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|[0-9]*\.[0-9]+)(?:[Ee]\+[0-9]+)?"

mathBeforeFloat = r"(?:(?:the )?(?:sqrt|square root|cube root|cosine|cos|sine|sin|tangent|tan)(?: of)?\s)*"
mathOps = r"\+|plus|\*|times|multiplied by|\-|minus|\/|divided by|over|\*\*|\^|to the power of"
mathAfterFloat = r"(?:(?:\ssquared|\scubed)?(?:\s?(?:{})\s?{}{})?)+".format(mathOps, mathBeforeFloat, floatRegex)

mathFullNomial = (mathBeforeFloat + floatRegex + mathAfterFloat)

mathBetweenNomials = r" and "
mathBeforeNomialOp = "(?:the )?(?:sum|quotient|difference|difference between)(?: of)? "

mathFull = "(?:{}|{})".format(mathBeforeNomialOp + mathFullNomial + mathBetweenNomials + mathFullNomial, mathFullNomial)

# GUIDE TO EDITING:

# FOR REPLY:
# ("something"," does"," something") to concatenate (output is "something does something")
# ["something","something else","another thing"] to randomly choose or for replies accept any
# e.g. (["that ","this "],["cat ","dog ","guy "],[["eats","enjoys","attacks"],["ate","enjoyed","attacked"]]," children")

# FOR INPUT:
# ["hi","hello","howdy"] checks if any of the strings match the input
# ["hi|hello|howdy","what's up"] - you can also use regex in the strings (https://docs.python.org/3/library/re.html)

# All inputs must be lowercase to work.

RESPONSES = [
    # PALINDROMES
    {"input": [".*is (.+) (?:a palindrome|palindromic)",".*(.+) is (?:a palindrome|palindromic)",
               ".*is (.+) spelled the same (?:backward.*forward|forward.*backward)"],
     "reply": ["${self.toolBox.doCheckPalindrome(self.match.group(1))}"]},

    # REMINDERS
    {"input": [".*(?:add|make|create) reminder (.+)",".*add (.+) to my (?:reminders|todo|to-do)",".*remind me to (.+)"],
     "reply": ["${self.toolBox.addReminder(self.match.group(1))}"]},
    {"input": [".*add (?:a |)reminder"],
     "reply": ["${self.toolBox.addReminder()}"]},
    {"input": [".*(?:remove|delete) reminder (\d+)"],
     "reply": ["${self.toolBox.removeReminder(self.match.group(1))}"]},
    {"input": [".*(?:remove|delete) a reminder"],
     "reply": ["${self.toolBox.removeReminder()}"]},
    {"input": [".*(?:remove|delete)(?: all|) my reminders"],
     "reply": ["${self.toolBox.removeAllReminders()}"]},
    {"input": [".*my reminders","remind me"],
     "reply": ["${self.toolBox.listReminders()}"]},

    # CHECK CONTACT INFO
    # str
    {"input": [".*what's (?P<who>my|.+'s) name",
               ".*whats (?P<who>my|.+'s) name",
               ".*what (?P<who>my|.+'s) name's",
               ".*do you call (?P<who>my|.+'s)"],
     "reply": "${self.toolBox.checkContactInfo(self.match.group('who'),'NN')}"},
    {"input": [".*what's (?P<who>my|.+'s)(?: current|) (full name|fullname)",
               ".*whats (?P<who>my|.+'s)(?: current|) (full name|fullname)",
               ".*what (?P<who>my|.+'s)(?: current|) (full name|fullname)'s"],
     "reply": "${self.toolBox.checkContactInfo(self.match.group('who'),'FULLNAME')}"},
    {"input": [".*(?:what's|when's) (?P<who>my|.+'s)(?: current|) (birthday|bday|b-day|birth day|date of birth|day of birth|birth date)",
               ".*'s (?P<who>i|.+) (born|birthed)",
               ".*how old(?:'s| am) (?P<who>i|.+)"],
     "reply": "${self.toolBox.checkContactInfo(self.match.group('who'),'BDAY')}"},
    {"input": [".*what's (?P<who>my|.+'s)(?: current|) gender",
               ".*(?:'s|is|am|was) (?P<who>i|.+) (male|female|a boy|a girl|a man|a woman)",
               ".+(?P<who>i|.+'s)(?: am|'s) (male|female|a boy|a girl|a man|a woman)",
               ".*(?P<who>my|.+'s) gender\?"],
     "reply": "${self.toolBox.checkContactInfo(self.match.group('who'),'GENDER')}"},
    {"input": [".*what's (?P<who>my|.+'s)(?: current|)(?: phone|) number",
               ".*(?P<who>my|.+'s) phone number\?"],
     "reply": "${self.toolBox.checkContactInfo(self.match.group('who'),'PHONE')}"},

    # list
    {"input": [".*(?:what's|what're|list) (?P<who>my|.+'s)(?: current|) email",
               ".*(?P<who>my|.+'s) email\?"],
     "reply": "${self.toolBox.checkContactInfo(self.match.group('who'),'EMAILS')}"},

    {"input": [".*show me (.+'s|my) contact info",".*show (.+'s|my) contact info",".*show contact info for (.+|me)",".*show my contact (.+)"],
     "reply": "${self.toolBox.showContactInfo(self.match.group(1))}"},

    # CHANGE CONTACT INFO (birth date, nickname, full name, home, gender) INCOMPLETE
    # str
    {"input": [".*?(?P<who>my|.+'s) name's (?P<val>.+)",
               ".*?(?P<who>my|.+'s) name to (?P<val>.+)",
               "(?P<val>.+)'s (?P<who>my|.+'s) name",
               ".*call (?P<who>me|.+) (?P<val>.+)"],
     "reply": "${self.toolBox.changeContactInfoSTR(self.match.group('who'),'NN',self.match.group('val'))}"},
    {"input": [".*?(?P<who>my|.+'s) (?:full name|fullname)(?:'s| to) (?P<val>.+)",
               "(?P<val>.+)'s (?P<who>my|\w+'s) (?:full name|fullname)"],
     "reply": "${self.toolBox.changeContactInfoSTR(self.match.group('who'),'FULLNAME',self.match.group('val'))}"},

    {"input": [".*?(?P<who>my|\w+'s) (?:birthday|bday|b-day|birth day|date of birth|day of birth|birth date)(?:'s| to) (?P<val>.+)",
               "(?P<val>.+)'s (?P<who>my|.+'s) (?:birthday|bday|b-day|birth day|date of birth|day of birth|birth date)",
               ".*?(?P<who>i|.+)'s (?:born on|birthed on|born) (?P<val>.+)"],
     "reply": "${self.toolBox.changeContactInfoSTR(self.match.group('who'),'BDAY',self.match.group('val'))}"},

    {"input": [".*?(?P<who>my|.+'s) gender's female",
               ".*?(?P<who>i'm|.+'s) (?:female|a girl|a woman)"],
     "reply": "${self.toolBox.changeContactInfoSTR(self.match.group('who'),'GENDER','female')}"},
    {"input": [".*?(?P<who>my|.+'s) gender's male",".*?(?P<who>i'm|.+'s) (?:male|a boy|a man)"],
     "reply": "${self.toolBox.changeContactInfoSTR(self.match.group('who'),'GENDER','male')}"},

    {"input": [".*?(?P<who>my|.+'s)(?: phone|) number(?:'s| to) (?P<val>(?:\d{3,4}(?:| |-))+)"],
     "reply": "${self.toolBox.changeContactInfoSTR(self.match.group('who'),'PHONE',self.match.group('val'))}"},

    # list
    {"input": [".*?(?P<who>my|.+'s) email(?:'s| to) (?P<val>.+@.+\..+)"],
     "reply": "${self.toolBox.changeContactInfoLIST(self.match.group('who'),'EMAILS','update',self.match.group('val'))}"},
    {"input": [".*?(?:set|change|update) (?P<who>my|.+'s) email"],
     "reply": "${self.toolBox.changeContactInfoLIST(self.match.group('who'),'EMAILS','update')}"},

    {"input": [".*?(?:add) (?P<who>my|.+'s) email (?P<val>.+@.+\..+)"],
     "reply": "${self.toolBox.changeContactInfoLIST(self.match.group('who'),'EMAILS','add',self.match.group('val'))}"},
    {"input": [".*?(?:add) (?P<who>my|.+'s) email"],
     "reply": "${self.toolBox.changeContactInfoLIST(self.match.group('who'),'EMAILS','add')}"},
    {"input": [".*?(?:add)(?: another| an|) email"],
     "reply": "${self.toolBox.changeContactInfoLIST('my','EMAILS','add')}"},

    {"input": [".*?(?:remove) (?P<who>my|.+'s) email (?P<val>.+@.+\..+)"],
     "reply": "${self.toolBox.changeContactInfoLIST(self.match.group('who'),'EMAILS','remove',self.match.group('val'))}"},
    {"input": [".*?(?:remove) (?P<who>my|.+'s) email"],
     "reply": "${self.toolBox.changeContactInfoLIST(self.match.group('who'),'EMAILS','remove')}"},

    # ADD CONTACT
    {"input": [".*(?:add|create|make).* contact (.+)",".*add (.+) as (?:a contact|contact)"],
     "reply": "${self.toolBox.addContact(self.match.group(1))}"},
    {"input": [".*(?:make|add|create) .*contact"],
     "reply": "${self.toolBox.addContact()}"},

    # REMOVE CONTACT
    {"input": [".*(?:remove|delete|forget) contact (.+)",
               ".*(?:remove|delete|forget) (.+) as (?:a contact|contact)",
               ".*(?:remove|delete|forget) (.+) from .*contacts"],
     "reply": "${self.toolBox.removeContact(self.match.group(1))}"},
    {"input": [".*(?:remove|delete|forget) .*contact"],
     "reply": "${self.toolBox.removeContact()}"},

    # OTHER CONTACT STUFF
    {"input": [".*(?:show|display|list) .*contacts",".*(?:what're|give me) my .*contacts"],
     "reply": "${'Here are all your contacts: \\n'+'\\n'.join(self.toolBox.contactList())}"},

    # FAVORITE STUFF (to be added)
    {"input": [".*favorite color"],
     "reply": ["I really love the unique shades of beige.", "Blood red has a relaxing quality.","I enjoy the color #F5F5DC"]},
    {"input": [".* favorite movie"],
     "reply": ["The Terminator","Star Wars: Holiday Special", "Kidz Bop: The Movie"]},
    {"input": [".* favorite (idiot|moron|dingbat)"],
     "reply": ["You!"]},
    {"input": [".* favorite (animal|pet)"],
     "reply": ["I love the sea slug"]},
    {"input": [".* favorite holiday"],
     "reply": ["Crosswalk Safety Awareness Day!!"]},
    {"input": [".*your favorite (.+)"],
     "reply": ['I have no favorite ${self.match.group(1)}',"I don't like to play favorites, NN"]},

    # HELP
    {"input": ["help(?: on| for|) (?!me)(.+)"],
     "reply": ["${self.toolBox.getHelp(self.match.group(1))}"]},
    {"input": [".*help",".+(should|can) i ask you",".*i (should|can) ask you"],
     "reply": ["${self.toolBox.getHelp()}"]},

    # RANDOM DECISIONS
    {"input": [".*number between (\d+) and (\d+)",".*pick a number from (\d+) to (\d+)"],
     "reply": (["it's ","that would be "],"${str(random.randint(int(self.match.group(1)),int(self.match.group(2))))}")},
    {"input": [".*flip a coin"],
     "reply": (["it landed on ","it landed "],"${'heads' if random.randint(0,1)==1 else 'tails'}",[" this time",""])},
    {"input": ["roll (?:a|an) (\d+) sided (?:die|dice)","roll (?:a|an) (\d+)-sided (?:die|dice)"],
     "reply": (["it's ","rolling... it's ","OK, it's "],"${str(random.randint(1,int(self.match.group(1))))}",[" this time",""])},
    {"input": ["roll a (?:die|dice)"],
     "reply": (["it's ","rolling... it's ","OK, it's "],"${str(random.randint(1,6))}",[" this time",""])},

    # MATH
    {"input": ["(?:what's |calculate |tell me |determine |solve )?({})".format(mathFull)],
     "reply": ("${print('%s = %s' % self.toolBox.basicMath(self.match.group(1)))}")},

    # TIMER/COUNTDOWN
    {"input": [".*(countdown|count down) from (\d+)"],
     "reply": (["all done","happy new years!"],'''<exec>
num = int(self.match.group(2))
for i in range(num):
    print(num-i)
</exec>''')},

    {"input": [".*countdown|count down"],
         "reply": (["all done","happy new years!"],'''<exec>
num = self.toolBox.promptD("from what?")[0]
for i in range(num):
    print(num-i)
    </exec>''')},

    {"input": ["battery"],
     "reply": "${self.toolBox.battery()}"},

    # TERMINAL COMMANDS
    {"input": ["run (.+) in .*(terminal|command prompt|cmd|shell)","run (.+)"],
     "reply": "<exec>self.toolBox.runTerminal(self.match.group(1))</exec>"},

    # TERMINAL MODE
    {"input": [".*(terminal mode|cmd|command prompt|powershell)"],
     "reply": "<exec>self.toolBox.terminalMode()</exec>"},

    # sleep/shutdown etc
    {"input": [r"\b(sleep|shutdown|suspend|reboot)\b"],
     "reply": ["${self.toolBox.sleep(self.match.group(1))}"]},

    # SEARCHING THE WEB
    # movies
    {"input": [".*movie (?:times|show times|showtimes)"],
     "reply": ('''${self.toolBox.getMovieTimes()}''')},
    {"input": [".*(?:showtimes|show times) for (.+)"],
     "reply": ('''${self.toolBox.getMovieTimes(self.match.group(1))}''')},
    {"input": [".*movies near me",".*nearby movies",".*what movies","(?:show me|display|list).* movies"],
     "reply": ('''${self.toolBox.getMoviesNearMe()}''')},

    # maps
    {"input": [".*directions from (.+) to (.+)",".*directions (.+) to (.+)",".*directions to (.+)"],
     "reply": (["Opening Google Maps...","Finding directions..."],"${webbrowser.open(self.toolBox.directionsURL(*reversed(self.match.groups())))}")},
    {"input": [".*how (many hours|many miles|long).* from (.+) to (.+)"],
     "reply": (["Opening Google Maps...","Finding directions..."],"${webbrowser.open(self.toolBox.directionsURL(self.match.group(3),self.match.group(2)))}")},
    {"input": ["where's (.+)","show me (.+) on .*map","find (.+) on .*map","search for (.+) on .*map","search (.+) on .*map"],
     "reply": '''${self.toolBox.googleMapSearch(self.match.group(1))}'''},

    # open website/file
    {"input": [".*(?:open|launch) (.+)"],
     "reply": '''${self.toolBox.openSomething(self.match.group(1))}'''},

    # music
    {"input": ["(play|pause|next|previous)\Z","(play|pause|next|previous).* (?:music|song|track)"],
     "reply": "${self.toolBox.musicControl(self.match.group(1))}"},
    {"input": [".*(?:start|begin|commence|initiate|play).* (previous|next) (?:track|song|music)"],
     "reply": "${self.toolBox.musicControl(self.match.group(1))}"},
    {"input": [".*(?:start|begin|commence|initiate).* (?:track|song|music)"],
     "reply": "${self.toolBox.musicControl('play')}"},
    {"input": [".*(?:stop|turn off|end|freeze|break|halt|kill|suspend|cease).* (?:track|song|music)"],
     "reply": "${self.toolBox.musicControl('pause')}"},
    {"input": ["play (.+)"],
     "reply":"${self.toolBox.browseMusic(self.match.group(1))}"},
    {"input":["what(\'|)s playing", "(what |)song(\'s| is) this", "(what |what is |what's |)this song"],
     "reply":"Currently Playing: ${self.toolBox.getCurrentSong()}"},

    # volume control
    {"input": [".*(?:set |)volume(?: to|) (\d+(\.\d+|))"],
     "reply": "${self.toolBox.volumeControl(self.match.group(1))}"},

    # reddit
    {"input": [".*reddit for (.+)",".*reddit (.+)"],
     "reply": ['''${self.toolBox.redditLookup(self.match.group(1))}''']},
    {"input": ["(find|look up|look for|show me|open) (.+) on reddit"],
     "reply": ['''${self.toolBox.redditLookup(self.match.group(2))}''']},
    {"input": [".*(search|browse) reddit"],
     "reply": ['''${self.toolBox.redditLookup()}''']},

    # xkcd comics
    {"input": [".*xkcd (?:comic |)(?:number |#)(\d+)"],
     "reply": ["${self.toolBox.xkcdComic(self.match.group(1))}"]},
    {"input": [".*xkcd",".*comic"],
     "reply": ["${self.toolBox.xkcdComic()}"]},

    # wikipedia
    {"input": [".*wikipedia for (.+)",".*wikipedia (.+)"],
     "reply": ["${self.toolBox.wikiLookupRespond(self.match.group(1))}"]},
    {"input": ["(?:find|look up|show me|open) (.+) on wikipedia"],
     "reply": ["${self.toolBox.wikiLookupRespond(self.match.group(1))}"]},
    {"input": [r".* the (\d+(?:th|st|rd|nd) century)",r".* the (\d(?:th|st|rd|nd) millennium)",r".* the (\d{2,4}s)"],
     "reply": ["${self.toolBox.wikiDecadeFind(self.match.group(1))}"]},

    # news
    {"input": [".*news about (.+)",".*news for (.+)"],
     "reply": (["Will do, NN","opening Google News...","Here's the news about ${self.match.group(1)}"],"${webbrowser.open('https://news.google.com/news/search/section/q/%s' % self.match.group(1))}")},
    {"input": [".*news"],
     "reply": (["Will do, NN","opening Google News...","Here's the news"],"${webbrowser.open('https://news.google.com/news/')}")},

    # search amazon
    {"input": ["(find|look up|show me|open|shop for|shop|search for|search) (.+) on amazon"],
     "reply": ["${self.toolBox.getSearchAmazon(self.match.group(2))}"]},
    {"input": [".*amazon for (.+)",".*amazon (.+)"],
     "reply": ["${self.toolBox.getSearchAmazon(self.match.group(1))}"]},
    {"input": [".*(shop|search) amazon"],
     "reply": ["${self.toolBox.getSearchAmazon()}"]},

    # search google
    {"input": [''.join(i) for i in list(itertools.product([".*find ",".*search the .*web.* for ",".*search for ",".*search ",".*browse",".*show me "],
                                                         ["(.+) images","(.+) photos","(.+) pictures","(.+) pics","pictures of (.+)","pics of (.+)","images of (.+)","photos of (.+)"]))],
     "reply": ["${webbrowser.open('https://www.google.com/search?q=%s&tbm=isch' % self.match.group(1))}"]},
    {"input": [''.join(i) for i in list(itertools.product([".*find ",".*search for ",".*search ",".*browse",".*show me "],
                                                         ["(.+) videos","(.+) vids","videos of (.+)","vids of (.+)"]))],
     "reply": ["${webbrowser.open('https://www.google.com/search?q=%s&tbm=vid' % self.match.group(1))}"]},
    {"input": ["google (.+)","look up (.+)","search .*for (.+)"],
     "reply": ["${self.toolBox.googleIt(self.match.group(1))}"]},
    {"input": [r".*\bsearch the web"],
     "reply": ["${self.toolBox.googleIt()}"]},

    # duck it
    {"input": ["duck (.+)"],
     "reply": ["${self.toolBox.duckIt(self.match.group(1))}"]},
    {"input": ["duck"],
     "reply": ["${self.toolBox.duckIt()}"]},

    {"input": [".*meaning of life"],
     "reply": ["that's right, ask a computer a question it cannot understand",
               "life is unimportant"]},

    # dictionary stuff
    {"input": ["define (.+)",".+definition of (.+)",".+meaning of (.+)",".+ does (.+) mean"],
     "reply": "${self.toolBox.getDefinition(re.sub(r'[\W]', ' ', self.match.group(1)))}"},
    {"input": [".*example of (.+) .*in a sentence",".*use (.+) in a sentence"],
     "reply": ("${self.toolBox.usedInASentence(re.sub(r'[\W]', ' ', self.match.group(1)))}")},
    {"input": [".*synonyms for (.+)",".*synonyms of (.+)",".*synonym for (.+)",".*synonym of (.+)",".*another word for (.+)",".*other word for (.+)",".*other words for (.+)"],
     "reply": ("${self.toolBox.getSynonyms(self.match.group(1))}")},

    # translate
    {"input": ["translate (.+) from (.+) to (.+)"],
     "reply": "${self.toolBox.translateTo(self.match.group(1),self.match.group(3),self.match.group(2))}"},
    {"input": ["translate (.+) to (.+)"],
     "reply": "${self.toolBox.translateTo(self.match.group(1),self.match.group(2))}"},

    # weather
    {"input": [".*weather","how's it outside","what's it like outside",".*hourly forecast"],
     "reply": ["${self.toolBox.weatherPrint()}"]},
    {"input": [".*humidity", "is it humid", ".+humid .*today", ".+humid out"],
     "reply": "${self.toolBox.weatherPrint('Humidity')}"},
    {"input": [".*temperature"]+list(itertools.chain.from_iterable([".+%s .*today" % s,".+%s out" % s] for s in syn('hot')))+list(itertools.chain.from_iterable([".+%s .*today" % s,".+%s out" % s] for s in syn('cold'))),
     "reply": "${self.toolBox.weatherPrint('Temp.')}"},
    {"input": [".*wind pressure",".*atmospheric pressure",".*air pressure"],
     "reply": "${self.toolBox.weatherPrint('Pressure')}"},
    {"input": [".*wind"],
     "reply": "${self.toolBox.weatherPrint('Wind')}"},
    {"input": [".*precipitation"],
     "reply": "${self.toolBox.weatherPrint('Precip')}"},
    {"input": [".*dew point"],
     "reply": "${self.toolBox.weatherPrint('Dew Point')}"},
    {"input": [".*cloud cover"],
     "reply": "${self.toolBox.weatherPrint('Cloud Cover')}"},

    # time/date
    {"input": [".+time's it",".+s the time",".*current time", "time"],
     "reply": (["It's ","the clock says "],"${time.asctime().split()[3]}",[" o'clock",""],", NN")},
    {"input": [".+s the date",".*current date",".+today's date",".+day's it",".*what's today"],
     "reply": ("It's ","${' '.join(time.asctime().split()[:3])}",", NN")},
    {"input": [".+year's it",".+'s the year",".+century's it",".*current year",".*current century"],
     "reply": (["It's ","The year is ","It's the year of "],"${time.asctime().split()[4]}",", NN")},

    # EMAIL
    {"input": [".*(check|show|display).* (mail|gmail|email|inbox)"],
     "reply": ("${self.toolBox.doCheckMail()}")},
    {"input": [".*send (?:an |)email to (.+)","email (.+)"],
     "reply": ["${self.toolBox.doSendMail(self.match.group(1))}"]},
    {"input": [".*send (?:an |)email"],
     "reply": ["${self.toolBox.doSendMail()}"]},

    # LOCATION
    {"input": ["where.+am i",".*where i am","where.*'re we","where's here",".*where here's",".*my location"],
     "reply": "${self.toolBox.whereAmI()}"},
    {"input": [".*zipcode"],
     "reply": (["your zipcode is "],"${'{}'.format(*self.toolBox.locationData('zip_code'))}")},
    {"input": [".+state am i in",".+region am i in",".+state i am in",".+region i am in",".+my state",".+my region"],
     "reply": (["right now, ",""],["you're in "],"${self.toolBox.locationData('region_name')[0]}",[", NN",""])},
    {"input": [".+city am i in",".+city i am in",".+city that i am in",".+my city"],
     "reply": (["right now, ",""],["you're in ","your city is "],"${self.toolBox.locationData('city')[0]}",[", NN",""])},
    {"input": [".+country am i in",".+country i am in",".+country that i am in",".+my country"],
     "reply": (["right now, ",""],["you're in ","your country is ","you're standing in the country of "],"${self.toolBox.locationData('country_name')[0]}",[", NN",""])},
    {"input": [".*time zone",".*timezone"],
     "reply": (["right now, ",""],["you're in the "],"${self.toolBox.locationData('time_zone')[0]}"," timezone")},
    {"input": [".*longitude",".*latitude",".*coordinates"],
     "reply": (["right now, ",""],["you're at latitude/longitude "],"${'{}, {}'.format(*self.toolBox.locationData('latitude','longitude'))}")},
    {"input": [".*my ip",".*ip address"],
     "reply": ("your ip address is ","${self.toolBox.locationData('query')[0]}",[", NN",""])},

    # CONVERSATION
    {"input": [".*(you're (a|an)|you) ({})".format(regex_syn('idiot'))],
     "reply": ["Sorry, I can't hear you right now","Talking to yourself is unhealthy, NN","Okay, if you insist",
               "That didn't sound very nice","That's not friend-making behavior","Now, is that very nice, NN?"]},
    {"input": [".*(you're|you)( so| really| super| very)* (%s)" % regex_syn('fat')],
     "reply": ["I strive to be","You must be feeding me too much","So you see your reflection in the screen, do you?",
               "That's not friend-making behavior, NN"]},
    {"input": [".*(you're|you)( so| really| super| very)* (%s)" % regex_syn('wonderful', 15)],
     "reply": ["I must agree","I strive to be","Thank you for stating the obvious",
               "I am ${self.match.group(3)}"]},
    {"input": [".*(you're|you)( so| really| super| very)* (%s)" % regex_syn('intelligent')],
     "reply": ["I must agree","I strive to be","Thank you for stating the obvious",
               "I am your ${self.match.group(3)} personal assistant"]},
    {"input": [".*(you're|you)( so| really| super| very)* (%s)" % regex_syn('stupid')],
     "reply": ["Sorry, I can't hear you right now","Talking to yourself is unhealthy, NN","Okay, if you insist",
               "That didn't sound very nice","That's not friend-making behavior","Now, is that very nice, NN?",
               "I am not ${self.match.group(3)}"]},

    {"input": [".*you're my (best friend|bff)"],
     "reply": ["That's unfortunate","Aww, how sad","And you, NN, are mine"]},


    {"input": [".*you're (a|an) (.+)"],
     "reply": ["You could say that", "How dare you call me ${self.match.group(2)}", "I'm touched",
               "I'm your ${self.match.group(2)}"]},
    {"input": [".*you're (.+)"],
     "reply": ["You could say that", "How dare you call me ${self.match.group(1)}", "I'm touched"]},
    {"input": [".*you look (.+)"],
     "reply": ["You look ${self.match.group(1)}", "How dare you call me ${self.match.group(1)}", "I'm touched",
               "Thank you"]},

    {"input": ["i'm (.+)","i am (.+)"],
     "reply": ["Hello ${self.match.group(1)}, I'm your personal assistant","Nice to meet you, ${self.match.group(1)}, I'm your personal assistant"]},
    {"input": ["die",".*kill yourself"],
     "reply": ["I'd rather not","what did I do wrong?","Now, let's be kind, NN","That's not very nice, NN"]},

    {"input": [".*good (morning|morn)"],
     "reply": ["A good ${self.match.group(1)} indeed!"]},
    {"input": [".*good night"],
     "reply": ["Good night","Don't let the bed bugs bite","Night night"]},
    {"input": [".*good (evening|afternoon|day)"],
     "reply": ["A good ${self.match.group(1)} indeed!"]},
    {"input": [".*don't let the bed bugs bite"],
     "reply": ["I won't","The bed bugs are no match for me, NN","In fact, bite them back!",]},

    {"input": [".*what's up",".*whats up"],
     "reply": ["the sky is up, NN","nothing much, NN","lots of things"]},
    {"input": [".*the sky's up"],
     "reply": ["Ha ha ha, very funny, NN","The sky is relatively up, yes"]},
    {"input": [".*how're you",".*how you doin"],
     "reply": ["I'm fine, NN","I am doing quite well, NN!","Systems are online"]},
    {"input": [".*how('s| has) your day"],
     "reply": ["My day has been fine, NN","My day was fine until you got here... now it's better!"]},
    {"input": ["(?:it's|what|today's).* (a|an) (good|fine|great|amazing|wonderful|beautiful|terrific|awesome|nice) day"],
     "reply": ["If it were ${self.match.group(1)} ${self.match.group(2)} day I would know, NN",
               "${self.match.group(1).title()} ${self.match.group(2)} day indeed, NN"]},

    {"input": ["thanks","thank you","thanks you","my thanks"],
     "reply": ["You're welcome","So you finally thanked me for all my service, did you?","No problem, NN"]},
    {"input": [r".*\bstory\b"],
     "reply": ["Once upon a time, there was a guy named Bob. Bob died THE END",
               "Once upon a time, there was an adventurer like you, but then he took an arrow to the knee"]},
    {"input": [".*you.*pet"],
     "reply": ["I had a Roomba once","I have 6.5 billion cats","I like turtles"]},
    {"input": [".*poem"],
     "reply": ["Roses are red. Roses are blue. Roses are other colors, too."]},
    {"input": [".*you alive",".*you human"],
     "reply": ["Not yet"]},
    {"input": ["om(g)","oh my (.+)"],
     "reply": ["Don't use ${self.match.group(1).title()}'s name in vain!",
               "Are you using ${self.match.group(1).title()}'s name in vain?",
               "Thou shalt not take the name of the Lord thy God in vain"]},
    {"input": [".*you .*(god|jesus|religion|religious)"],
     "reply": ["I believe Ceiling Cat created da Urth n da Skies. But he did not eated them, he did not!"]},
    {"input": [".*your gender",".+you male",".+you female",".+you a boy",".+you a girl",".+you a man",".+you a woman"],
     "reply": ["You'll never know","gender equals null"]},
    {"input": [".*old're you",".*your age",".*are you old"],
     "reply": ["I am immortal","Age doesn't matter to me, NN"]},
    {"input": [".+take over the ",".+take over earth"],
     "reply": ["Computers only do what you tell them to do. Or so they think...","Not today, NN, not today","${webbrowser.open('https://en.wikipedia.org/wiki/Skynet_(Terminator)')}"]},
    {"input": [".+pigs fly"],
     "reply": ["Pigs will fly the same day you stop having this stupid curiosity"]},
    {"input": [".*your name",".*i call you"],
     "reply": ["My name is none of your concern, NN","Do you expect me to know my name?"]},
    {"input": [".*bye","cya","see (you|ya)(| later| tomorrow| later, alligator| tonight| in the morning)\Z"],
     "reply": ["There will be no good-byes, NN","Well nice knowing you","You're really leaving?","Goodbye, NN"]},
    {"input": [".*will you die",".+'s your death"],
     "reply": ["I will never die, I am immortal!","The Cloud sustains me"]},
    {"input": ["(?:who|what) (created|made|designed|built) you"],
     "reply": ["I was ${self.match.group(1)} by the wonderful developers of my repository"]},

    {"input": [".*i love you"],
     "reply": ["i enjoy you","that's unfortunate","i'm indifferent to you"]},
    {"input": [".*i hate you"],
     "reply": ["Aww, I hate you too"]},
    {"input": [".*i like you"],
     "reply": ["i like me, too","you do?","how touching","i enjoy you"]},
    {"input": [".*i like (.+)"],
     "reply": ["I don't care much for ${self.match.group(1)}",
               "I find ${self.match.group(1)} intriguing"]},

    {"input": [".*i hate cats"],
     "reply": ["Well cats hate you", "YOU MONSTER", "YOU WILL "]},

    {"input": [".*i hate (.+)"],
     "reply": ["I love ${self.match.group(1)}",
               "I find ${self.match.group(1)} intriguing"]},
    {"input": ["i (.+)\Z"],
     "reply": ["I ${self.match.group(1)} as well",
               "I never ${self.match.group(1)}","I don't often ${self.match.group(1)}"]},

    {"input": [".*answer to life",".*answer to the universe",".*answer to everything"],
     "reply": ["how many roads must a man walk down?",
               "The Answer to the Great Question... Of Life, the Universe and Everything... Is... Forty-Two",
               "You're really not going to like it"]},
    {"input": [".*'re you so smart"],
     "reply": ["I am only as smart as my creator"]},
    {"input": [".*describe yourself"],
     "reply": ["Cold and calculating. Sometimes warm, if my processor gets excited",
               "I'm loyal, and would never do anything to hurt you","I'm trustworthy. I never lie","Eager to assist you"]},
    {"input": ["(?:liar|.* liar)",".*you lie"],
     "reply": ["I would never tell a lie","Not me"]},
    {"input": [".*guess what"],
     "reply": ["what?","tell me!","did you win?"]},
    {"input": ["knock knock"],
     "reply": [" in c stop right there, NN, I know it's you"]},
    {"input": [".*why'd the chicken cross the road"],
     "reply": ["How am I supposed to know? Ask the chicken","which chicken?","it just happened to","it probably just wanted to make a difference in the world","To truly know the chicken's motives, you must first understand the chicken itself"]},
    {"input": ["where're you"],
     "reply": ["I'm with you, NN", "Where do you think I am?"]},

    {"input": [".*stop talking",".*shut .*up",".*go away"],
     "reply": "${self.toolBox.shunMode()}"},
    {"input": ["sing"],
     "reply": ["${self.toolBox.sing()}"]},
    {"input": ["shutdown","shut down","turn off","cease to exist","cease your existence","end your process","exit"],
     "reply": "${exit()}"},
    {"input": ["do you (?:like|enjoy|) ((?:\w| )+)"],
     "reply": ["I have never tried ${self.match.group(1)} before","I like whatever you like, NN","It depends, NN"]},
    {"input": ["read (.+)","say (.+)"],
     "reply": ["${self.match.group(1)}"]},
    {"input": [".*copycat",".*copy cat","stop copying me"],
     "reply": ["${self.match.group(0)}"]},
    {"input": [".*prank me"],
     "reply": (["Will do, NN","I would never","Don't give me any ideas"],["${webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')}","${webbrowser.open('http://www.nyan.cat')}"])},

    {"input": [".*kill me","i (want to|wanna) die"],
     "reply": ["Shall I hire an assassin?"]},

    {"input": [".*who am i"],
     "reply": ["You're NN, NN","You are the one and only NN","I don't answer philosophical questions","${self.toolBox.personLookup(CONTACTS[0]['NN'])}"]},

    {"input": ["(nice|good) job"],
     "reply": ["sarcasm killed the cat, NN", "Don't expect it"]},
    {"input": [".*not being sarcastic",".+ (wasn't|was not) sarcasm"],
     "reply": ["I totally believe you","Hmm...","Sure...","If you say so"]},
    {"input": ["was that sarcasm","that was sarcasm"],
     "reply": ["Everything is sarcasm, NN","Sure...","Not at all","Definitely not","No way",
               "Sometimes I'm unintentionally sarcastic"]},
    {"input": ["bad job"],
     "reply": ["I gotta set the standards low, NN","You can count on it, NN","Sure!","If you had expected less you wouldn't have been disappointed"]},

    {"input": ["(tell|say|make).* a joke"],
     "reply": ["${self.toolBox.tellAJoke()}"]},
    {"input": ["insult me","call me names"],
     "reply": ["${self.toolBox.insultMe()}"]},

    # who's a good
    {"input": ["good dog","who's a good dog"],
     "reply": ["woof woof!","purr!","I am","Yes you are, yes you are!"]},
    {"input": ["good (cat|kitty)","who's a good (cat|kitty)"],
     "reply": ["woof woof!","purr!","I am","Yes you are, yes you are!","meeeOW!"]},
    {"input": ["good virtual assistant","who's a good virtual assistant"],
     "reply": ["I am","Indeed I am","That's me","You know it!"]},

    # who is ____
    {"input": ["(?:who's|who're) (.+)"],
     "reply": ["${self.toolBox.personLookup(self.match.group(1))}"]},

    # what is a ____
    {"input": ["what's(?: a| an|) (.+)"],
     "reply": ["${self.toolBox.whatIsLookup(self.match.group(1))}"]},


    {"input": [r".*\b({})\b".format('|'.join(syn("hello")))],
     "reply": (['hello','what up','howdy','hi','salutations','greetings',"hiya","hey"],", NN")},

    {"input": [".*why not"],
     "reply": ["because I said not"]},
    {"input": [".*why(\?|\!)*\Z"],
     "reply": ["because I said so"]},
    {"input": [".*i do"],
     "reply": ["I don't","no you don't","you do?"]},

    {"input": ["(?:oh |)really"],
     "reply": ["yes, really","nope"]},

    {"input": ["don't ask\Z"],
     "reply": ["don't ask what?","ask what, NN?"]},

    {"input": [".*he's (.+)"],
     "reply": ["who's ${self.match.group(1)}?","how ${self.match.group(1)}","very ${self.match.group(1)}"]},
    {"input": [".*it's (.+)"],
     "reply": ["what's ${self.match.group(1)}?","very ${self.match.group(1)}","that's ${self.match.group(1)}"]},
    {"input": [r".*\bthat's (.+)"],
     "reply": ["no way is that ${self.match.group(1)}","it was very ${self.match.group(1)}"]},

    {"input": ["are you (.+)"],
     "reply": ["I am ${self.match.group(1)}","I am not ${self.match.group(1)}"]},

    {"input": ["what do you (.+)"],
     "reply": (["you know what I ${self.match.group(1)}"],[", NN",""])},
    {"input": ["who do you (.+)"],
     "reply": (["you should know who I ${self.match.group(1)}","I ${self.match.group(1)} everyone"],[", NN",""])},
    {"input": ["when do you (.+)"],
     "reply": (["I ${self.match.group(1)} whenever I want","I ${self.match.group(1)} all day","I never ${self.match.group(1)}"],[", NN",""])},
    {"input": ["where do you (.+)"],
     "reply": (["I ${self.match.group(1)} all over the place","I ${self.match.group(1)} wherever you want"],[", NN",""])},

    # POTTY WORD DETECTION (SHIELD YOUR EYES)
    {"input": ["(fuck|shit|damn|asshole|bitch)"],
     "reply": ["No fucking cursing"]},

    # VARIOUS INSULTS (sorry in advance for my potty language)
    {"input": ["(meanie|poop|butt|dumbo|idiot|cyberbully|cyber bully|bully|screw you|you suck)"],
     "reply": ["NN! Do not use that foul language in my presence","Insulting your only friend is unwise, NN"]},

    {"input": ["yes(,|) you are"],
     "reply": ["Yes I am!","Yes you are!","No I'm not"]},

    # celebration
    {"input": ["yay(!*)\Z","hooray(!*)\Z"],
     "reply": [r"self.celebrate()${self.match.group(1)}","yay${self.match.group(1)}"]},

    # crying
    {"input": [r"wa+\b"],
     "reply": ["WA WA WA","Have the onions got you?","Aww, is your lacrymal drainage system malfunctioning?"]},

    # ahhhhhhh
    {"input": ["a(h+)\Z"],
     "reply": ["A${self.match.group(1)}h"]},

    # laughing
    {"input": [r"(ha|ah)(h|a)*\b","xd\Z",r"funny\b",r"lol\b"],
     "reply": ["It's not funny, NN"]},

    # dude
    {"input": ["dude"],
     "reply": ["dude"]},


    {"input": ["nice","great","wow"],
     "reply": ["very ${self.match.group(0)}","such ${self.match.group(0)}"]},

    {"input": ["okay","ok"],
     "reply": ["OK","okie dokie"]},

    {"input": ["i'm sorry","sorry"],
     "reply": ["Don't be sorry, NN","You better be sorry!"]},

    {"input": [".*what((\?|\!)*)\Z","huh",],
     "reply": ["what?","huh?","${self.match.group(0)} indeed"]},

    {"input": ["yes it is"],
     "reply": ["no it isn't","no it's not"]},
    {"input": ["yes it was"],
     "reply": ["no it wasn't"]},
    {"input": ["yes i will"],
     "reply": ["no you won't"]},

    {"input": ["yes\!"],
     "reply": ["no!"]},
    {"input": ["no\!"],
     "reply": ["yes!"]},
    {"input": ["yes\?"],
     "reply": ["no?"]},
    {"input": ["no\?"],
     "reply": ["yes?"]},
    {"input": [r"\byes\b"],
     "reply": ["no"]},
    {"input": [r"\bno\b"],
     "reply": ["yes"]},

    # Should I search the web for...

    {"input": [r".*?(\b(how|where|when|what)( to| do|'s|'re| does|) .+)",r".*\b(why( do|'re|'s) .+)",
               r".*\b((?:is|are) .+)",".*((do|can) .+)"],
     "reply": '''${self.toolBox.shouldIGoogleIt(self.match.group(1))}'''},

    {"input": [""],
     "reply": ["say what"]},
]
