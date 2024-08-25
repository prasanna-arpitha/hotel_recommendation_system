
let signup = document.querySelector(".signup");
let login = document.querySelector(".login");
let slider = document.querySelector(".slider");
let formSection = document.querySelector(".form-section");

 
login.addEventListener("click", () => {
    slider.classList.remove("moveslider");
    formSection.classList.remove("form-section-move");
});


signup.addEventListener("click", () => {
    // Navigate to logsign.html with a parameter indicating signup
    window.location.href = "/logsign.html?signup=true";
});


document.addEventListener("DOMContentLoaded", function() {
    const params = new URLSearchParams(window.location.search);
    const isSignup = params.get('signup');
    if (isSignup === "true") {
        // Adjust the slider for signup
        const slider = document.querySelector(".slider");
        const formSection = document.querySelector(".form-section");
        slider.classList.add("moveslider");
        formSection.classList.add("form-section-move");
    }
});

console.log("Element:", document.getElementById('forgotPasswordForm'));

document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('forgotPasswordForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        const form = event.target;
        const username = form.username.value;
        const email = form.email.value;
        const newPassword = form.newPassword.value;
        const confirmPassword = form.confirmPassword.value;

        if (newPassword !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        var users = JSON.parse(localStorage.getItem('users')) || [];

        var foundUser = users.find(function(user) {
            return user.username === username && user.email === email;
        });

        if (foundUser) {
            // Update user's password
            foundUser.password = newPassword;
            localStorage.setItem('users', JSON.stringify(users));
            
            // Redirect to login page
            window.location.href = 'login.html';
        } 
        else {
            alert("User not found. Please check your username and email.");
        }
    });
});
// Function to save users data to localStorage
function saveUsers(users) {
    if (localStorage) {
        localStorage.setItem('users', JSON.stringify(users));
        console.log("Users data saved successfully.");
    } else {
        console.log("LocalStorage is not supported in this environment.");
    }
}

// Function to load users data from localStorage
function loadUsers() {
    if (localStorage) {
        const users = JSON.parse(localStorage.getItem('users')) || {};
        console.log("Users data loaded successfully.");
        return users;
    } else {
        console.log("LocalStorage is not supported in this environment.");
        return {};
    }
}

function generateNewPassword(){
    window.location.href = "/input.html";
}

function setParameterInForm(parameter) {
    // Get the input field by ID
    var inputField = document.getElementById('inputField');
    
    // Set the value of the input field to the parameter value
    inputField.value = parameter;
}

function redirectToInputPage() {
    console.log("function called");
    window.location.href = "/input.html";
}

function redirectToVerificationPage() {
    console.log("function called");
    window.location.href = "/verification.html";
}

function verification(){
    var email = document.getElementById('email').value;
    console.log("email"+email);
    redirectToVerificationPage();
}

function send_code(form){
    const email = form.email.value;
    console.log("email"+email);
    fetch('/send_email_verification_code', {
        method: 'POST', // Use POST method to send email data
        headers: {
            'Content-Type': 'application/json' // Specify JSON content type
        },
        body: JSON.stringify({ email: email }) // Send email as JSON in the request body
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.result);
        // Perform further actions with the result if needed
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function send_email_for_login(form){
    const email = form.email.value;
    console.log("email"+email);
    fetch('/send_email_for_login', {
        method: 'POST', // Use POST method to send email data
        headers: {
            'Content-Type': 'application/json' // Specify JSON content type
        },
        body: JSON.stringify({ email: email }) // Send email as JSON in the request body
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.result);
        // Perform further actions with the result if needed
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


async function signupbtn(form) {
    const username = form.username.value;
    const email = form.email.value;
    const password = form.password.value;
    const cpass = form.cpass.value;

    let users = loadUsers();
    if (username in users) {
        alert("Username already exists. Please choose a different one.");
        return;
    }
    if (email in users) {
        alert("Email already registered.");
        return;
    }
    if (password === cpass) {
        users[username] = {email:email, password:password}
        saveUsers(users);
        send_email_for_login(form);
        alert("SignUp successfull. You can Login now.")
        return true;
 
    }
    else{
        alert("Password does not match");
        return false;
    }
}

function loginbtn(form) {
    const username = form.username.value;
    const password = form.password.value;

    let users = loadUsers();

    if (!(username in users)) {
        alert("Username not found. Please sign up first.");
        return false;
    }

    if (users[username] && users[username].password === password){
        redirectToInputPage();
        alert("Login successful. Welcome back "+username);
        return true;

    } 
    else {
        alert("Incorrect password. Please try again.");
        return false;
    }
}
