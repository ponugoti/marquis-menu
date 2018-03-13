# Marquis Menu

I found the [culinary center's website](http://www.usask.ca/culinaryservices/marquis-menu.php) clumsy to navigate so I built a small terminal application to look up the menu, and search for food.

## Daily Menu

The daily menu of the culinary center can be looked up in two way:
* For today's menu, run `python menu.py`.
* For menu of another day, run `python menu.py -d <month> <day>`.

The menu for the appropriate day is displayed.

| Specific date | Current date |
| :---:|:---: |
| ![](/screenshots/menu_on_date.png) | ![](/screenshots/menu_today.png) |

## Food Search

To search for a food item using a search term, use one of the two supported ways:
* For results from the whole term, run `python menu.py -s <keyword>`
* For results in a specific range, run `python menu.py -s <keyword> <[from] mm dd> <[to] mm dd>`

The search results from the appropriate date range are displayed.

| Entire term                        |  Specified range                 |
| :---:|:---: |
| ![](/screenshots/search_general.png) | ![](/screenshots/search_in_range.png) |
