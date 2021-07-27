document.addEventListener('DOMContentLoaded', function () {

    clickEdit();

  });

function clickEdit() {
    // Listen for "Edit" click
    let edit_buttons = document.querySelectorAll('.edit');

    for (let i = 0; i < edit_buttons.length; i++) {
        edit_buttons[i].addEventListener('click', Edit, false);
    }
}

function clickSave() {
    // Listen for "Save" click
    let buttons = document.querySelectorAll('.edit');

    for (let i = 0; i < buttons.length; i++) {
        if (buttons[i].innerHTML == 'Save'){
            buttons[i].addEventListener('click', Save, false);
        }
    }
}

function Edit() {
    let siblings = getSiblings(this);
    let post_text;
    let post_editor;

    // Grab post text and post editor elements from card
    for (let i = 0; i < siblings.length; i++){
        if (siblings[i].classList.contains('post-content')){
            post_text = siblings[i];
        }
        if (siblings[i].classList.contains('post-editor')){
            post_editor = siblings[i];
        }
    }

    // Show textarea and switch 'Edit' -> 'Save
    post_editor.style.display = 'block';
    this.innerHTML = 'Save';

    clickSave();
}

function Save() {
    let siblings = getSiblings(this);
    let post_text;
    let post_editor;

    // Grab post text and post editor elements from card
    for (let i = 0; i < siblings.length; i++){
        if (siblings[i].classList.contains('post-content')){
            post_text = siblings[i];
        }
        if (siblings[i].classList.contains('post-editor')){
            post_editor = siblings[i];
        }
    }

    fetch('', {
        method: 'PUT',
        body: JSON.stringify({
          text: post_editor.value
        })
      })
      .then(() => {
        post_editor.style.display = 'none';
        this.innerHTML = 'Edit';
      });

}

function getSiblings(e) {
    // for collecting siblings
    let siblings = []; 
    // if no parent, return no sibling
    if(!e.parentNode) {
        return siblings;
    }
    // first child of the parent node
    let sibling  = e.parentNode.firstChild;
    // collecting siblings
    while (sibling) {
        if (sibling.nodeType === 1 && sibling !== e) {
            siblings.push(sibling);
        }
        sibling = sibling.nextSibling;
    }
    return siblings;
}