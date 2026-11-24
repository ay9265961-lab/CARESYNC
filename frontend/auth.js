
const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");

if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("login-email").value;
        const password = document.getElementById("login-password").value;
        const message = document.getElementById("login-message");

        try {
            await loginUser(email, password);

            message.textContent = "Login successful! Opening dashboard...";

            window.location.href = "index.html";
        } catch (error) {
            message.textContent = error.message;
        }
    });
}


if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const user = {
            name: document.getElementById("register-name").value,
            email: document.getElementById("register-email").value,
            password: document.getElementById("register-password").value,
            role: document.getElementById("register-role").value
        };

        const message = document.getElementById("register-message");

        try {
            const result = await apiRequest("/auth/register", {
                method: "POST",
                body: JSON.stringify(user)
            });

            message.textContent =
                result.message || "Account created successfully! You can now log in.";

            registerForm.reset();

        } catch (error) {
            message.textContent = error.message;
        }
    });
}
