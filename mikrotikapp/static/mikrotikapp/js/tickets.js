// Store modal instances globally
let successModalInstance = null;
let errorModalInstance = null;

document.addEventListener("DOMContentLoaded", function () {
  // Initialize tickets functionality
  initializeTickets();
});

function initializeTickets() {
  // Set up form submission handler
  const ticketLoginForm = document.getElementById("ticketLoginForm");
  if (ticketLoginForm) {
    ticketLoginForm.addEventListener("submit", handleTicketLogin);
  }
}

function handleTicketLogin(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const ticketUsername = formData.get("ticketUsername");
  const ticketPassword = formData.get("ticketPassword");
  const macAddress = document.getElementById("ticketMacAddress")?.value;
  const ipAddress = document.getElementById("ticketIpAddress")?.value;
  const linkOrig = document.getElementById("ticketLinkOrig")?.value;

  // Basic validation
  if (
    !ticketUsername ||
    !ticketPassword ||
    !macAddress ||
    !ipAddress ||
    !linkOrig
  ) {
    showError("Please fill in all required fields.");
    return;
  }

  // Prepare data for the API request
  const postData = {
    username: ticketUsername,
    password: ticketPassword,
    mac_address: macAddress,
    ip_address: ipAddress,
  };

  console.log("Sending ticket validation request:", postData);

  fetch("/api/tickets/validate/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(postData),
  })
    .then((response) => {
      console.log("Ticket validation response status:", response.status);
      return response
        .json()
        .then((data) => ({ status: response.status, body: data }));
    })
    .then(({ status, body }) => {
      console.log("Ticket validation response body:", body);
      if (status >= 200 && status < 300) {
        showSuccess(body.message || "Ticket validated successfully", linkOrig);
      } else {
        showError(body.error || "Failed to validate ticket");
      }
    })
    .catch((error) => {
      console.error("Error during ticket validation fetch:", error);
      showError("An error occurred during ticket validation.");
    });
}

function showSuccess(message, redirectUrl = null) {
  const successModal = document.getElementById("successModal");
  const successMessage = document.getElementById("successMessage");

  if (!successModal || !successMessage) {
    console.error("Success modal elements not found");
    return;
  }

  // Set the message
  successMessage.textContent = message;

  // Show the modal
  successModal.style.display = "block";

  // Add redirect handler if URL is provided
  if (redirectUrl) {
    setTimeout(() => {
      window.location.href = redirectUrl;
    }, 1500);
  }
}

function showError(message) {
  const errorModal = document.getElementById("errorModal");
  const errorMessage = document.getElementById("errorMessage");

  if (!errorModal || !errorMessage) {
    console.error("Error modal elements not found");
    return;
  }

  // Set the message
  errorMessage.textContent = message;

  // Show the modal
  errorModal.style.display = "block";
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "none";
  }
}

// Close modal when clicking outside
window.onclick = function (event) {
  if (event.target.classList.contains("custom-modal")) {
    event.target.style.display = "none";
  }
};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
