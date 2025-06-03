// Function to get CSRF token from cookies
function getCookie(name) {
  console.log("Getting cookie:", name);
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
  console.log("Cookie value:", cookieValue);
  return cookieValue;
}

// Function to show toast notifications
function showToast(message, type = "info") {
  const toastContainer =
    document.querySelector(".toast-container") || createToastContainer();
  const toast = document.createElement("div");
  toast.className = `toast show bg-${
    type === "error" ? "danger" : type === "success" ? "success" : "info"
  } text-white`;
  toast.setAttribute("role", "alert");
  toast.setAttribute("aria-live", "assertive");
  toast.setAttribute("aria-atomic", "true");

  toast.innerHTML = `
    <div class="toast-header bg-${
      type === "error" ? "danger" : type === "success" ? "success" : "info"
    } text-white">
      <i class="fas fa-${
        type === "error"
          ? "exclamation-circle"
          : type === "success"
          ? "check-circle"
          : "info-circle"
      } me-2"></i>
      <strong class="me-auto">Notification</strong>
      <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">
      ${message}
    </div>
  `;

  toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 5000);
}

// Function to create toast container if it doesn't exist
function createToastContainer() {
  const container = document.createElement("div");
  container.className = "toast-container position-fixed top-0 end-0 p-3";
  container.style.zIndex = "11";
  document.body.appendChild(container);
  return container;
}

// Function to convert duration to minutes
function convertToMinutes(value, unit) {
  const numValue = parseInt(value);
  switch (unit) {
    case "days":
      return numValue * 24 * 60;
    case "hours":
      return numValue * 60;
    case "minutes":
      return numValue;
    default:
      return numValue;
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

// Initialize packages functionality when the document is ready
document.addEventListener("DOMContentLoaded", function () {
  console.log("Initializing packages functionality...");
  setupEventListeners();
});

function setupEventListeners() {
  console.log("Setting up event listeners...");
  const packageForm = document.getElementById("packageForm");
  const addPackageModal = document.getElementById("addPackageModal");
  const savePackageBtn = document.getElementById("savePackage");

  console.log("Elements found:", {
    packageForm: !!packageForm,
    addPackageModal: !!addPackageModal,
    savePackageBtn: !!savePackageBtn,
  });

  // Only set up listeners if the package form exists on the page
  if (packageForm && addPackageModal) {
    const modalTitle = addPackageModal.querySelector(".modal-title");
    const savePackageBtn = addPackageModal.querySelector("#savePackage");

    // Function to handle package save/update
    function handlePackageSave() {
      console.log("Save button clicked");
      const formData = new FormData(packageForm);
      const packageId = packageForm.dataset.packageId;

      // Get duration value and unit
      const durationValue = formData.get("duration_value");
      const durationUnit = formData.get("duration_unit");

      console.log("Form data:", {
        price: formData.get("price"),
        durationValue,
        durationUnit,
        packageId,
      });

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

      console.log("Making request:", { url, method, packageData });

      // Get the CSRF token
      const csrftoken = getCookie("csrftoken");
      if (!csrftoken) {
        showToast("CSRF token not found. Please refresh the page.", "error");
        return;
      }

      fetch(url, {
        method: method,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        credentials: "same-origin",
        body: JSON.stringify(packageData),
      })
        .then((response) => {
          console.log("Response status:", response.status);
          if (!response.ok) {
            return response.json().then((data) => {
              throw new Error(
                data.detail || data.error || "Failed to save package"
              );
            });
          }
          return response.json();
        })
        .then((data) => {
          console.log("Success response:", data);
          showToast(
            `Package ${packageId ? "updated" : "created"} successfully`,
            "success"
          );
          location.reload();
        })
        .catch((error) => {
          console.error("Error:", error);
          showToast(
            error.message || "An error occurred while saving the package",
            "error"
          );
        });
    }

    // Save Package button click handler
    if (savePackageBtn) {
      console.log("Found savePackageBtn, adding listener.");
      savePackageBtn.addEventListener("click", handlePackageSave);
    } else {
      console.error("Save package button not found!");
    }

    // Reset modal when hidden
    addPackageModal.addEventListener("hidden.bs.modal", function () {
      modalTitle.textContent = "Add New Package";
      savePackageBtn.textContent = "Save Package";
      packageForm.reset();
      delete packageForm.dataset.packageId;
    });

    // Edit Package buttons
    const editButtons = document.querySelectorAll(".edit-package");
    console.log("Edit buttons found:", editButtons.length);
    editButtons.forEach((button) => {
      console.log("Adding listener to edit button:", button);
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
        modalTitle.textContent = "Edit Package";
        savePackageBtn.textContent = "Update Package";

        // Populate the form with existing data
        document.getElementById("packagePrice").value = price;
        document.getElementById("durationValue").value = durationValue;
        document.getElementById("durationUnit").value = durationUnit;
        packageForm.dataset.packageId = packageId;

        // Show the modal using Bootstrap's data attributes
        const modal = new bootstrap.Modal(addPackageModal);
        modal.show();
      });
    });

    // Delete Package buttons
    const deleteButtons = document.querySelectorAll(".delete-package");
    console.log("Delete buttons found:", deleteButtons.length);
    deleteButtons.forEach((button) => {
      console.log("Adding listener to delete button:", button);
      button.addEventListener("click", function () {
        const packageId = this.dataset.id;
        if (confirm("Are you sure you want to delete this package?")) {
          const csrftoken = getCookie("csrftoken");
          if (!csrftoken) {
            showToast(
              "CSRF token not found. Please refresh the page.",
              "error"
            );
            return;
          }

          fetch(`/api/packages/${packageId}/`, {
            method: "DELETE",
            headers: {
              "X-CSRFToken": csrftoken,
            },
            credentials: "same-origin",
          })
            .then((response) => {
              if (!response.ok) {
                throw new Error("Failed to delete package");
              }
              showToast("Package deleted successfully", "success");
              location.reload();
            })
            .catch((error) => {
              console.error("Error:", error);
              showToast(
                error.message || "An error occurred while deleting the package",
                "error"
              );
            });
        }
      });
    });
  } else {
    console.error("Required elements not found:", {
      packageForm: !!packageForm,
      addPackageModal: !!addPackageModal,
    });
  }
}

// Function to refresh the packages list
function refreshPackages() {
  console.log("Refreshing packages...");
  window.location.reload();
}
