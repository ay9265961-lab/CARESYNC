
const familyForm = document.getElementById("family-request-form");
const familyMessage = document.getElementById("family-request-message");
const familyList = document.getElementById("family-request-list");
const familyListMessage = document.getElementById("family-list-message");
const loadFamilyButton = document.getElementById("load-family-requests");


// Send a family connection request
familyForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const elderlyUserId = document.getElementById("elderly-user-id").value;

    familyMessage.textContent = "Sending request...";

    try {
        const result = await apiRequest(
            `/family/request/${elderlyUserId}`,
            { method: "POST" }
        );

        familyMessage.textContent =
            result.message || "Connection request sent successfully!";

        familyForm.reset();

    } catch (error) {
        familyMessage.textContent = error.message;
    }
});


// Load incoming family requests for an elderly user
async function loadFamilyRequests() {
    familyList.innerHTML = "";
    familyListMessage.textContent = "Loading requests...";

    try {
        const requests = await apiRequest("/family/requests");

        if (requests.length === 0) {
            familyListMessage.textContent =
                "There are no pending family requests.";
            return;
        }

        familyListMessage.textContent =
            requests.length + " pending request(s) found.";

        requests.forEach((request) => {
            const card = document.createElement("article");
            card.className = "feature-card";

            const name = document.createElement("h3");
            name.textContent = request.family_member;

            const status = document.createElement("p");
            status.textContent = "Status: " + request.status;

            const approveButton = document.createElement("button");
            approveButton.textContent = "Approve Request";

            approveButton.addEventListener("click", async () => {
                try {
                    const result = await apiRequest(
                        `/family/approve/${request.request_id}`,
                        { method: "POST" }
                    );

                    familyListMessage.textContent =
                        result.message || "Family request approved.";

                    await loadFamilyRequests();

                } catch (error) {
                    familyListMessage.textContent = error.message;
                }
            });

            card.append(name, status, approveButton);
            familyList.appendChild(card);
        });

    } catch (error) {
        familyListMessage.textContent =
            error.message || "Unable to load family requests.";
    }
}


// Refresh incoming requests
loadFamilyButton.addEventListener("click", loadFamilyRequests);


// Load requests when the page opens
loadFamilyRequests();
