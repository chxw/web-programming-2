document.addEventListener('DOMContentLoaded', function () {

    clickAveragesGraphed();

});

function clickAveragesGraphed() {
    let button = document.querySelector('.graphed');

    button.onclick = displayGraph;
}

function displayGraph() {
    console.log('hello');
}