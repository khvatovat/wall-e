import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Grid from './components/Grid';

type Robot = {
  id: number;
  x: number;
  y: number;
  hasTrash: boolean;
};

type Trash = {
  id: number;
  x: number;
  y: number;
};

function App() {
  const [robots, setRobots] = useState<Robot[]>([]);
  const [trash, setTrash] = useState<Trash[]>([]);
  const [base, setBase] = useState<{x: number, y: number}>({x: 0, y: 0});

  const fetchSimulation = () => {
    axios.get('http://127.0.0.1:8000/simulation/')
      .then(response => {
        setRobots(response.data.robots);
        setTrash(response.data.trash);
        setBase(response.data.base);
      })
      .catch(error => console.error(error));
  };

  useEffect(() => {
    fetchSimulation();
  
    const interval = setInterval(() => {
      axios.get('http://127.0.0.1:8000/simulation/')
        .then(response => {
          setRobots(response.data.robots);
          setTrash(response.data.trash);
          setBase(response.data.base);
  
          if (response.data.trash.length === 0) {
            clearInterval(interval);
            console.log("Simulation complete: no trash left.");
          }
        })
        .catch(error => console.error(error));
    }, 500);
  
    return () => clearInterval(interval);
  }, []);

  const startSimulation = () => {
    axios.post('http://127.0.0.1:8000/simulation/start/')
      .then(() => fetchSimulation())
      .catch(error => console.error(error));
  };

  return (
    <div>
      <h1>WALL-E</h1>
      <button onClick={startSimulation}>Start Simulation</button>
      <Grid robots={robots} trash={trash} base={base} />
    </div>
  );
}

export default App;