from flask import Flask, render_template, request, jsonify
from algorithms.bfs import bfs as ref_bfs
from algorithms.dfs import dfs as ref_dfs
from algorithms.ucs import ucs as ref_ucs
from algorithms.dijkstra import dijkstra as ref_dijkstra
from algorithms.a_star import a_star as ref_a_star

import importlib.util
import sys

app = Flask(__name__)

def load_student_module(algorithm):
    spec = importlib.util.spec_from_file_location(
        f"student_{algorithm}",
        f"../student_code/{algorithm}.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test():
    data = request.json
    try:
        ref_result = "Hello"
        
        return jsonify({
            'reference': ref_result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    data = request.json
    algorithm = data['algorithm']
    grid_size = data['grid_size']
    start = tuple(data['start'])
    goal = tuple(data['goal'])
    weights = data['weights']
    heuristicFuntion = data['heuristicFuntion'] 

    if algorithm == 'bfs':
        result = ref_bfs(grid_size, start, goal)
    elif algorithm == 'dfs':
        result = ref_dfs(grid_size, start, goal)
    elif algorithm == 'ucs':
        result = ref_ucs(grid_size, start, goal)
    elif algorithm == 'dijkstra':
        result = ref_dijkstra(grid_size, start, goal, weights)
    elif algorithm == 'a_star':
        result = ref_a_star(grid_size, start, goal, weights, heuristicFuntion)

    return jsonify(result)

@app.route('/test_code', methods=['POST'])
def test_code():
    data = request.json
    algorithm = data['algorithm']
    grid_size = data['grid_size']
    start = tuple(data['start'])
    goal = tuple(data['goal'])

    try:
        ref_module = sys.modules[f'algorithms.{algorithm}']
        student_module = load_student_module(algorithm)
        
        ref_result = getattr(ref_module, algorithm)(grid_size, start, goal)
        student_result = getattr(student_module, algorithm)(grid_size, start, goal)
        
        return jsonify({
            'passed': ref_result == student_result,
            'reference': ref_result,
            'student': student_result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app = Flask(__name__)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)