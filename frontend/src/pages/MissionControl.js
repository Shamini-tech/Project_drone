import React from "react";
import { useNavigate } from "react-router-dom";
import "./MissionControl.css";
import { FiArrowLeft } from "react-icons/fi";

function MissionControl() {
  const navigate = useNavigate();

  return (
    <div className="mission-container">

      {/* Back Button */}
      <button className="back-btn" onClick={() => navigate("/dashboard")}>
        <FiArrowLeft /> Back
      </button>

      <div className="mission-header">
        <h1>Mission Control</h1>
        <p>Configure and execute drone missions professionally</p>
      </div>

      <div className="mission-panel">
        <div className="mission-card">
          <h3>Start Mission</h3>
          <button className="btn primary">Launch Mission</button>
        </div>

        <div className="mission-card">
          <h3>Waypoint Setup</h3>
          <button className="btn secondary">Add Waypoints</button>
        </div>

        <div className="mission-card">
          <h3>Abort Mission</h3>
          <button className="btn danger">Abort</button>
        </div>
      </div>
    </div>
  );
}

export default MissionControl;
