document.addEventListener("DOMContentLoaded", function () {
  // Initialize dashboard
  initializeDashboard();
});

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
  const totalAmount = transactions.reduce((sum, t) => sum + t.amount, 0);
  document.querySelector("#transactions-total").textContent =
    formatCurrency(totalAmount);
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
