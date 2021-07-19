# Name:
chxw

# Date:
07/18/21

# Summary:
A front-end implementation for an email client that makes API calls to a pre-written API in order to send and receive emails. 

The Django project is named `project3`. Within this project, there is a single app titled `mail`. 

This project was an exercise in writing JavaScript and making API calls.

## Index of function documentation
Located in `project3/mail/static/mail/inbox.js`. 
```javascript
/**
 * Display New email page. Send user-inputed values from form to API as an email. 
 * Sending POST to /emails endpoint.
 * @param {string} recipients A valid email address stored within the API. 
 * @param {string} subject    Subject line of email. 
 * @param {string} email_body Body of email. 
 */
function composeEmail(recipients, subject, email_body)

/**
 * Display list of emails in different mailboxes. 
 * Sending GET to /emails/[mailbox] endpoint.
 * @param {string} mailbox Expecting one of the following: 'inbox', 'sent', or 'archive'. 
 */
function loadMailbox(mailbox)

/**
 * Given a list of emails, create a list of email cards. 
 * @param {JSON} emails List of emails to create HTML cards for.
 * @param {*} mailbox   The mailbox these emails belong to.
 */
function createEmailCards(emails, mailbox)

/**
 * Display single email based on email_id. 
 * Sending GET to /emails/[email_id].
 * @param {string} email_id ID of individual email used in API request.
 * @param {string} mailbox  Expecting one of the following: 'inbox', 'sent', or 'archive'.
 */
function loadEmail(email_id, mailbox)

/**
 * Create HTML layout for individual email.
 * @param {JSON} email        JSON representation of email defined by API.   
 * @param {string} email_url  Expecting '/emails/email_id' that specifies which email to refer to.
 * @param {string} mailbox    The mailbox that this email belongs to. 
 */
function createEmailPage(email, email_url, mailbox)

/**
 * Set 'read' attribute to true on a given email (identified by email_url).
 * @param {string} email_url Expecting '/emails/email_id' that specifies which email to refer to.
 */
function readEmail(email_url)

/**
 * Toggle between (1) archiving and (2) unarchiving a given email (identified by email_url).
 * @param {string} email_url Expecting '/emails/email_id' that specifies which email to refer to.
 */
function toggleArchive(email_url)

/**
 * 
 * @param {JSON} email      JSON representation of email defined by API. 
 */
function replyTo(email)
```

# Files:
```
.
├── db.sqlite3
├── mail
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── static
│   │   └── mail
│   │       ├── inbox.js        This is the main file that was worked on for this project. 
│   │       └── styles.css      
│   ├── templates
│   │   └── mail
│   │       ├── inbox.html
│   │       ├── layout.html
│   │       ├── login.html
│   │       └── register.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
└── project3
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
4. Within `project3` directory, run: `python3 manage.py makemigrations auctions`
5. `python3 manage.py migrate`
6. `python3 manage.py runserver`

# References:
- https://stackoverflow.com/questions/27441803/why-does-jshint-throw-a-warning-if-i-am-using-const
- https://stackoverflow.com/questions/35642809/understanding-javascript-truthy-and-falsy
- https://stackoverflow.com/questions/61966996/how-do-i-fetch-only-once
- https://stackoverflow.com/questions/65248601/prevent-multiple-http-request-send-by-using-fetch
- https://stackoverflow.com/questions/56989777/addeventlistener-even-firing-multiple-times
- https://stackoverflow.com/questions/50029580/why-is-my-fetch-request-being-called-twice
- https://stackoverflow.com/questions/13506481/change-placeholder-text/13506567
- https://stackoverflow.com/questions/7975005/format-a-javascript-string-using-placeholders-and-an-object-of-substitutions
- https://stackoverflow.com/questions/4361585/how-to-check-if-a-variable-is-not-null
- https://stackoverflow.com/questions/2874688/how-to-disable-an-input-type-text
- https://stackoverflow.com/questions/2647867/how-can-i-determine-if-a-variable-is-undefined-or-null
- https://stackoverflow.com/questions/3723415/append-style-to-dom-not-replacing-existing
- https://stackoverflow.com/questions/11107823/what-happens-if-i-dont-pass-a-parameter-in-a-javascript-function
- https://stackoverflow.com/questions/32027935/addeventlistener-is-not-a-function-why-does-this-error-occur
- https://stackoverflow.com/questions/54706080/generating-dynamic-html-cards-from-a-javascript-array
- https://stackoverflow.com/questions/54868328/html-how-to-automatically-create-bootstrap-cards-from-a-js-file
- https://stackoverflow.com/questions/15641474/django-not-reflecting-updates-to-javascript-files
- https://stackoverflow.com/questions/37487826/send-form-data-to-javascript-on-submit