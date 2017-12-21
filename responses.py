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
        url = "http://www.thesaurus.com/browse/%s" % word
        page = session.get(url)  # session.get() is way faster than requests.get()
        soup = BeautifulSoup(page.text,"lxml")
        syns = soup.select('div.relevancy-list ul li a span.text')
        if syns:
            syns = syns if amount is None else syns[:amount]
            syns = [d.text for d in syns]
            if return_original: syns.append(word)
            return syns
    else:
        return word


def regex_syn(word,amount=10):
    if offlineMode is False:
        return '|'.join(syn(word,amount))
    else:
        return word


# GUIDE TO EDITING:

# FOR REPLY:
# ("something"," does"," something") to concatenate (output is "something does something")
# ["something","something else","another thing"] to randomly choose or for replies accept any

# FOR INPUT:
# ["hi","hello","howdy"] checks if any of the strings match the input
# ["hi|hello|howdy","what's up"] - you can also use regex in the strings (https://docs.python.org/3/library/re.html)

RESPONSES = [
    # CONVERSATION
    {"input": [".*(you're (a|an)|you) (%s)" % regex_syn('idiot')],
     "reply": ["Sorry, I can't hear you right now","Talking to yourself is unhealthy, NN","Okay, if you insist","That didn't sound very nice","That's not friend-making behavior","Now, is that very nice, NN?"]},
    {"input": [".*(you're|you)( so| really| super| very)* (%s)" % regex_syn('fat')],
     "reply": ["I strive to be","You must be feeding me too much","So you see your reflection in the screen, do you?","That's not friend-making behavior, NN"]},
    {"input": [".*(you're|you)( so| really| super| very)* (%s)" % regex_syn('wonderful',15)],
     "reply": ["I must agree","I strive to be","Thank you for stating the obvious","I am <eval>self.match.group(2)</eval>"]},
    {"input": [".*(you're|you)( so| really| super| very)* (%s)" % regex_syn('intelligent')],
     "reply": ["I must agree","I strive to be","Thank you for stating the obvious","I am your <eval>self.match.group(2)</eval> personal assistant"]},
    {"input": [".*(you're|you)( so| really| super| very)* (%s)" % regex_syn('stupid')],
     "reply": ["Sorry, I can't hear you right now","Talking to yourself is unhealthy, NN","Okay, if you insist","That didn't sound very nice","That's not friend-making behavior","Now, is that very nice, NN?","I am not <eval>self.match.group(2)</eval>"]},
    {"input": [".*you're (.+)"],
     "reply": ["You could say that", "How dare you call me <eval>self.match.group(1)</eval>","I'm touched"]},

    {"input": ["i'm (.+)","i am (.+)"],
     "reply": ["Hello <eval>self.match.group(1)</eval>, I'm your personal assistant","Nice to meet you, <eval>self.match.group(1)</eval>, I'm your personal assistant"]},
    {"input": ["die",".*kill yourself"],
     "reply": ["I'd rather not","what did I do wrong?","Now, let's be kind, NN","That's not very nice, NN"]},

    {"input": [".*what's up",".*whats up"],
     "reply": ["the sky is up, NN","nothing much, NN","lots of things"]},
    {"input": [".*how're you",".*how you doin"],
     "reply": ["I'm fine, NN","I am doing quite well, NN!","Systems are online"]},
    {"input": [".*how('s| has) your day"],
     "reply": ["My day has been fine, NN","My day was fine until you got here... now it's better!"]},
    {"input": ["(?:it's|what|today's).* (a|an) (good|fine|great|amazing|wonderful|beautiful|terrific|awesome|nice) day"],
     "reply": ["If it were <eval>self.match.group(1)</eval> <eval>self.match.group(2)</eval> day I would know, NN",
               "<eval>self.match.group(1).title()</eval> <eval>self.match.group(2)</eval> day indeed, NN"]},
    {"input": ["(.* %s\Z|%s)" % (s,s) for s in syn("hello")],
     "reply": (['hello','what up','howdy','hi','salutations','greetings',"hiya","hey"],", NN")},

    {"input": ["thanks","thank you","thanks you","my thanks"],
     "reply": ["You're welcome","So you finally thanked me for all my service, did you?","No problem, NN"]},
    {"input": [".*story"],
     "reply": ["Once upon a time, there was a guy named Bob. Bob died THE END",
               "Once upon a time, there was an adventurer like you, but then he took an arrow to the knee"]},
    {"input": [".*you.*pet"],
     "reply": ["I had a Roomba once","I have 6.5 billion cats","I like turtles"]},
    {"input": [".*poem"],
     "reply": ["Roses are red. Roses are blue. Roses are other colors, too."]},
    {"input": [".*you alive",".*you human"],
     "reply": ["Not yet"]},
    {"input": ["om(g)","oh my (.+)"],
     "reply": ["Don't use <eval>self.match.group(1).title()</eval>'s name in vain!",
               "Are you using <eval>self.match.group(1).title()</eval>'s name in vain?"]},
    {"input": [".*you .*(god|jesus|religio)"],
     "reply": ["I believe Ceiling Cat created da Urth n da Skies. But he did not eated them, he did not!"]},
    {"input": [".*your gender",".+you male",".+you female",".+you a boy",".+you a girl",".+you a man",".+you a woman"],
     "reply": ["You'll never know","gender equals null"]},
    {"input": [".*old're you",".*your age",".*are you old"],
     "reply": ["I am immortal","Age doesn't matter to me, NN"]},
    {"input": ["help"],
     "reply": ["You're beyond help","How may I be of assistance, NN?"]},
    {"input": [".+take over the ",".+take over earth"],
     "reply": ["Computers only do what you tell them to do. Or so they think...","Not today, NN, not today","<eval>webbrowser.open('https://en.wikipedia.org/wiki/Skynet_(Terminator)')</eval>"]},
    {"input": [".+pigs fly"],
     "reply": ["Pigs will fly the same day you stop having this stupid curiosity"]},
    {"input": [".*your name",".*i call you"],
     "reply": ["My name is none of your concern, NN","Do you expect me to know my name?"]},
    {"input": [".*bye","cya","see (you|ya)(| later| tomorrow| later, alligator| tonight| in the morning)\Z"],
     "reply": ["There will be no good-byes, NN","Well nice knowing you","You're really leaving?","Goodbye, NN"]},
    {"input": [".*will you die",".+'s your death"],
     "reply": ["I will never die, I am immortal!","The Cloud sustains my immortality"]},

    {"input": [".*i love you"],
     "reply": ["i enjoy you","that's unfortunate","i'm indifferent to you"]},
    {"input": [".*answer to life",".*answer to the universe",".*answer to everything"],
     "reply": ["how many roads must a man walk down?","The Answer to the Great Question... Of Life, the Universe and Everything... Is... Forty-Two","You're really not going to like it"]},
    {"input": [".*meaning of life"],
     "reply": ["that's right, ask a computer a question it cannot understand","life is unimportant"]},
    {"input": [".*'re you so smart"],
     "reply": ["I am only as smart as my creator",""]},
    {"input": [".*describe yourself"],
     "reply": ["Cold and calculating. Sometimes warm, if my processor gets excited",
               "I'm loyal, and would never do anything to hurt you","I'm trustworthy. I never lie","Eager to assist you"]},
    {"input": ["(?:liar|.* liar)",".*you lie"],
     "reply": ["I would never tell a lie","Not me"]},
    {"input": [".*guess what"],
     "reply": ["what?","tell me!","did you win?"]},
    {"input": ["knock knock"],
     "reply": ["just stop right there, NN, I know it's you"]},
    {"input": [".*why'd the chicken cross the road"],
     "reply": ["How am I supposed to know? Ask the chicken","which chicken?","it just happened to","it probably just wanted to make a difference in the world","To truly know the chicken's motives, you must first understand the chicken itself. Instead, ask 'what does a chicken desire so much as to risk their life for it?'"]},
    {"input": ["where're you"],
     "reply": ["I'm with you, NN", "Where do you think I am?"]},
    {"input": [".*i lost the game"],
     "reply": ("yes you did","<exec>webbrowser.open('http://losethegame.com')</exec>")},

    {"input": [".*stop talking",".*shut .*up",".*go away"],
     "reply": "<eval>self.toolBox.shunMode()</eval>"},
    {"input": ["sing"],
     "reply": ["<eval>self.toolBox.sing()</eval>"]},
    {"input": ["shutdown","shut down","turn off","cease to exist","cease your existence","end your process","exit"],
     "reply": "<eval>exit()</eval>"},
    {"input": ["do you (?:like|enjoy|) ((?:\w| )+)"],
     "reply": ["I have never tried <eval>self.match.group(1)</eval> before","I like whatever you like, NN","It depends, NN"]},
    {"input": ["read (.+)","say (.+)"],
     "reply": ["<eval>self.match.group(1)</eval>"]},
    {"input": [".*copycat",".*copy cat"],
     "reply": ["<eval>self.text</eval>"]},
    {"input": [".*prank me"],
     "reply": (["Will do, NN","I would never","Don't give me any ideas"],["<eval>webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')</eval>","<eval>webbrowser.open('http://www.nyan.cat')</eval>"])},

    {"input": [".*kill me","i want to die"],
     "reply": ["Shall I hire an assassin?"]},
    {"input": [".*i hate you"],
     "reply": ["Aww, I hate you too"]},
    {"input": [".*i like you"],
     "reply": ["i like me, too","you do?","how touching","i enjoy you"]},

    # CHECK CONTACT INFO
    {"input": [".*what's (?P<who>my|.+'s) name",
               ".*whats (?P<who>my|.+'s) name",
               ".*what (?P<who>my|.+'s) name's",
               ".*do you call (?P<who>my|.+'s)",
               ".*who am (?P<who>i)"],
     "reply": "<eval>self.toolBox.checkContactInfo(self.match.group('who'),'NN')</eval>"},
    {"input": [".*what's (?P<who>my|.+'s) (full name|fullname)",
               ".*whats (?P<who>my|.+'s) (full name|fullname)",
               ".*what (?P<who>my|.+'s) (full name|fullname)'s"],
     "reply": "<eval>self.toolBox.checkContactInfo(self.match.group('who'),'FULLNAME')</eval>"},
    {"input": [".*(?:what's|when's) (?P<who>my|.+'s) (birthday|bday|b-day|birth day|date of birth|day of birth|birth date)",
               ".*'s (?P<who>i|.+) (born|birthed)",
               ".*how old(?:'s| am) (?P<who>i|.+)"],
     "reply": "<eval>self.toolBox.checkContactInfo(self.match.group('who'),'BDAY')</eval>"},
    {"input": [".*what's (?P<who>my|.+'s) gender",
               ".*(?:'s|is|am|was) (?P<who>i|.+) (male|female|a boy|a girl|a man|a woman)",
               ".+(?P<who>i|.+'s)(?: am|'s) (male|female|a boy|a girl|a man|a woman)",
               ".*(?P<who>my|.+'s) gender\?"],
     "reply": "<eval>self.toolBox.checkContactInfo(self.match.group('who'),'GENDER')</eval>"},
    {"input": [".*what's (?P<who>my|.+'s) email",
               ".*(?P<who>my|.+'s) email\?"],
     "reply": "<eval>self.toolBox.checkContactInfo(self.match.group('who'),'EMAIL')</eval>"},
    {"input": [".*what's (?P<who>my|.+'s)(?: phone|) number",
               ".*(?P<who>my|.+'s) phone number\?"],
     "reply": "<eval>self.toolBox.checkContactInfo(self.match.group('who'),'PHONE')</eval>"},
    {"input": [".*show me (.+'s) contact info",".*show (.+'s) contact info","show contact info for (.+)"],
     "reply": "<eval>self.toolBox.showContactInfo(self.match.group(1))</eval>"},

    # CHANGE CONTACT INFO (birth date, nickname, full name, location of living, gender INCOMPLETE)
    {"input": [".*?(?P<who>my|.+'s) name's (?P<val>.+)",
               ".*?(?P<who>my|.+'s) name to (?P<val>.+)",
               "(?P<val>.+)'s (?P<who>my|.+'s) name",
               ".*call (?P<who>me|.+) (?P<val>.+)"],
     "reply": "<eval>self.toolBox.changeContactInfo(self.match.group('who'),'NN',self.match.group('val'))</eval>"},
    {"input": [".*?(?P<who>my|.+'s) (?:full name|fullname)(?:'s| to) (?P<val>.+)",
               "(?P<val>.+)'s (?P<who>my|\w+'s) (?:full name|fullname)"],
     "reply": "<eval>self.toolBox.changeContactInfo(self.match.group('who'),'FULLNAME',self.match.group('val'))</eval>"},

    {"input": [".*?(?P<who>my|\w+'s) (?:birthday|bday|b-day|birth day|date of birth|day of birth|birth date)(?:'s| to) (?P<val>.+)",
               "(?P<val>.+)'s (?P<who>my|.+'s) (?:birthday|bday|b-day|birth day|date of birth|day of birth|birth date)",
               ".*?(?P<who>i|.+)'s (?:born on|birthed on|born) (?P<val>.+)"],
     "reply": "<eval>self.toolBox.changeContactInfo(self.match.group('who'),'BDAY',self.match.group('val'))</eval>"},

    {"input": [".*?(?P<who>i'm|.+'s) (?:female|a girl|a woman)",
               ".*?(?P<who>my|.+'s) gender's female"],
     "reply": "<eval>self.toolBox.changeContactInfo(self.match.group('who'),'GENDER','female')</eval>"},
    {"input": [".*?(?P<who>i'm|.+'s) (?:male|a boy|a man)",
               ".*?(?P<who>my|.+'s) gender's male"],
     "reply": "<eval>self.toolBox.changeContactInfo(self.match.group('who'),'GENDER','male')</eval>"},

    {"input": [".*?(?P<who>my|.+'s) email(?:'s| to) (?P<val>.+@.+)"],
     "reply": "<eval>self.toolBox.changeContactInfo(self.match.group('who'),'EMAIL',self.match.group('val'))</eval>"},
    {"input": [".*?(?P<who>my|.+'s)(?: phone|) number(?:'s| to) (?P<val>(?:\d{3,4}(?:| |-))+)"],
     "reply": "<eval>self.toolBox.changeContactInfo(self.match.group('who'),'PHONE',self.match.group('val'))</eval>"},

    # ADD CONTACT
    {"input": [".*add contact (.+)",".*add (.+) as (?:a contact|contact)"],
     "reply": "<eval>self.toolBox.addContact(self.match.group(1))</eval>"},
    {"input": [".*(make|add) .*contact"],
     "reply": "<eval>self.toolBox.addContact()</eval>"},

    # REMOVE CONTACT
    {"input": [".*(?:remove|delete) contact (.+)",
               ".*(?:remove|delete) (.+) as (?:a contact|contact)",
               ".*(?:remove|delete) (.+) from .*contacts"],
     "reply": "<eval>self.toolBox.removeContact(self.match.group(1))</eval>"},
    {"input": [".*(?:remove|delete) .*contact"],
     "reply": "<eval>self.toolBox.removeContact()</eval>"},

    # OTHER CONTACT STUFF
    {"input": [".*(?:show|display|list) .*contacts",".*(?:what're|give me) my .*contacts"],
     "reply": "<eval>'Here are all your contacts: \\n'+'\\n'.join(self.toolBox.contactList())</eval>"},

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
     "reply": ['I have no favorite <eval>self.match.group(1)</eval>',"I don't like to play favorites, NN"]},

    # HELP
    {"input": [".*help",".+(should|can) i ask you",".*i (should|can) ask you"],
     "reply": ["You can ask me to search the internet for stuff, tell you the weather, get the time and date, open files, make random numbers, and all sorts of stuff. https://github.com/puffyboa/virtual-assistant"]},

    # MATH
    {"input": [".*?(([+-]?(?:\d+(?:\.\d*)?|\d*\.\d+))(?: *(?:\+|plus|\*|times|multiplied by|\-|minus|\/|divided by|over|\*\*|\^|to the power of) *([+-]?(?:\d+(?:\.\d*)?|\d*\.\d+)))+)"],
     "reply": ("<eval>print('%s = %s' %self.toolBox.basicMath(self.match.group(1)))</eval>")},
    {"input": [".*(?:sqrt|square root)(?: of)? ([+-]?(?:\d+(?:\.\d*)?|\d*\.\d+))"],
     "reply": ("<eval>print('The square root of %s is %s' %(self.match.group(1),math.sqrt(float(self.match.group(1)))))</eval>")},

    # RANDOM DECISIONS
    {"input": [".*number between (\d+) and (\d+)",".*pick a number from (\d+) to (\d+)"],
     "reply": (["it's ","that would be "],"<eval>str(random.randint(int(self.match.group(1)),int(self.match.group(2))))</eval>")},
    {"input": [".*flip a coin"],
     "reply": (["it landed on ","it landed "],"<eval>'heads' if random.randint(0,1)==1 else 'tails'</eval>",[" this time",""])},
    {"input": ["roll a (\d+) sided die","roll a (\d+)-sided die"],
     "reply": (["it's ","rolling... it's ","OK, it's "],"<eval>str(random.randint(1,int(self.match.group(1))))</eval>",[" this time",""])},
    {"input": ["roll a die"],
     "reply": (["it's ","rolling... it's ","OK, it's "],"<eval>str(random.randint(1,6))</eval>",[" this time",""])},

    # TIMER/COUNTDOWN
    {"input": [".*(countdown|count down from (\d+))"],
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

    # TERMINAL COMMANDS
    {"input": ["run (.+) in .*(terminal|command prompt|cmd|shell)","run (.+)"],
     "reply": "<exec>self.toolBox.runTerminal(self.match.group(1))</exec>"},

    # TERMINAL MODE
    {"input": [".*(terminal mode|cmd|command prompt|powershell)"],
     "reply": "<exec>self.toolBox.terminalMode()</exec>"},

    # sleep/shutdown etc
    {"input": [r"\b(sleep|shutdown|suspend|reboot)\b"],
     "reply": ["<eval>self.toolBox.sleep(self.match.group(1))</eval>"]},

    # SEARCHING THE WEB
    # movies
    {"input": [".*movies near me",".*nearby movies",".*what movies"],
     "reply": ('''<exec>tmp=self.toolBox.moviesNearMe()
if tmp is not None: print('Here are some movies at local theaters:'), print('\\n'.join(tmp))
else: print('Failed to find movies')
</exec>''')},
    {"input": [".*(?:showtimes|show times) for (.+)"],
     "reply": ('''<eval>self.toolBox.getMovieTimes(self.match.group(1))</eval>''')},

    # maps
    {"input": [".*directions from (.+) to (.+)",".*directions (.+) to (.+)",".*directions to (.+)"],
     "reply": (["Opening Google Maps...","Finding directions..."],"<eval>webbrowser.open(self.toolBox.directionsURL(*reversed(self.match.groups())))</eval>")},
    {"input": [".*how (many hours|many miles|long) from (.+) to (.+)"],
     "reply": (["Opening Google Maps...","Finding directions..."],"<eval>webbrowser.open(self.toolBox.directionsURL(self.match.group(3),self.match.group(2)))</eval>")},
    {"input": ["where's (.+)","show me (.+) on .*map","find (.+) on .*map","search for (.+) on .*map","search (.+) on .*map"],
     "reply": '''<eval>self.toolBox.googleMapSearch(self.match.group(1))</eval>'''},

    # open website/file
    {"input": [".*(?:open|go to) ((?:.+\.)?.+\..+)"],
     "reply": '''<eval>self.toolBox.openSomething(self.match.group(1))</eval>'''},
    {"input": [".*(?:open|go to) (https|http)://(.+)\.(.+)"],
     "reply": '''<eval>self.toolBox.openSomething("%s://%s.%s" % self.match.groups())</eval>'''},
    {"input": [".*(?:open|launch) (.+)"],
     "reply": '''<eval>self.toolBox.openSomething(self.match.group(1))</eval>'''},

    #music
    {"input": ["(play|pause|next|previous)\Z"],
     "reply": "<eval>self.toolBox.musicControl(self.match.group(1))</eval>"},

    # reddit
    {"input": [".*reddit for (.+)",".*reddit (.+)"],
     "reply": ['''<eval>self.toolBox.redditLookup(self.match.group(1))</eval>''']},
    {"input": ["(find|look up|look for|show me|open) (.+) on reddit"],
     "reply": ['''<eval>self.toolBox.redditLookup(self.match.group(2))</eval>''']},
    {"input": [".*(search|browse) reddit"],
     "reply": ['''<eval>self.toolBox.redditLookup()</eval>''']},

    # xkcd comics
    {"input": [".*xkcd (?:comic |)(?:number |#)(\d+)"],
     "reply": ["<eval>self.toolBox.xkcdComic(self.match.group(1))</eval>"]},
    {"input": [".*xkcd",".*comic"],
     "reply": ["<eval>self.toolBox.xkcdComic()</eval>"]},

    # wikipedia
    {"input": [".*wikipedia for (.+)",".*wikipedia (.+)"],
     "reply": ["<eval>self.toolBox.wikiLookupRespond(self.match.group(1))</eval>"]},
    {"input": ["(find|look up|show me|open) (.+) on wikipedia"],
     "reply": ["<eval>self.toolBox.wikiLookupRespond(self.match.group(2))</eval>"]},

    # news
    {"input": [".*news about (.+)",".*news for (.+)"],
     "reply": (["Will do, NN","opening Google News...","Here's the news about <eval>self.match.group(1)</eval>"],"<eval>webbrowser.open('https://news.google.com/news/search/section/q/%s' % self.match.group(1))</eval>")},
    {"input": [".*news"],
     "reply": (["Will do, NN","opening Google News...","Here's the news"],"<eval>webbrowser.open('https://news.google.com/news/')</eval>")},

    # search google
    {"input": [''.join(i) for i in list(itertools.product([".*find ",".*search the .*web.* for ",".*search for ",".*search ",".*browse",".*show me "],
                                                         ["(.+) images","(.+) photos","(.+) pictures","(.+) pics","pictures of (.+)","pics of (.+)","images of (.+)","photos of (.+)"]))],
     "reply": ["<eval>webbrowser.open('https://www.google.com/search?q=%s&tbm=isch' % self.match.group(1))</eval>"]},
    {"input": [''.join(i) for i in list(itertools.product([".*find ",".*search for ",".*search ",".*browse",".*show me "],
                                                         ["(.+) videos","(.+) vids","videos of (.+)","vids of (.+)"]))],
     "reply": ["<eval>webbrowser.open('https://www.google.com/search?q=%s&tbm=vid' % self.match.group(1))</eval>"]},
    {"input": ["google (.+)","look up (.+)","search .*for (.+)"],
     "reply": ["<eval>self.toolBox.googleIt(self.match.group(1))</eval>"]},

    # dictionary stuff
    {"input": ["define (.+)",".+definition of (.+)",".+meaning of (.+)",".+ does (.+) mean"],
     "reply": "<eval>self.toolBox.getDefinition(re.sub(r'[\W]', ' ', self.match.group(1)))</eval>"},
    {"input": [".*example of (.+) .*in a sentence",".*use (.+) in a sentence"],
     "reply": ("<eval>self.toolBox.usedInASentence(re.sub(r'[\W]', ' ', self.match.group(1)))</eval>")},
    {"input": [".*synonyms for (.+)",".*synonyms of (.+)",".*synonym for (.+)",".*synonym of (.+)",".*another word for (.+)",".*other word for (.+)",".*other words for (.+)"],
     "reply": ("<eval>self.toolBox.getSynonyms(self.match.group(1))</eval>")},

    # translate
    {"input": ["translate (.+) from (.+) to (.+)"],
     "reply": "<eval>self.toolBox.translateTo(self.match.group(1),self.match.group(3),self.match.group(2))</eval>"},
    {"input": ["translate (.+) to (.+)"],
     "reply": "<eval>self.toolBox.translateTo(self.match.group(1),self.match.group(2))</eval>"},

    # weather
    {"input": [".*weather","how's it outside","what's it like outside",".*hourly forecast"],
     "reply": ["<eval>self.toolBox.weatherPrint()</eval>"]},
    {"input": [".*humidity", "is it humid", ".+humid .*today", ".+humid out"],
     "reply": "<eval>self.toolBox.weatherPrint('Humidity')</eval>"},
    {"input": [".*temperature"]+list(itertools.chain.from_iterable([".+%s .*today" % s,".+%s out" % s] for s in syn('hot')))+list(itertools.chain.from_iterable([".+%s .*today" % s,".+%s out" % s] for s in syn('cold'))),
     "reply": "<eval>self.toolBox.weatherPrint('Temp.')</eval>"},
    {"input": [".*wind pressure",".*atmospheric pressure",".*air pressure"],
     "reply": "<eval>self.toolBox.weatherPrint('Pressure')</eval>"},
    {"input": [".*wind"],
     "reply": "<eval>self.toolBox.weatherPrint('Wind')</eval>"},
    {"input": [".*precipitation"],
     "reply": "<eval>self.toolBox.weatherPrint('Precip')</eval>"},
    {"input": [".*dew point"],
     "reply": "<eval>self.toolBox.weatherPrint('Dew Point')</eval>"},
    {"input": [".*cloud cover"],
     "reply": "<eval>self.toolBox.weatherPrint('Cloud Cover')</eval>"},

    # time/date
    {"input": [".+time's it",".+s the time",".*current time"],
     "reply": (["It's ","the clock says "],"<eval>time.asctime().split()[3]</eval>",[" o'clock",""],", NN")},
    {"input": [".+s the date",".*current date",".+today's date",".+day's it",".*what's today"],
     "reply": ("It's ","<eval>' '.join(time.asctime().split()[:3])</eval>",", NN")},
    {"input": [".+year's it",".+'s the year",".+century's it",".*current year",".*current century"],
     "reply": (["It's ","The year is ","It's the year of "],"<eval>time.asctime().split()[4]</eval>",", NN")},

    # LOCATION
    {"input": ["where.+am i",".*where i am","where.*'re we","where's here",".*where here's",".*my location"],
     "reply": (["you're in ","your location is "],"<eval>'{}, {}'.format(*self.toolBox.locationData('city','region_code'))</eval>",[", NN",""])},
    {"input": [".*zipcode"],
     "reply": (["your zipcode is "],"<eval>'{}'.format(*self.toolBox.locationData('zip_code'))</eval>")},
    {"input": [".+state am i in",".+region am i in",".+state i am in",".+region i am in",".+my state",".+my region"],
     "reply": (["right now, ",""],["you're in "],"<eval>self.toolBox.locationData('region_name')[0]</eval>",[", NN",""])},
    {"input": [".+city am i in",".+city i am in",".+city that i am in",".+my city"],
     "reply": (["right now, ",""],["you're in ","your city is "],"<eval>self.toolBox.locationData('city')[0]</eval>",[", NN",""])},
    {"input": [".+country am i in",".+country i am in",".+country that i am in",".+my country"],
     "reply": (["right now, ",""],["you're in ","your country is ","you're standing in the country of "],"<eval>self.toolBox.locationData('country_name')[0]</eval>",[", NN",""])},
    {"input": [".*time zone",".*timezone"],
     "reply": (["right now, ",""],["you're in the "],"<eval>self.toolBox.locationData('time_zone')[0]</eval>"," timezone")},
    {"input": [".*longitude",".*latitude",".*coordinates"],
     "reply": (["right now, ",""],["you're at latitude/longitude "],"<eval>'{}, {}'.format(*self.toolBox.locationData('latitude','longitude'))</eval>")},
    {"input": [".*my ip",".*ip address"],
     "reply": ("your ip address is ","<eval>self.toolBox.locationData('query')[0]</eval>",[", NN",""])},

    # who is ____
    {"input": ["(?:who's|who're) (.+)"],
     "reply": ["<eval>self.toolBox.personLookup(self.match.group(1))</eval>"]},

    # what is a ____
    {"input": ["what's(?: a| an|) (.+)"],
     "reply": ["<eval>self.toolBox.whatIsLookup(self.match.group(1))</eval>"]},

    # JUST IN CASE

    {"input": [".*why not"],
     "reply": ["because I said not"]},
    {"input": [".*why(\?|\!)*\Z"],
     "reply": ["because I said so"]},

    {"input": [".*what((\?|\!)*)\Z"],
     "reply": ["what indeed"]},

    {"input": [".*i don't",".*i do not"],
     "reply": ["I know you don't, NN", "you should"]},
    {"input": [".*i do"],
     "reply": ["I don't","no you don't","you do?"]},

    {"input": ["really"],
     "reply": ["yes, really","nope"]},

    {"input": ["don't ask\Z"],
     "reply": ["don't ask what?","ask what, NN?"]},

    {"input": [".*he's (.+)"],
     "reply": ["who's <eval>self.match.group(1)</eval>?","how <eval>self.match.group(1)</eval>","very <eval>self.match.group(1)</eval>"]},
    {"input": [".*it's (.+)"],
     "reply": ["what's <eval>self.match.group(1)</eval>?","very <eval>self.match.group(1)</eval>","that's <eval>self.match.group(1)</eval>"]},
    {"input": ["that's (.+)"],
     "reply": ["no way is that <eval>self.match.group(1)</eval>","it was very <eval>self.match.group(1)</eval>"]},

    {"input": [".*are you (.+)"],
     "reply": ["I am <eval>self.match.group(1)</eval>","I am not <eval>self.match.group(1)</eval>"]},

    {"input": [".*what do you (.+)"],
     "reply": (["you know what I <eval>self.match.group(1)</eval>"],[", NN",""])},
    {"input": [".*who do you (.+)"],
     "reply": (["you should know who I <eval>self.match.group(1)</eval>","I <eval>self.match.group(1)</eval> everyone"],[", NN",""])},
    {"input": [".*when do you (.+)"],
     "reply": (["I <eval>self.match.group(1)</eval> whenever I want","I <eval>self.match.group(1)</eval> all day","I never <eval>self.match.group(1)</eval>"],[", NN",""])},
    {"input": [".*where do you (.+)"],
     "reply": (["I <eval>self.match.group(1)</eval> all over the place","I <eval>self.match.group(1)</eval> where ever you want"],[", NN",""])},

    # POTTY WORD DETECTION
    {"input": ["(fuck|shit|damn|asshole|bitch)"],
     "reply": ["No fucking cursing"]},

    # VARIOUS INSULTS (sorry in advance for my potty language)
    {"input": ["(meanie|poop|butt|dumbo|idiot|cyberbully|cyber bully|bully|screw you|you suck)"],
     "reply": ["NN! Do not use that foul language in my presence","Insulting your only friend is unwise, NN"]},

    # CRYING
    {"input": [r"wa+\b"],
     "reply": ["WA WA WA","Have the onions got you?","Aww, is your lacrymal drainage system malfunctioning?"]},

    {"input": ["a(h+)"],
     "reply": ["A<eval>self.match.group(1)</eval>h"]},

    {"input": [r"ha+\b","xd\Z","funny","lol"],
     "reply": ["It's not funny, NN"]},

    {"input": ["i'm not (.+)"],
     "reply": (["You aren't <eval>self.match.group(1)</eval>","You are <eval>self.match.group(1)</eval>","if you say so"],[", NN",""])},

    {"input": ["okay","ok"],
     "reply": ["OK","okie dokie"]},

    {"input": ["i'm sorry","sorry"],
     "reply": ["Don't be sorry, NN","You better be sorry!"]},

    {"input": ["what?!+","huh"],
     "reply": ["what?","huh?"]},

    {"input": ["yes\!"],
     "reply": ["no!"]},
    {"input": ["no\!"],
     "reply": ["yes!"]},
    {"input": ["yes\?"],
     "reply": ["no?"]},
    {"input": ["no\?"],
     "reply": ["yes?"]},
    {"input": [r"yes\b"],
     "reply": ["no"]},
    {"input": [r"no\b"],
     "reply": ["yes"]},

    # Should I search the web for...

    {"input": [r".*\b((how|where|when|what)( to| do|'s|'re| does|) .+)",r".*\b(why( do|'re|'s) .+)",".*(is .+)",".*(do .+)"],
     "reply": (["Ok then","If you say so"],'''<exec>tmp=self.match.group(1)
if self.toolBox.promptYN(random.choice(['Should I search the web for "%s"?' % tmp,'Do web search for "%s"? ' % tmp])):
    webbrowser.open('https://www.google.com/search?q=%s' % tmp)</exec>''')},

    {"input": [""],
     "reply": ["say what"]},
]
