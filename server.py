from sys import argv, exit
import pickle
import os
from datetime import date, timedelta
from scraper import create_menu_pickle

# meal plan start and end date
term_start_date = date(2018, 1, 3)
term_end_date = date(2018, 4, 28)


class Reporter():
    """Print daily menu or other query responses that looks pretty."""

    def __init__(self, food_dictionary):
        self.menu = food_dictionary
        self.weekend_meals = ('brunch', 'supper')
        self.weekday_meals = ('lunch', 'supper')

    def _print_search_results(self, matches, longest):
        print("+--------+--------+" + '-' * (longest + 2) + "+")
        print("| DATE   | MEAL   | FOOD ITEM" + ' ' * (longest - 9), '|')
        print("+--------+--------+" + '-' * (longest + 2) + "+")
        for day in matches:
            print('|', day.strftime("%b %d"), end=' ')
            for meal in matches[day]:
                if meal is not list(matches[day].keys())[0]:
                    print("\n|       ", end=' ')
                print('|', meal, end=' ' * (6 - len(meal)))
                for item in matches[day][meal]:
                    if item is not matches[day][meal][0]:
                        print("\n|        |" + ' ' * 7, end='')
                    print(' |', item, end=' ' * (longest - len(item)))
                    print(' |', end='')
            print()
            if day is not list(matches.keys())[-1]:
                print("+--------+--------+" + '-' * (longest + 2) + "+")
        print("+--------+--------+" + '-' * (longest + 2) + "+\n")

    def search(self, target, from_day=None, till_day=None):
        """Report when a given food item occurs on the menu during the term."""
        current_date = term_start_date if from_day is None else from_day
        last_date = term_end_date if till_day is None else till_day

        matches = dict()    # all matches for target
        times_seen = 0      # number of times the target was matched
        longest_item = 0    # longest length of all food items found

        while current_date != last_date:
            daily_menu = self.menu[current_date]
            for meal in daily_menu:
                for category in daily_menu[meal]:
                    for food_item in daily_menu[meal][category]:
                        if food_item and target.lower() in food_item.lower():
                            longest_item = max(len(food_item), longest_item)
                            if current_date not in matches:
                                matches[current_date] = {}
                            if meal not in matches[current_date]:
                                matches[current_date][meal] = []
                            matches[current_date][meal].append(food_item)
                            times_seen += 1
            current_date += timedelta(days=1)

        if times_seen > 0:
            self._print_search_results(matches, longest_item)
            print("Search complete.", times_seen, "items found.")
        else:
            print("\nCouldn't find anything with", target, "on the menu.")

    def mega_super_print(self, day, meal=None, category=None):
        """Display the container in a pretty way on the command line."""
        # Brunch on weekends is replaced by lunch on weekends
        todays_meals = self.menu[day][meal] if meal else self.menu[day]

        try:
            print("+------------------------------+")
            print("| Marquis Hall menu for", day.strftime("%b %d"), '|')
            print("+------------------------------+")
            for meal in todays_meals:
                print(meal.title())
                # Food categories in each meal
                for category in self.menu[day][meal]:
                    print("\n    ", category.title())
                    # Foods items in each category
                    food_items = self.menu[day][meal][category]
                    for food in food_items:
                        print("\t", food)
        except AttributeError:
            print("Sorry! The menu for this day is not available.")


if __name__ == '__main__':
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
        rep.report_menu(day=date.today())

    if len(argv) > 1:
        flag = argv[1]
        if flag in ('-s', '--search'):
            # Occurance of a particular food item
            if len(argv) is 7:
                rep.search(target=argv[2], \
                           from_day=date(2018, int(argv[3]), int(argv[4])), \
                           till_day=date(2018, int(argv[5]), int(argv[6])))
            else:
                rep.search(target=argv[2])

        elif flag in ('-d', '--date'):
            # Menu for certain date
            year, month, day = 2018, int(argv[2]), int(argv[3])
            rep.report_menu(day=date(year, month, day))
