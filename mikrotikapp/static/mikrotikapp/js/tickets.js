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

  // Initialize Bootstrap modals (ensure Bootstrap JS is loaded before this)
  const successModalElement = document.getElementById("successModal");
  if (successModalElement) {
    const successModal = new bootstrap.Modal(successModalElement);
    successModalElement.addEventListener("hidden.bs.modal", function (event) {
      // Optional: Clear messages or reset modal state on hide
    });
  }

  const errorModalElement = document.getElementById("errorModal");
  if (errorModalElement) {
    const errorModal = new bootstrap.Modal(errorModalElement);
    errorModalElement.addEventListener("hidden.bs.modal", function (event) {
      // Optional: Clear messages or reset modal state on hide
    });
  }
}

function handleTicketLogin(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const ticketUsername = formData.get("ticketUsername");
  const ticketPassword = formData.get("ticketPassword");
  // Use the updated unique IDs for hidden fields
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
    // link_orig is not sent to the backend validation endpoint,
    // but we store it to use for redirection on success.
  };

  console.log("Sending ticket validation request:", postData);

  fetch("/api/tickets/validate/", {
    // Use the correct validation endpoint
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(postData), // Send JSON body
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
        // Success
        showSuccess(body.message || "Ticket validated successfully");
        // Redirect to original link after successful login
        // Use the stored linkOrig
        if (linkOrig) {
          // Add a small delay before redirecting to allow the success modal to be seen
          setTimeout(() => {
            window.location.href = linkOrig;
          }, 1500); // Redirect after 1.5 seconds
        } else {
          console.warn("linkOrig is not available for redirection.");
          // Fallback or inform user
        }
      } else {
        // Error
        showError(body.error || "Failed to validate ticket");
      }
    })
    .catch((error) => {
      console.error("Error during ticket validation fetch:", error);
      showError("An error occurred during ticket validation.");
    });
}

function showSuccess(message) {
  const successModalElement = document.getElementById("successModal");
  const successMessageElement = document.getElementById("successMessage");
  if (successModalElement && successMessageElement) {
    successMessageElement.textContent = message;
    const successModal =
      bootstrap.Modal.getInstance(successModalElement) ||
      new bootstrap.Modal(successModalElement);
    successModal.show();
  }
}

function showError(message) {
  const errorModalElement = document.getElementById("errorModal");
  const errorMessageElement = document.getElementById("errorMessage");
  if (errorModalElement && errorMessageElement) {
    errorMessageElement.textContent = message;
    const errorModal =
      bootstrap.Modal.getInstance(errorModalElement) ||
      new bootstrap.Modal(errorModalElement);
    errorModal.show();
  }
}

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
