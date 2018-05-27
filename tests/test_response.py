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

def test_you_are():
    you_are = ["You could say that", "How dare you call me ${self.match.group(1)}","I'm touched"]
    assert virt.reply("you're a meanie") == you_are
    assert virt.reply("i think you're a scary robot") == you_are

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