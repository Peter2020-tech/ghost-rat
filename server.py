# server.py
from flask import Flask, render_template, request, jsonify
from ghost.core.console import Console
from ghost.core.device import Device
from ghost.core.loader import Loader

app = Flask(__name__)
console = Console()
device = Device("localhost", port=5555)  # You may want to configure this based on your needs
loader = Loader()
modules = loader.load_modules(device)

@app.route('/')
def index():
    return render_template('index.html', modules=modules)

@app.route('/run_module/<module_name>')
def run_module(module_name):
    try:
        module = modules[module_name]
        module.device = device
        module.run(0, [])
        return jsonify({'status': 'success', 'message': f'Module {module_name} executed successfully.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
