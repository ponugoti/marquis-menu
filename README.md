# Marquis Menu

I found the [culinary center's website](http://www.usask.ca/culinaryservices/marquis-menu.php) clumsy to navigate so I built a small application to look up the menu from the terminal.

To get started, run `python server.py` to get the current day's menu.

To look up a specific date, run `python server.py -d <month> <day>`

If the cache file isn't present in the same directory during the first run of `server.py`, then the menu for the term is scraped from the official website. Once it's done, menus can looked up locally.

The menu for the appropriate date is displayed and will look something similar to these images.

| Specific date                      |  Current date                    |
| :---------------------------------:|:-------------------------------: |
| ![](/screenshots/menu_on_date.png) | ![](/screenshots/menu_today.png) |
