import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Signup.css";

function Signup() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    email: "",
    role: "",
    idCard: null,
    password: "",
  });

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    setForm({
      ...form,
      [name]: files ? files[0] : value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Account created successfully!");
    navigate("/");
  };

  return (
    <div className="signup-container">
      <form className="signup-box" onSubmit={handleSubmit}>
        <h2>Create New Account</h2>

        <input
          type="text"
          name="username"
          placeholder="Enter Username"
          value={form.username}
          onChange={handleChange}
          required
        />

        <input
          type="email"
          name="email"
          placeholder="Enter Email"
          value={form.email}
          onChange={handleChange}
          required
        />

        {/* Updated Role Dropdown */}
        <select name="role" value={form.role} onChange={handleChange} required>
          <option value="">Select Role</option>
          <option value="Operator">Operator</option>
          <option value="User">User</option>
        </select>

        <label className="upload-label">Upload ID Card (PNG)</label>
        <input type="file" name="idCard" accept="image/png" onChange={handleChange} required />

        <input
          type="password"
          name="password"
          placeholder="Create Password"
          value={form.password}
          onChange={handleChange}
          required
        />

        <button type="submit">Create Account</button>

        <p className="login-link" onClick={() => navigate("/")}>
          Already have an account? Login
        </p>
      </form>
    </div>
  );
}

export default Signup;
