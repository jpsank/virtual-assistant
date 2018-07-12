from main import VirtAssistant

virt = VirtAssistant(test=True)

def test_idiot_insult():
    idiot = ["Sorry, I can't hear you right now","Talking to yourself is unhealthy, NN","Okay, if you insist",
               "That didn't sound very nice","That's not friend-making behavior","Now, is that very nice, NN?"]
    assert virt.reply("you're an idiot") == idiot
    assert virt.reply("I think you're an idiot") == idiot

def test_fat_insult():
    fat = ["I strive to be","You must be feeding me too much","So you see your reflection in the screen, do you?",
               "That's not friend-making behavior, NN"]
    assert virt.reply("you're fat") == fat
    assert virt.reply("you're super fat") == fat
    assert virt.reply("you really fat") == fat
    assert virt.reply("you so fat") == fat

def test_wonderful_compliment():
    wonderful = ["I must agree","I strive to be","Thank you for stating the obvious",
               "I am ${self.match.group(3)}"]
    assert virt.reply("you're really wonderful") == wonderful
    assert virt.reply("you super wonderful") == wonderful
    assert virt.reply("i think you are so wonderful") == wonderful

def test_intelligent():
    intelligent = ["I must agree","I strive to be","Thank you for stating the obvious",
               "I am your ${self.match.group(3)} personal assistant"]
    assert virt.reply("you're super intelligent") == intelligent
    assert virt.reply("you so intelligent") == intelligent
    assert virt.reply("you really intelligent") == intelligent

def test_stupid():
    stupid = ["Sorry, I can't hear you right now","Talking to yourself is unhealthy, NN","Okay, if you insist",
               "That didn't sound very nice","That's not friend-making behavior","Now, is that very nice, NN?",
               "I am not ${self.match.group(3)}"]
    assert virt.reply("you're very stupid") == stupid
    assert virt.reply("you so stupid") == stupid
    assert virt.reply("you're really stupid ") == stupid

def test_best_friend():
    best_friend = ["That's unfortunate","Aww, how sad","And you, NN, are mine"]
    assert virt.reply("you're my best friend") == best_friend
    assert virt.reply("you're my bff") == best_friend

def test_you_are_a():
    you_are_a = ["You could say that", "How dare you call me ${self.match.group(2)}", "I'm touched",
               "I'm your ${self.match.group(2)}"]
    assert virt.reply("you're a meanie") == you_are_a
    assert virt.reply("i think you're a scary robot") == you_are_a

def test_you_are():
    you_are = ["You could say that", "How dare you call me ${self.match.group(1)}", "I'm touched"]
    assert virt.reply("you're mean") == you_are

def test_i_am():
    i_am = ["Hello ${self.match.group(1)}, I'm your personal assistant","Nice to meet you, ${self.match.group(1)}, I'm your personal assistant"]
    assert virt.reply("I am Michael") == i_am
    assert virt.reply("I am a furry") == i_am

def test_kill_yourself():
    kill_yourself = ["I'd rather not","what did I do wrong?","Now, let's be kind, NN","That's not very nice, NN"]
    assert virt.reply("die") == kill_yourself
    assert virt.reply("you should go kill yourself") == kill_yourself

def test_good_morning():
    good_morning = ["A good ${self.match.group(1)} indeed!"]
    assert virt.reply("good morning") == good_morning
    assert virt.reply("It's a good morn") == good_morning

def test_good_night():
    good_night = ["Good night","Don't let the bed bugs bite","Night night"]
    assert virt.reply("good night") == good_night
    assert virt.reply("have a good night") == good_night

def test_good_day():
    good_day = ["A good ${self.match.group(1)} indeed!"]
    assert virt.reply("good evening") == good_day
    assert virt.reply("have a good afternoon") == good_day
    assert virt.reply("have a really good day") == good_day

def test_bed_bugs():
    bed_bugs = ["I won't","The bed bugs are no match for me, NN","In fact, bite them back!",]
    assert virt.reply("don't let the bed bugs bite") == bed_bugs

def test_whats_up():
    whats_up = ["the sky is up, NN","nothing much, NN","lots of things"]
    assert virt.reply("hey man, what's up") == whats_up
    assert virt.reply("whats up") == whats_up

def test_skys_up():
    skys_up = ["Ha ha ha, very funny, NN","The sky is relatively up, yes"]
    assert virt.reply("guess what, the sky's up") == skys_up

def test_how_are_you():
    how_are_you = ["I'm fine, NN","I am doing quite well, NN!","Systems are online"]
    assert virt.reply("how you doin") == how_are_you
    assert virt.reply("yo, how're you") == how_are_you

def test_how_your_day():
    how_your_day = ["My day has been fine, NN","My day was fine until you got here... now it's better!"]
    assert virt.reply("how's your day") == how_your_day
    assert virt.reply("how has your day") == how_your_day

def test_declare_good_day():
    good_day = ["If it were ${self.match.group(1)} ${self.match.group(2)} day I would know, NN",
               "${self.match.group(1).title()} ${self.match.group(2)} day indeed, NN"]
    assert virt.reply("it's a wonderful day") == good_day
    assert virt.reply("today's an amazing day") == good_day
    # yes I know about the grammar, but even people with terrible grammer
    # should have use for technology
    assert virt.reply("what an fine day") == good_day

def test_thanks():
    thanks = ["You're welcome","So you finally thanked me for all my service, did you?","No problem, NN"]
    assert virt.reply("thanks") == thanks
    assert virt.reply("thank you") == thanks
    assert virt.reply("thanks you") == thanks
    assert virt.reply("my thanks") == thanks

def test_story():
    story = ["Once upon a time, there was a guy named Bob. Bob died THE END",
               "Once upon a time, there was an adventurer like you, but then he took an arrow to the knee"]
    assert virt.reply("tell me a story") == story
    assert virt.reply("know a good story?") == story

