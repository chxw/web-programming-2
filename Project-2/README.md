# Name:
chxw

# Date:
07/09/21

# Summary:
An implementation of an Ebay.com-like online auction site usint Python and Django.

The Django projects is named `commerce`. Within this project, there is a single app titled `auctions`. 

This project was an exercise in using the SQLite language and using Django's [model class](https://docs.djangoproject.com/en/3.2/topics/db/models/).

## Models
There are 6 implemented models in `models.py`.
1. User - implemented using Django's `AbstractUser`
2. Category
    - `id` field: Django's auto-generated id
    - `category` field: name of category
3. Listing
    - `id` field: Django's auto-generated id
    - `owner` field: user who created listing (ForeignKey to User table)
    - `title` field: title of listing
    - `description` field: description of listing
    - `starting_bid` field: starting bid set by user when listing is created
    - `image` field: URL to image (optional)
    - `current_price` field: highest bid currently = current price of listing
    - `is_active` field: Boolean for whether or not this listing is active
    - `created_on` field: timestamp of when listing was created
    - `category` field: mapping to which category is attached to listing (ForeignKey to Category table)
4. Bid
    - `id` field: Django's auto-generated id
    - `bidder` field: who submitted this bid (ForeignKey to User table)
    - `bid` field: value of bid
    - `created_on` field: timestamp of when bid was submitted
    - `listing` field: which listing this bid is attached to
5. Comment
    - `author` field: user who wrote the comment (ForeignKey to User table)
    - `text` field: text of comment
    - `listing` field: listing this comment is attached to
    - `created_on` field: timestamp of when comment was created
6. Watchlist
    - `watcher` field: user who has added this listing to their watchlist (ForeignKey to User table)
    - `listing` field: the listing the user has added to their watchlist 

# Files:
```
.
├── auctions
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_watchlist_watcher.py
│   │   ├── 0003_alter_bid_bid.py
│   │   └── __init__.py
│   ├── models.py
│   ├── static
│   │   └── auctions
│   │       └── styles.css
│   ├── templates
│   │   └── auctions
│   │       ├── categories.html
│   │       ├── create.html
│   │       ├── index.html
│   │       ├── layout.html
│   │       ├── listing.html
│   │       ├── login.html
│   │       ├── register.html
│   │       └── watchlist.html
│   ├── tests.py
│   ├── urls.py
│   ├── util.py
│   └── views.py
├── commerce
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
└── manage.py
```

# Instructions:
1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip3 install -r requirements.txt`
4. `python3 manage.py makemigrations auctions`
5. `python3 manage.py migrate`
6. `python3 manage.py runserver`

# References: