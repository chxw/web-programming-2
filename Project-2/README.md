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
- https://stackoverflow.com/questions/16349545/optional-fields-in-django-models
- https://stackoverflow.com/questions/4341739/adding-an-attribute-to-the-input-tag-for-a-django-modelform-field
- https://stackoverflow.com/questions/22739701/django-save-modelform
- https://stackoverflow.com/questions/26185687/you-are-trying-to-add-a-non-nullable-field-new-field-to-userprofile-without-a
- https://stackoverflow.com/questions/5870537/whats-the-difference-between-django-onetoonefield-and-foreignkey
- https://stackoverflow.com/questions/48433682/users-as-foreign-key-in-django
- https://stackoverflow.com/questions/58258995/django-error-you-are-trying-to-add-a-non-nullable-field-author-to-entry-with
- https://stackoverflow.com/questions/48433682/users-as-foreign-key-in-django
- https://stackoverflow.com/questions/60382260/django-db-utils-integrityerror-not-null-constraint-failed-users-profile-user-i
- https://stackoverflow.com/questions/60446491/django-db-utils-integrityerror-not-null-constraint-failed-new-users-personal
- https://stackoverflow.com/questions/49554070/using-bootstrap-cards-as-a-hyperlink
- https://stackoverflow.com/questions/9710110/connect-to-user-model-in-django
- https://stackoverflow.com/questions/12110654/django-set-default-value-of-a-model-field-to-a-self-attribute
- https://stackoverflow.com/questions/7080486/how-do-you-specify-a-default-for-the-django-foreignkey-field/7081062#7081062
- https://stackoverflow.com/questions/39527289/associating-users-with-models-django
- https://stackoverflow.com/questions/1110153/what-is-the-most-efficient-way-to-store-a-list-in-the-django-models
- https://stackoverflow.com/questions/4300365/django-database-query-how-to-get-object-by-id
- https://stackoverflow.com/questions/30314741/django-date-query-from-newest-to-oldest
- https://stackoverflow.com/questions/30314741/django-date-query-from-newest-to-oldest
- https://stackoverflow.com/questions/48606087/getting-values-of-queryset-in-django
- https://stackoverflow.com/questions/8571383/how-to-identify-button-click-event-of-template-page-in-view-page-of-django
- https://stackoverflow.com/questions/21505255/identify-which-submit-button-was-clicked-in-django-form-submit
- https://stackoverflow.com/questions/26986342/how-to-get-foreignkey-value-for-specific-field-in-django-view
- https://stackoverflow.com/questions/19799955/django-get-the-set-of-objects-from-many-to-one-relationship
- https://stackoverflow.com/questions/13821866/queryset-object-has-no-attribute-name
- https://stackoverflow.com/questions/1395807/proper-way-to-handle-multiple-forms-on-one-page-in-django
- https://stackoverflow.com/questions/3052975/django-models-avoid-duplicates
- https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple
- https://stackoverflow.com/questions/61429416/efficient-way-of-avoiding-adding-duplicate-entries-to-django-model
- https://stackoverflow.com/questions/49245743/how-do-i-avoid-saving-duplicate-data-django
- https://stackoverflow.com/questions/3805958/how-to-delete-a-record-in-django-models
- https://stackoverflow.com/questions/67783120/warning-auto-created-primary-key-used-when-not-defining-a-primary-key-type-by