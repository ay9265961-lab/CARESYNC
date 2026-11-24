
function showMessage(feature) {
    const message = document.getElementById("message");

    message.textContent =
        feature + " section selected. Feature integration is in progress.";
}


// Check whether the backend is running
async function checkBackendStatus() {
    const message = document.getElementById("message");

    try {
        const result = await apiRequest("/health");

        message.textContent =
            "CARESYNC Backend: " + result.status.toUpperCase();

    } catch (error) {
        message.textContent =
            "Backend connection unavailable. Please start the server.";
    }
}


// Run the health check when the dashboard loads
document.addEventListener("DOMContentLoaded", () => {
    checkBackendStatus();
});
