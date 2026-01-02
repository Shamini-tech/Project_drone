import React, { createContext, useState } from "react";

export const TaskContext = createContext();

export const TaskProvider = ({ children }) => {
  const [tasks, setTasks] = useState([]); // All tasks from users
  const [history, setHistory] = useState([]); // Completed / Rejected tasks

  // ----------------------------
  // USER: Create New Task
  // ----------------------------
  const addTask = (newTask) => {
    const taskWithId = {
      id: Date.now(),
      status: "Pending", // Pending → Accepted → In Progress → Completed
      ...newTask,
    };

    setTasks((prev) => [...prev, taskWithId]);
  };

  // ----------------------------
  // OPERATOR: Accept Task
  // ----------------------------
  const acceptTask = (taskId) => {
    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId ? { ...task, status: "Accepted" } : task
      )
    );
  };

  // ----------------------------
  // OPERATOR: Reject Task
  // ----------------------------
  const rejectTask = (taskId) => {
    const rejectedTask = tasks.find((t) => t.id === taskId);

    if (rejectedTask) {
      setHistory((prev) => [
        ...prev,
        { ...rejectedTask, status: "Rejected" },
      ]);
    }

    setTasks((prev) => prev.filter((task) => task.id !== taskId));
  };

  // ----------------------------
  // OPERATOR: Mark In-Progress
  // ----------------------------
  const startDelivery = (taskId) => {
    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId ? { ...task, status: "In Progress" } : task
      )
    );
  };

  // ----------------------------
  // OPERATOR: Mark as Completed
  // ----------------------------
  const completeDelivery = (taskId) => {
    const completedTask = tasks.find((t) => t.id === taskId);

    if (completedTask) {
      setHistory((prev) => [
        ...prev,
        { ...completedTask, status: "Completed" },
      ]);
    }

    setTasks((prev) => prev.filter((task) => task.id !== taskId));
  };

  return (
    <TaskContext.Provider
      value={{
        tasks,
        history,
        addTask,
        acceptTask,
        rejectTask,
        startDelivery,
        completeDelivery,
      }}
    >
      {children}
    </TaskContext.Provider>
  );
};
