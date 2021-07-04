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