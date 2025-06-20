document.addEventListener("DOMContentLoaded", function () {
  // Initialize dashboard
  // initializeDashboard();
  // Set up event listeners for buttons
  document
    .getElementById("dateTransactions")
    .addEventListener("click", function (e) {
      e.preventDefault();
      getTransactionsByDate();
    });
});

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

function getTransactionsByDate() {
  const startDate = document.getElementById("startDate").value;
  const endDate = document.getElementById("endDate").value;
  const url = `/api/payed_date_range/?start_date=${startDate}&end_date=${endDate}`;
  console.log("Fetching transactions from", startDate, "to", endDate);
  fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      console.log("Transactions data:", data);
      transactions = data.transactions;
      total_amount = data.total_amount;
      updateTransactionsTable(transactions);
      document.getElementById(
        "total_paid"
      ).innerText = `Total: KSH ${total_amount}`;
    }
  });
}

function initializeDashboard() {
  // Load initial data
  loadDashboardData();

  // Set up auto-refresh every 30 seconds
  setInterval(loadDashboardData, 30000);
}

function loadDashboardData() {
  // Fetch dashboard data from the server
  fetch("/api/dashboard/")
    .then((response) => response.json())
    .then((data) => {
      updateTransactionsTable(data.transactions);
      updatePendingPaymentsTable(data.pending_payments);
    })
    .catch((error) => {
      console.error("Error loading dashboard data:", error);
    });
}

function updateTransactionsTable(transactions) {
  const tbody = document.querySelector("#transactions-table tbody");
  tbody.innerHTML = "";

  transactions.forEach((transaction) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>${formatDateTime(transaction.origination_time)}</td>
            <td>${formatCurrency(transaction.amount)}</td>
            <td>${transaction.sender_phone_number}</td>
            <td>${transaction.sender_first_name}</td>
        `;
    tbody.appendChild(row);
  });

  // Update total amount
  // const totalAmount = transactions.reduce((sum, t) => sum + t.amount, 0);
  // document.querySelector("#transactions-total").textContent =
  //   formatCurrency(totalAmount);
}

function updatePendingPaymentsTable(payments) {
  const tbody = document.querySelector("#pending-payments-table tbody");
  tbody.innerHTML = "";

  payments.forEach((payment) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>${formatDateTime(payment.time)}</td>
            <td>${formatCurrency(payment.amount)}</td>
            <td>${payment.phoneNumber}</td>
            <td>${payment.ipAddress}</td>
            <td>${payment.macAddress}</td>
        `;
    tbody.appendChild(row);
  });

  // Update total amount
  const totalAmount = payments.reduce((sum, p) => sum + p.amount, 0);
  document.querySelector("#pending-total").textContent =
    formatCurrency(totalAmount);
}

function formatDateTime(dateTimeString) {
  const date = new Date(dateTimeString);
  return date.toLocaleString();
}

function formatCurrency(amount) {
  return new Intl.NumberFormat("en-KE", {
    style: "currency",
    currency: "KES",
  }).format(amount);
}

function updateActiveSessions() {
  fetch("/api/sessions/active")
    .then((response) => response.json())
    .then((data) => {
      const tbody = document
        .getElementById("active-sessions-table")
        .getElementsByTagName("tbody")[0];
      tbody.innerHTML = "";

      if (data.length === 0) {
        tbody.innerHTML =
          '<tr><td colspan="6" class="text-center">No active sessions</td></tr>';
        return;
      }

      data.forEach((session) => {
        const row = tbody.insertRow();
        row.innerHTML = `
          <td>${session.mac_address}</td>
          <td>${session.phone_number}</td>
          <td>KES ${session.package_amount}</td>
          <td>${new Date(session.starting_time).toLocaleTimeString("en-US", {
            hour: "2-digit",
            minute: "2-digit",
          })}</td>
          <td>${new Date(session.end_time).toLocaleTimeString("en-US", {
            hour: "2-digit",
            minute: "2-digit",
          })}</td>
          <td>${session.period}</td>
        `;
      });
    })
    .catch((error) => {
      console.error("Error fetching active sessions:", error);
      const tbody = document
        .getElementById("active-sessions-table")
        .getElementsByTagName("tbody")[0];
      tbody.innerHTML =
        '<tr><td colspan="6" class="text-center text-danger">Error loading active sessions</td></tr>';
    });
}

// Update active sessions every 30 seconds
setInterval(updateActiveSessions, 30000);

// Initial update
updateActiveSessions();
