from server import Reporter
from scraper import create_menu_pickle
import pickle
from sys import argv
import os
from datetime import date, timedelta

fname = 'term_menu.pickle'
if not os.path.isfile(fname):
    print("Creating menu pickle (cache) file...")
    create_menu_pickle()

# Load huge dictionary containing the whole term's menu
with open(fname, 'rb') as pfile:
    food_dictionary = pickle.load(pfile)

# Report relevant information based on command line query
rep = Reporter(food_dictionary)

# No inputs, show today's menu
if len(argv) is 1:
    rep.display_menu(day=date.today())

if len(argv) > 1:
    flag = argv[1]
    if flag in ('-s', '--search'):
        # Search for food in the menu
        if len(argv) is 4:
            if argv[3] == 'today':
                rep.search(target=argv[2],
                           from_day=date.today(),
                           till_day=date.today() + timedelta(days=1))
            elif argv[3] == 'tomorrow':
                rep.search(target=argv[2],
                           from_day=date.today() + timedelta(days=1),
                           till_day=date.today() + timedelta(days=2))
        elif len(argv) is 7:
            rep.search(target=argv[2],
                       from_day=date(2018, int(argv[3]), int(argv[4])),
                       till_day=date(2018, int(argv[5]), int(argv[6])))
        else:
            rep.search(target=argv[2])

    elif flag in ('-d', '--date'):
        # Menu for certain date
        year, month, day = 2018, int(argv[2]), int(argv[3])
        rep.display_menu(day=date(year, month, day))
