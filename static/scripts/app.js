let grid = [];
let start = null;
let goal = null;
let heuristicFuntion = "";

let weights = []; // 2D array for weights

document.getElementById('gridSize').addEventListener('change', initGrid);
document.getElementById('visualizationMode').addEventListener('change', initGrid);
document.getElementById('heuristicFunction').addEventListener('change', initGrid);
document.getElementById('algorithm').addEventListener('change', initGrid);
document.getElementById('resetButton').addEventListener('click', reset);

const allowedAlgorithms = ['dijkstra'];
const allowedHeuristicAlgorithms = ['a_star'];

document.addEventListener('contextmenu', (e) => {
    const algorithm = document.getElementById('algorithm').value;
    if (allowedAlgorithms.includes(algorithm)) {
        e.preventDefault(); 
        const cell = e.target.closest('.cell');
        if (cell) {
            assignWeight(cell);
        }
    }
});

function controlVisibilityOfElement() {
    const weightInfocontainer = document.getElementById('weightInfo');
    const heuristicFunctionDiv = document.getElementById('heuristicFunctionDiv');

    const algorithm = document.getElementById('algorithm').value;
    const heuristicFunction = document.getElementById('heuristicFunction').value;

    if (allowedAlgorithms.includes(algorithm)) {
        weightInfocontainer.style.display = 'block';
        weightInfocontainer.style.color = '#00008B';
        weightInfocontainer.style.marginTop = '10px';
    }else{
        weightInfocontainer.style.display = 'none';
    }


    if (allowedHeuristicAlgorithms.includes(algorithm)) {
        heuristicFunctionDiv.style.display = 'block';
    }else{
        heuristicFunctionDiv.style.display = 'none';
    }
}

function initGrid() {
    controlVisibilityOfElement();

    const size = parseInt(document.getElementById('gridSize').value);
    const container = document.getElementById('grid');
    heuristicFuntion = document.getElementById('heuristicFunction').value;

    container.innerHTML = '';
    start = null;
    goal = null;

    container.style.gridTemplateColumns = `repeat(${size}, 30px)`;

    grid = Array.from({ length: size }, (_, i) =>
        Array.from({ length: size }, (_, j) => {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.x = i;
            cell.dataset.y = j;
            cell.addEventListener('click', handleCellClick);
            container.appendChild(cell);
            return cell;
        })
    );

    weights = Array.from({ length: size }, () => Array(size).fill(1));

}

function validateInput(weight) {
    errorObject = {
        isValid: true,
        message: ''
    }
    isValid = /^\d+$/.test(weight);
    errorMessage = 'Invalid weight. Please enter a valid weight.';

    if (isValid) {
        if (weight.length > 3) {
            isValid = false;
            errorMessage = 'Weight should have at most 3 digits';
        }
    }else{
        if (parseInt(weight) < 1) {
            isValid = false;
            errorMessage = 'Weight should be greater than 0';
        }
    }

    errorObject.isValid = isValid;
    errorObject.errorMessage = errorMessage;
    return errorObject;
}

function assignWeight(cell) {
    const x = parseInt(cell.dataset.x);
    const y = parseInt(cell.dataset.y);
    if (start && (x === start[0] && y === start[1])) {
        alert('Cannot assign weight to start cell');
        return;
    }



    let newWeight = prompt("Enter weight (e.g., 1 or 2 or 3):", "1");
    if (newWeight !== null) {
        weights[x][y] = parseInt(newWeight);
        cell.classList.add('weighted');
        cell.textContent = newWeight; 
    }

    newWeight = newWeight.trim().replace(/^0+/, '');
    let errorObject = validateInput(newWeight)
    if (!errorObject.isValid) {
        alert(errorObject.errorMessage);
        weights[x][y] = 1;
        cell.textContent = '';
        cell.classList.remove('weighted');
        return;
    }

    
}


function handleCellClick(e) {
    const cell = e.target;
    if (!start) {
        start = [parseInt(cell.dataset.x), parseInt(cell.dataset.y)];
        cell.classList.add('start');
    } else if (!goal) {
        goal = [parseInt(cell.dataset.x), parseInt(cell.dataset.y)];
        cell.classList.add('goal');
        runAlgorithm();
    }
}

async function runAlgorithm() {
    const algorithm = document.getElementById('algorithm').value;
    const mode = document.getElementById('visualizationMode').value;
    
    const response = await fetch('/run_algorithm', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            algorithm,
            grid_size: [grid.length, grid[0].length],
            start,
            goal,
            weights,
            heuristicFuntion
        })
    });
    
    const result = await response.json();
    
    visualize(result.path, result.visited, mode === 'animated');
}

function visualize(path, visited, animated) {

    // visited = visited.filter(([x, y]) => x !== start[0] || y !== start[1]);
    // visited = visited.filter(([x, y]) => x !== goal[0] || y !== goal[1]);
    // path = path.filter(([x, y]) => x !== start[0] || y !== start[1]);
    // path = path.filter(([x, y]) => x !== goal[0] || y !== goal[1]);


    if (animated) {
        visited.forEach(([x, y], i) => {
            setTimeout(() => {
                grid[x][y].classList.add('visited');
            }, 100 * i);
        });
        
        setTimeout(() => {
            path.forEach(([x, y], i) => {
                setTimeout(() => {
                    grid[x][y].classList.add('path');
                }, 50 * i);
            });
        }, 100 * visited.length);

    } else {
        visited.forEach(([x, y]) => {
            grid[x][y].classList.add('visited');
        });

        path.forEach(([x, y]) => {
            grid[x][y].classList.add('path');
        });
     
    }

    grid[start[0]][start[1]].classList.add('start_after_colplete');
    grid[goal[0]][goal[1]].classList.add('goal_after_colplete');
    
}

function reset() {
    console.log("Test button clicked");
    initGrid();
    start = null;
    goal = null;
    weights = Array.from({ length: grid.length }, () => Array(grid[0].length).fill(1))
}

initGrid();