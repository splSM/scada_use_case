from random import randrange as randomNum
from random import choice as randomChar
from datetime import datetime as when
from time import sleep as snooze
import string, re

def EventGen():
    categories = ['ADVISORY', 'ALARM', 'CLEARED']
    category = categories[randomNum(3)]
    types = ['ALFA', 'BRAVO']
    type = types[randomNum(2)]
    textLetters = string.ascii_uppercase
    t1 = randomChar(textLetters)
    t2 = str(randomNum(9))
    t3 = str(randomNum(9))
    t4 = randomChar(textLetters)
    text = t1 + t2 + t3 + t4
    time = re.sub( '\s', 'T', str(when.now()) )
    time = time[0:23]
    event = time+' '+category+' '+type+' '+text
    # NOTE: This app was just a quick effort to play with a use case, so I didn't go to hard on this script.
    #       If necessary, change the following line to the correct directory where this script is installed!
    with open('/opt/splunk/etc/apps/scada_use_case/log/scada.log', 'a') as log:
         log.write(event + '\n')

EventGen();snooze(9)
EventGen();snooze(9)
EventGen();snooze(9)
EventGen();snooze(9)
EventGen();snooze(9)
EventGen()
