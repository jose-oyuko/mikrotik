// Get the modal and form elements
const modal = document.getElementById("packageModal");
const packageForm = document.getElementById("packageForm");
const modalTitle = document.getElementById("modalTitle");

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

// Function to open the add package modal
function openAddModal() {
  document.getElementById("modalTitle").textContent = "Add New Package";
  document.getElementById("packageId").value = "";
  document.getElementById("periodValue").value = "";
  document.getElementById("price").value = "";
  new bootstrap.Modal(document.getElementById("packageModal")).show();
}

// Function to open the edit package modal
function openEditModal(id, period, price) {
  document.getElementById("modalTitle").textContent = "Edit Package";
  document.getElementById("packageId").value = id;
  document.getElementById("periodValue").value = period;
  document.getElementById("price").value = price;
  new bootstrap.Modal(document.getElementById("packageModal")).show();
}

// Function to close the modal
function closeModal() {
  modal.style.display = "none";
}

// Handle form submission
packageForm.addEventListener("submit", async function (e) {
  e.preventDefault();

  const id = document.getElementById("packageId").value;
  const periodValue = parseInt(document.getElementById("periodValue").value);
  const periodUnit = document.getElementById("periodUnit").value;
  const price = parseFloat(document.getElementById("price").value);

  // Convert period to hours
  const periodInHours = periodUnit === "days" ? periodValue * 24 : periodValue;

  const packageData = {
    period_in_hours: periodInHours,
    price: price,
  };

  try {
    const csrfToken = getCookie("csrftoken");
    let response;
    if (id) {
      // Update existing package
      response = await fetch(`/api/packages/${id}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        credentials: "include",
        body: JSON.stringify(packageData),
      });
    } else {
      // Create new package
      response = await fetch("/api/packages/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        credentials: "include",
        body: JSON.stringify(packageData),
      });
    }

    if (response.ok) {
      // Reload the page to show updated data
      window.location.reload();
    } else {
      const data = await response.json();
      alert("Error: " + (data.error || "Failed to save package"));
    }
  } catch (error) {
    alert("Error saving package. Please try again.");
    console.error("Error:", error);
  }
});

// Function to delete a package
function deletePackage(id) {
  if (confirm("Are you sure you want to delete this package?")) {
    fetch(`/api/packages/${id}/`, {
      method: "DELETE",
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
          .value,
      },
    }).then((response) => {
      if (response.ok) {
        location.reload();
      } else {
        alert("Error deleting package");
      }
    });
  }
}

// Close modal when clicking outside
window.addEventListener("click", function (event) {
  if (event.target === modal) {
    closeModal();
  }
});

// Initialize package form submission handler
document.addEventListener("DOMContentLoaded", function () {
  const packageForm = document.getElementById("packageForm");
  if (packageForm) {
    packageForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const id = document.getElementById("packageId").value;
      const url = id ? `/api/packages/${id}/` : "/api/packages/";
      const method = id ? "PUT" : "POST";

      fetch(url, {
        method: method,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
        },
        body: JSON.stringify({
          period_in_hours: document.getElementById("periodValue").value,
          price: document.getElementById("price").value,
        }),
      }).then((response) => {
        if (response.ok) {
          location.reload();
        } else {
          alert("Error saving package");
        }
      });
    });
  }
});

// Package CRUD Operations
document.addEventListener("DOMContentLoaded", function () {
  // Save Package
  document
    .getElementById("savePackage")
    ?.addEventListener("click", function () {
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
          alert(error.message);
        });
    });

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
            alert(error.message);
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
            alert(error.message);
          });
      }
    });
  });

  // Mikrotik Configuration
  document
    .getElementById("mikrotikConfigForm")
    ?.addEventListener("submit", function (e) {
      e.preventDefault();
      const formData = new FormData(this);

      fetch("/api/mikrotik/config/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      })
        .then((response) => {
          if (response.ok) {
            location.reload();
          } else {
            return response.json().then((data) => {
              throw new Error(data.error || "Failed to save configuration");
            });
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert(error.message);
        });
    });
});
