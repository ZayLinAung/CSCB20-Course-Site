
    document.getElementById('registerForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission
    
    
        const name = document.getElementById('Username').value;
        const email = document.getElementById('Email').value;
        const password = document.getElementById('Password').value;
    
        if (name && email && password) {
            alert('Registration Successful!');
        } else {
            alert('Please fill in all fields.');
        }
    });

