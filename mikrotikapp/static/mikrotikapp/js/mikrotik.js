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

// Initialize Mikrotik configuration
document.addEventListener("DOMContentLoaded", function () {
  const mikrotikForm = document.getElementById("mikrotikConfigForm");
  if (mikrotikForm) {
    mikrotikForm.addEventListener("submit", function (e) {
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
          showToast(error.message, "error");
        });
    });
  }
});
