document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    // Simple validation (as an example, real validation should be more comprehensive)
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (name && email && password) {
        // Here you would typically send data to server
        alert('Registration Successful!');
    } else {
        alert('Please fill in all fields.');
    }
});