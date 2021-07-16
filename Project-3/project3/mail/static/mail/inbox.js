document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  let form = document.getElementById('compose-form');

  form.addEventListener('submit', (event) => {
      // Prevent form submission
      event.preventDefault;

      // Set variables
      const recipients = document.querySelector('#compose-recipients').value;
      const subject = document.querySelector('#compose-subject').value;
      const body = document.querySelector('#compose-body').value;
    
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      });
  }, false);

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Set variables
  const container = document.querySelector('#emails-view')
  
  // Show mailbox name
  container.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails
  fetch('/emails/inbox')
  .then(response => response.json())
  .then(emails => {
      let cardContainer

      let createCard = (email) => {
        const link = document.createElement('a');
        link.style = 'color: inherit';
        link.href = "".concat('emails/',email.id)

        const card = document.createElement('div');
        card.className = 'card shadow pe-auto';

        const cardBody = document.createElement('div');
        cardBody.className = 'card-body';

        const sender = document.createElement('h5');
        sender.innerText = email.sender;

        const subject = document.createElement('h5');
        subject.innerText = email.subject;

        const timestamp = document.createElement('p');
        timestamp.className = 'float-right';
        timestamp.innerText = email.timestamp;

        cardBody.appendChild(sender);
        cardBody.appendChild(subject);
        cardBody.appendChild(timestamp);
        card.appendChild(cardBody);
        link.appendChild(card)
        cardContainer.appendChild(link);
      }

      let initListOfEmails = () => {
        if (cardContainer) {
            container.innerHTML += cardContainer;
            return;
        }
    
        cardContainer = document.getElementById('emails-view');
        emails.forEach((email) => {
            createCard(email);
        });
      };

      initListOfEmails();

  });
  }