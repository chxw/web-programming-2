document.addEventListener('DOMContentLoaded', function () {

    clickEditOrSave();
    clickLike();

});

function clickLike() {
    // Listen for like click
    let buttons = document.querySelectorAll('.like');

    for (let i = 0; i < buttons.length; i++) {
        if (buttons[i].innerHTML == 'Like') {
            buttons[i].onclick = like;
        }
        else if (buttons[i].innerHTML == 'Unlike') {
            buttons[i].onclick = unlike;
        }
    }
}

function like() {
    fetch('', {
        method: 'PUT',
        body: JSON.stringify({
            like: true,
            id: this.dataset.id
        })
    })
        .then(() => {
            this.innerHTML = 'Unlike';
            clickLike();
        });
}

function unlike() {

    fetch('', {
        method: 'PUT',
        body: JSON.stringify({
            like: false,
            id: this.dataset.id
        })
    })
        .then(() => {
            this.innerHTML = 'Like';
            clickLike();
        });
}

function clickEditOrSave() {
    // Listen for button click
    let buttons = document.querySelectorAll('.edit');

    for (let i = 0; i < buttons.length; i++) {
        if (buttons[i].innerHTML == 'Save') {
            buttons[i].onclick = saveText;
        }
        else if (buttons[i].innerHTML == 'Edit') {
            buttons[i].onclick = editText;
        }
    }
}

function editText() {
    let siblings = getSiblings(this);
    let post_editor;

    // Grab post editor element from card
    for (let i = 0; i < siblings.length; i++) {
        if (siblings[i].classList.contains('post-editor')) {
            post_editor = siblings[i];
        }
    }

    // Show textarea and switch 'Edit' -> 'Save'
    post_editor.style.display = 'block';
    this.innerHTML = 'Save';

    clickEditOrSave();
}

function saveText() {
    let siblings = getSiblings(this);
    let post_text;
    let post_editor;

    // Grab post text and post editor elements from card
    for (let i = 0; i < siblings.length; i++) {
        if (siblings[i].classList.contains('post-content')) {
            post_text = siblings[i];
        }
        if (siblings[i].classList.contains('post-editor')) {
            post_editor = siblings[i];
        }
    }

    fetch('', {
        method: 'PUT',
        body: JSON.stringify({
            text: post_editor.value,
            id: post_editor.dataset.id
        })
    })
        .then(() => {
            fetch('api/posts/' + String(post_editor.dataset.id))
                .then(response => response.json())
                .then(data => {
                    post_text.innerHTML = data.text;
                });
        })
        .then(() => {
            post_editor.style.display = 'none';
            this.innerHTML = 'Edit';
            clickEditOrSave();
        });
}

function getSiblings(e) {
    // for collecting siblings
    let siblings = [];
    // if no parent, return no sibling
    if (!e.parentNode) {
        return siblings;
    }
    // first child of the parent node
    let sibling = e.parentNode.firstChild;
    // collecting siblings
    while (sibling) {
        if (sibling.nodeType === 1 && sibling !== e) {
            siblings.push(sibling);
        }
        sibling = sibling.nextSibling;
    }
    return siblings;
}