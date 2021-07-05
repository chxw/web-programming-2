# Name:
chxw
# Date:
07/04/21
# Summary:
An implementation of a Wikipedia.org-like online encyclopedia using Python and the web framework, Django. 

The Django project is titled `wiki`. Within this project, there is a single app titled `encyclopedia`. The basic structure of the files is shown below. For a full `tree` see [Files](#Files). 
```
wiki/                                       - Outer root
    manage.py
    wiki/                                   - Inner root
        ...
        urls.py                             - URL declarations for project
        ...
        encyclopedia/                       - App
            urls.py                         - URL delcarations for app     
            util.py                         - Utility functions, pre-written for course
            models.py                       - Not used for this assignment
            views.py                        - Views functions
            forms.py                        - Django Form class definitions
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
                    404.html                - 404 Not Found error page
            entries/
                *.md                        - Where entries exist/are saved as .md files
```
## General
On every page there is a side-navigation bar. On the side-nav, there is 
1. a "Home" link to the Index page, 
2. a "Create New Page" link to the Create New page, and
3. a "Random Page" link to a random entry page. 

## Index Page
Displays list of all existing entries and links to those pages.

## Entry Page
Each encyclopedia entry's contents can be viewed by visiting that entry's page at `/wiki/[entry name]`. Each entry page has an "Edit" button that takes you to the the Edit Page. 

## Search
The searchbar exists on the side-nav bar. You can type in a query and click "Enter" to search existing entries. If there is an exact match to your query (i.e. you search "Python" and there exists an entry titled "Python"), you will be redirected to the existing entry page. If there is no exact match, but there are substring matches (i.e. you search "Py" and there exists "Python" and "Pythonidae" entries), you will be shown a page that displays all search results. All results are linked, and clicking on any of the results will take you to the corresponding page.

## Create New Page
On this page, there is a form where users can enter a "Subject" and "Context" where users are asked to **title** and **describe, detail, or define** the subject of their entry article. The title must be 100 chars or shorter or else the form won't submit successfully.

Clicking on "Submit" will save the new entry. Clicking on "Cancel" will take the user back to the previous page.

## Edit Page
On this page, there is a form where users can edit the "Context" of an existing entry. The "Context" must be written in [Markdown format](https://www.markdownguide.org/basic-syntax/). The title ("Subject") is not editable. 

# Files:
```
.
├── Assignment.md
├── README.md
├── requirements.txt
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
    │   │       ├── 404.html
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
    │   ├── Python.md
    │   └── Pythonidae.md
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
* https://docs.djangoproject.com/en/3.2/
* https://getbootstrap.com/
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
* https://stackoverflow.com/questions/47923952/python-django-how-to-display-error-messages-on-invalid-login
* https://stackoverflow.com/questions/8067510/onclick-javascript-to-make-browser-go-back-to-previous-page