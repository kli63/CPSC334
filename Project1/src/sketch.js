let grid;
let nextGrid;
let ageGrid;
let healthGrid;
let agingFactorGrid;
let cellWidth, cellHeight;
let rows = 0, cols = 0; 
let previousCsvIndex = -1;
let currentGridIndex = 0;
let timeInterval = 30000; 
let randomnessFactor = 0.3; 
let frameSpeed = 60;
let inTransition = false;
let transitionDuration = 30000; 
let transitionStartTime = 0;
let transitionComplete = false;

const baseDecayRate = 0.80;
const maxAgingFactor = 0.1;
const additionalDeathChance = 0.3;

function preload() {
  loadStrings('../data/grids/csv_list.txt', function(lines) {
    csvFiles = lines.map(fileName => `../data/grids/${fileName}`);
    loadGrid(true);
  }, (error) => {
    console.error("Error loading CSV list:", error);
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
  if (!grid || !grid.length) return [];
  return grid.map(row => row.slice());
}

function initializeAgeHealthGrids() {
  ageGrid = [];
  healthGrid = [];
  agingFactorGrid = [];

  for (let i = 0; i < rows; i++) {
    let ageRow = [];
    let healthRow = [];
    let agingFactorRow = [];

    for (let j = 0; j < cols; j++) {
      ageRow.push(0);
      healthRow.push(1);
      agingFactorRow.push(0);
    }

    ageGrid.push(ageRow);
    healthGrid.push(healthRow);
    agingFactorGrid.push(agingFactorRow);
  }
}

function draw() {
  adjustCellSize();

  if (!inTransition) {
    playGame();

    if (millis() - lastSwitchTime > timeInterval) {
      startTransition();
    }
  } else {
    transitionBetweenFaces();
  }
}

function playGame() {
  let newGrid = deepCopyGrid(grid);

  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      let x = j * cellWidth;
      let y = i * cellHeight;

      let aliveNeighbors = countAliveNeighbors(i, j);
      let randomFactor = random(1);
      
      let currentHealth = healthGrid[i][j];
      let currentAge = ageGrid[i][j];
      let currentAgingFactor = agingFactorGrid[i][j];

      if (grid[i][j] == 1) {
        ageGrid[i][j]++;
        healthGrid[i][j] *= (baseDecayRate - currentAgingFactor);

        if ((aliveNeighbors < 2 || aliveNeighbors > 3) && randomFactor > (randomnessFactor * currentHealth)) {
          newGrid[i][j] = 0;
          ageGrid[i][j] = 0;
          healthGrid[i][j] = 1;
          agingFactorGrid[i][j] = 0;
        } else {
          let extraDeathChance = random(1);
          if (extraDeathChance < (additionalDeathChance * (1 - currentHealth))) {
            newGrid[i][j] = 0;
            ageGrid[i][j] = 0;
            healthGrid[i][j] = 1;
            agingFactorGrid[i][j] = 0;
          }
        }
      } else {
        if (aliveNeighbors == 3 && randomFactor > 0.05) {
          newGrid[i][j] = 1;
          ageGrid[i][j] = 0;
          healthGrid[i][j] = random(0.9, 1);
          agingFactorGrid[i][j] = random(0, maxAgingFactor);
        }
      }

      fill(newGrid[i][j] == 1 ? 0 : 255);
      stroke(200);
      rect(x, y, cellWidth, cellHeight);
    }
  }

  grid = newGrid;
}

function startTransition() {
  inTransition = true;
  transitionComplete = false;
  transitionStartTime = millis();
  loadGrid(false); 
}

function transitionBetweenFaces() {
  if (!nextGrid || nextGrid.length === 0) {
    console.error("Next grid not loaded yet!");
    return;
  }

  let newGrid = deepCopyGrid(grid);
  transitionComplete = true;

  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      if (newGrid[i][j] !== nextGrid[i][j] && random(1) < 0.05) { 
        newGrid[i][j] = nextGrid[i][j];
      }

      if (newGrid[i][j] !== nextGrid[i][j]) {
        transitionComplete = false;
      }

      let x = j * cellWidth;
      let y = i * cellHeight;
      fill(newGrid[i][j] == 1 ? 0 : 255);
      stroke(200);
      rect(x, y, cellWidth, cellHeight);
    }
  }

  grid = newGrid;

  if (transitionComplete || (millis() - transitionStartTime) > transitionDuration) {
    inTransition = false;
    lastSwitchTime = millis();
    initializeAgeHealthGrids();
  }
}

function loadGrid(isInitial) {
  let nextIndex;
  do {
    nextIndex = Math.floor(random(0, csvFiles.length));
  } while (nextIndex === previousCsvIndex);

  previousCsvIndex = nextIndex;

  loadTable(csvFiles[nextIndex], 'csv', (table) => {
    let tempGrid = [];
    rows = table.getRowCount();
    cols = table.getColumnCount();

    for (let i = 0; i < rows; i++) {
      let row = [];
      for (let j = 0; j < cols; j++) {
        row.push(parseInt(table.get(i, j)));
      }
      tempGrid.push(row);
    }

    if (isInitial) {
      grid = tempGrid;
      initializeAgeHealthGrids();
    } else {
      nextGrid = tempGrid;
    }
  }, (error) => {
    console.error("Error loading grid file:", error);
  });
}

function countAliveNeighbors(x, y) {
  let aliveCount = 0;

  for (let i = -1; i <= 1; i++) {
    for (let j = -1; j <= 1; j++) {
      if (i == 0 && j == 0) continue;

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
