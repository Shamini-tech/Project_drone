import React from "react";
import { useNavigate } from "react-router-dom";
import "./TaskStatus.css";
import { FiArrowLeft, FiMapPin, FiClock, FiCheckCircle } from "react-icons/fi";

function TaskStatus() {
  const navigate = useNavigate();

  // Temporary sample data, replace with API data later
  const task = {
    id: "TASK-1023",
    type: "Medical Supplies",
    weight: "2.4 kg",
    pickup: "Dock A",
    drop: "Warehouse 7",
    distanceCovered: 3.2,
    totalDistance: 5.0,
    eta: "12 mins",
    status: "In Progress",
  };

  // Calculate progress percentage
  const progress = (task.distanceCovered / task.totalDistance) * 100;

  return (
    <div className="task-status-container">

      {/* Back Button */}
      <button className="back-btn" onClick={() => navigate("/user-dashboard")}>
        <FiArrowLeft /> Back
      </button>

      {/* Header */}
      <div className="header">
        <h1>Task Status</h1>
        <p>Track your current delivery in real time</p>
      </div>

      {/* Status Card */}
      <div className="status-card">

        <div className="row">
          <h2>{task.type}</h2>
          <span className={`status-badge ${task.status.replace(" ", "").toLowerCase()}`}>
            {task.status}
          </span>
        </div>

        <div className="details">
          <p><FiMapPin /> <strong>Pickup:</strong> {task.pickup}</p>
          <p><FiMapPin /> <strong>Drop:</strong> {task.drop}</p>
          <p><FiCheckCircle /> <strong>Weight:</strong> {task.weight}</p>
        </div>

        {/* Progress Bar */}
        <div className="progress-container">
          <label>Distance Covered</label>
          <div className="progress-bar">
            <div className="progress" style={{ width: `${progress}%` }}></div>
          </div>
          <p>{task.distanceCovered} km / {task.totalDistance} km</p>
        </div>

        {/* ETA */}
        <div className="eta-box">
          <FiClock className="eta-icon" />
          <div>
            <h4>Estimated Time of Arrival</h4>
            <p>{task.eta}</p>
          </div>
        </div>

      </div>
    </div>
  );
}

export default TaskStatus;
