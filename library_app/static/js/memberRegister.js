document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("registerForm");
    const username = document.getElementById("username");
    const firstname = document.getElementById("firstname");
    const lastname = document.getElementById("lastname");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmPassword");
    const passwordMessage = document.getElementById("passwordMessage"); // Access the values from the form. 

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
        event.preventDefault();

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
            const response = await fetch("/api/member-register/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                alert("Member created successfully!");
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