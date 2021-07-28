document.addEventListener('DOMContentLoaded', function () {

    clickPost();
    clickEditOrSave();
    clickLike();

});

function clickPost() {
    let buttons = document.getElementsByName('Post');
    
    for (let i = 0; i < buttons.length; i++) {
        // Prevent multiple button presses
        buttons[i].onclick="this.disabled=true,this.form.submit()";
    }
}

function clickLike() {
    let buttons = document.querySelectorAll('.like');

    for (let i = 0; i < buttons.length; i++) {
        // Listen for clicking .like button
        buttons[i].onclick = likeOrUnlike;
    }
}


function clickEditOrSave() {
    let buttons = document.querySelectorAll('.edit');

    for (let i = 0; i < buttons.length; i++) {
        // Listen for clicking .edit button
        buttons[i].onclick = editOrSave;
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

    // Grab num_likes element from card
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

function editOrSave() {
    let siblings = getSiblings(this);
    let post_editor;
    let post_content;

    // Grab relevant elements from card
    for (let i = 0; i < siblings.length; i++) {
        if (siblings[i].classList.contains('post-editor')) {
            post_editor = siblings[i];
        }
        if (siblings[i].classList.contains('post-content')){
            post_content = siblings[i];
        }
    }

    if (this.innerHTML == "Edit"){
        // Show textarea, hide content, and switch 'Edit' -> 'Save'
        post_content.style.display = 'none';
        post_editor.style.display = 'block';
        post_editor.value = post_content.innerHTML;
        this.innerHTML = 'Save';

        clickEditOrSave();
    }
    else { 
        // This is a "Save" button
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
}

function getSiblings(e) {
    let siblings = [];

    // No siblings
    if (!e.parentNode) {
        return siblings;
    }

    // Linked list traversal to get siblings
    let sibling = e.parentNode.firstChild;
    while (sibling) {
        if (sibling.nodeType === 1 && sibling !== e) {
            siblings.push(sibling);
        }
        sibling = sibling.nextSibling;
    }
    return siblings;
}