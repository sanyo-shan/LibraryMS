document.addEventListener("DOMContentLoaded", async () => {
    document.getElementById("logout-btn").addEventListener("click", logout);
    console.log("Home Page")

    // Not logged in at all -> back to login, don't even call the API.
    if (!getAccessToken()) {
        console.log("No data")
        window.location.href = "/api/login/";
        return;
    }

    try {
        const response = await authFetch("/api/home/member/1/");
        if (!response.ok) throw new Error(`Home API returned ${response.status}`);

        const data = await response.json()
        document.getElementById("welcome").textContent = data.message;
        document.getElementById("role").textContent = `Logged in as (${data.username})`;

        document.getElementById("loading").hidden = true;
        document.getElementById("content").hidden = false;

        } catch (error) {
        // authFetch already redirects to /login/ if the session expired.
        console.error(error);
        document.getElementById("loading").textContent = "Could not load your page.";
    }
});