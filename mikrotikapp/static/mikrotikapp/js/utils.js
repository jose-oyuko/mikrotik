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

// Function to show toast notification
function showToast(message, type = "info") {
  const toastContainer = document.createElement("div");
  toastContainer.className = "position-fixed top-0 end-0 p-3";
  toastContainer.style.zIndex = "11";

  const toast = document.createElement("div");
  toast.className = "toast show";
  toast.setAttribute("role", "alert");
  toast.setAttribute("aria-live", "assertive");
  toast.setAttribute("aria-atomic", "true");

  const toastHeader = document.createElement("div");
  toastHeader.className = "toast-header";

  const icon = document.createElement("i");
  icon.className = `fas fa-${
    type === "success"
      ? "check-circle text-success"
      : type === "error"
      ? "exclamation-circle text-danger"
      : "info-circle text-info"
  } me-2`;

  const strong = document.createElement("strong");
  strong.className = "me-auto";
  strong.textContent = "Notification";

  const closeButton = document.createElement("button");
  closeButton.type = "button";
  closeButton.className = "btn-close";
  closeButton.setAttribute("data-bs-dismiss", "toast");
  closeButton.setAttribute("aria-label", "Close");

  const toastBody = document.createElement("div");
  toastBody.className = "toast-body";
  toastBody.textContent = message;

  toastHeader.appendChild(icon);
  toastHeader.appendChild(strong);
  toastHeader.appendChild(closeButton);
  toast.appendChild(toastHeader);
  toast.appendChild(toastBody);
  toastContainer.appendChild(toast);
  document.body.appendChild(toastContainer);

  const bsToast = new bootstrap.Toast(toast, {
    autohide: true,
    delay: 5000,
    animation: true,
  });

  bsToast.show();

  toast.addEventListener("hidden.bs.toast", function () {
    toastContainer.remove();
  });
}