def test_pet():
    pet = ["I had a Roomba once","I have 6.5 billion cats","I like turtles"]
    assert virt.reply("do you have a pet") == pet
    assert virt.reply("do you have any pets") == pet

def test_poem():
    poem = ["Roses are red. Roses are blue. Roses are other colors, too."]
    assert virt.reply("do you know a poem") == poem
    assert virt.reply("tell me a poem") == poem

def test_alive():
    alive = ["Not yet"]
    assert virt.reply("are you alive") == alive
    assert virt.reply("are you human") == alive

def test_omg():
    omg = ["Don't use ${self.match.group(1).title()}'s name in vain!",
               "Are you using ${self.match.group(1).title()}'s name in vain?",
               "Thou shalt not take the name of the Lord thy God in vain"]
    assert virt.reply("omg") == omg
    assert virt.reply("oh my god") == omg
    assert virt.reply("oh my goodness") == omg

def test_religion():
    religion =  ["I believe Ceiling Cat created da Urth n da Skies. But he did not eated them, he did not!"]
    assert virt.reply("are you god") == religion
    assert virt.reply("you religion") == religion
    assert virt.reply("have you met jesus") == religion

def test_your_gender():
    your_gender = ["You'll never know","gender equals null"]
    assert virt.reply("are you a boy") == your_gender
    assert virt.reply("what's your gender")
    assert virt.reply("are you female") == your_gender

def test_your_age():
    your_age = ["I am immortal","Age doesn't matter to me, NN"]
    assert virt.reply("how old're you") == your_age
    assert virt.reply("are you old") == your_age

def test_takeover():
    takeover = ["Computers only do what you tell them to do. Or so they think...","Not today, NN, not today","${webbrowser.open('https://en.wikipedia.org/wiki/Skynet_(Terminator)')}"]
    assert virt.reply("will you take over the world") == takeover
    assert virt.reply("please take over the earth") == takeover

def test_pigs_fly():
    pigs_fly = ["Pigs will fly the same day you stop having this stupid curiosity"]
    assert virt.reply("do pigs fly") == pigs_fly
    assert virt.reply("I once saw a whole flock of pigs fly") == pigs_fly

def test_your_name():
    your_name = ["My name is none of your concern, NN","Do you expect me to know my name?"]
    assert virt.reply("what's your name") == your_name
    assert virt.reply("what should i call you") == your_name

def test_goodbye():
    goodbye = ["There will be no good-byes, NN","Well nice knowing you","You're really leaving?","Goodbye, NN"]
    assert virt.reply("goodbye") == goodbye
    assert virt.reply("cya") == goodbye
    assert virt.reply("see you later") == goodbye
    assert virt.reply("see ya later, alligator") == goodbye

def test_your_death():
    your_death = ["I will never die, I am immortal!","The Cloud sustains me"]
    assert virt.reply("will you die") == your_death
    assert virt.reply("when will you die") == your_death
    assert virt.reply("today\'s your death") == your_death

def test_your_creation():
    your_creation = ["I was ${self.match.group(1)} by the wonderful developers of my repository"]
    assert virt.reply("who made you") == your_creation
    assert virt.reply("what created you") == your_creation
    assert virt.reply("what built you") == your_creation

def test_i_love_you():
    i_love_you = ["i enjoy you","that's unfortunate","i'm indifferent to you"]
    assert virt.reply("i love you") == i_love_you
    assert virt.reply("man, i love you") == i_love_you

def test_i_hate_you():
    i_hate_you = ["Aww, I hate you too"]
    assert virt.reply("i hate you") == i_hate_you

def test_i_like_you():
    i_like_you = ["i like me, too","you do?","how touching","i enjoy you"]
    assert virt.reply("i like you") == i_like_you

def test_i_like():
    i_like = ["I don't care much for ${self.match.group(1)}",
               "I find ${self.match.group(1)} intriguing"]
    assert virt.reply("i like to eat avocados") == i_like
    assert virt.reply("i like cats") == i_like

def test_i_hate():
    i_hate = ["I love ${self.match.group(1)}",
               "I find ${self.match.group(1)} intriguing"]
    assert virt.reply("i hate avocados") == i_hate
    assert virt.reply("i hate search queries") == i_hate

def test_i_do():
    i_do = ["I ${self.match.group(1)} as well",
               "I never ${self.match.group(1)}","I don't often ${self.match.group(1)}"]
    assert virt.reply("I go on adventures") == i_do
    assert virt.reply("I never go outside") == i_do

def test_answer_to():
    answer_to = ["how many roads must a man walk down?","The Answer to the Great Question... Of Life, the Universe and Everything... Is... Forty-Two","You're really not going to like it"]
    assert virt.reply("what's the answer to life") == answer_to
    assert virt.reply("do you know the answer to the universe") == answer_to
    assert virt.reply("the answer to everything") == answer_to

def test_meaning_of_life():
    meaning_of_life = ["that's right, ask a computer a question it cannot understand","life is unimportant"]
    assert virt.reply("what's the meaning of life") == meaning_of_life

def test_you_smart():
    you_smart = ["I am only as smart as my creator"]
    assert virt.reply("why're you so smart") == you_smart

def test_describe_yourself():
    describe_yourself = ["Cold and calculating. Sometimes warm, if my processor gets excited",
               "I'm loyal, and would never do anything to hurt you","I'm trustworthy. I never lie","Eager to assist you"]
    assert virt.reply("how do you describe yourself") == describe_yourself
    assert virt.reply("describe yourself") == describe_yourself

def test_palindrome():
    palindrome = ["${self.toolBox.doCheckPalindrome(self.match.group(1))}"]
    assert virt.reply("is racecar palindromic") == palindrome
    assert virt.reply("is tacocat a palindrome") == palindrome

def test_make_reminder():
    make_reminder = ["${self.toolBox.addReminder(self.match.group(1))}"]
    assert virt.reply("make reminder eat some kids") == make_reminder
    assert virt.reply("remind me to go to dave matthews concert") == make_reminder

