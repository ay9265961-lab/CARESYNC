
function showMessage(feature) {
    const message = document.getElementById("backend-status");

    if (message) {
        message.textContent =
            feature + " section selected. Feature integration is in progress.";
    }
}

// Check whether the backend is running
async function checkBackendStatus() {
    const status = document.getElementById("backend-status");

    if (!status) {
        console.error("Backend status element not found.");
        return;
    }

    try {
        const result = await apiRequest("/health");

        status.textContent =
            "CARESYNC Backend: " + result.status.toUpperCase();

    } catch (error) {
        status.textContent =
            "Backend connection unavailable. Please start the server.";
    }
}

// Run the health check when the dashboard loads
document.addEventListener("DOMContentLoaded", () => {
    checkBackendStatus();
});
