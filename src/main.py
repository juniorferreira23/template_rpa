from flask import Flask, jsonify, request

from src.tasks import hello, run_bot_example

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Api rodando'}), 200


@app.route('/hello', methods=['POST'])
def hello_route():
    data = request.get_json()
    name: str = data.get('name')

    if not name:
        return jsonify({'error': 'argumento name é necessário'}), 400

    message = hello.delay(name)  # type: ignore

    return jsonify({
        'task_id': message.id,
        'message': 'Requisição processada com sucesso!',
    }), 200


@app.route('/run_bot_example', methods=['POST'])
def run_bot():
    data = request.get_json()
    headless_arg: str = data.get('headless_arg')

    if not headless_arg:
        return jsonify({'error': 'argumento headless é necessário'}), 400

    headless = headless_arg.lower() == 'true'

    run_bot_example.delay(headless)  # type: ignore

    return jsonify({'message': 'Requisição processada com sucesso!'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