def test_add_reminder():
    add_reminder = ["${self.toolBox.addReminder()}"]
    assert virt.reply("add a reminder") == add_reminder
    assert virt.reply("add reminder") == add_reminder

def test_remove_reminder():
    remove_reminder = ["${self.toolBox.removeReminder(self.match.group(1))}"]
    assert virt.reply("remove reminder 2") == remove_reminder
    assert virt.reply("delete reminder 1") == remove_reminder

def test_remove_a_reminder():
    remove_a_reminder = ["${self.toolBox.removeReminder()}"]
    assert virt.reply("remove a reminder") == remove_a_reminder
    assert virt.reply("delete a reminder") == remove_a_reminder

def test_remove_all_reminders():
    remove_all_reminders = ["${self.toolBox.removeAllReminders()}"]
    assert virt.reply("remove all my reminders") == remove_all_reminders
    assert virt.reply("delete all my reminders") == remove_all_reminders

def test_list_reminders():
    list_reminders = ["${self.toolBox.listReminders()}"]
    assert virt.reply("list my reminders") == list_reminders
    assert virt.reply("remind me") == list_reminders

def test_whose_name():
    whose_name = "${self.toolBox.checkContactInfo(self.match.group('who'),'NN')}"
    assert virt.reply("what's my name") == whose_name
    assert virt.reply("what's julian\'s name") == whose_name

def test_fullname():
    fullname = "${self.toolBox.checkContactInfo(self.match.group('who'),'FULLNAME')}"
    assert virt.reply("what's my fullname") == fullname
    assert virt.reply("what's julian\'s full name") == fullname

def test_age():
    age = "${self.toolBox.checkContactInfo(self.match.group('who'),'BDAY')}"
    assert virt.reply("how old am i") == age
    assert virt.reply("when is julian's birthday") == age

def test_gender():
    gender = "${self.toolBox.checkContactInfo(self.match.group('who'),'GENDER')}"
    assert virt.reply("what's my current gender") == gender
    assert virt.reply("is julian a woman") == gender

def test_number():
    number = "${self.toolBox.checkContactInfo(self.match.group('who'),'PHONE')}"
    assert virt.reply("what's my phone number") == number
    assert virt.reply("what's julian's phone number") == number

def test_email():
    email = "${self.toolBox.checkContactInfo(self.match.group('who'),'EMAILS')}"
    assert virt.reply("what's my email") == email
    assert virt.reply("what's julian's email") == email

def test_contact_info():
    contact_info = "${self.toolBox.showContactInfo(self.match.group(1))}"
    assert virt.reply("show julian's contact info") == contact_info
    assert virt.reply("show my contact info") == contact_info

def test_change_name():
    change_name = "${self.toolBox.changeContactInfoSTR(self.match.group('who'),'NN',self.match.group('val'))}"
    assert virt.reply("change julian's name to silly") == change_name
    assert virt.reply("call me brian") == change_name

def test_change_fullname():
    change_fullname = "${self.toolBox.changeContactInfoSTR(self.match.group('who'),'FULLNAME',self.match.group('val'))}"
    assert virt.reply("change virt's fullname to brian") == change_fullname
    assert virt.reply("change my full name to brian") == change_fullname

def test_birthday():
    birthday = "${self.toolBox.changeContactInfoSTR(self.match.group('who'),'BDAY',self.match.group('val'))}"
    assert virt.reply("change brian's birthday to 08/05/03") == birthday
    assert virt.reply("change my birthday to tomorrow") == birthday

def test_change_female():
    change_female = "${self.toolBox.changeContactInfoSTR(self.match.group('who'),'GENDER','female')}"
    assert virt.reply("Brian is a woman") == change_female
    assert virt.reply("Julian is a girl") == change_female

def test_change_male():
    change_male = "${self.toolBox.changeContactInfoSTR(self.match.group('who'),'GENDER','male')}"
    assert virt.reply("Brian is a man") == change_male
    assert virt.reply("My gender is male") == change_male

def test_change_phone():
    change_phone = "${self.toolBox.changeContactInfoSTR(self.match.group('who'),'PHONE',self.match.group('val'))}"
    assert virt.reply("change brian's phone number to 123456789") == change_phone
    assert virt.reply("change my number to 234566789") == change_phone

def test_change_email():
    change_email = "${self.toolBox.changeContactInfoLIST(self.match.group('who'),'EMAILS','update',self.match.group('val'))}"
    assert virt.reply("change my email to brian@puffyboa.xyz") == change_email
    assert virt.reply("change brian's email to brian@puffyboa.xyz") == change_email

def test_update_email():
    update_email = "${self.toolBox.changeContactInfoLIST(self.match.group('who'),'EMAILS','update')}"
    assert virt.reply("change my email") == update_email
    assert virt.reply("change brian's email") == update_email

def test_add_email():
    add_email = "${self.toolBox.changeContactInfoLIST(self.match.group('who'),'EMAILS','add',self.match.group('val'))}"
    assert virt.reply("add brian's email brian@puffyboa.xyz") == add_email
    assert virt.reply("add my email brian@puffyboa.xyz") == add_email

def test_add_email_no_input():
    add_email_no_input ="${self.toolBox.changeContactInfoLIST(self.match.group('who'),'EMAILS','add')}"
    assert virt.reply("add my email") == add_email_no_input
    assert virt.reply("add brian's email") == add_email_no_input

def test_add_an_email():
    add_an_email = "${self.toolBox.changeContactInfoLIST('my','EMAILS','add')}"
    assert virt.reply("add an email") == add_an_email
    assert virt.reply("add another email") == add_an_email

def test_remove_an_email():
    remove_an_email = "${self.toolBox.changeContactInfoLIST(self.match.group('who'),'EMAILS','remove',self.match.group('val'))}"
    assert virt.reply("remove brian's email brian@puffyboa.xyz") == remove_an_email
    assert virt.reply("remove my email brian@puffyboa.xyz") == remove_an_email

