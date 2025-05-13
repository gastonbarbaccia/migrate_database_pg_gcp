from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

DUMP_FILE = 'full_dump.dump'

def dump_full(source):
    cmd = [
        'pg_dump',
        '-h', source['host'],
        '-p', source['port'],
        '-U', source['user'],
        '-Fc',
        '-f', DUMP_FILE,
        source['dbname']
    ]
    env = os.environ.copy()
    env['PGPASSWORD'] = source['password']
    subprocess.run(cmd, env=env, check=True)

def restore_full(target):
    cmd = [
        'pg_restore',
        '-h', target['host'],
        '-p', target['port'],
        '-U', target['user'],
        '-d', target['dbname'],
        '--clean',
        '--create',
        '--verbose',
        DUMP_FILE
    ]
    env = os.environ.copy()
    env['PGPASSWORD'] = target['password']
    subprocess.run(cmd, env=env, check=True)

@app.route('/clone', methods=['POST'])
def clone():
    data = request.get_json()
    source = data.get('source')
    target = data.get('target')

    if not source or not target:
        return jsonify({"error": "Faltan parámetros 'source' o 'target'"}), 400

    try:
        dump_full(source)
        restore_full(target)
        return jsonify({"message": "Clonación exitosa"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Falló la clonación: {str(e)}"}), 500

@app.route('/')
def index():
    return "Servicio de clonación listo."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
