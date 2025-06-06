(function () {
  document.addEventListener("DOMContentLoaded", function () {
    // Initialize commands functionality
    initializeCommands();
  });

  let commandsRefreshInterval = null;

  function initializeCommands() {
    // Load initial commands
    loadCommands();

    // Add event listener for refresh button
    const refreshButton = document.getElementById("refresh-commands");
    if (refreshButton) {
      refreshButton.addEventListener("click", loadCommands);
    }

    // Add event listener for save button in modal
    const saveButton = document.getElementById("save-command");
    if (saveButton) {
      saveButton.addEventListener("click", saveCommand);
    }

    // Add event listener for tab changes
    const commandsTab = document.getElementById("commands-tab");
    if (commandsTab) {
      commandsTab.addEventListener("shown.bs.tab", function (e) {
        // Start auto-refresh when commands tab is shown
        startAutoRefresh();
      });

      commandsTab.addEventListener("hidden.bs.tab", function (e) {
        // Stop auto-refresh when commands tab is hidden
        stopAutoRefresh();
      });

      // If commands tab is active on page load, start auto-refresh
      if (commandsTab.classList.contains("active")) {
        startAutoRefresh();
      }
    }
  }

  function startAutoRefresh() {
    // Clear any existing interval
    stopAutoRefresh();
    // Start new interval
    commandsRefreshInterval = setInterval(loadCommands, 30000);
  }

  function stopAutoRefresh() {
    if (commandsRefreshInterval) {
      clearInterval(commandsRefreshInterval);
      commandsRefreshInterval = null;
    }
  }

  function loadCommands() {
    // Fetch commands from the server
    fetch("/api/commands/list/")
      .then((response) => response.json())
      .then((data) => {
        // Handle both array response and object with commands property
        const commands = Array.isArray(data) ? data : data.commands || [];
        updateCommandsTable(commands);
      })
      .catch((error) => {
        console.error("Error loading commands:", error);
        showError("Failed to load commands");
      });
  }

  function updateCommandsTable(commands) {
    const tbody = document.querySelector("#commands-table tbody");
    tbody.innerHTML = "";

    // Update total count
    document.getElementById(
      "total-commands"
    ).textContent = `Total: ${commands.length}`;

    if (commands.length === 0) {
      tbody.innerHTML =
        '<tr><td colspan="6" class="text-center">No commands found</td></tr>';
      return;
    }

    commands.forEach((command) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${command.id}</td>
        <td>${command.data.type}</td>
        <td>${formatParameters(command.data.params)}</td>
        <td>${
          command.executed
            ? '<span class="badge bg-success">Executed</span>'
            : '<span class="badge bg-warning">Pending</span>'
        }</td>
        <td>${formatDateTime(command.created_at)}</td>
        <td>
          <button class="btn btn-sm btn-primary edit-command" data-command-id="${
            command.id
          }">
            <i class="fas fa-edit"></i>
          </button>
          <button class="btn btn-sm btn-danger delete-command" data-command-id="${
            command.id
          }">
            <i class="fas fa-trash"></i>
          </button>
        </td>
      `;
      tbody.appendChild(row);
    });

    // Add event listeners for edit and delete buttons
    addCommandButtonListeners();
  }

  function formatParameters(params) {
    try {
      return JSON.stringify(params, null, 2);
    } catch (e) {
      return params;
    }
  }

  function formatDateTime(dateTimeString) {
    const date = new Date(dateTimeString);
    return date.toLocaleString();
  }

  function addCommandButtonListeners() {
    // Edit button listeners
    document.querySelectorAll(".edit-command").forEach((button) => {
      button.addEventListener("click", function () {
        console.log("Edit button clicked");
        const commandId = this.getAttribute("data-command-id");
        console.log("Command ID:", commandId);
        openEditModal(commandId);
      });
    });

    // Delete button listeners
    document.querySelectorAll(".delete-command").forEach((button) => {
      button.addEventListener("click", function () {
        const commandId = this.getAttribute("data-command-id");
        if (confirm("Are you sure you want to delete this command?")) {
          deleteCommand(commandId);
        }
      });
    });
  }

  function openEditModal(commandId) {
    console.log("Opening edit modal for command:", commandId);
    // Fetch command details
    fetch(`/api/commands/detail/${commandId}/`)
      .then((response) => {
        console.log("Response status:", response.status);
        return response.json();
      })
      .then((command) => {
        console.log("Command data received:", command);
        document.getElementById("command-id").value = command.id;
        document.getElementById("command-type").value = command.data.type;
        document.getElementById("command-params").value = JSON.stringify(
          command.data.params,
          null,
          2
        );

        // Show modal
        const modalElement = document.getElementById("editCommandModal");
        console.log("Modal element:", modalElement);
        const modal = new bootstrap.Modal(modalElement);
        console.log("Modal instance created");
        modal.show();
        console.log("Modal show called");
      })
      .catch((error) => {
        console.error("Error fetching command details:", error);
        showError("Failed to load command details");
      });
  }

  function saveCommand() {
    const commandId = document.getElementById("command-id").value;
    const params = document.getElementById("command-params").value;

    try {
      const parsedParams = JSON.parse(params);

      fetch(`/api/commands/detail/${commandId}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          params: parsedParams,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          // Close modal
          const modal = bootstrap.Modal.getInstance(
            document.getElementById("editCommandModal")
          );
          modal.hide();

          // Refresh commands list
          loadCommands();
          showSuccess("Command updated successfully");
        })
        .catch((error) => {
          console.error("Error updating command:", error);
          showError("Failed to update command");
        });
    } catch (e) {
      showError("Invalid JSON format");
    }
  }

  function deleteCommand(commandId) {
    fetch(`/api/commands/detail/${commandId}/`, {
      method: "DELETE",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => {
        if (response.ok) {
          loadCommands();
          showSuccess("Command deleted successfully");
        } else {
          throw new Error("Failed to delete command");
        }
      })
      .catch((error) => {
        console.error("Error deleting command:", error);
        showError("Failed to delete command");
      });
  }

  function showSuccess(message) {
    // Implement your success notification here
    console.log("Success:", message);
  }

  function showError(message) {
    // Implement your error notification here
    console.error("Error:", message);
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
})();