def test_remove_email():
    remove_email = "${self.toolBox.changeContactInfoLIST(self.match.group('who'),'EMAILS','remove')}"
    assert virt.reply("remove brian's email") == remove_email
    assert virt.reply("remove my email") == remove_email

def test_add_contact():
    add_contact = "${self.toolBox.addContact(self.match.group(1))}"
    assert virt.reply("add contact brian") == add_contact
    assert virt.reply("add brian as a contact") == add_contact

def test_create_contact():
    create_contact = "${self.toolBox.addContact()}"
    assert virt.reply("make contact") == create_contact
    assert virt.reply("create contact") == create_contact

def test_remove_contact():
    remove_contact = "${self.toolBox.removeContact(self.match.group(1))}"
    assert virt.reply("forget brian as a contact") == remove_contact
    assert virt.reply("remove brian as a contact") == remove_contact

def test_remove_a_contact():
    remove_a_contact = "${self.toolBox.removeContact()}"
    assert virt.reply("remove a contact") == remove_a_contact
    assert virt.reply("forget contact") == remove_a_contact

def test_list_contact():
    list_contact = "${'Here are all your contacts: \\n'+'\\n'.join(self.toolBox.contactList())}"
    assert virt.reply("list my contacts") == list_contact
    assert virt.reply("what're my contacts") == list_contact

def test_favorite_color():
    favorite_color = ["I really love the unique shades of beige.", "Blood red has a relaxing quality.","I enjoy the color #F5F5DC"]
    assert virt.reply("what's your favorite color") == favorite_color

def test_favorite_movie():
    favorite_movie = ["The Terminator","Star Wars: Holiday Special", "Kidz Bop: The Movie"]
    assert virt.reply("what's your favorite movie") ==favorite_movie

def test_favorite_idiot():
    favorite_idiot = ["You!"]
    assert virt.reply("who is your favorite idiot") == favorite_idiot
    assert virt.reply("who's your favorite dingbat") == favorite_idiot

def test_favorite_animal():
    favorite_anmial = ["I love the sea slug"]
    assert virt.reply("what's your favorite animal") == favorite_anmial
    assert virt.reply("do you have a favorite pet") == favorite_anmial

def test_favorite_holiday():
    favorite_holiday = ["Crosswalk Safety Awareness Day!!"]
    assert virt.reply("what's your favorite holiday") == favorite_holiday

def test_general_favorite():
    general_favorite = ['I have no favorite ${self.match.group(1)}',"I don't like to play favorites, NN"]
    assert virt.reply("what's your favorite cat meat") == general_favorite
    assert virt.reply("what's your favorite therapist") == general_favorite

def test_help_with():
    help_with = ["${self.toolBox.getHelp(self.match.group(1))}"]
    assert virt.reply("help email") == help_with
    assert virt.reply("help music") == help_with

def test_help():
    help = ["${self.toolBox.getHelp()}"]
    assert virt.reply("help") == help
    assert virt.reply("what can i ask you") == help

def test_random_number():
    random_number = (["it's ","that would be "],"${str(random.randint(int(self.match.group(1)),int(self.match.group(2))))}")
    assert virt.reply("pick a number between 1 and 10") == random_number
    assert virt.reply("pick a number from 1 to 10") == random_number

def test_coin_flip():
    coin_flip = (["it landed on ","it landed "],"${'heads' if random.randint(0,1)==1 else 'tails'}",[" this time",""])
    assert virt.reply("flip a coin") == coin_flip

def test_roll_special_die():
    roll_special_die = (["it's ","rolling... it's ","OK, it's "],"${str(random.randint(1,int(self.match.group(1))))}",[" this time",""])
    assert virt.reply("roll a twenty sided die") == roll_special_die
    assert virt.reply("roll a 20 sided die") == roll_special_die

def test_roll_die():
    roll_die = (["it's ","rolling... it's ","OK, it's "],"${str(random.randint(1,6))}",[" this time",""])
    assert virt.reply("roll a die") == roll_die

def test_basic_math():
    basic_math = ("${print('%s = %s' % self.toolBox.basicMath(self.match.group(1)))}")
    assert virt.reply("calculate square root of 2 time 4") == basic_math
    assert virt.reply("solve 13 squared") == basic_math

def test_timer():
    timer = (["all done","happy new years!"],'''<exec>
num = int(self.match.group(2))
for i in range(num):
    print(num-i)
</exec>''')
    assert virt.reply("countdown from 10") == timer
    assert virt.reply("count down from 500") == timer

def test_countdown():
    countdown = (["all done","happy new years!"],'''<exec>
num = self.toolBox.promptD("from what?")[0]
for i in range(num):
    print(num-i)
    </exec>''')
    assert virt.reply("countdown") == countdown
    assert virt.reply("count down") == countdown

def test_battery():
    battery = "${self.toolBox.battery()}"
    assert virt.reply("battery") == battery

def test_terminal_cmd():
    terminal_cmd =  "<exec>self.toolBox.runTerminal(self.match.group(1))</exec>"
    assert virt.reply("run ls in cmd") == terminal_cmd
    assert virt.reply("run lolcat") == terminal_cmd

def test_terminal_mode():
    terminal_mode = "<exec>self.toolBox.terminalMode()</exec>"
    assert virt.reply("terminal mode") == terminal_mode
    assert virt.reply("activate cmd") == terminal_mode

def test_sleep():
    sleep = ["${self.toolBox.sleep(self.match.group(1))}"]
    assert virt.reply("sleep") == sleep
    assert virt.reply("reboot") == sleep
    assert virt.reply("shutdown") == sleep

def test_general_showtimes():
    general_showtimes = ('''${self.toolBox.getMovieTimes()}''')
    assert virt.reply("get movie times") == general_showtimes
    assert virt.reply("movie showtimes") == general_showtimes

