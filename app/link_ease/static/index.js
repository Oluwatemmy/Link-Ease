// Get the form element, cancel button and the email validation message element
const form = document.getElementById('register-form');
const emailValidationMessage = document.getElementById('email-validation-message');

// Function to validate the form
function validateForm(event) {
    // Get the form inputs
    const nameInput = form.elements['name'];
    const emailInput = form.elements['email'];
    const passwordInput = form.elements['password'];
    const confirmPasswordInput = form.elements['confirm_password'];
    const agreeTermsInput = form.elements['agree_terms'];

    // Perform basic validation
    if (nameInput.value.trim() === '') {
        alert('Please enter your name');
        event.preventDefault();
        return;
    }

    if (emailInput.value.trim() === '') {
        alert('Please enter your email');
        event.preventDefault();
        return;
    }

    if (!isValidEmail(emailInput.value)) {
        alert('Please enter a valid email');
        event.preventDefault();
        return;
    }

    if (passwordInput.value.trim() === '') {
        alert('Please enter a password');
        event.preventDefault();
        return;
    }

    if (confirmPasswordInput.value.trim() === '') {
        alert('Please confirm your password');
        event.preventDefault();
        return;
    }

    if (passwordInput.value !== confirmPasswordInput.value) {
        alert('Passwords do not match');
        event.preventDefault();
        return;
    }

    if (!agreeTermsInput.checked) {
        alert('Please agree to the terms and conditions');
        event.preventDefault();
        return;
    }

    // Check if the email is valid
    if (emailInput.validity.valid) {
        // Set the success message
        emailValidationMessage.innerHTML = '<i class="fas fa-check"></i>';
    } else {
        // Set the error message
        emailValidationMessage.innerHTML = '< class="help is-danger"></>';
    }
}


// Function to validate email format
function isValidEmail(email) {
    // Regular expression to validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Add event listener for cancel button click
cancelButton.addEventListener('click', clearForm);

// Add event listener for form submission
form.addEventListener('submit', validateForm);


