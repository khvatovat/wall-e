import React from 'react';

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

type Props = {
  robots: Robot[];
  trash: Trash[];
  base: { x: number, y: number };
};

const GRID_SIZE = 32;

const Grid: React.FC<Props> = ({ robots, trash , base}) => {
  const getRobotAt = (x: number, y: number) => 
    robots.find(robot => robot.x === x && robot.y === y);

  const hasTrash = (x: number, y: number) =>
    trash.some(t => t.x === x && t.y === y);

  const isBase = (x: number, y: number) =>
    x === base.x && y === base.y;

  const cells = [];
  for (let y = 0; y < GRID_SIZE; y++) {
    for (let x = 0; x < GRID_SIZE; x++) {
      const robotHere = getRobotAt(x, y);
      const trashHere = hasTrash(x, y);

      let bgColor = 'white';
      if (isBase(x, y)) bgColor = 'black';
      else if (robotHere && robotHere.hasTrash) bgColor = 'saddlebrown';    // carrying → brown
      else if (robotHere) bgColor = 'green';
      else if (trashHere) bgColor = 'red';

      cells.push(
        <div key={`${x}-${y}`}
             style={{
               width: 20,
               height: 20,
               backgroundColor: bgColor,
               border: '1px solid #ddd',
               boxSizing: 'border-box'
             }}>
        </div>
      );
    }
  }

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: `repeat(${GRID_SIZE}, 20px)`,
      gridTemplateRows: `repeat(${GRID_SIZE}, 20px)`
    }}>
      {cells}
    </div>
  );
};

export default Grid;