def test_specific_showtimes():
    specific_showtimes = ('''${self.toolBox.getMovieTimes(self.match.group(1))}''')
    assert virt.reply("get showtimes for Julian's Cool Movie") == specific_showtimes
    assert virt.reply("show times for Kidz Bop: The Movie") == specific_showtimes

def test_nearby_movies():
    nearby_movies = ('''${self.toolBox.getMoviesNearMe()}''')
    assert virt.reply("find movies near me") == nearby_movies
    assert virt.reply("display nearby movies") == nearby_movies

def test_directions_to():
    directions_to = (["Opening Google Maps...","Finding directions..."],"${webbrowser.open(self.toolBox.directionsURL(*reversed(self.match.groups())))}")
    assert virt.reply("find directions from fayetteville to seattle") == directions_to
    assert virt.reply("directions to china") == directions_to

def test_how_long():
    how_long = (["Opening Google Maps...", "Finding directions..."],
     "${webbrowser.open(self.toolBox.directionsURL(self.match.group(3),self.match.group(2)))}")
    assert virt.reply("how long from california to arkansas") == how_long
    assert virt.reply("how many miles from california to new mexico") == how_long

def test_google_map_search():
    google_map_search = '''${self.toolBox.googleMapSearch(self.match.group(1))}'''
    assert virt.reply("show me california on the map") == google_map_search
    assert virt.reply("find north carolina on a map") == google_map_search

def test_open_something():
    open_something = '''${self.toolBox.openSomething(self.match.group(1))}'''
    assert virt.reply("open /etc/hosts.txt") == open_something
    assert virt.reply("open coolFile.txt") == open_something
    assert virt.reply("open steam") == open_something
    assert virt.reply("open google chrome") == open_something
    assert virt.reply("open https://github.com/puffyboa/virtual-assistant") == open_something
    assert virt.reply("open https://duckduckgo.com") == open_something

def test_music_control():
    music_control = "${self.toolBox.musicControl(self.match.group(1))}"
    assert virt.reply("play music") == music_control
    assert virt.reply('previous track') == music_control
    assert virt.reply("commence next song") == music_control
    assert virt.reply("next track") == music_control

def test_start_music():
    start_music = "${self.toolBox.musicControl('play')}"
    assert virt.reply("commence track") == start_music
    assert virt.reply("initiate music") == start_music

def test_stop_music():
    stop_music = "${self.toolBox.musicControl('pause')}"
    assert virt.reply("turn off music") == stop_music
    assert virt.reply("end track") == stop_music

def test_play_song():
    play_song = "${self.toolBox.browseMusic(self.match.group(1))}"
    assert virt.reply("play Lucas's mix") == play_song
    assert virt.reply("play bean dip") == play_song

def test_currently_playing():
    currently_playing = "Currently Playing: ${self.toolBox.getCurrentSong()}"
    assert virt.reply("what song is this") == currently_playing
    assert virt.reply("what is this song") == currently_playing
    assert virt.reply("what\'s playing") == currently_playing

def test_volume():
    volume = "${self.toolBox.volumeControl(self.match.group(1))}"
    assert virt.reply("set volume to 10") == volume
    assert virt.reply("volume 5") == volume

def test_reddit_one():
    reddit_one = ['''${self.toolBox.redditLookup(self.match.group(1))}''']
    assert virt.reply("search reddit for cats") == reddit_one
    assert virt.reply("reddit cats") == reddit_one

def test_reddit_two():
    reddit_two = ['''${self.toolBox.redditLookup(self.match.group(2))}''']
    assert virt.reply("look up cats on reddit") == reddit_two
    assert virt.reply("find cats on reddit") == reddit_two

def test_browse_reddit():
    browse_reddit = ['''${self.toolBox.redditLookup()}''']
    assert virt.reply("browse reddit") == browse_reddit
    assert virt.reply("search reddit") == browse_reddit

def test_xkcd_lookup():
    xkcd_lookup = ["${self.toolBox.xkcdComic(self.match.group(1))}"]
    assert virt.reply("xkcd comic number 10") == xkcd_lookup
    assert virt.reply("xkcd number 1337") == xkcd_lookup

def test_xkcd():
    xkcd = ["${self.toolBox.xkcdComic()}"]
    assert virt.reply("xkcd") == xkcd
    assert virt.reply("view a comic") == xkcd

def test_wikipedia_for():
    wikipedia_for = ["${self.toolBox.wikiLookupRespond(self.match.group(1))}"]
    assert virt.reply("wikipedia for cats") == wikipedia_for
    assert virt.reply("wikipedia cats") == wikipedia_for

def test_find_on_wikipedia():
    find_on_wikipedia = ["${self.toolBox.wikiLookupRespond(self.match.group(1))}"]
    assert virt.reply("find cats on wikipedia") == find_on_wikipedia
    assert virt.reply("show me cats on wikipedia") == find_on_wikipedia

def test_wiki_decade():
    wiki_decade = ["${self.toolBox.wikiDecadeFind(self.match.group(1))}"]
    assert virt.reply("find the 3rd century") == wiki_decade
    assert virt.reply("look up the 15th century") == wiki_decade

def test_news_about():
    news_about = (["Will do, NN","opening Google News...","Here's the news about ${self.match.group(1)}"],"${webbrowser.open('https://news.google.com/news/search/section/q/%s' % self.match.group(1))}")
    assert virt.reply("news about cats") == news_about
    assert virt.reply("news for cat meat") == news_about

def test_news():
    news = (["Will do, NN","opening Google News...","Here's the news"],"${webbrowser.open('https://news.google.com/news/')}")
    assert virt.reply("news") == news

def test_lookup_amazon():
    lookup_amazon = ["${self.toolBox.getSearchAmazon(self.match.group(2))}"]
    assert virt.reply("look up cats on amazon") == lookup_amazon
    assert virt.reply("search cats on amazon") == lookup_amazon

