
const appointmentForm = document.getElementById("appointment-form");
const appointmentMessage = document.getElementById("appointment-message");
const appointmentList = document.getElementById("appointment-list");
const loadAppointmentsButton = document.getElementById("load-appointments");


// Load saved appointments
async function loadAppointments() {
    appointmentList.innerHTML = "";
    appointmentMessage.textContent = "Loading appointments...";

    try {
        const appointments = await apiRequest("/appointments/");

        if (appointments.length === 0) {
            appointmentMessage.textContent =
                "No appointments scheduled yet.";
            return;
        }

        appointmentMessage.textContent =
            appointments.length + " appointment(s) found.";

        appointments.forEach((appointment) => {
            const card = document.createElement("article");
            card.className = "feature-card";

            const title = document.createElement("h3");
            title.textContent = appointment.title;

            const date = document.createElement("p");
            date.textContent =
                "Date: " +
                new Date(appointment.appointment_time).toLocaleString();

            const location = document.createElement("p");
            location.textContent =
                "Location: " + (appointment.location || "Not specified");

            const notes = document.createElement("p");
            notes.textContent =
                "Notes: " + (appointment.notes || "None");

            card.append(title, date, location, notes);
            appointmentList.appendChild(card);
        });

    } catch (error) {
        appointmentMessage.textContent = error.message;
    }
}


// Save a new appointment
appointmentForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const title = document.getElementById("appointment-title").value;
    const dateValue = document.getElementById("appointment-date").value;
    const notes = document.getElementById("appointment-notes").value;

    if (!dateValue || new Date(dateValue) <= new Date()) {
        appointmentMessage.textContent =
            "Please select a future date and time.";
        return;
    }

    const appointmentData = {
        title: title,
        appointment_time: new Date(dateValue).toISOString(),
        notes: notes || null,
        location: null
    };

    try {
        await apiRequest("/appointments/", {
            method: "POST",
            body: JSON.stringify(appointmentData)
        });

        appointmentMessage.textContent =
            "Appointment saved successfully!";

        appointmentForm.reset();

        await loadAppointments();

    } catch (error) {
        appointmentMessage.textContent = error.message;
    }
});


// Refresh appointments
loadAppointmentsButton.addEventListener("click", loadAppointments);


// Load appointments when the page opens
loadAppointments();
