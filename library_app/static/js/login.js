// document.addEventListener("DOMContentLoaded", () => { // Wait for the DOM to be fully loaded
//     const form = document.getElementById("member-login-form");

//     form.addEventListener("submit", async (event) => { // Listen for the submit button click, execute when submit is clicked. 
//         event.preventDefault();

//         const username = document.getElementById("member-username").value;
//         const password = document.getElementById("member-password").value;

//         try {
//             const response = await fetch("/api/token/", { // Send the credentials to JWT API
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json" // The data I am sending is JSON
//                 },
//                 body: JSON.stringify({ // Making the payload to JSON
//                     username: username,
//                     password: password
//                 })
//             });

//             const data = await response.json(); // Waiting for the response. 

//             if (response.ok) {
//                 localStorage.setItem("access_token", data.access);
//                 localStorage.setItem("refresh_token", data.refresh);    // Stores it in the browser storage

//                 window.location.href = "/home/"; // Redirects to homepage
//             } else {
//                 alert("Invalid credentials");
//             }
//         } catch (error) {
//             alert("Something went wrong");
//             console.error(error);
//         }
//     });
// });

function setupLogin(formId, usernameId, passwordId, apiUrl) {
    const form = document.getElementById(formId);

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const username = document.getElementById(usernameId).value;
        const password = document.getElementById(passwordId).value;

        try {
            const response = await fetch(apiUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username,
                    password
                })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("access_token", data.access);
                localStorage.setItem("refresh_token", data.refresh);

                window.location.href = "/home/member/";
            } else {
                alert("Invalid credentials");
            }
        } catch (error) {
            alert("Something went wrong");
            console.error(error);
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    setupLogin(
        "member-login-form",
        "member-username",
        "member-password",
        "/api/member-login/"
    );

    setupLogin(
        "librarian-login-form",
        "librarian-username",
        "librarian-password",
        "/api/librarian-login/"
    );
});