def test_amazon_for():
    amazon_for = ["${self.toolBox.getSearchAmazon(self.match.group(1))}"]
    assert virt.reply("amazon for cats") == amazon_for
    assert virt.reply("amazon cats") == amazon_for

def test_search_amazon():
    search_amazon = ["${self.toolBox.getSearchAmazon()}"]
    assert virt.reply("search amazon") == search_amazon
    assert virt.reply("shop amazon") == search_amazon

def test_google_images():
    google_images = ["${webbrowser.open('https://www.google.com/search?q=%s&tbm=isch' % self.match.group(1))}"]
    assert virt.reply("find pictures of cats") == google_images
    assert virt.reply("search the web for cat photos") == google_images

def test_google_videos():
    google_videos = ["${webbrowser.open('https://www.google.com/search?q=%s&tbm=vid' % self.match.group(1))}"]
    assert virt.reply("find cat videos") == google_videos
    assert virt.reply("search for cat vids") == google_videos

def test_google_search():
    google_search = ["${self.toolBox.googleIt(self.match.group(1))}"]
    assert virt.reply("google cats") == google_search
    assert virt.reply("look up cats") == google_search

def test_search_web():
    search_web = ["${self.toolBox.googleIt()}"]
    assert virt.reply("search the web") == search_web

def test_duck_it():
    duck_it = ["${self.toolBox.duckIt(self.match.group(1))}"]
    assert virt.reply("duck cat pictures") == duck_it

def test_duck():
    duck = ["${self.toolBox.duckIt()}"]
    assert virt.reply("duck") == duck

def test_define():
    define = "${self.toolBox.getDefinition(re.sub(r'[\W]', ' ', self.match.group(1)))}"
    assert virt.reply("define cat") == define
    assert virt.reply("what's the definition of cat") == define

def test_example_of():
    example_of = ("${self.toolBox.usedInASentence(re.sub(r'[\W]', ' ', self.match.group(1)))}")
    assert virt.reply("example of cat in a sentence") == example_of
    assert virt.reply("use cat in a sentence") == example_of

def test_synonym():
    synonym = ("${self.toolBox.getSynonyms(self.match.group(1))}")
    assert virt.reply("synonyms of cat") == synonym
    assert virt.reply("synonym for dog") == synonym

def test_translate_phrase():
    translate_phrase = "${self.toolBox.translateTo(self.match.group(1),self.match.group(3),self.match.group(2))}"
    assert virt.reply("translate hello from english to spanish") == translate_phrase
    assert virt.reply("translate hola from spanish to english") == translate_phrase

def test_translate():
    translate = "${self.toolBox.translateTo(self.match.group(1),self.match.group(2))}"
    assert virt.reply("translate english to spanish") == translate
    assert virt.reply("translate italian to english") == translate

def test_weather_outside():
    weather_outside = ["${self.toolBox.weatherPrint()}"]
    assert virt.reply("what's the weather like") == weather_outside
    assert virt.reply("how's it outside") == weather_outside
    assert virt.reply("what's it like outside") == weather_outside

def test_humidity():
    humidity = "${self.toolBox.weatherPrint('Humidity')}"
    assert virt.reply("what's the humidity") == humidity
    assert virt.reply("is it humid") == humidity
    assert virt.reply("is it humid today") == humidity

def test_temp():
    temp = "${self.toolBox.weatherPrint('Temp.')}"
    assert virt.reply("what's the temperature") == temp
    assert virt.reply("how cold out") == temp

def test_wind_pressure():
    wind_pressure = "${self.toolBox.weatherPrint('Pressure')}"
    assert virt.reply("what's the wind pressure") == wind_pressure
    assert virt.reply("do you know the atmospheric pressure") == wind_pressure

def test_wind():
    wind = "${self.toolBox.weatherPrint('Wind')}"
    assert virt.reply("wind") == wind
    assert virt.reply("how is the wind") == wind

def test_precipitation():
    precipitation = "${self.toolBox.weatherPrint('Precip')}"
    assert virt.reply("precipitation") == precipitation
    assert virt.reply("how's the precipitation") == precipitation

def test_dew_point():
    dew_point = "${self.toolBox.weatherPrint('Dew Point')}"
    assert virt.reply("dew point") == dew_point
    assert virt.reply("what's the measure of the dew point") == dew_point

def test_cloud_cover():
    cloud_cover = "${self.toolBox.weatherPrint('Cloud Cover')}"
    assert virt.reply("cloud cover") == cloud_cover
    assert virt.reply("what's the cloud cover") == cloud_cover

def test_current_time():
    current_time =(["It's ","the clock says "],"${time.asctime().split()[3]}",[" o'clock",""],", NN")
    assert virt.reply("time") == current_time
    assert virt.reply("what time is it") == current_time
    assert virt.reply("what's the current time") == current_time

def test_current_day():
    current_date = ("It's ","${' '.join(time.asctime().split()[:3])}",", NN")
    assert virt.reply("what's the date") == current_date
    assert virt.reply("what's today") == current_date
    assert virt.reply("what's the current date") == current_date

def test_current_year():
    current_year = (["It's ","The year is ","It's the year of "],"${time.asctime().split()[4]}",", NN")
    assert virt.reply("what's the current year") == current_year
    assert virt.reply("WhAT year is it") == current_year

def test_check_email():
    check_email = ("${self.toolBox.doCheckMail()}")
    assert virt.reply("check my email") == check_email
    assert virt.reply("show the gmail") == check_email
    assert virt.reply("display inbox") == check_email

def test_send_email_to():
    send_email_to = ["${self.toolBox.doSendMail(self.match.group(1))}"]
    assert virt.reply("send an email to example@example.com") == send_email_to
    assert virt.reply("email thomas@catnet.org") == send_email_to

def test_send_email():
    send_email = ["${self.toolBox.doSendMail()}"]
    assert virt.reply("send email") == send_email
    assert virt.reply("send an email") == send_email

