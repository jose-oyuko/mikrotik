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

// Handle form submission
document
  .getElementById("paymentForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const phoneNumber = document.getElementById("phoneNumber").value;
    const amount = document.getElementById("amount").value;

    try {
      const response = await fetch("/api/pending/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          phoneNumber: phoneNumber,
          amount: amount,
          macAddress: "00:11:22:33:44:55", // Hardcoded for now
          ipAddress: "192.168.1.100", // Hardcoded for now
        }),
      });

      if (response.ok) {
        alert(
          "Payment request submitted successfully! Please check your phone for the M-Pesa prompt."
        );
        modal.style.display = "none";
        document.getElementById("paymentForm").reset();
      } else {
        const data = await response.json();
        alert("Error: " + (data.error || "Failed to submit payment request"));
      }
    } catch (error) {
      alert("Error submitting payment request. Please try again.");
      console.error("Error:", error);
    }
  });
