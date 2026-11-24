document.addEventListener("DOMContentLoaded", function () {

    console.log("JS file accessed")
    const form = document.getElementById("registerForm");
    const username = document.getElementById("username");
    const firstname = document.getElementById("firstname");
    const lastname = document.getElementById("lastname");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmPassword");
    const passwordMessage = document.getElementById("passwordMessage"); // Access the values from the form.
    const endpoint = form.dataset.endpoint; // To get endpoint from the data that is being sent.  

    confirmPassword.addEventListener("keyup", function () {

        if (password.value === confirmPassword.value) {
            passwordMessage.textContent = "Passwords match";
            passwordMessage.style.color = "green";
        } else {
            passwordMessage.textContent = "Passwords do not match";
            passwordMessage.style.color = "red";
        }

    });

    form.addEventListener("submit", async function (event) { 
        // 'async' -> waits until the user clicks the submit button. 
        event.preventDefault(); // Normally, when the form is submitted the page reloads. This prevents that. 

        if (password.value !== confirmPassword.value) {
            alert("Password and Confirm Password must be the same.");
            return;
        }

        const payload = {
            username: username.value,
            first_name: firstname.value,
            last_name: lastname.value,
            password: password.value,
            confirm_password: confirmPassword.value
        };

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                if (endpoint.includes("member")) { 
                alert("Member created successfully!");
                } else {
                    alert("Librarian created successfully!")
                }
                form.reset();
                window.location.href = "/api/login/"

            } else {
                alert(data.message || "Registration failed");
            }

        } catch (error) {
            console.error(error);
            alert("Server error occurred");
        }
    });

});