import React, { useState } from "react";
import "./Login.css";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    // Temporary authentication
    if (username === "admin" && password === "1234") {
      if (role === "Operator") {
        navigate("/dashboard");
      } else if (role === "User") {
        navigate("/user-dashboard");
      }
    } else {
      alert("Invalid Login Credentials");
    }
  };

  return (
    <div className="login-container">

      <form className="login-box" onSubmit={handleLogin}>
        <h2>Login</h2>

        <input
          type="text"
          placeholder="Enter Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Enter Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {/* Updated Role Dropdown */}
        <select value={role} onChange={(e) => setRole(e.target.value)} required>
          <option value="">Select Role</option>
          <option value="Operator">Operator</option>
          <option value="User">User</option>
        </select>

        <button type="submit" className="login-btn">
          Login
        </button>

        <p className="signup-text">
          Don't have an account?{" "}
          <span onClick={() => navigate("/signup")}>Signup</span>
        </p>
      </form>
    </div>
  );
}

export default Login;
