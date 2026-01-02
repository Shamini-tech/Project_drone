import React from "react";
import { useNavigate } from "react-router-dom";
import "./UserDashboard.css";
import { FiArrowLeft, FiPlusCircle, FiList, FiClock } from "react-icons/fi";

function UserDashboard() {
  const navigate = useNavigate();

  return (
    <div className="user-dashboard-container">

      {/* Logout / Back Button */}
      <button className="back-btn" onClick={() => navigate("/")}>
        <FiArrowLeft className="back-icon" /> Logout
      </button>

      {/* Header */}
      <div className="header">
        <h1>User Dashboard</h1>
        <p>Manage and track your assigned deliveries</p>
      </div>

      {/* Action Cards */}
      <div className="card-grid">

        <div className="dashboard-card" onClick={() => navigate("/assign-task")}>
          <FiPlusCircle className="icon" />
          <h3>Assign Task</h3>
          <p>Request pickup & delivery tasks</p>
        </div>

        <div className="dashboard-card" onClick={() => navigate("/user-status")}>
          <FiList className="icon" />
          <h3>Task Status</h3>
          <p>Track real-time progress</p>
        </div>

        <div className="dashboard-card" onClick={() => navigate("/user-history")}>
          <FiClock className="icon" />
          <h3>History</h3>
          <p>View past completed tasks</p>
        </div>

      </div>

    </div>
  );
}

export default UserDashboard;
