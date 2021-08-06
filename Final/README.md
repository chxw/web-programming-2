# NBA Stats

## Name
chxw

## Date
08/05/21

## Using NBA Stats Application

The NBA Stats app is designed to allow users to search for active NBA players and view player statistics. Different statistics can be viewed in a static table (under player's "Bio" tab) or in a time-series line chart (under player's "Averages Graphed" tab). 

The app uses data.nba.net endpoints for retrieving accurate and up-to-date NBA data. The NBA.com website was used as a reference for understanding which player data and basketball stats should be prioritized.* 

Users can perform the following actions:
1. register an account with the site,
2. login/logout of the site,
3. view 5 random featured players on the site's homepage,
4. search for active NBA players, 
5. (un)favorite players, and
6. view favorited players on user profile page. 

*Please see NBA.com's [Stats Glossary](https://www.nba.com/stats/help/glossary/) if any abbreviation, such as "apg", "mpg" is unclear. 


# Files
```
.
├── README.md
└── final
    ├── db.sqlite3
    ├── final
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py
    └── nbastats
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── migrations
        │   ├── 0001_initial.py
        │   └── __init__.py
        ├── models.py                           # here
        ├── static
        │   └── nbastats
        │       ├── nbastats.js                 # here
        │       └── styles.css
        ├── templates
        │   └── nbastats                        # here
        │       ├── index.html
        │       ├── layout.html
        │       ├── login.html
        │       ├── player.html
        │       ├── register.html
        │       ├── search_results.html
        │       └── user.html
        ├── tests.py
        ├── urls.py
        ├── util.py                             # here
        └── views.py                            # here
```

# Design




# References

- https://www.nba.com
- https://www.d3-graph-gallery.com/graph/line_select.html
- https://github.com/kshvmdn/nba.js/blob/master/docs/api/DATA.md
- https://data.nba.net/
- https://www.balldontlie.io/
- https://stackoverflow.com/questions/60898397/field-id-expected-a-number-but-got-built-in-function-id
- https://stackoverflow.com/questions/9400615/whats-the-best-way-to-make-a-d3-js-visualisation-layout-responsive
- https://stackoverflow.com/questions/38580538/responsive-inline-svg-using-bootstrap
- https://stackoverflow.com/questions/13612006/get-object-property-name-as-a-string
- https://stackoverflow.com/questions/16919280/how-to-update-axis-using-d3-js
- https://stackoverflow.com/questions/43741271/d3-change-and-update-axis-domain-scatterplot
- https://stackoverflow.com/questions/44270083/how-to-specify-date-format-d3-js-for-x-axis
- https://stackoverflow.com/questions/28527712/how-to-add-key-value-pair-in-the-json-object-already-declared
- https://stackoverflow.com/questions/13181194/d3js-when-to-use-datum-and-data
- https://stackoverflow.com/questions/38397894/get-json-key-name
- https://stackoverflow.com/questions/22565077/javascript-get-object-property-name
- https://stackoverflow.com/questions/12622744/how-to-loop-through-the-attributes-of-a-json-obj
- https://stackoverflow.com/questions/55169313/performing-fetch-request-in-a-loop/55169496
- https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas
- https://stackoverflow.com/questions/20643437/create-pandas-dataframe-from-json-objects
- https://stackoverflow.com/questions/5993621/fastest-way-to-search-a-list-in-python
- https://stackoverflow.com/questions/45414082/the-fastest-method-to-find-element-in-json-python
- https://stackoverflow.com/questions/14048948/how-to-find-a-particular-json-value-by-key/42183539
- https://stackoverflow.com/questions/1133147/how-to-extract-the-year-from-a-python-datetime-object
- https://stackoverflow.com/questions/32028119/where-to-store-api-key-in-django