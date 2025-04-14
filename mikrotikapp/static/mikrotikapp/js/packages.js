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

// Initialize package CRUD operations
document.addEventListener("DOMContentLoaded", function () {
  // Save Package
  const savePackageBtn = document.getElementById("savePackage");
  if (savePackageBtn) {
    savePackageBtn.addEventListener("click", function () {
      const form = document.getElementById("packageForm");
      const formData = new FormData(form);
      const packageData = {
        price: formData.get("price"),
        period_in_hours: formData.get("period_in_hours"),
      };

      fetch("/api/packages/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(packageData),
      })
        .then((response) => {
          if (response.ok) {
            location.reload();
          } else {
            return response.json().then((data) => {
              throw new Error(data.error || "Failed to save package");
            });
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          showToast(error.message, "error");
        });
    });
  }

  // Edit Package
  document.querySelectorAll(".edit-package").forEach((button) => {
    button.addEventListener("click", function () {
      const packageId = this.dataset.id;
      const row = this.closest("tr");
      const price = row.cells[0].textContent;
      const period = row.cells[1].textContent;

      // Populate the form
      document.getElementById("packagePrice").value = price;
      document.getElementById("packagePeriod").value = period;

      // Show the modal
      const modal = new bootstrap.Modal(
        document.getElementById("addPackageModal")
      );
      modal.show();

      // Update the save button to handle edit
      const saveButton = document.getElementById("savePackage");
      const originalText = saveButton.textContent;
      saveButton.textContent = "Update Package";

      // Store the original click handler
      const originalClickHandler = saveButton.onclick;

      // Set new click handler for edit
      saveButton.onclick = function () {
        const form = document.getElementById("packageForm");
        const formData = new FormData(form);
        const packageData = {
          price: formData.get("price"),
          period_in_hours: formData.get("period_in_hours"),
        };

        fetch(`/api/packages/${packageId}/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify(packageData),
        })
          .then((response) => {
            if (response.ok) {
              location.reload();
            } else {
              return response.json().then((data) => {
                throw new Error(data.error || "Failed to update package");
              });
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            showToast(error.message, "error");
          });
      };

      // Reset the modal when hidden
      document.getElementById("addPackageModal").addEventListener(
        "hidden.bs.modal",
        function () {
          saveButton.textContent = originalText;
          saveButton.onclick = originalClickHandler;
          document.getElementById("packageForm").reset();
        },
        { once: true }
      );
    });
  });

  // Delete Package
  document.querySelectorAll(".delete-package").forEach((button) => {
    button.addEventListener("click", function () {
      const packageId = this.dataset.id;
      if (confirm("Are you sure you want to delete this package?")) {
        fetch(`/api/packages/${packageId}/`, {
          method: "DELETE",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
        })
          .then((response) => {
            if (response.ok) {
              location.reload();
            } else {
              throw new Error("Failed to delete package");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            showToast(error.message, "error");
          });
      }
    });
  });
});