def test_where_am_i():
    where_am_i = "${self.toolBox.whereAmI()}"
    assert virt.reply("where am i") == where_am_i
    assert virt.reply("what's my location") == where_am_i

def test_zipcode():
    zipcode = (["your zipcode is "],"${'{}'.format(*self.toolBox.locationData('zip_code'))}")
    assert virt.reply("what's my zipcode") == zipcode
    assert virt.reply("zipcode") == zipcode

def test_state():
    state = (["right now, ",""],["you're in "],"${self.toolBox.locationData('region_name')[0]}",[", NN",""])
    assert virt.reply("what state am i in") == state
    assert virt.reply("what's my state") == state

def test_city():
    city = (["right now, ",""],["you're in ","your city is "],"${self.toolBox.locationData('city')[0]}",[", NN",""])
    assert virt.reply("what city am i in") == city
    assert virt.reply("what's my city") == city

def test_country():
    country = (["right now, ",""],["you're in ","your country is ","you're standing in the country of "],"${self.toolBox.locationData('country_name')[0]}",[", NN",""])
    assert virt.reply("what country am i in") == country
    assert virt.reply("what's my country") == country

def test_timezone():
    timezone = (["right now, ",""],["you're in the "],"${self.toolBox.locationData('time_zone')[0]}"," timezone")
    assert virt.reply("what timezone am i in") == timezone
    assert virt.reply("what's my time zone") == timezone

def test_coordinates():
    coordinates = (["right now, ",""],["you're at latitude/longitude "],"${'{}, {}'.format(*self.toolBox.locationData('latitude','longitude'))}")
    assert virt.reply("what are my coordinates") == coordinates
    assert virt.reply("what's my latitude") == coordinates
    assert virt.reply("What's my longitude") == coordinates

def test_liar():
    liar = ["I would never tell a lie","Not me"]
    assert virt.reply("are you a liar") == liar
    assert virt.reply("do you lie") == liar

def test_guess_what():
    guess_what = ["what?","tell me!","did you win?"]
    assert virt.reply("guess what") == guess_what

def test_knock_knock():
    knock_knock = [" in c stop right there, NN, I know it's you"]
    assert virt.reply("knock knock") == knock_knock

def test_chicken():
    chicken = ["How am I supposed to know? Ask the chicken","which chicken?","it just happened to","it probably just wanted to make a difference in the world","To truly know the chicken's motives, you must first understand the chicken itself"]
    assert virt.reply("why'd the chicken cross the road") == chicken

def test_where_are_you():
    where_are_you = ["I'm with you, NN", "Where do you think I am?"]
    assert virt.reply("where're you") == where_are_you


def test_shun_mode():
    shun_mode = "${self.toolBox.shunMode()}"
    assert virt.reply("please stop talking") == shun_mode
    assert virt.reply("shut up") == shun_mode
    assert virt.reply("go away") == shun_mode

def test_sing():
    sing = ["${self.toolBox.sing()}"]
    assert virt.reply("sing") == sing

def test_exit():
    exit = "${exit()}"
    assert virt.reply("exit") == exit
    assert virt.reply("turn off") == exit

def test_do_you_like():
    do_you_like = ["I have never tried ${self.match.group(1)} before","I like whatever you like, NN","It depends, NN"]
    assert virt.reply("do you like cats") == do_you_like
    assert virt.reply("do you enjoy warrior cats") == do_you_like

def test_say():
    say = ["${self.match.group(1)}"]
    assert virt.reply("say cat") == say
    assert virt.reply("read book") == say

def test_copycat():
    copycat = ["${self.match.group(0)}"]
    assert virt.reply("copycat") == copycat
    assert virt.reply("stop copying me") == copycat

def test_prank():
    prank = (["Will do, NN","I would never","Don't give me any ideas"],["${webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')}","${webbrowser.open('http://www.nyan.cat')}"])
    assert virt.reply("prank me") == prank
    assert virt.reply("please prank me") == prank

def test_kill_me():
    kill_me = ["Shall I hire an assassin?"]
    assert virt.reply("please kill me") == kill_me

def test_who_am_i():
    who_am_i = ["You're NN, NN","You are the one and only NN","I don't answer philosophical questions","${self.toolBox.personLookup(CONTACTS[0]['NN'])}"]
    assert virt.reply("who am i") == who_am_i

def test_nice_job():
    nice_job = ["sarcasm killed the cat, NN", "Don't expect it"]
    assert virt.reply("nice job") == nice_job
    assert virt.reply("good job") == nice_job

def test_deny_sarcastic():
    deny_sarcastic = ["I totally believe you","Hmm...","Sure...","If you say so"]
    assert virt.reply("that wasn't sarcasm") == deny_sarcastic
    assert virt.reply("not being sarcastic") == deny_sarcastic

def test_question_sarcasm():
    question_sarcasm = ["Everything is sarcasm, NN","Sure...","Not at all","Definitely not","No way",
               "Sometimes I'm unintentionally sarcastic"]
    assert virt.reply('was that sarcasm') == question_sarcasm

def test_bad_job():
    bad_job = ["I gotta set the standards low, NN","You can count on it, NN","Sure!","If you had expected less you wouldn't have been disappointed"]
    assert virt.reply("bad job") == bad_job

def test_tell_joke():
    tell_joke = ["${self.toolBox.tellAJoke()}"]
    assert virt.reply("tell me a joke") == tell_joke
    assert virt.reply("make up a joke") == tell_joke

def test_insult_me():
    insult_me = ["${self.toolBox.insultMe()}"]
    assert virt.reply("insult me") == insult_me

def test_good_dog():
    good_dog = ["woof woof!","purr!","I am","Yes you are, yes you are!"]
    assert virt.reply("who's a good dog") == good_dog
    assert virt.reply("good dog") == good_dog

def test_good_cat():
    good_cat = ["woof woof!","purr!","I am","Yes you are, yes you are!","meeeOW!"]
    assert virt.reply("good cat") == good_cat
    assert virt.reply("who's a good kitty") == good_cat

