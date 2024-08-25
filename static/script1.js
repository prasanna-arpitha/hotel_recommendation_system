document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');
    const loginForm = document.getElementById('loginForm');
    const message = document.getElementById('message');

    signupForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(signupForm);
        fetch('/signup', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            message.innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
    });

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(loginForm);
        fetch('/login', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            message.innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
    });
});
