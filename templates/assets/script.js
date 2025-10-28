console.log("StaticJinjaPlus JS loaded!");

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.backgroundColor = this.style.backgroundColor === 'lightblue' ? '' : 'lightblue';
        });
    });
});