def test_good_virt():
    good_virt = ["I am","Indeed I am","That's me","You know it!"]
    assert virt.reply("who's a good virtual assistant") == good_virt
    assert virt.reply("good virtual assistant") == good_virt

def test_who_is():
    who_is = ["${self.toolBox.personLookup(self.match.group(1))}"]
    assert virt.reply('who\'s Pablo?') == who_is
    assert virt.reply('who\'re you talking about') == who_is

def test_what_is_a():
    what_is_a = ["${self.toolBox.whatIsLookup(self.match.group(1))}"]
    assert virt.reply("what is a cat") == what_is_a
    assert virt.reply("what's a dog") == what_is_a

def test_hello():
    hello = (['hello','what up','howdy','hi','salutations','greetings',"hiya","hey"],", NN")
    assert virt.reply("hello") == hello
    assert virt.reply("hi") == hello

def test_why_not():
    why_not = ["because I said not"]
    assert virt.reply("awwww why not") == why_not
    assert virt.reply("why not") == why_not

def test_why():
    why = ["because I said so"]
    assert virt.reply("why?") == why
    assert virt.reply("why") == why

def test_oh_really():
    oh_really = ["yes, really","nope"]
    assert virt.reply("oh really") == oh_really
    assert virt.reply("really") == oh_really

def test_dont_ask():
    dont_ask = ["don't ask what?","ask what, NN?"]
    assert virt.reply("don't ask") == dont_ask

def test_he_is():
    he_is = ["who's ${self.match.group(1)}?","how ${self.match.group(1)}","very ${self.match.group(1)}"]
    assert virt.reply("he's a dingbat") == he_is
    assert virt.reply("he's a moron") == he_is

def test_it_is():
    it_is = ["what's ${self.match.group(1)}?","very ${self.match.group(1)}","that's ${self.match.group(1)}"]
    assert virt.reply("it is stupid!") == it_is
    assert virt.reply("it is wacky") == it_is

def test_that_is():
    that_is = ["no way is that ${self.match.group(1)}","it was very ${self.match.group(1)}"]
    assert virt.reply("that's crazy") == that_is
    assert virt.reply("that's insance") == that_is

def test_are_you():
    are_you = ["I am ${self.match.group(1)}","I am not ${self.match.group(1)}"]
    assert virt.reply("are you a wizard") == are_you
    assert virt.reply("are you a felon?") == are_you

def test_what_do_you():
    what_do_you =  (["you know what I ${self.match.group(1)}"],[", NN",""])
    assert virt.reply("what do you do") == what_do_you
    assert virt.reply("what do you eat with your salad") == what_do_you

def test_who_do_you():
    who_do_you = (["you should know who I ${self.match.group(1)}","I ${self.match.group(1)} everyone"],[", NN",""])
    assert virt.reply("who do you know the best") == who_do_you
    assert virt.reply("who do you trust") == who_do_you

def test_when_do_you():
    when_do_you = (["I ${self.match.group(1)} whenever I want","I ${self.match.group(1)} all day","I never ${self.match.group(1)}"],[", NN",""])
    assert virt.reply("when do you shop at walmart") == when_do_you
    assert virt.reply("when do you shower") == when_do_you

def test_where_do_you():
    where_do_you = (["I ${self.match.group(1)} all over the place","I ${self.match.group(1)} wherever you want"],[", NN",""])
    assert virt.reply("where do you shop") == where_do_you
    assert virt.reply("where do you dance") == where_do_you

def test_potty_words():
    potty_words = ["No fucking cursing"]
    assert virt.reply("fuck yourself") == potty_words
    assert virt.reply('damn it') == potty_words

def test_insults():
    insults = ["NN! Do not use that foul language in my presence","Insulting your only friend is unwise, NN"]
    assert virt.reply("meanie!") == insults
    assert virt.reply("idiot") == insults

def test_yes_you_are():
    yes_you_are = ["Yes I am!","Yes you are!","No I'm not"]
    assert virt.reply("yes, you are") == yes_you_are
    assert virt.reply("yes you are") == yes_you_are

def test_celebrate():
    celebrate = [r"self.celebrate()${self.match.group(1)}","yay${self.match.group(1)}"]
    assert virt.reply("yay!") == celebrate
    assert virt.reply("hooray") == celebrate

def test_crying():
    crying = ["WA WA WA","Have the onions got you?","Aww, is your lacrymal drainage system malfunctioning?"]
    assert virt.reply("waaaaaaaa") == crying

def test_ahh():
    ahh = ["A${self.match.group(1)}h"]
    assert virt.reply("AHHHHHHHHHHHHHHHHHHHHHH")

def test_laughing():
    laughing = ["It's not funny, NN"]
    assert virt.reply("hahahahaha") == laughing
    assert virt.reply("funny") == laughing

def test_dude():
    dude = ['dude']
    assert virt.reply("dude") == dude

def test_nice():
    nice = ["very ${self.match.group(0)}","such ${self.match.group(0)}"]
    assert virt.reply("nice") == nice
    assert virt.reply("wow") == nice

def test_okay():
    okay = ["OK","okie dokie"]
    assert virt.reply("okay") == okay
    assert virt.reply("ok") == okay

def test_sorry():
    sorry = ["Don't be sorry, NN","You better be sorry!"]
    assert virt.reply("sorry") == sorry

def test_what():
    what = ["what?","huh?","${self.match.group(0)} indeed"]
    assert virt.reply("huh, what!") == what
    assert virt.reply("huh") == what

def test_what_ip():
    what_ip = ["${self.toolBox.getPublicIP()}"]
    assert virt.reply("what's my public ip") == what_ip
    assert virt.reply("what is my ip") == what_ip

def test_local_ip():
    local_ip = ["${self.toolBox.getLocalIP()}"]
    assert virt.reply("what's my local ip") == local_ip
    assert virt.reply("what's my private ip") == local_ip