from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

def validate_fields(data, prefix):
    required = ['host', 'port', 'user', 'password', 'database']
    if not all(key in data for key in required):
        return False, f"Missing fields in '{prefix}'. Required: {required}"
    return True, ""

@app.route('/migrate', methods=['POST'])
def migrate_db():
    req_data = request.json

    if 'source' not in req_data or 'target' not in req_data:
        return jsonify({'error': "Both 'source' and 'target' sections are required"}), 400

    source = req_data['source']
    target = req_data['target']

    # Validar campos
    valid_source, msg = validate_fields(source, 'source')
    if not valid_source:
        return jsonify({'error': msg}), 400
    valid_target, msg = validate_fields(target, 'target')
    if not valid_target:
        return jsonify({'error': msg}), 400

    # Crear archivo temporal para el dump
    with tempfile.NamedTemporaryFile(delete=False, suffix=".sql") as tmp_file:
        dump_file = tmp_file.name

    # Setear variables de entorno para pg_dump
    env = os.environ.copy()
    env['PGPASSWORD'] = source['password']

    try:
        # Dump de la base source
        subprocess.run([
            'pg_dump',
            '-h', source['host'],
            '-p', str(source['port']),
            '-U', source['user'],
            '-d', source['database'],
            '-f', dump_file
        ], env=env, check=True)

        # Setear pass del target
        env['PGPASSWORD'] = target['password']

        # Restaurar en base destino
        subprocess.run([
            'psql',
            '-h', target['host'],
            '-p', str(target['port']),
            '-U', target['user'],
            '-d', target['database'],
            '-f', dump_file
        ], env=env, check=True)

        return jsonify({'message': f"Base de datos '{source['database']}' migrada exitosamente a '{target['database']}'"}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Error ejecutando pg_dump o psql', 'details': str(e)}), 500
    finally:
        if os.path.exists(dump_file):
            os.remove(dump_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
