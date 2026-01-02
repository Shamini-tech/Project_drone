import React from "react";
import "./MainDashboard.css";
import { useNavigate } from "react-router-dom";
import { 
  FiHome, 
  FiVideo, 
  FiCpu, 
  FiPackage, 
  FiClock, 
  FiPower 
} from "react-icons/fi";

function MainDashboard() {
  const navigate = useNavigate();

  return (
    <div className="main-container">

      {/* Sidebar */}
      <aside className="sidebar">
        <h2 className="logo">DroneOps</h2>

        <nav>
          <ul>

            <li className="active" onClick={() => navigate("/dashboard")}>
              <FiHome /> Dashboard
            </li>

            <li onClick={() => navigate("/live")}>
              <FiVideo /> Live Video
            </li>

            <li onClick={() => navigate("/alerts-ai")}>
              <FiCpu /> AI Alerts
            </li>

            <li onClick={() => navigate("/mission")}>
              <FiPackage /> Mission Control
            </li>

            <li onClick={() => navigate("/cargo")}>
              <FiPackage /> Cargo Management
            </li>

            <li onClick={() => navigate("/history")}>
              <FiClock /> History
            </li>

          </ul>
        </nav>

        <button className="logout" onClick={() => navigate("/")}>
          <FiPower /> Logout
        </button>
      </aside>

      {/* Main Content */}
      <main className="content">

        <div className="topbar">
          <div>
            <h1>Dashboard</h1>
            <p>Real-time drone monitoring and operations control</p>
          </div>
        </div>

        {/* Status Cards */}
        <section className="status-section">
          <div className="status-card">
            <h3>Battery</h3>
            <p>82%</p>
          </div>

          <div className="status-card">
            <h3>GPS</h3>
            <p>Connected</p>
          </div>

          <div className="status-card">
            <h3>Altitude</h3>
            <p>12.5 m</p>
          </div>

          <div className="status-card">
            <h3>Speed</h3>
            <p>3.2 m/s</p>
          </div>
        </section>

        {/* Quick Actions */}
        <h2 className="section-title">Quick Actions</h2>

        <div className="actions">
          <button className="action-btn green">Take Off</button>
          <button className="action-btn red">Land</button>
          <button className="action-btn blue">Return Home</button>
        </div>

        {/* Map */}
        <h2 className="section-title">Harbour Map</h2>
        <div className="map-panel">Map Loading...</div>

      </main>
    </div>
  );
}

export default MainDashboard;
