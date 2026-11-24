
const assistantForm = document.getElementById("assistant-form");
const assistantInput = document.getElementById("assistant-input");
const assistantResponse = document.getElementById("assistant-response");

function getAssistantReply(message) {
    const text = message.toLowerCase();

    if (text.includes("medicine") || text.includes("stock")) {
        return "You can manage medicine records through the Medicines section. Open the Medicines page to view recorded stock.";
    }

    if (text.includes("appointment") || text.includes("doctor")) {
        return "Open the Appointments section to view or create an appointment reminder.";
    }

    if (text.includes("family") || text.includes("link")) {
        return "Open the Family section to request or manage family connections.";
    }

    if (text.includes("approval") || text.includes("request")) {
        return "Open the Approvals section to review pending family approval requests.";
    }

    if (text.includes("activity") || text.includes("history")) {
        return "Open the Activity section to view available activity logs.";
    }

    if (text.includes("help") || text.includes("what can you do")) {
        return "I can guide you through Medicines, Appointments, Family Coordination, Approvals, and Activity Logs.";
    }

    if (text.includes("hello") || text.includes("hi")) {
        return "Hello! Welcome to CARESYNC. How can I help you use the application today?";
    }

    return "I can help you navigate CARESYNC. Try asking about medicines, appointments, family connections, approvals, or activity logs.";
}

assistantForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const message = assistantInput.value.trim();

    if (!message) {
        assistantResponse.textContent = "Please enter a message.";
        return;
    }

    assistantResponse.textContent = getAssistantReply(message);

    assistantInput.value = "";
});
