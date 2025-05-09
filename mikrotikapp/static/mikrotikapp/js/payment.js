// Get the modal
const modal = document.getElementById("paymentModal");
const span = document.getElementsByClassName("close")[0];

// Function to open modal
function openModal(packageId, amount) {
  modal.style.display = "block";
  document.getElementById("packageId").value = packageId;
  document.getElementById("amount").value = amount;
}

// Close modal when clicking the X
span.onclick = function () {
  modal.style.display = "none";
};

// Close modal when clicking outside
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

// Function to get CSRF token from cookies
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

// Function to start session check
function startSessionCheck(macAddress) {
  console.log("Starting session check with MAC:", macAddress);
  console.log("MAC address type:", typeof macAddress);

  if (!macAddress) {
    console.error("MAC address is undefined or empty");
    return;
  }

  const eventSource = new EventSource(`/api/payment-status/${macAddress}/`);

  eventSource.onmessage = function (event) {
    console.log("Received SSE message:", event.data);
    const data = JSON.parse(event.data);
    if (data.status === "success") {
      console.log("Session check successful, redirecting to:", data.link_orig);
      eventSource.close();
      window.location.href = data.link_orig;
    }
  };

  eventSource.onerror = function (error) {
    console.error("EventSource failed:", error);
    eventSource.close();
  };
}

// Handle form submission
document.getElementById("paymentForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const formData = new FormData(this);
  console.log("Form MAC address:", formData.get("macAddress"));

  const data = {
    phoneNumber: formData.get("phoneNumber"),
    amount: formData.get("amount"),
    macAddress: formData.get("macAddress"),
    ipAddress: formData.get("ipAddress"),
    username: formData.get("username"),
    linkLogin: formData.get("linkLogin"),
    linkLoginOnly: formData.get("linkLoginOnly"),
    linkOrig: formData.get("linkOrig"),
  };

  console.log("Submitting payment data:", data);

  fetch("/api/pending/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((err) => {
          throw err;
        });
      }
      return response.json();
    })
    .then((data) => {
      console.log("Payment API response:", data);
      // Close the modal
      modal.style.display = "none";
      // Show success message
      alert(
        "Payment request sent successfully! Please check your phone for the M-Pesa prompt."
      );
      // Start checking for active session
      startSessionCheck(data.macAddress);
      // Reset form
      document.getElementById("paymentForm").reset();
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error: " + (error.error || "Failed to submit payment request"));
    });
});
