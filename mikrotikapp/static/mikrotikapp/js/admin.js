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
  modalTitle.textContent = "Add New Package";
  document.getElementById("packageId").value = "";
  document.getElementById("periodValue").value = "";
  document.getElementById("periodUnit").value = "hours";
  document.getElementById("price").value = "";
  modal.style.display = "block";
}

// Function to open the edit package modal
function openEditModal(id, period, price) {
  modalTitle.textContent = "Edit Package";
  document.getElementById("packageId").value = id;

  // Convert hours to days if applicable
  if (period >= 24 && period % 24 === 0) {
    document.getElementById("periodValue").value = period / 24;
    document.getElementById("periodUnit").value = "days";
  } else {
    document.getElementById("periodValue").value = period;
    document.getElementById("periodUnit").value = "hours";
  }

  document.getElementById("price").value = price;
  modal.style.display = "block";
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
async function deletePackage(id) {
  if (!confirm("Are you sure you want to delete this package?")) {
    return;
  }

  try {
    const csrfToken = getCookie("csrftoken");
    const response = await fetch(`/api/packages/${id}/`, {
      method: "DELETE",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      credentials: "include",
    });

    if (response.ok) {
      // Reload the page to show updated data
      window.location.reload();
    } else {
      const data = await response.json();
      alert("Error: " + (data.error || "Failed to delete package"));
    }
  } catch (error) {
    alert("Error deleting package. Please try again.");
    console.error("Error:", error);
  }
}

// Close modal when clicking outside
window.addEventListener("click", function (event) {
  if (event.target === modal) {
    closeModal();
  }
});
