import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { TaskProvider } from "./context/TaskContext";

// Auth pages
import Login from "./components/Login";
import Signup from "./components/Signup";

// Operator pages
import MainDashboard from "./pages/MainDashboard";
import LiveVideo from "./pages/LiveVideo";
import AIAlerts from "./pages/AIAlerts";
import MissionControl from "./pages/MissionControl";
import CargoManagement from "./pages/CargoManagement";
import HistoryPage from "./pages/HistoryPage";

// User pages
import UserDashboard from "./pages/UserDashboard";
import AssignTask from "./pages/AssignTask";
import TaskStatus from "./pages/TaskStatus";
import UserHistory from "./pages/UserHistory";

function App() {
  return (
    <TaskProvider>
      <Router>
        <Routes>

          {/* Authentication */}
          <Route path="/" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          {/* Operator Dashboard System */}
          <Route path="/dashboard" element={<MainDashboard />} />
          <Route path="/live" element={<LiveVideo />} />
          <Route path="/alerts-ai" element={<AIAlerts />} />
          <Route path="/mission" element={<MissionControl />} />
          <Route path="/cargo" element={<CargoManagement />} />
          <Route path="/history" element={<HistoryPage />} />

          {/* User Dashboard System */}
          <Route path="/user-dashboard" element={<UserDashboard />} />
          <Route path="/assign-task" element={<AssignTask />} />
          <Route path="/user-status" element={<TaskStatus />} />
          <Route path="/user-history" element={<UserHistory />} />

        </Routes>
      </Router>
    </TaskProvider>
  );
}

export default App;
