import React from "react";
import { useNavigate } from "react-router-dom";
import "./AIAlerts.css";
import { FiArrowLeft, FiAlertTriangle } from "react-icons/fi";

function AIAlerts() {
  const navigate = useNavigate();

  return (
    <div className="alerts-container">
      
      {/* Back Button */}
      <button className="back-btn" onClick={() => navigate(-1)}>
        <FiArrowLeft size={18} /> Back
      </button>

      <h1 className="alerts-title">
        <FiAlertTriangle /> AI Alerts
      </h1>

      <p className="subtitle">
        Monitor real-time anomaly detections from onboard AI systems.
      </p>

      <div className="alerts-table">
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Alert Type</th>
              <th>Severity</th>
              <th>Location</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>10:22 AM</td>
              <td>Obstacle Detected</td>
              <td className="high">High</td>
              <td>Port Zone 3</td>
            </tr>

            <tr>
              <td>09:50 AM</td>
              <td>Low Battery Return</td>
              <td className="medium">Medium</td>
              <td>Dock 14</td>
            </tr>

            <tr>
              <td>09:21 AM</td>
              <td>Cargo Secure</td>
              <td className="low">Low</td>
              <td>Loading Bay</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  );
}

export default AIAlerts;
