import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LiveVideo.css";
import { FiArrowLeft } from "react-icons/fi";

function LiveVideo() {
  const navigate = useNavigate();
  const [frame, setFrame] = useState(null);
  const wsRef = useRef(null);

  useEffect(() => {
    console.log("Connecting to WebSocket...");

    wsRef.current = new WebSocket("ws://localhost:8000/ws/video");

    wsRef.current.onopen = () => {
      console.log("WebSocket Connected!");
    };

    wsRef.current.onmessage = (event) => {
      // backend must send BASE64 image strings
      setFrame(`data:image/jpeg;base64,${event.data}`);
    };

    wsRef.current.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    wsRef.current.onclose = () => {
      console.log("WebSocket Closed.");
    };

    return () => wsRef.current && wsRef.current.close();
  }, []);

  return (
    <div className="live-container">
      <button className="back-btn" onClick={() => navigate(-1)}>
        <FiArrowLeft /> Back
      </button>

      <h1 className="live-title">Live Drone Video Feed</h1>
      <p className="live-sub">Real-time visual monitoring from deployed drone</p>

      <div className="video-box">
        {frame ? (
          <img src={frame} className="video-feed" alt="Drone Live Feed" />
        ) : (
          <div className="video-placeholder">
            <p>Live Stream Loading...</p>
          </div>
        )}
      </div>

      <div className="status-panel">
        <div className="status-card">Battery: 82%</div>
        <div className="status-card">Signal: Strong</div>
        <div className="status-card">Altitude: 11.4 m</div>
        <div className="status-card">Speed: 3.1 m/s</div>
      </div>
    </div>
  );
}

export default LiveVideo;
