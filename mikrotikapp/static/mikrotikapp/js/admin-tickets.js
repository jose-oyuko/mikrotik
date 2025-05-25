// Initialize tickets functionality when the document is ready
document.addEventListener("DOMContentLoaded", function () {
  console.log("Initializing tickets functionality...");
  initializeTickets();
  setupEventListeners();
});

// Global variables
let tickets = [];
let ticketsRefreshInterval;

function initializeTickets() {
  console.log("Loading initial tickets...");
  // Load initial tickets
  loadTickets();

  // Set up auto-refresh every 30 seconds
  ticketsRefreshInterval = setInterval(loadTickets, 30000);
}

function setupEventListeners() {
  console.log("Setting up event listeners...");
  // Search functionality
  const searchInput = document.getElementById("ticketSearch");
  if (searchInput) {
    searchInput.addEventListener("input", filterTickets);
  }

  // Status filter
  const statusFilter = document.getElementById("ticketStatusFilter");
  if (statusFilter) {
    statusFilter.addEventListener("change", filterTickets);
  }

  // Period filter
  const periodFilter = document.getElementById("ticketPeriodFilter");
  if (periodFilter) {
    periodFilter.addEventListener("change", filterTickets);
  }
}

function loadTickets() {
  console.log("Fetching tickets from API...");
  const csrfToken = getCookie("csrftoken");
  console.log("CSRF Token:", csrfToken ? "Present" : "Missing");

  fetch("/api/tickets/", {
    method: "GET",
    headers: {
      "X-CSRFToken": csrfToken,
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    credentials: "include", // This ensures cookies are sent with the request
  })
    .then((response) => {
      console.log("API Response status:", response.status);
      console.log(
        "API Response headers:",
        Object.fromEntries(response.headers.entries())
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      console.log("Received tickets data:", data);
      if (Array.isArray(data)) {
        tickets = data;
        updateTicketsTable(data);
      } else {
        console.error("Received data is not an array:", data);
        showToast("Invalid data format received", "error");
      }
    })
    .catch((error) => {
      console.error("Error loading tickets:", error);
      console.error("Error details:", {
        message: error.message,
        stack: error.stack,
      });
      showToast("Failed to load tickets: " + error.message, "error");
    });
}

function updateTicketsTable(tickets) {
  console.log("Updating tickets table with data:", tickets);
  const tableBody = document.getElementById("ticketsTableBody");
  if (!tableBody) {
    console.error("Tickets table body not found!");
    return;
  }

  tableBody.innerHTML = "";

  tickets.forEach((ticket) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>${ticket.ticketUsername}</td>
            <td>${ticket.ticketPassword}</td>
            <td>${ticket.ticketPeriod} Minutes</td>
            <td>
                <span class="badge ${ticket.used ? "bg-danger" : "bg-success"}">
                    ${ticket.used ? "Used" : "Available"}
                </span>
            </td>
            <td>${formatDateTime(ticket.created_at)}</td>
            <td>
                <button class="btn btn-sm btn-info" onclick="viewTicket(${
                  ticket.id
                })">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteTicket(${
                  ticket.id
                })">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
    tableBody.appendChild(row);
  });
}

function showCreateTicketModal() {
  console.log("Showing create ticket modal...");
  const modal = new bootstrap.Modal(
    document.getElementById("createTicketModal")
  );
  modal.show();
}

function createTicket() {
  console.log("Creating new ticket...");
  const period = document.getElementById("ticketPeriod").value;
  if (!period) {
    showToast("Please enter a period", "error");
    return;
  }

  fetch("/api/tickets/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ ticketPeriod: period }),
  })
    .then((response) => {
      console.log("Create ticket response status:", response.status);
      return response.json();
    })
    .then((data) => {
      console.log("Create ticket response data:", data);
      const modal = bootstrap.Modal.getInstance(
        document.getElementById("createTicketModal")
      );
      modal.hide();
      showToast("Ticket created successfully");
      loadTickets();
    })
    .catch((error) => {
      console.error("Error creating ticket:", error);
      showToast("Failed to create ticket", "error");
    });
}

