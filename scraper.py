from bs4 import BeautifulSoup as soup
from datetime import date, timedelta
from collections import defaultdict
from os import path
from unicodedata import normalize
import pickle
import requests

# meal plan start and end date
start_date = date(2018, 1, 3)
end_date = date(2018, 4, 28)

base_url = "http://www.usask.ca/culinaryservices/marquis-meals/"
space = "%20"
tail_url = ".php"

class food_database():
    """Stores all the food for the term."""
    def __init__(self):
        self.db = defaultdict()
        self.categories = ('woks', 'wells', 'hot plates', 'grills', 'noodles', 'pizza', 'soup')
        self.meals = ('brunch', 'lunch', 'supper')

    def add(self, day, meal=None, category=None, item=None):
        if day not in self.db:
            self.db[day] = {}
        if meal not in self.db[day]:
            self.db[day][meal] = {}
        if category not in self.db[day][meal]:
            self.db[day][meal][category] = []

        self.db[day][meal][category].append(item)

def make_url(first_date, last_date):
    def second_week_of_feb():
        return (first_month == 'Feb' and last_month == 'Feb') and (first_day == '4' and last_day == '10')

    first_month, last_month = first_date.strftime("%b"), last_date.strftime("%b")
    first_day, last_day = first_date.strftime("%d"), last_date.strftime("%d")

    # Remove leading 0 for days if there is one
    first_day = first_day[1] if first_day[0] == '0' else first_day
    last_day = last_day[1] if last_day[0] == '0' else last_day

    url = base_url
    url += first_month + space
    url += first_day + space
    url += "-" + space
    if not second_week_of_feb():
        url += last_month + space
    url += last_day + tail_url
    return url

def get_weeks():
    # First week is shorter than the rest
    weeks = [(date(2018, 1, 3), date(2018, 1, 6))]
    # Fill in all the weeks until last day of the term
    while weeks[-1][1] != end_date:
        _, last_sat = weeks[-1]
        next_week = last_sat + timedelta(days=1), last_sat + timedelta(days=7)
        weeks.append(next_week)
    return weeks

def get_days(week):
    first_date, last_date = week
    # Make a list of all the days in a given week
    days = [first_date]
    while days[-1] != last_date:
        days.append(days[-1] + timedelta(days=1))
    return days

def format_like_tag(day):
    # Format the day like the div tag element on each week's menu page
    daily_tag = "WeeklyMenu-"
    daily_tag += day.strftime("%A")
    daily_tag += day.strftime("%b")
    two_digits = day.strftime("%d")
    daily_tag += two_digits[1] if two_digits[0] == '0' else two_digits
    return daily_tag

def fetch_term_meals():
    weeks = get_weeks()
    week_date = start_date
    foods = food_database()

    for week in weeks:
        # Get contents from usask culinary servies page
        try:
            week_url = make_url(week[0], week[1])
            response = requests.get(week_url, timeout=5)
        except requests.Timeout as e:
            print("request timed out:", e)

        content = soup(response.content, "html.parser")

        # Get menu for each day of the week
        week_days = get_days(week)
        for today in week_days:
            # Mar 24 has no menu in lieu of Student Iron Chef
            # Apr 21 has no menu either for whatever reason
            if today == date(2018, 3, 24) or today == date(2018, 4, 21):
                foods.add(day=today)
                continue

            # Format of tag for a specific day
            weekday_tag = format_like_tag(today)

            # Menu response in raw html format
            raw_menu = content.find_all('div', id=weekday_tag)[0].find('table').find('tbody').find_all('td')
            raw_menu_list = [item.text.strip() for item in raw_menu if item.contents and item.text.strip()]

            # Remove weird HTML artifact unicode symbols
            menu_list = [normalize("NFKD", item) for item in raw_menu_list]

            # Add soups to brunch instead of lunch on weekends
            if today.isoweekday() in (6, 7):
                todays_meal_types = ('brunch', 'supper')
            else:
                todays_meal_types = ('lunch', 'supper')

            # Extract soups for the day and add them to both lunch/brunch and supper
            for meal in todays_meal_types:
                soup_cursor = 1
                while menu_list[soup_cursor].lower() not in todays_meal_types:
                    foods.add(day=today,
                              meal=meal,
                              category='soup',
                              item=menu_list[soup_cursor])
                    soup_cursor += 1

            # keep track of position, current meal, and category in the menu while iterating
            cursor = soup_cursor
            current_meal = menu_list[cursor].lower()
            cursor += 1
            current_category = menu_list[cursor].lower()
            cursor += 1

            while True:
                # Add the current menu item to the specific day, meal, and category
                foods.add(day=today,
                          meal=current_meal,
                          category=current_category,
                          item=menu_list[cursor])
                cursor += 1
                # Reached the end of the menu for the day
                if cursor == len(menu_list):
                    break

                # A lot of things are broken on valentine's day (including hearts)
                if today == date(2018, 2, 14):
                    # There are no entries for this category on this day, deal with it...
                    if menu_list[cursor].lower() == "hot plates":
                        current_category = menu_list[cursor].lower()
                        foods.add(day=today,
                                  meal=current_meal,
                                  category=current_category,
                                  item=None)
                        cursor += 1

                    elif menu_list[cursor].lower() == "dessert":
                        current_category = menu_list[cursor].lower()
                        cursor += 1


                if today == date(2018, 2, 14) and menu_list[cursor].lower() == "hot plates":
                    current_category = menu_list[cursor].lower()
                    foods.add(day=today, meal=current_meal, category=current_category, item=None)
                    cursor += 1
                # If the current positon is that of a category header, update current category
                if menu_list[cursor].lower() in foods.categories:
                    current_category = menu_list[cursor].lower()
                    cursor += 1
                # If the current cursor is that of a meal header, update current meal
                if menu_list[cursor].lower() in foods.meals:
                    current_meal = menu_list[cursor].lower()
                    cursor += 1
                    # The supper header in changed on valentine's day. Sigh.
                    if today == date(2018, 2, 14) and \
                                menu_list[cursor].lower() == "valentine's day special menu":
                        cursor += 1
                    current_category = menu_list[cursor].lower()
                    cursor += 1

    return foods

def create_menu_pickle():
    fname = 'term_menu.pickle'
    if not path.isfile(fname):
        foods = fetch_term_meals()
        with open(fname, 'wb') as pfile:
            pickle.dump(foods.db, pfile)
        print(fname, "created in current directiory.")
