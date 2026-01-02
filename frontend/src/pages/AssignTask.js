import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./AssignTask.css";
import { FiArrowLeft, FiCheckCircle, FiXCircle } from "react-icons/fi";

function AssignTask() {
  const navigate = useNavigate();

  const [taskList, setTaskList] = useState([]);
  const [form, setForm] = useState({
    type: "",
    weight: "",
    pickup: "",
    drop: "",
    date: "",
    time: "",
    ampm: "AM",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const newTask = {
      id: Date.now(),
      ...form,
      status: "Pending",
    };

    setTaskList([newTask, ...taskList]);

    // Reset fields
    setForm({
      type: "",
      weight: "",
      pickup: "",
      drop: "",
      date: "",
      time: "",
      ampm: "AM",
    });
  };

  return (
    <div className="assign-container">

      {/* Back Button */}
      <button className="back-btn" onClick={() => navigate("/user-dashboard")}>
        <FiArrowLeft /> Back
      </button>

      {/* Page Header */}
      <div className="assign-header">
        <h1>Assign Task</h1>
        <p>Fill the details to request a cargo delivery</p>
      </div>

      {/* Form */}
      <form className="assign-form" onSubmit={handleSubmit}>

        <div className="form-row">
          <label>Cargo Type</label>
          <input 
            type="text" 
            name="type" 
            value={form.type}
            onChange={handleChange}
            placeholder="Eg: Medical Supplies"
            required 
          />
        </div>

        <div className="form-row">
          <label>Weight (kg)</label>
          <input 
            type="number" 
            name="weight"
            value={form.weight}
            onChange={handleChange}
            placeholder="Eg: 2.5"
            required 
          />
        </div>

        <div className="form-row">
          <label>Pickup Location</label>
          <input 
            type="text" 
            name="pickup"
            value={form.pickup}
            onChange={handleChange}
            placeholder="Eg: Zone A - Dock 3"
            required 
          />
        </div>

        <div className="form-row">
          <label>Drop Location</label>
          <input 
            type="text" 
            name="drop"
            value={form.drop}
            onChange={handleChange}
            placeholder="Eg: Storage Yard 2"
            required 
          />
        </div>

        <div className="date-time-row">
          <div>
            <label>Date</label>
            <input 
              type="date" 
              name="date"
              value={form.date}
              onChange={handleChange}
              required 
            />
          </div>

          <div>
            <label>Time</label>
            <input 
              type="time" 
              name="time"
              value={form.time}
              onChange={handleChange}
              required 
            />
          </div>

          <div>
            <label>AM/PM</label>
            <select name="ampm" value={form.ampm} onChange={handleChange}>
              <option>AM</option>
              <option>PM</option>
            </select>
          </div>
        </div>

        {/* Buttons */}
        <div className="buttons-row">
          <button type="submit" className="submit-btn">
            <FiCheckCircle /> Submit
          </button>

          <button 
            type="button" 
            className="cancel-btn"
            onClick={() => navigate("/user-dashboard")}
          >
            <FiXCircle /> Cancel
          </button>
        </div>
      </form>

      {/* Task List Section */}
      <div className="task-list-container">
        <h2>Assigned Tasks</h2>

        {taskList.length === 0 && (
          <p className="no-tasks">No tasks assigned yet.</p>
        )}

        <ul className="task-list">
          {taskList.map((task) => (
            <li key={task.id} className="task-item">
              <div>
                <strong>{task.type}</strong> — {task.weight} kg  
                <br />
                <span>{task.pickup} ➜ {task.drop}</span>
                <br />
                <small>{task.date} | {task.time} {task.ampm}</small>
              </div>
              
              <span className={`status ${task.status.toLowerCase()}`}>
                {task.status}
              </span>
            </li>
          ))}
        </ul>

      </div>

    </div>
  );
}

export default AssignTask;
