// static/js/payment.js

document.addEventListener("DOMContentLoaded", function () {
  const paymentModal = document.getElementById("paymentModal");
  const modalPrice = document.getElementById("modal-price");
  const loadingModal = new bootstrap.Modal(
    document.getElementById("loadingModal")
  );
  const resultModal = new bootstrap.Modal(
    document.getElementById("resultModal")
  );
  let currentPrice = null;

  paymentModal.addEventListener("show.bs.modal", function (event) {
    const button = event.relatedTarget;
    currentPrice = button.getAttribute("data-price");
    console.log("Opening payment modal with price:", currentPrice);
    modalPrice.textContent = currentPrice;
  });

  const payForm = paymentModal.querySelector("form");
  payForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const phone = document.getElementById("mpesaNumber").value;
    console.log("Sending payment request...");
    console.log("Price:", currentPrice);
    console.log("Phone:", phone);
    const csrfToken = getCSRFToken();

    const pending_payment_url = "/api/pending/";
    const pending_payment_data = {
      phoneNumber: formData.get("phoneNumber"),
      amount: currentPrice,
      macAddress: formData.get("macAddress"),
      ipAddress: formData.get("ipAddress"),
    };

    loadingModal.show();

    fetch(pending_payment_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(pending_payment_data),
    })
      .then(async (res) => {
        const data = await res.json();
        loadingModal.hide();

        if (res.ok) {
          showResult(
            "Payment Initiated",
            data.message || "You will receive an mpesa prompt shortly.",
            "success"
          );
          startSessionCheck(data.macAddress);
        } else {
          showResult(
            "Payment Error",
            data.message || "An error occurred while processing your payment.",
            "danger"
          );
        }
      })
      .catch((err) => {
        console.error("Payment error:", err);
        loadingModal.hide();
        showResult(
          "Payment Error",
          "An unexpected error occurred. Please try again.",
          "danger"
        );
      });
    function showResult(title, message, type) {
      const titleElem = document.getElementById("resultTitle");
      const msgElem = document.getElementById("resultMessage");

      titleElem.innerText = title;
      msgElem.innerText = message;

      titleElem.className = `text-${type}`;
      resultModal.show();
    }
  });
});

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
