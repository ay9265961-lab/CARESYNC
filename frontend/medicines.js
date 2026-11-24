
const loadButton = document.getElementById("load-medicines");
const medicineList = document.getElementById("medicine-list");
const medicineMessage = document.getElementById("medicine-message");


async function loadMedicines() {
    medicineMessage.textContent = "Loading medicines...";
    medicineList.innerHTML = "";

    try {
        const medicines = await apiRequest("/medicines/");

        if (medicines.length === 0) {
            medicineMessage.textContent =
                "No medicines have been recorded yet.";
            return;
        }

        medicineMessage.textContent =
            medicines.length + " medicine record(s) found.";

        medicines.forEach((medicine) => {
            const card = document.createElement("article");
            card.className = "feature-card";

            const name = document.createElement("h3");
            name.textContent = medicine.name;

            const stock = document.createElement("p");
            stock.textContent =
                "Recorded stock: " + medicine.stock_count;

            const frequency = document.createElement("p");
            frequency.textContent =
                "Units used per day: " +
                (medicine.units_used_per_day ?? "Not recorded");

            card.append(name, stock, frequency);
            medicineList.appendChild(card);
        });

    } catch (error) {
        medicineMessage.textContent =
            error.message || "Unable to load medicine records.";
    }
}


loadButton.addEventListener("click", loadMedicines);


// Load records when the page opens
loadMedicines();
