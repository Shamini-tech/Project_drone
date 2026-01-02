import React, { useState } from "react";
import { FiArrowLeft, FiDownload } from "react-icons/fi";
import "./UserHistory.css";
import { useNavigate } from "react-router-dom";

function UserHistory() {
  const navigate = useNavigate();

  // Dummy history data
  const allHistory = [
    {
      id: "TASK-001",
      type: "Medical Supplies",
      weight: "2.4 kg",
      pickup: "Warehouse A",
      drop: "Dock 5",
      date: "2025-02-02",
      status: "Completed",
    },
    {
      id: "TASK-002",
      type: "Food Packets",
      weight: "1.2 kg",
      pickup: "Gate 3",
      drop: "Control Room",
      date: "2025-02-03",
      status: "Pending",
    },
    {
      id: "TASK-003",
      type: "Electronic Parts",
      weight: "3.0 kg",
      pickup: "Store B",
      drop: "Dock 2",
      date: "2025-02-03",
      status: "In Progress",
    },
  ];

  const [selectedDate, setSelectedDate] = useState("");

  // Filter tasks based on selected date
  const filteredHistory = selectedDate
    ? allHistory.filter((t) => t.date === selectedDate)
    : allHistory;

  // Download CSV
  const downloadCSV = () => {
    const rows = [
      ["ID", "Type", "Weight", "Pickup", "Drop", "Date", "Status"],
      ...filteredHistory.map((task) => [
        task.id,
        task.type,
        task.weight,
        task.pickup,
        task.drop,
        task.date,
        task.status,
      ]),
    ];

    let csvContent = rows.map((e) => e.join(",")).join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `task_history_${selectedDate || "all"}.csv`;
    link.click();
  };

  return (
    <div className="history-container">

      {/* Back Button */}
      <button className="back-btn" onClick={() => navigate("/user-dashboard")}>
        <FiArrowLeft /> Back
      </button>

      {/* Header */}
      <div className="history-header">
        <h1>Task History</h1>
        <p>View your completed & ongoing tasks</p>
      </div>

      {/* Date Filter */}
      <div className="filter-section">
        <label>Select Date:</label>
        <input
          type="date"
          value={selectedDate}
          onChange={(e) => setSelectedDate(e.target.value)}
        />

        <button className="download-btn" onClick={downloadCSV}>
          <FiDownload /> Download CSV
        </button>
      </div>

      {/* History Table */}
      <div className="history-table-container">
        <table className="history-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Type</th>
              <th>Weight</th>
              <th>Pickup</th>
              <th>Drop</th>
              <th>Date</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {filteredHistory.length > 0 ? (
              filteredHistory.map((task, idx) => (
                <tr key={idx}>
                  <td>{task.id}</td>
                  <td>{task.type}</td>
                  <td>{task.weight}</td>
                  <td>{task.pickup}</td>
                  <td>{task.drop}</td>
                  <td>{task.date}</td>
                  <td className={`status ${task.status.toLowerCase()}`}>
                    {task.status}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="7" className="no-data">
                  No tasks found for selected date
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

    </div>
  );
}

export default UserHistory;
