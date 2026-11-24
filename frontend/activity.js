
async function loadActivity() {
    const activityList = document.getElementById("activity-list");
    const activityMessage = document.getElementById("activity-message");

    activityList.innerHTML = "";
    activityMessage.textContent = "Loading activity logs...";

    try {
        const logs = await apiRequest("/activity/");

        if (!Array.isArray(logs) || logs.length === 0) {
            activityMessage.textContent = "No activity logs available yet.";
            return;
        }

        activityMessage.textContent = "";

        logs.forEach((log) => {
            const item = document.createElement("div");
            item.className = "card";

            const action = document.createElement("h3");
            action.textContent = log.action || "Activity";

            const decision = document.createElement("p");
            decision.textContent = "Decision: " + (log.decision || "N/A");

            const details = document.createElement("p");
            details.textContent = "Details: " + (log.details || "No additional details");

            const date = document.createElement("p");
            date.textContent = "Date: " +
                (log.created_at
                    ? new Date(log.created_at).toLocaleString()
                    : "Not available");

            item.appendChild(action);
            item.appendChild(decision);
            item.appendChild(details);
            item.appendChild(date);

            activityList.appendChild(item);
        });

    } catch (error) {
        activityMessage.textContent =
            error.message || "Unable to load activity logs.";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadActivity();

    const refreshButton = document.getElementById("refresh-activity");

    if (refreshButton) {
        refreshButton.addEventListener("click", loadActivity);
    }
});
