import React, { useState } from "react";
import "./HistoryPage.css";
import { useNavigate } from "react-router-dom";

function HistoryPage() {
  const navigate = useNavigate();
  const [selectedDate, setSelectedDate] = useState("");

  // --- Sample dummy history data ---
  const missionData = [
    { date: "2025-02-10", mission: "Harbour Patrol", status: "Completed" },
    { date: "2025-02-11", mission: "Cargo Delivery", status: "Success" },
    { date: "2025-02-11", mission: "Thermal Scan", status: "Completed" }
  ];

  const alertData = [
    { date: "2025-02-10", alert: "Obstacle Detected", level: "High" },
    { date: "2025-02-11", alert: "Low Battery", level: "Medium" },
    { date: "2025-02-11", alert: "GPS Loss", level: "Critical" }
  ];

  // --- Filter by selected date ---
  const filteredMissions = selectedDate
    ? missionData.filter(item => item.date === selectedDate)
    : missionData;

  const filteredAlerts = selectedDate
    ? alertData.filter(item => item.date === selectedDate)
    : alertData;

  // --- CSV Download Function ---
  const downloadCSV = () => {
    const rows = [
      ["Type", "Date", "Description", "Status/Level"],
      ...filteredMissions.map(m => ["Mission", m.date, m.mission, m.status]),
      ...filteredAlerts.map(a => ["Alert", a.date, a.alert, a.level])
    ];

    const csvContent =
      "data:text/csv;charset=utf-8," +
      rows.map(e => e.join(",")).join("\n");

    const encoded = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encoded);
    link.setAttribute("download", "history_report.csv");
    document.body.appendChild(link);
    link.click();
  };

  return (
    <div className="history-container">

      {/* Back Button */}
      <button className="back-btn" onClick={() => navigate(-1)}>← Back</button>

      <h1 className="title">History Overview</h1>

      {/* Date Filter */}
      <div className="filter-section">
        <label>Select Date:</label>
        <input
          type="date"
          className="date-input"
          value={selectedDate}
          onChange={(e) => setSelectedDate(e.target.value)}
        />

        <button className="download-btn" onClick={downloadCSV}>
          Download CSV
        </button>
      </div>

      {/* Mission History Table */}
      <h2 className="section-title">Mission History</h2>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Mission</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filteredMissions.length > 0 ? (
              filteredMissions.map((item, index) => (
                <tr key={index}>
                  <td>{item.date}</td>
                  <td>{item.mission}</td>
                  <td>{item.status}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="3" style={{ textAlign: "center" }}>No Data</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Alerts History Table */}
      <h2 className="section-title">Alerts History</h2>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Alert</th>
              <th>Level</th>
            </tr>
          </thead>
          <tbody>
            {filteredAlerts.length > 0 ? (
              filteredAlerts.map((item, index) => (
                <tr key={index}>
                  <td>{item.date}</td>
                  <td>{item.alert}</td>
                  <td>{item.level}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="3" style={{ textAlign: "center" }}>No Data</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

    </div>
  );
}

export default HistoryPage;
