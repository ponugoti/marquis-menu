from server import Reporter
from scraper import create_menu_pickle
import pickle
from sys import argv
import os
from datetime import date, timedelta
# import argparse

fname = 'term_menu.pickle'
if not os.path.isfile(fname):
    print("Creating menu pickle (cache) file...")
    create_menu_pickle()

# Load dictionary containing the whole term's menu
with open(fname, 'rb') as pfile:
    food_dictionary = pickle.load(pfile)

# Report relevant information based on command line query
rep = Reporter(food_dictionary)

# TODO switch to using argparse instead of the mess below

# No inputs, show today's menu
if len(argv) is 1:
    rep.display_menu(day=date.today())

if len(argv) > 1:
    flag = argv[1]
    if flag in ('-s', '--search'):
        # Search for food in the menu
        if len(argv) is 4:
            # Either 'today' or 'tomorrow' must be specified
            if argv[3] == 'today':
                start = date.today()
                end = date.today() + timedelta(days=1)

            elif argv[3] == 'tomorrow':
                start = date.today() + timedelta(days=1)
                end = date.today() + timedelta(days=2)

            rep.search(target=argv[2], from_day=start, till_day=end)

        elif len(argv) is 7:
            # Full dates are assumed to be provided for date range
            start = date(2018, int(argv[3]), int(argv[4]))
            end = date(2018, int(argv[5]), int(argv[6]))

            rep.search(target=argv[2], from_day=start, till_day=end)

        else:
            rep.search(target=argv[2])

    elif flag in ('-d', '--date'):
        # Menu for today or tomorrow
        if len(argv) is 3:
            if argv[2] == 'today':
                rep.display_menu(day=date.today())
            elif argv[2] == 'tomorrow':
                rep.display_menu(day=date.today() + timedelta(days=1))

        else:
            # Menu for certain date
            year, month, day = 2018, int(argv[2]), int(argv[3])
            rep.display_menu(day=date(year, month, day))
