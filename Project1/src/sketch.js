let grid;
let cellWidth, cellHeight;
let rows = 0, cols = 0; 
let previousCsvIndex = -1;
let currentGridIndex = 0;
let timeInterval = 10000; 
let randomnessFactor = 0.2; 
let frameSpeed = 60;
let gridLoaded = false;

function preload() {
  loadStrings('../data/grids/csv_list.txt', function(lines) {
    csvFiles = lines.map(fileName => `../data/grids/${fileName}`);
    loadNextGrid();
  });
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  lastSwitchTime = millis();
  frameRate(frameSpeed);
}

function adjustCellSize() {
  if (rows > 0 && cols > 0) {
    cellWidth = width / cols;
    cellHeight = height / rows;
  }
}

function deepCopyGrid(grid) {
  return grid.map(row => row.slice());
}

function draw() {
  background(255);

  if (!gridLoaded || !grid || rows === 0 || cols === 0) {
    return;
  }

  adjustCellSize();

  let newGrid = deepCopyGrid(grid);

  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      let x = j * cellWidth;
      let y = i * cellHeight;

      let aliveNeighbors = countAliveNeighbors(i, j);
      let randomFactor = random(1);

      if (grid[i][j] == 1) {
        if ((aliveNeighbors < 2 || aliveNeighbors > 3) && randomFactor > randomnessFactor) {
          newGrid[i][j] = 0;
        }
      } else {
        if (aliveNeighbors == 3 && randomFactor > randomnessFactor) {
          newGrid[i][j] = 1;
        }
      }

      if (newGrid[i][j] == 1) {
        fill(0);
      } else {
        fill(255);
      }
      stroke(200);
      rect(x, y, cellWidth, cellHeight);
    }
  }

  grid = newGrid;

  if (millis() - lastSwitchTime > timeInterval) {
    loadNextGrid();
    lastSwitchTime = millis();
  }
}

function loadNextGrid() {
  gridLoaded = false; 

  let nextIndex;
  do {
    nextIndex = Math.floor(random(0, csvFiles.length));
  } while (nextIndex === previousCsvIndex);

  previousCsvIndex = nextIndex; 
  currentGridIndex = nextIndex;

  loadTable(csvFiles[currentGridIndex], 'csv', (table) => {
    grid = [];
    rows = table.getRowCount();
    cols = table.getColumnCount();

    if (rows === 0 || cols === 0) {
      console.error('CSV file is empty or malformed:', csvFiles[currentGridIndex]);
      return;
    }

    for (let i = 0; i < rows; i++) {
      let row = [];
      for (let j = 0; j < cols; j++) {
        row.push(parseInt(table.get(i, j)));
      }
      grid.push(row);
    }

    gridLoaded = true;
    adjustCellSize();
  }, (error) => {
    console.error('Error loading CSV:', error);
    gridLoaded = false;
  });
}

function countAliveNeighbors(x, y) {
  let aliveCount = 0;

  for (let i = -1; i <= 1; i++) {
    for (let j = -1; j <= 1; j++) {
      if (i == 0 && j == 0) {
        continue;
      }

      let row = (x + i + rows) % rows;
      let col = (y + j + cols) % cols;

      aliveCount += grid[row][col];
    }
  }

  return aliveCount;
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
  adjustCellSize();
  redraw();
}
