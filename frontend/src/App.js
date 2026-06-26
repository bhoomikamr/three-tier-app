import React, { useState, useEffect } from 'react';

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  // In production, this URL is injected via Nginx config or Environment variables
  const API_URL = window._env_?.API_URL || "http://localhost:5000/api/v1/tasks";

  useEffect(() => {
    fetch(API_URL)
      .then(res => res.json())
      .then(data => setTasks(data))
      .catch(err => console.error("Error fetching tasks:", err));
  }, [API_URL]);

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title })
    })
    .then(res => res.json())
    .then(newTask => {
      setTasks([...tasks, newTask]);
      setTitle('');
    });
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial' }}>
      <h2>Production Task Dashboard</h2>
      <form onSubmit={handleSubmit}>
        <input 
          value={title} 
          onChange={(e) => setTitle(e.target.value)} 
          placeholder="Enter new critical task..." 
          required 
          style={{ padding: '8px', width: '250px' }}
        />
        <button type="submit" style={{ padding: '8px 15px', marginLeft: '10px' }}>Submit</button>
      </form>
      <h3>Active System Sync Tasks:</h3>
      <ul>
        {tasks.map(t => (
          <li key={t.id}><strong>{t.title}</strong> - Status: <i>{t.status}</i></li>
        ))}
      </ul>
    </div>
  );
}

export default App;