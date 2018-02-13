from sys import argv, exit
import pickle
import os
from datetime import date

class Reporter():
    """Print daily menu or other query responses that looks pretty."""
    def __init__(self, food_dictionary):
        self.menu = food_dictionary
        self.categories = ('woks', 'wells', 'hot plates', 'grills', 'noodles', 'pizza', 'soup')
        self.weekend_meals = ('brunch', 'supper')
        self.weekday_meals = ('lunch', 'supper')

    def report_food_frequency(self, food_item):
        """Report how many times a given food item occurs on the menu during the term."""
        # TODO
        pass

    def report_food_occurance(self, food_item):
        """Report when a given food item occurs on the menu during the term."""
        # TODO
        pass

    def report_menu(self, day, meal=None, category=None):
        """Report the menu for the specified occasion."""
        if date is None:
            raise AttributeError("no date specified")
        if meal is None and category is None:
            self.mega_super_print(day)
        # TODO

    def mega_super_print(self, day):
        """Display the container in a pretty way on the command line."""
        # Brunch on weekends is replaced by lunch on weekends
        todays_menu = self.menu[day]
        todays_meals = self.weekend_meal if day.isoweekday() in (6, 7) else self.weekday_meals

        for meal in todays_meals:
            print(meal.title())
            # Food categories in each meal
            for category in self.categories:
                print("    ", category.title())
                # Foods items in each category
                food_items = todays_menu[meal][category]
                for food in food_items:
                    print("\t", food)


if __name__ == '__main__':
    fname = 'term_menu.pickle'
    if not os.path.isfile(fname):
        print(fname, "does not exist in current directiory.")
        exit()

    # Load huge dictionary containing the whole term's menu
    with open(fname, 'rb') as pfile:
        food_dictionary = pickle.load(pfile)

    # Report relevant information based on command line query
    reporter = Reporter(food_dictionary)

    # No inputs, show today's menu
    if len(argv) is 1:
        reporter.report_menu(day=date.today())

    elif len(argv) is 2:
        if argv[1] in ('supper', 'dinner'):
            reporter.report_menu(day=date.today(), meal="dinner")
        else:
            reporter.report_menu(day=date.today(), meal=argv[1])

    # Input was date only, show menu for the day
    elif len(argv) is 3:
        year, month, day = 2018, int(argv[1]), int(argv[2])
        reporter.report_menu(day=date(year, month, day))
