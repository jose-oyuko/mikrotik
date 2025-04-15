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

// Function to convert duration to minutes
function convertToMinutes(value, unit) {
  switch (unit) {
    case "minutes":
      return parseInt(value);
    case "hours":
      return parseInt(value) * 60;
    case "days":
      return parseInt(value) * 60 * 24;
    default:
      return parseInt(value);
  }
}

// Function to convert minutes to human readable format
function minutesToHumanReadable(minutes) {
  if (minutes % (24 * 60) === 0) {
    return `${minutes / (24 * 60)} days`;
  } else if (minutes % 60 === 0) {
    return `${minutes / 60} hours`;
  } else {
    return `${minutes} minutes`;
  }
}

// Initialize package CRUD operations
document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("addPackageModal");
  const modalTitle = document.getElementById("modalTitle");
  const savePackageBtn = document.getElementById("savePackage");
  const packageForm = document.getElementById("packageForm");

  // Function to handle package save/update
  function handlePackageSave() {
    const formData = new FormData(packageForm);
    const packageId = packageForm.dataset.packageId;

    // Get duration value and unit
    const durationValue = formData.get("duration_value");
    const durationUnit = formData.get("duration_unit");

    // Convert to minutes
    const periodInMinutes = convertToMinutes(durationValue, durationUnit);

    const packageData = {
      price: formData.get("price"),
      period_in_minutes: periodInMinutes,
    };

    // Validate that duration is provided
    if (!durationValue) {
      showToast("Please provide duration", "error");
      return;
    }

    const url = packageId ? `/api/packages/${packageId}/` : "/api/packages/";
    const method = packageId ? "PUT" : "POST";

    fetch(url, {
      method: method,
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
  }

  // Save Package
  if (savePackageBtn) {
    savePackageBtn.addEventListener("click", handlePackageSave);
  }

  // Edit Package
  document.querySelectorAll(".edit-package").forEach((button) => {
    button.addEventListener("click", function () {
      const packageId = this.dataset.id;
      const price = this.dataset.price;
      const minutes = this.dataset.minutes;

      // Convert minutes to the most appropriate unit
      let durationValue, durationUnit;
      if (minutes % (24 * 60) === 0) {
        durationValue = minutes / (24 * 60);
        durationUnit = "days";
      } else if (minutes % 60 === 0) {
        durationValue = minutes / 60;
        durationUnit = "hours";
      } else {
        durationValue = minutes;
        durationUnit = "minutes";
      }

      // Update modal title
      modal.querySelector(".modal-title").textContent = "Edit Package";
      savePackageBtn.textContent = "Update Package";

      // Populate the form with existing data
      document.getElementById("packagePrice").value = price;
      document.getElementById("durationValue").value = durationValue;
      document.getElementById("durationUnit").value = durationUnit;
      packageForm.dataset.packageId = packageId;

      // Show the modal
      const modalInstance = new bootstrap.Modal(modal);
      modalInstance.show();
    });
  });

  // Reset modal when hidden
  modal.addEventListener("hidden.bs.modal", function () {
    modal.querySelector(".modal-title").textContent = "Add New Package";
    savePackageBtn.textContent = "Save Package";
    packageForm.reset();
    delete packageForm.dataset.packageId;
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
