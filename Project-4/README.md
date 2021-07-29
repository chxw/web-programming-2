# Name:
chxw

# Date:
07/28/21

# Summary:
Design and implement of a Twitter-like social network website for making posts and following users. 

The purpose of this project was to put together the Front-end (JavaScript, Bootstrap, Django templating language) and Back-end (Django models, API returns, Handling site views). 

Look for `# See here` comments in Files section to see which files were worked on for this project. 


# Files:
```
.
├── README.md
├── db.sqlite3
├── manage.py
├── network
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py                   # See here
│   ├── static
│   │   └── network
│   │       ├── network.js          # See here
│   │       └── styles.css
│   ├── templates
│   │   └── network
│   │       ├── index.html          # See here
│   │       ├── layout.html
│   │       ├── login.html
│   │       └── register.html
│   ├── tests.py
│   ├── urls.py                     # See here
│   ├── util.py
│   └── views.py                    # See here
└── project4
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

# Instructions:
1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip3 install -r requirements.txt`
4. Within `project4` directory, run: `python3 manage.py makemigrations network`
5. `python3 manage.py migrate`
6. `python3 manage.py runserver`

# References:
- https://stackoverflow.com/questions/5773408/how-to-clear-form-fields-after-a-submit-in-django
- https://stackoverflow.com/questions/4101258/how-do-i-add-a-placeholder-on-a-charfield-in-django
- https://stackoverflow.com/questions/49048414/how-do-i-remove-from-django-widgets-html5-attributes
- https://stackoverflow.com/questions/4123155/how-do-i-send-empty-response-in-django-without-templates
- https://stackoverflow.com/questions/1912351/django-where-to-put-helper-functions/1914081
- https://stackoverflow.com/questions/926816/how-to-prevent-form-from-submitting-multiple-times-from-client-side
- https://stackoverflow.com/questions/6320113/how-to-prevent-form-resubmission-when-page-is-refreshed-f5-ctrlr
- https://stackoverflow.com/questions/42971186/django-prevent-multiple-submits
- https://stackoverflow.com/questions/23326873/prevent-a-form-to-be-submitted-multiple-times-django
- https://stackoverflow.com/questions/2753732/how-to-access-svg-elements-with-javascript
- https://stackoverflow.com/questions/58376907/how-to-fix-uncaught-in-promise-syntaxerror-unexpected-token-in-json-at-pos
- https://stackoverflow.com/questions/37280274/syntaxerror-unexpected-token-in-json-at-position-0
- https://stackoverflow.com/questions/37269808/react-js-uncaught-in-promise-syntaxerror-unexpected-token-in-json-at-posit
- https://stackoverflow.com/questions/59260119/how-to-update-p-element-as-i-change-the-textarea
- https://stackoverflow.com/questions/5085567/what-is-the-hasclass-function-with-plain-javascript
- https://stackoverflow.com/questions/19655189/javascript-click-event-listener-on-class
- https://stackoverflow.com/questions/5525071/how-to-wait-until-an-element-exists
- https://stackoverflow.com/questions/27441803/why-does-jshint-throw-a-warning-if-i-am-using-const
- https://stackoverflow.com/questions/36496909/bootstrap-pagination-with-dynamic-content
- https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
- https://stackoverflow.com/questions/31237042/whats-the-difference-between-select-related-and-prefetch-related-in-django-orm
- https://stackoverflow.com/questions/431628/how-can-i-combine-two-or-more-querysets-in-a-django-view/42186970#42186970
- https://stackoverflow.com/questions/27293081/how-to-get-a-list-from-a-queryset-in-django/27296634
- https://stackoverflow.com/questions/4424435/how-to-convert-a-django-queryset-to-a-list
- https://stackoverflow.com/questions/58978754/how-to-pass-optional-parameters-in-url-via-path-function
- https://stackoverflow.com/questions/39935578/invalid-block-tag-endblock-did-you-forget-to-register-or-load-this-tag
- https://stackoverflow.com/questions/5439901/getting-a-count-of-objects-in-a-queryset-in-django
- https://stackoverflow.com/questions/13134743/one-line-if-else-condition-in-python
- https://stackoverflow.com/questions/40069192/django-models-database-design-for-user-and-follower
- https://stackoverflow.com/questions/45054529/laravel-5-eloquent-many-to-many-relationships
- https://stackoverflow.com/questions/14220852/django-many-to-many-relationship-with-built-in-user-model
- https://stackoverflow.com/questions/9834038/django-order-by-query-set-ascending-and-descending
- https://stackoverflow.com/questions/39325414/line-break-in-html-with-n
- https://stackoverflow.com/questions/37280274/syntaxerror-unexpected-token-in-json-at-position-0
- https://stackoverflow.com/questions/5064561/sending-html-code-through-json
- https://stackoverflow.com/questions/12495756/why-doesnt-git-allow-me-to-safely-delete-a-branch
- https://stackoverflow.com/questions/2862590/how-to-replace-master-branch-in-git-entirely-from-another-branch