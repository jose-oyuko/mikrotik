document.addEventListener("DOMContentLoaded", function () {
  const notConnectingModalElement =
    document.getElementById("notConnectingModal");
  const notConnectingModal = new bootstrap.Modal(notConnectingModalElement); // Define once

  const notConnectingButton = document.getElementById("not_connecting_button");
  notConnectingButton.addEventListener("click", function () {
    console.log("Not connecting button clicked");
    notConnectingModal.show();
  });

  const notConnectingForm = notConnectingModalElement.querySelector("form");
  notConnectingForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const data = {
      mpesa_code: formData.get("mpesaCode"),
      mac_address: formData.get("macAddress"),
      ip_address: formData.get("ipAddress"),
    };
    const csrfToken = getCSRFToken();
    console.log("Sending not connecting request:", data);
    notConnectingModal.hide();

    try {
      const response = await fetch("api/mpesa_code/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(data),
      });

      const response_data = await response.json();
      if (response_data.ok) {
        console.log(response_data);

        displayMessage(
          response_data.message || "Request sent successfully!",
          "success"
        );
        sleep(3000).then(() => {
          clearMessage();
        });
      } else {
        console.error("Error:", response_data.error);
        displayMessage(
          response_data.error || "Failed to send request.",
          "danger"
        );
        sleep(3000).then(() => {
          clearMessage();
        });
      }
    } catch (error) {
      console.log("Error sending not connecting request:", error);
    }
  });
});

function getCSRFToken() {
  const name = "csrftoken";
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i].trim();
    if (cookie.startsWith(name + "=")) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return null;
}

// Display messages
function displayMessage(message, type = "info") {
  const messageBox = document.getElementById("responseMessage");
  if (messageBox) {
    messageBox.innerHTML = `<div class="alert alert-${type}" role="alert">${message}</div>`;
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function clearMessage() {
  const messageBox = document.getElementById("responseMessage");
  if (messageBox) {
    messageBox.innerHTML = "";
  }
}
