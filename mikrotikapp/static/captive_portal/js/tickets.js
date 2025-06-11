document.addEventListener("DOMContentLoaded", function () {
  // Initialize tickets functionality
  initializeTickets();
});

function toggleLoading(show) {
  const loader = document.getElementById("loadingIndicator");
  if (loader) {
    loader.style.display = show ? "block" : "none";
  }
}

// display messages
function displayMessage(message, type = "infor") {
  const messageBox = document.getElementById("responseMessage");
  if (messageBox) {
    messageBox.innerHTML = `<div class="alert alert-${type}" role="alert">${message}</div>`;
  }
}

function clearMessage() {
  const messageBox = document.getElementById("responseMessage");
  if (messageBox) {
    messageBox.innerHTML = "";
  }
}

function initializeTickets() {
  const ticketLoginForm = document.getElementById("ticketLoginForm");
  if (ticketLoginForm) {
    ticketLoginForm.addEventListener("submit", handleTicketLogin);
  }
}

function handleTicketLogin(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const ticketData = {
    username: formData.get("ticketUsername"),
    password: formData.get("ticketPassword"),
    mac_address: formData.get("ticketMacAddress"),
    ip_address: formData.get("ticketIpAddress"),
  };

  console.log("Sending ticket validation request:", ticketData);
  toggleLoading(true);
  clearMessage();
  fetch("/api/tickets/validate/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(ticketData),
  })
    .then(async (res) => {
      toggleLoading(false);
      const data = await res.json();

      if (res.ok) {
        displayMessage(data.message || "Login successful!", "success");
      } else {
        displayMessage(
          data.message || "Login failed. Please try again.",
          "danger"
        );
      }
    })
    .catch((err) => {
      toggleLoading(false);
      console.error("Login error:", err);
      displayMessage("Something went wrong. Please try again later.", "danger");
    });
}
