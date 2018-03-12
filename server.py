from sys import argv, exit
import pickle
import os
from datetime import date
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

    def report_food_occurance(self, food_item, from_day=None, till_day=None):
        """Report when a given food item occurs on the menu during the term."""
        current_date = term_start_date if from_day is None else from_day
        last_date = term_end_date if till_day is None else till_day

        while current_date != term_end_date:
            daily_menu = self.menu[current_date]
            for meal in daily_menu:
                for category in daily_menu[meal]:
                    for food_item in daily_menu[meal][category]:
                        print("{} is served on {} for {}").format(fooditem, current_date, meal)

            current_date += timedelta(days=1)

    def report_menu(self, day, meal=None, category=None):
        """Report the menu for the specified day, meal, and/or category."""
        # TODO

        self.mega_super_print(day, meal, category)

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
        if flag is "-o":
            # Occurance
            # TODO
            pass

        elif flag == "-d" or flag == "--date":
            # Menu for certain date
            year, month, day = 2018, int(argv[2]), int(argv[3])
            rep.report_menu(day=date(year, month, day))
