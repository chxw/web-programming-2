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

For a screen recorded demonstration of how to use the application, please see `demo.mov`.

*Please see NBA.com's [Stats Glossary](https://www.nba.com/stats/help/glossary/) if any abbreviation, such as "apg", "mpg" is unclear. 

# Design

## Files
The primary files that were worked on are highlighted below as `# here`. They will be discussed below.
```
.
├── README.md
├── demo.mov
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

### `models.py`
`User`, `Player`, `Bookmark` models are defined here. 

`User`: basic Abstract User.

`Player`:
    player_id = data.nba.net's equivalent to "personId" (see [here](https://data.nba.net/data/10s/prod/v1/2021/players.json))

`Bookmark`:
    user = foreign key to `User` model
    player = foreign key to `Player` model. 

### `nbastats.js`
Functionality for (1) `Averages Graphed` and (2) `(Un)Favorite`. 

(1) `Averages Graphed`
```javascript
    clickElement('#graph-link', displayGraph);
```
When a user clicks "Averages Graphed" tab on `/player` page, display D3.js produced line chart with dropdown menu.

```javascript
    clickElement('#bio-link', displayBio);
```
When a user clicks "Bio" tab on `/player` page, return to player page with image, background info, table of statistics. 

(2) `Un(Favorite)`
```javascript
    clickElement('.favorite', favoritePlayer);
```
When a user clicks "Favorite" or "Unfavorite", send a `"PUT"` request to the site's `/bookmark` endpoint.

### `templates/nbastats/*.html`
`layout.html` - Baseline layout template that gets extended for/used in every other template below. 

`index.html` - Home page that displays 5 featured players (randomly selected).

`user.html` - User profile page that displays username and list of favorited players.

`player.html` - Player page that displays player information, statistics, and averages graphed on dynamic D3.js line chart visualization.

`login.html` - Login page.

`register.html` - Register page. 

### `util.py`

Helper functions for the `views.py` file. These functions mostly request and clean data retreieved from the following endpoints:
```python
nba_endpoint = "https://data.nba.net/data/10s/prod/v1/"
headshot_endpoint = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/1040x760/"
logo_endpoint = "https://cdn.nba.com/logos/nba/"
```

### `views.py`

Displays different "views" of the site. These include:

- index: home page that retrieves 5 random NBA players and displays them in `index.html` template.
- search: conduct search based on user's search query and displays them in `index.html` template.
- player: player page that retreives and cleans player information, headshot, team name, team logo, and season averages, then displays them in `player.html` template. 
- user: user profile page that retrieves a user's bookmarked (favorited) players and displays them in `user.html` template.
- bookmark: API endpoint that either responds with `200` or `404` response code. Used by `nbastats.js` for editing a user's bookmarked (favorited) players. 
- login_view: display `login.html` template and login user if user inputs correct username, password.
- logout_view: log user out, redirect to indedx.
- register: display `register.html` and register new user using form information.

# Reflection

## Data quality
For this project, I definitely underestimated how long it would take to find a quality data source. I attempted the following data sources:
1. https://rapidapi.com/nucklehead/api/nba-stats4/
2. https://www.balldontlie.io/ (also https://rapidapi.com/theapiguy/api/free-nba/)

I quickly realized that `407ms` latency and 


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