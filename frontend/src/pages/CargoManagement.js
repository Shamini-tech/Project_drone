import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import "./CargoManagement.css";
import { FiArrowLeft, FiCheckCircle, FiXCircle } from "react-icons/fi";
import { TaskContext } from "../context/TaskContext";

function CargoManagement() {
  const navigate = useNavigate();
  const { tasks, updateTaskStatus } = useContext(TaskContext); // from global context

  return (
    <div className="cargo-operator-container">

      {/* Back Button */}
      <button className="back-btn" onClick={() => navigate("/dashboard")}>
        <FiArrowLeft /> Back
      </button>

      {/* Header */}
      <div className="header">
        <h1>Operator Cargo Management</h1>
        <p>Review and manage user-assigned cargo tasks</p>
      </div>

      {/* TASK TABLE */}
      <div className="task-table-wrapper">
        <table className="task-table">
          <thead>
            <tr>
              <th>Task ID</th>
              <th>User</th>
              <th>Cargo Type</th>
              <th>Weight</th>
              <th>Pickup</th>
              <th>Drop</th>
              <th>Date</th>
              <th>Time</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {tasks.length === 0 ? (
              <tr>
                <td colSpan="10" className="no-data">No tasks assigned yet</td>
              </tr>
            ) : (
              tasks.map((task) => (
                <tr key={task.id}>
                  <td>{task.id}</td>
                  <td>{task.username}</td>
                  <td>{task.cargoType}</td>
                  <td>{task.weight} kg</td>
                  <td>{task.pickupLocation}</td>
                  <td>{task.dropLocation}</td>
                  <td>{task.date}</td>
                  <td>{task.time}</td>

                  {/* STATUS */}
                  <td>
                    <span className={`status-tag ${task.status}`}>
                      {task.status}
                    </span>
                  </td>

                  {/* ACTION BUTTONS */}
                  <td className="action-buttons">
                    {task.status === "Pending" && (
                      <>
                        <button
                          className="accept-btn"
                          onClick={() => updateTaskStatus(task.id, "Approved")}
                        >
                          <FiCheckCircle /> Accept
                        </button>

                        <button
                          className="reject-btn"
                          onClick={() => updateTaskStatus(task.id, "Rejected")}
                        >
                          <FiXCircle /> Reject
                        </button>
                      </>
                    )}

                    {task.status !== "Pending" && (
                      <span className="no-actions">—</span>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

    </div>
  );
}

export default CargoManagement;
