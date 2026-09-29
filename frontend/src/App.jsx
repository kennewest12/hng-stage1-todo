import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || "Something went wrong");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

function App() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState("all");
  const [priority, setPriority] = useState("all");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [taskPriority, setTaskPriority] = useState("medium");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [openNotes, setOpenNotes] = useState(null);
  const [notes, setNotes] = useState({});
  const [noteText, setNoteText] = useState("");

  async function loadTasks() {
    setLoading(true);
    setError("");

    try {
      const params = new URLSearchParams();

      if (filter === "active") params.set("completed", "false");
      if (filter === "completed") params.set("completed", "true");
      if (priority !== "all") params.set("priority", priority);

      const data = await request(`/api/v1/tasks?${params.toString()}`);
      setTasks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadTasks();
  }, [filter, priority]);

  async function createTask(event) {
    event.preventDefault();

    if (!title.trim()) return;

    try {
      const task = await request("/api/v1/tasks", {
        method: "POST",
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim() || null,
          priority: taskPriority,
        }),
      });

      setTasks((current) => [task, ...current]);
      setTitle("");
      setDescription("");
      setTaskPriority("medium");
      setError("");
    } catch (err) {
      setError(err.message);
    }
  }

  async function toggleTask(task) {
    try {
      const updated = await request(`/api/v1/tasks/${task.id}/complete`, {
        method: "PATCH",
      });

      setTasks((current) =>
        current.map((item) => (item.id === updated.id ? updated : item)),
      );
    } catch (err) {
      setError(err.message);
    }
  }

  async function loadNotes(taskId) {
    try {
      const data = await request(`/api/v1/tasks/${taskId}/notes`);
      setNotes((current) => ({ ...current, [taskId]: data }));
    } catch (err) {
      setError(err.message);
    }
  }

  async function toggleNotes(taskId) {
    if (openNotes === taskId) {
      setOpenNotes(null);
      return;
    }

    setOpenNotes(taskId);
    setNoteText("");
    await loadNotes(taskId);
  }

  async function addNote(taskId) {
    if (!noteText.trim()) return;

    try {
      const note = await request(`/api/v1/tasks/${taskId}/notes`, {
        method: "POST",
        body: JSON.stringify({ content: noteText.trim() }),
      });
      setNotes((current) => ({
        ...current,
        [taskId]: [...(current[taskId] || []), note],
      }));
      setNoteText("");
    } catch (err) {
      setError(err.message);
    }
  }

  async function deleteNote(taskId, noteId) {
    try {
      await request(`/api/v1/notes/${noteId}`, { method: "DELETE" });
      setNotes((current) => ({
        ...current,
        [taskId]: (current[taskId] || []).filter((note) => note.id !== noteId),
      }));
    } catch (err) {
      setError(err.message);
    }
  }

  async function deleteTask(taskId) {
    try {
      await request(`/api/v1/tasks/${taskId}`, { method: "DELETE" });
      setTasks((current) => current.filter((task) => task.id !== taskId));
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main className="app-shell">
      <section className="app-card">
        <header className="app-header">
          <div>
            <p className="eyebrow">HNG Internship 15</p>
            <h1>My To-Do List</h1>
            <p className="subtitle">
              Keep your tasks organized and track what needs to get done.
            </p>
          </div>
        </header>

        <form className="task-form" onSubmit={createTask}>
          <input
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            placeholder="What needs to be done?"
            aria-label="Task title"
          />
          <textarea
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            placeholder="Add a description (optional)"
            rows="3"
            aria-label="Task description"
          />
          <div className="form-row">
            <select
              value={taskPriority}
              onChange={(event) => setTaskPriority(event.target.value)}
              aria-label="Task priority"
            >
              <option value="low">Low priority</option>
              <option value="medium">Medium priority</option>
              <option value="high">High priority</option>
            </select>
            <button type="submit">Add Task</button>
          </div>
        </form>

        <div className="filters">
          <div className="filter-group">
            {["all", "active", "completed"].map((value) => (
              <button
                className={filter === value ? "filter active" : "filter"}
                key={value}
                type="button"
                onClick={() => setFilter(value)}
              >
                {value[0].toUpperCase() + value.slice(1)}
              </button>
            ))}
          </div>

          <select
            value={priority}
            onChange={(event) => setPriority(event.target.value)}
            aria-label="Filter by priority"
          >
            <option value="all">All priorities</option>
            <option value="low">Low priority</option>
            <option value="medium">Medium priority</option>
            <option value="high">High priority</option>
          </select>
        </div>

        {error && <p className="error">{error}</p>}

        {loading ? (
          <p className="empty-state">Loading tasks...</p>
        ) : tasks.length === 0 ? (
          <p className="empty-state">No tasks found.</p>
        ) : (
          <div className="task-list">
            {tasks.map((task) => (
              <article className={task.completed ? "task completed" : "task"} key={task.id}>
                <div className="task-main">
                  <button
                    className="check-button"
                    type="button"
                    onClick={() => toggleTask(task)}
                    aria-label={task.completed ? "Mark task active" : "Mark task completed"}
                  >
                    {task.completed ? "✓" : ""}
                  </button>
                  <div>
                    <h2>{task.title}</h2>
                    {task.description && <p>{task.description}</p>}
                    <span className={`priority priority-${task.priority}`}>
                      {task.priority}
                    </span>
                  </div>
                </div>
                <button
                  className="delete-button"
                  type="button"
                  onClick={() => deleteTask(task.id)}
                >
                  Delete
                </button>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

export default App;
