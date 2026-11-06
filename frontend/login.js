const API = "http://127.0.0.1:8000";

const form = document.getElementById("loginForm");
const message = document.getElementById("loginMessage");

async function register() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    if (!username || password.length < 8) {
        message.textContent = "Enter a username and password with at least 8 characters.";
        return;
    }

    try {
        const response = await fetch(API + "/api/auth/register", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password})
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.detail || "Registration failed.";
            return;
        }

        localStorage.setItem("token", data.access_token);
        location.href = "index.html";
    } catch {
        message.textContent = "Cannot reach API. Start the backend first.";
    }
}

document.getElementById("registerBtn").addEventListener("click", register);

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const body = new URLSearchParams();
    body.set("username", document.getElementById("username").value.trim());
    body.set("password", document.getElementById("password").value);

    try {
        const response = await fetch(API + "/api/auth/login", {
            method: "POST",
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            body
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.detail || "Login failed.";
            return;
        }

        localStorage.setItem("token", data.access_token);
        location.href = "index.html";
    } catch {
        message.textContent = "Cannot reach API. Start the backend first.";
    }
});
