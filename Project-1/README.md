# Name:
chxw
# Date:
07/04/21
# Summary:
An implementation of Wikipedia.org using Python and the web framework, Django. The Django project is titled `wiki`. Within this project, there is a single app titled `encyclopedia`. The basic structure of the files is shown below. For a full `tree` see [Files](#Files). 
```
wiki/                                       - Outer root
    manage.py
    wiki/                                   - Inner root
        ...
        urls.py                             - URL declarations for project
        ...
        encyclopedia/                       - App
            urls.py                         - URL delcarations for app     
            util.py                         - Utility functions, pre-written
            models.py                       - Not used for this assignment
            tests.py                        - Written tests
            forms.py                        - Django Form class definitions
            apps.py                         - App configuration
            admin.py                        - Not used for this assignment
            static/
                encyclopedia/
                    styles.css              - CSS Stylesheet for app
            templates/
                encyclopedia/
                    layout.html             - General layout that is extended by other html templates
                    index.html              - Home page
                    new_entry.html          - Create a new page
                    search_results.html     - Display search results
                    edit_entry.html         - Edit a page
                    entry.html              - Display an entry
```


# Files:
```
├── Assignment.md
├── README.md
└── wiki
    ├── db.sqlite3
    ├── encyclopedia
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── migrations
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── static
    │   │   └── encyclopedia
    │   │       └── styles.css
    │   ├── templates
    │   │   └── encyclopedia
    │   │       ├── edit_entry.html
    │   │       ├── entry.html
    │   │       ├── index.html
    │   │       ├── layout.html
    │   │       ├── new_entry.html
    │   │       └── search_results.html
    │   ├── tests.py
    │   ├── urls.py
    │   ├── util.py
    │   └── views.py
    ├── entries
    │   ├── CSS.md
    │   ├── Django.md
    │   ├── Git.md
    │   ├── HTML.md
    │   └── Python.md
    ├── manage.py
    └── wiki
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
4. `python3 manage.py runserver`

# References:
* https://docs.djangoproject.com/en/3.2/.
* https://stackoverflow.com/questions/49016255/django-display-contents-of-txt-file-on-the-website
* https://stackoverflow.com/questions/38847441/django-exception-handling-best-practice-and-sending-customized-error-message
* https://stackoverflow.com/questions/49465281/how-to-return-404-page-intentionally-in-django
* https://stackoverflow.com/questions/9266135/django-include-html-not-rendering-correctly/9266364
* https://stackoverflow.com/questions/57449498/html-data-is-not-rendering-property-in-html-using-python-django
* https://stackoverflow.com/questions/4848611/rendering-a-template-variable-as-html
* https://stackoverflow.com/questions/54678389/search-bar-in-django
* https://stackoverflow.com/questions/4706255/how-to-get-value-from-form-field-in-django-framework
* https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
* https://stackoverflow.com/questions/52602663/how-do-i-add-input-type-button-as-a-formfield-in-django
* https://stackoverflow.com/questions/2080332/django-form-submit-button
* https://stackoverflow.com/questions/936376/prepopulate-django-non-model-form
* https://stackoverflow.com/questions/4945802/how-can-i-disable-a-model-field-in-a-django-form