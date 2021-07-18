document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email(recipients=null, subject=null, email_body=null));

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(recipients, subject, email_body) {

  // Show COMPOSE view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-email-view').style.display = 'none';

  // Disable recipients and subject inputs if this is a REPLY email
  if (recipients) {
    document.querySelector('#compose-recipients').placeholder = recipients;
    document.querySelector('#compose-recipients').disabled = true;
  }
  if (subject) {
    document.querySelector('#compose-subject').placeholder = subject;
    document.querySelector('#compose-subject').disabled = true;
  }

  let form = document.getElementById('compose-form');
  form.addEventListener('submit', (event) => {
    // Prevent form submission
    event.preventDefault();

    // Set variables if not set
    if (!recipients) {
      recipients = document.querySelector('#compose-recipients').value;
    }
    if (!subject) {
      subject = document.querySelector('#compose-subject').value;
    }
    if (!email_body){
      email_body = document.querySelector('#compose-body').value;
    } else {
      email_body = `${document.querySelector('#compose-body').value} <br> ${email_body}`;
    }

    // Prevent multiple submissions
    if (recipients && subject && email_body){
      // Send email to API
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: email_body
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      })
      .then(() => {
        load_mailbox('sent');
      });
    }

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
    document.querySelector('#compose-recipients').placeholder = 'Recipients';
    document.querySelector('#compose-recipients').disabled = false;
    document.querySelector('#compose-subject').placeholder = 'Subject';
    document.querySelector('#compose-subject').disabled = false;

    form.reset();

  }, false);
}

function load_mailbox(mailbox) {
  
  // Show MAILBOX and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';

  // Set variables
  const container = document.querySelector('#emails-view')
  
  // Show mailbox name
  container.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails from API
  mailbox_url = "".concat("/emails/", mailbox)
  fetch(mailbox_url)
  .then(response => response.json())
  .then(emails => {
      let createCard = (email) => {
        // Style email card
        const card = document.createElement('div');
        card.id = email.id
        card.className = 'card shadow';
        card.style.setProperty('cursor', 'pointer', '');
        if (email.read == true) {
          card.style.setProperty('background-color','gainsboro', '');
        }

        // Fill in email data
        const cardBody = document.createElement('div');
        cardBody.className = 'card-body';

        const sender = document.createElement('h5');
        sender.innerText = email.sender;

        const subject = document.createElement('h5');
        subject.innerText = email.subject;

        const timestamp = document.createElement('p');
        timestamp.className = 'float-right';
        timestamp.innerText = email.timestamp;

        // Build card with created elements
        cardBody.appendChild(sender);
        cardBody.appendChild(subject);
        cardBody.appendChild(timestamp);
        card.appendChild(cardBody);

        return card;
      }

      // Iterate through emails, create card, and append to cardContainer div
      let initListOfEmails = () => {
        let cardContainer = document.getElementById('emails-view');
        emails.forEach((email) => {
            card = createCard(email);
            cardContainer.appendChild(card)
        });
      };

      initListOfEmails();
  })
  .then(() => {
    // Add event listener on all cards to call load_email() function when clicked
    let cards = document.querySelectorAll('.card');
    for (let i = 0 ; i < cards.length; i++) {
      cards[i].addEventListener('click' , (event) => load_email(cards[i].id, mailbox) , false); 
  }
  });
}

function load_email(email_id, mailbox) {

  // Show the SINGLE EMAIL and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'block';

  // Get individual email
  const email_url = "".concat('/emails/',email_id)
  fetch(email_url)
  .then(response => response.json())
  .then(email => {
      // Create container for HTML elements
      let page = document.getElementById('single-email-view');

      // Utility elements
      const br = document.createElement('br'); // Line break
      const divider = document.createElement('hr'); // Horizontal line

      // From, to, subject, and time
      const from = document.createElement('p');
      from.innerHTML = "".concat("<b> From: </b> ",email.sender);
      
      const to = document.createElement('p');
      to.innerHTML = "".concat("<b> To: </b> ", email.recipients.join());

      const subject = document.createElement('p');
      subject.innerHTML = "".concat("<b> Subject: </b> ", email.subject);

      const time = document.createElement('p');
      time.innerHTML = "".concat("<b> Timestamp: </b> ", email.timestamp);

      // Reply button
      const reply = document.createElement('button');
      reply.innerText = "Reply";
      reply.className = "btn btn-sm btn-outline-primary";
      reply.addEventListener('click', () => reply_to(email, mailbox));

      // Archive toggle
      let archive = ''
      if (mailbox !== 'sent'){
        archive = document.createElement('button');
        archive.innerText = "Unarchive";
        if (email.archived == false){
          archive.innerText = "Archive";
        }
        archive.id = "archive";
        archive.className = "btn btn-sm btn-outline-primary";
        archive.addEventListener('click', () => toggle_archive(email_url));
      }
      
      // Body
      const body = document.createElement('p');
      body.innerHTML = email.body;

      // Build view email page structure
      items = [from, to, subject, time, reply, archive, divider, body];
      for (let i = 0 ; i < items.length; i++) {
        page.append(items[i]);
        page.append(br);
      }

      // Mark email as read
      read_email(email_url);
  });

  // Clear page for future loads
  document.querySelector('#single-email-view').innerHTML = '';
}

function read_email(email_url) {
  // Set 'read' attribute to true on given email_url
  fetch(email_url, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });
}

function toggle_archive(email_url) {
  fetch(email_url)
  .then(response => response.json())
  .then(email => {
    // Should we archive or unarchive?
    let set_to = false
    if (email.archived == false) {
      set_to = true;
    }

    // Update attribute and load archive mailbox
    fetch(email_url, {
      method: 'PUT',
      body: JSON.stringify({
          archived: set_to
      })
    })
    .then(() => {
      load_mailbox('archive');
    });
  });
}

function reply_to(email, mailbox) {
  // Clean subject line
  subject = email.subject;
  if (subject.slice(0, 4) !== "Re: "){
    subject = "".concat("Re: ", subject);
  }
  // Format body
  body = `<br> On ${email.timestamp} ${email.sender} wrote: <br> ${email.body}`;

  // Check if replying to a 'sent' email or non-'sent' email
  if (mailbox === 'sent') {
    compose_email(recipients=email.recipients, subject=subject, email_body=body);
  } else {
    compose_email(recipients=email.sender, subject=subject, email_body=body);
  }
}