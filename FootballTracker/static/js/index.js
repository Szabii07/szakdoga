const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

// Regisztrációs panel megjelenítése
signUpButton.addEventListener('click', () => {
    container.classList.add('right-panel-active');
});

// Bejelentkezési panel megjelenítése
signInButton.addEventListener('click', () => {
    container.classList.remove('right-panel-active');
});