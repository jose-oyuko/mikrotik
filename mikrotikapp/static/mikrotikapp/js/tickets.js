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

  fetch("/api/ticket-login/", {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        showSuccess("Ticket validated successfully");
        // Redirect to original link after successful login
        window.location.href = formData.get("linkOrig");
      } else {
        showError(data.message || "Failed to validate ticket");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      showError("Failed to process ticket login");
    });
}

function showSuccess(message) {
  const successModal = document.getElementById("successModal");
  const successMessage = document.getElementById("successMessage");
  if (successModal && successMessage) {
    successMessage.textContent = message;
    $(successModal).modal("show");
  }
}

function showError(message) {
  const errorModal = document.getElementById("errorModal");
  const errorMessage = document.getElementById("errorMessage");
  if (errorModal && errorMessage) {
    errorMessage.textContent = message;
    $(errorModal).modal("show");
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
