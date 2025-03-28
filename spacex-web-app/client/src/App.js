import React, { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import './App.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function App() {
  const [launches, setLaunches] = useState([]);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetch('/api/launches')
      .then((res) => res.json())
      .then((data) => setLaunches(data))
      .catch((err) => console.error('Error fetching launches:', err));
  }, []);

  const filteredLaunches = filter === 'all' ? launches : launches.filter((launch) => launch.status === filter);

  // Datos para el gráfico
  const statusCounts = launches.reduce((acc, launch) => {
    acc[launch.status] = (acc[launch.status] || 0) + 1;
    return acc;
  }, {});

  const chartData = {
    labels: ['Success', 'Failed', 'Upcoming'],
    datasets: [
      {
        label: 'Cantidad de Lanzamientos',
        data: [statusCounts.success || 0, statusCounts.failed || 0, statusCounts.upcoming || 0],
        backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56'],
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: { legend: { position: 'top' }, title: { display: true, text: 'Lanzamientos por Estado' } },
  };

  return (
    <div className="App">
      <h1>Lanzamientos de SpaceX</h1>
      <h3>By Jairo Cubillos</h3>
      <div>
        <label>Filtrar por estado: </label>
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">Todos</option>
          <option value="success">Success</option>
          <option value="failed">Failed</option>
          <option value="upcoming">Upcoming</option>
        </select>
      </div>
      <div style={{ margin: '20px 0' }}>
        <Bar data={chartData} options={chartOptions} />
      </div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Misión</th>
            <th>Cohete</th>
            <th>Fecha</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {filteredLaunches.map((launch) => (
            <tr key={launch.launch_id}>
              <td>{launch.launch_id}</td>
              <td>{launch.mission_name}</td>
              <td>{launch.rocket_name}</td>
              <td>{launch.launch_date}</td>
              <td>{launch.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;