function viewTicket(ticketId) {
  console.log("Viewing ticket:", ticketId);
  const ticket = tickets.find((t) => t.id === ticketId);
  if (!ticket) {
    console.error("Ticket not found:", ticketId);
    return;
  }

  document.getElementById("viewTicketUsername").value = ticket.ticketUsername;
  document.getElementById("viewTicketPassword").value = ticket.ticketPassword;
  document.getElementById(
    "viewTicketPeriod"
  ).value = `${ticket.ticketPeriod} Minutes`;
  document.getElementById("viewTicketStatus").value = ticket.used
    ? "Used"
    : "Available";

  const modal = new bootstrap.Modal(document.getElementById("viewTicketModal"));
  modal.show();
}

function deleteTicket(ticketId) {
  console.log("Deleting ticket:", ticketId);
  if (!confirm("Are you sure you want to delete this ticket?")) return;

  fetch(`/api/tickets/${ticketId}/`, {
    method: "DELETE",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => {
      console.log("Delete ticket response status:", response.status);
      if (response.ok) {
        showToast("Ticket deleted successfully");
        loadTickets();
      } else {
        throw new Error("Failed to delete ticket");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      showToast("Failed to delete ticket", "error");
    });
}

function toggleTicketStatus(ticketId) {
  console.log("Toggling ticket status:", ticketId);
  const ticket = tickets.find((t) => t.id === ticketId);
  if (!ticket) {
    console.error("Ticket not found:", ticketId);
    return;
  }

  fetch(`/api/tickets/${ticketId}/`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ used: !ticket.used }),
  })
    .then((response) => {
      console.log("Toggle status response status:", response.status);
      return response.json();
    })
    .then((data) => {
      console.log("Toggle status response data:", data);
      showToast("Ticket status updated successfully");
      loadTickets();
    })
    .catch((error) => {
      console.error("Error:", error);
      showToast("Failed to update ticket status", "error");
    });
}

function copyToClipboard(elementId) {
  console.log("Copying to clipboard:", elementId);
  const element = document.getElementById(elementId);
  const value = element.value;
  const formattedText = `"${elementId
    .replace("viewTicket", "ticket")
    .toLowerCase()}": "${value}"`;

  // Create a temporary textarea element
  const textarea = document.createElement("textarea");
  textarea.value = formattedText;
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);

  showToast("Copied to clipboard");
}

function copyTicketToDashboard() {
  console.log("Copying ticket to dashboard...");
  const username = document.getElementById("viewTicketUsername").value;
  const password = document.getElementById("viewTicketPassword").value;

  const formattedText = `Username: ${username},\n Password: ${password}`;

  // Create a temporary textarea element
  const textarea = document.createElement("textarea");
  textarea.value = formattedText;
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);

  showToast("Credentials copied to clipboard");
  const modal = bootstrap.Modal.getInstance(
    document.getElementById("viewTicketModal")
  );
  modal.hide();
}

function filterTickets() {
  console.log("Filtering tickets...");
  const searchTerm = document
    .getElementById("ticketSearch")
    .value.toLowerCase();
  const statusFilter = document.getElementById("ticketStatusFilter").value;
  const periodFilter = document.getElementById("ticketPeriodFilter").value;

  const filteredTickets = tickets.filter((ticket) => {
    const matchesSearch =
      ticket.ticketUsername.toLowerCase().includes(searchTerm) ||
      ticket.ticketPassword.toLowerCase().includes(searchTerm);

    const matchesStatus =
      statusFilter === "all" ||
      (statusFilter === "used" && ticket.used) ||
      (statusFilter === "unused" && !ticket.used);

    const matchesPeriod =
      periodFilter === "all" || ticket.ticketPeriod === periodFilter;

    return matchesSearch && matchesStatus && matchesPeriod;
  });

  updateTicketsTable(filteredTickets);
}

function refreshTickets() {
  console.log("Manually refreshing tickets...");
  loadTickets();
}

function formatDateTime(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString();
}

function showToast(message, type = "success") {
  console.log("Showing toast:", message, type);
  const toast = document.getElementById("successToast");
  const toastMessage = document.getElementById("successToastMessage");

  if (toast && toastMessage) {
    toastMessage.textContent = message;
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
  }
}

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
