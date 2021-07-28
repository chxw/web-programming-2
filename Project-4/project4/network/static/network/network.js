document.addEventListener('DOMContentLoaded', function () {

    clickPost();
    clickEditOrSave();
    clickLike();

});

function clickPost() {
    // Listen for post click
    let buttons = document.getElementsByName('Post');
    
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].onclick="this.disabled=true,this.form.submit()";
    }
}

function clickLike() {
    // Listen for like click
    let buttons = document.querySelectorAll('.like');

    for (let i = 0; i < buttons.length; i++) {
        buttons[i].onclick = likeOrUnlike;
    }
}

function likeOrUnlike() {
    let siblings = getSiblings(this);
    let num_likes_elem;
    const post_id = this.dataset.id;
    let like = false;
    
    if (this.innerHTML == 'Like') {
        like = true;
    }

    // Grab post editor element from card
    for (let i = 0; i < siblings.length; i++) {
        if (siblings[i].classList.contains('num-likes')) {
            num_likes_elem = siblings[i];
        }
    }

    fetch('', {
        method: 'PUT',
        body: JSON.stringify({
            like: like,
            id: post_id
        })
    })
    .then(response => console.log(response))
    .then(() => {
        fetch('api/likes/' + String(post_id))
            .then(response => response.json())
            .then(data => {
                num_likes_elem.textContent = data+" Likes";
            });
    })
    .then(() => {
        if (like){
            this.innerHTML = 'Unlike';
        } else {
            this.innerHTML = 'Like';
        }
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
        if (siblings[i].classList.contains('post-content')){
            post_content = siblings[i];
        }
    }

    // Show textarea, hide content, and switch 'Edit' -> 'Save'
    post_content.style.display = 'none';
    post_editor.style.display = 'block';
    post_editor.value = post_content.innerHTML;
    this.innerHTML = 'Save';

    clickEditOrSave();
}

function saveText() {
    let siblings = getSiblings(this);
    let post_content;
    let post_editor;

    // Grab post text and post editor elements from card
    for (let i = 0; i < siblings.length; i++) {
        if (siblings[i].classList.contains('post-content')) {
            post_content = siblings[i];
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
                    post_content.innerHTML = data.text;
                });
        })
        .then(() => {
            post_editor.style.display = 'none';
            post_content.style.display = 'block';
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