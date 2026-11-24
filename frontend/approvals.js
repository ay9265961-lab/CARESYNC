
const approvalList = document.getElementById("approval-list");
const approvalMessage = document.getElementById("approval-message");
const loadApprovalsButton = document.getElementById("load-approvals");


// Load pending approval requests
async function loadApprovals() {
    approvalList.innerHTML = "";
    approvalMessage.textContent = "Loading requests...";

    try {
        const requests = await apiRequest("/approvals/pending");

        if (requests.length === 0) {
            approvalMessage.textContent =
                "No pending approval requests.";
            return;
        }

        approvalMessage.textContent =
            requests.length + " pending request(s) found.";

        requests.forEach((request) => {
            const card = document.createElement("article");
            card.className = "feature-card";

            const heading = document.createElement("h3");
            heading.textContent = "Request #" + request.request_id;

            const action = document.createElement("p");
            action.textContent = "Action: " + request.action;

            const description = document.createElement("p");
            description.textContent =
                "Details: " + (request.description || "No details provided");

            const requester = document.createElement("p");
            requester.textContent =
                "Requested by user ID: " + request.requested_by;

            const approveButton = document.createElement("button");
            approveButton.textContent = "Approve";

            const rejectButton = document.createElement("button");
            rejectButton.textContent = "Reject";
            rejectButton.style.background = "#b42318";

            approveButton.addEventListener("click", async () => {
                await respondToRequest(request.request_id, "approve");
            });

            rejectButton.addEventListener("click", async () => {
                await respondToRequest(request.request_id, "reject");
            });

            card.append(
                heading,
                action,
                description,
                requester,
                approveButton,
                rejectButton
            );

            approvalList.appendChild(card);
        });

    } catch (error) {
        approvalMessage.textContent = error.message;
    }
}


// Approve or reject a request
async function respondToRequest(requestId, decision) {
    approvalMessage.textContent = "Processing request...";

    try {
        const result = await apiRequest(
            `/approvals/${requestId}/${decision}`,
            { method: "POST" }
        );

        approvalMessage.textContent =
            result.message || "Request updated successfully.";

        await loadApprovals();

    } catch (error) {
        approvalMessage.textContent = error.message;
    }
}


// Refresh requests
loadApprovalsButton.addEventListener("click", loadApprovals);


// Load requests when the page opens
loadApprovals();
