document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(recipients, subject, body) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-email-view').style.display = 'none';

  let form = document.getElementById('compose-form');

  // Set variables
  if (recipients) {
    document.querySelector('#compose-recipients').placeholder = recipients;
    document.querySelector('#compose-recipients').disabled = true;
  }
  if (subject) {
    document.querySelector('#compose-subject').placeholder = subject;
    document.querySelector('#compose-subject').disabled = true;
  }
      
  form.addEventListener('submit', (event) => {
      // Prevent form submission
      event.preventDefault();

      if (!recipients) {
        recipients = document.querySelector('#compose-recipients').value;
      }
      if (!subject) {
        subject = document.querySelector('#compose-subject').value;
      }
      if (!body){
        body = document.querySelector('#compose-body').value;
      } else {
        body = "".concat(body, document.querySelector('#compose-body').value);
      }

      // Send API POST request of email form
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
      })
      .then(response => response.json())
      .then(() => {
          load_mailbox('sent');
      });
  });

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
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
        // Create elements of individual card
        const card = document.createElement('div');
        card.id = email.id
        card.className = 'card shadow';
        card.style.setProperty('cursor', 'pointer', '');
        if (email.read == true) {
          card.style.setProperty('background-color','gainsboro', '');
        }

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

      // Iterate through emails and create card and append to div
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
      let cards = document.querySelectorAll('.card');

      for (let i = 0 ; i < cards.length; i++) {
        cards[i].addEventListener('click' , (event) => load_email(cards[i].id) , false ); 
     }
    });
  }

  function load_email(email_id) {

    // Show the individual email and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#single-email-view').style.display = 'block';

    const email_url = "".concat('/emails/',email_id)

    // Get individual email
    fetch(email_url)
    .then(response => response.json())
    .then(email => {
        // Create HTML to display email
        let page = document.getElementById('single-email-view');

        // Utility elements
        const br = document.createElement('br');
        const divider = document.createElement('hr');

        // From, to, subject, and time
        const from = document.createElement('p');
        from.innerHTML = "".concat("<b>", "From:", "</b> ",email.sender);
        
        const to = document.createElement('p');
        to.innerHTML = "".concat("<b>", "To:", "</b> ", email.recipients.join());

        const subject = document.createElement('p');
        subject.innerHTML = "".concat("<b>", "Subject:", "</b> ", email.subject);

        const time = document.createElement('p');
        time.innerHTML = "".concat("<b>", "Timestamp:", "</b> ", email.timestamp);

        // Reply button
        const reply = document.createElement('button');
        reply.innerText = "Reply";
        reply.className = "btn btn-sm btn-outline-primary";
        reply.addEventListener('click', () => reply_to(email));

        // Archive toggle
        const archive = document.createElement('button');
        if (email.archived == false){
          archive.innerText = "Archive";
        } else {
          archive.innerText = "Unarchive";
        }
        archive.id = "archive";
        archive.className = "btn btn-sm btn-outline-primary";
        archive.addEventListener('click', () => toggle_archive(email_url));
        
        // Body
        const body = document.createElement('p');
        body.innerHTML = email.body;

        items = [from, to, subject, time, reply, archive, divider, body];

        // Build view email page structure
        for (let i = 0 ; i < items.length; i++) {
          page.append(items[i]);
          page.append(br);
        }

        // Set email read attribute to true
        read_email(email_url);
    });

    // Clear page for future loads
    document.querySelector('#single-email-view').innerHTML = '';
  }

function read_email(email_url) {
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
    let set_to
    if (email.archived == false) {
      set_to = true;
    } else {
      set_to = false;
    }

    // Update attribute and load archive mailbox
    fetch(email_url, {
      method: 'PUT',
      body: JSON.stringify({
          archived: set_to
      })
    })
    .then(() => {
      load_mailbox('archive')
    });
  });
}

function reply_to(email) {
  if (email.subject.slice(0, 1) === "Re"){
    subject = email.subject.slice(1);
  }
  subject = "".concat("Re: ", email.subject);
  body = "".concat("On ", email.timestamp, " ", email.sender, " wrote:", "<br>");
  console.log(email.sender)
  console.log(body)
  compose_email(recipients=email.sender, subject=subject, body=body);
}