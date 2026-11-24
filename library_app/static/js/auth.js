const ACCESS_KEY = "access_token";
const REFRESH_KEY = "refresh_token";

function saveTokens(access, refresh) {
    console.log("Accessed method")
    localStorage.setItem(ACCESS_KEY, access);
    localStorage.setItem(REFRESH_KEY, refresh);
}

function getAccessToken() {
    console.log("access: ", ACCESS_KEY)
    return localStorage.getItem(ACCESS_KEY);
}

function clearTokens() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
}

function logout() {
    clearTokens();
    window.location.href = "/api/login/";
}

// Ask the server for a new access token. Returns true on success.
async function refreshAccessToken() {
    const refresh = localStorage.getItem(REFRESH_KEY);
    if (!refresh) return false;

    const response = await fetch("/api/token/refresh/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refresh }),
    });

    if (!response.ok) return false; // refresh token expired or invalid

    const data = await response.json();
    localStorage.setItem(ACCESS_KEY, data.access);
    // Only present if you turn on ROTATE_REFRESH_TOKENS in SIMPLE_JWT.
    if (data.refresh) localStorage.setItem(REFRESH_KEY, data.refresh);
    return true;
}

// Use this instead of fetch() for any protected API.
async function authFetch(url, options = {}) {
    console.log("AuthFetch")
    const send = () => fetch(url, {
        ...options,
        headers: {
            ...(options.headers || {}),
            Authorization: `Bearer ${getAccessToken()}`,
        },
    });

    // Why options? Copies those settings (postMethod, body) to fetch()
    // options.headers -> preserves existing headers while adding authorization

    let response = await send();

    if (response.status === 401) {
        // Access token expired (or missing). Try once to get a new one.
        const refreshed = await refreshAccessToken();
        if (!refreshed) {
            logout(); // refresh token is also gone/expired -> log in again
            throw new Error("Session expired");
        }
        response = await send(); // retry with the new access token
    }

    return response;
}