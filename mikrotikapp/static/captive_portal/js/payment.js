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
