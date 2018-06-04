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
    assert virt.reply("remove reminder go to dave matthews concert") == remove_reminder
    assert virt.reply("delete reminder eat some kids") == remove_reminder

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