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

// Display messages
function displayMessage(message, type = "info") {
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

function getCSRFToken() {
  const name = "csrftoken";
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i].trim();
    // Does this cookie string begin with the name we want?
    if (cookie.startsWith(name + "=")) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return null;
}

//  Add this sleep function (returns a Promise)
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function handleTicketLogin(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const csrfToken = getCSRFToken();
  const ticketData = {
    username: formData.get("ticketUsername"),
    password: formData.get("ticketPassword"),
    mac_address: formData.get("ticketMacAddress"),
    ip_address: formData.get("ticketIpAddress"),
  };

  console.log("Sending ticket validation request:", ticketData);
  toggleLoading(true);
  clearMessage();

  try {
    const res = await fetch("/api/tickets/validate/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(ticketData),
    });

    toggleLoading(false);
    const data = await res.json();

    if (res.ok) {
      displayMessage(data.message || "Login successful!", "success");
      await sleep(3000);
      clearMessage();
      // ✅ Ensure full URL with protocol
      window.location.href = "https://www.google.com";
    } else {
      console.log("Login failed:", data);
      displayMessage(
        data.message || "Login failed. Please try again.",
        "danger"
      );
    }
  } catch (err) {
    toggleLoading(false);
    console.error("Login error:", err);
    displayMessage("Something went wrong. Please try again later.", "danger");
  }
}
