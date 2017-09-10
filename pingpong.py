from game.determine_winner import find_winner
from config import *

from flask import Flask, jsonify, request
import pandas

app = Flask(__name__)

@app.route('/')
def index():
	return jsonify({"Hello" :"World"})


@app.route('/api/getwinner', methods=['GET'])
def hello():
	player1 = request.args.get('player1') or 'Chandler'
	player2 = request.args.get('player2') or 'Colwin'
	players_data = pandas.read_csv(DATA_FILE)
	winner = find_winner(player1, player2, players_data)
	return jsonify({'winner': winner})


if __name__=='__main__':
	app.run(debug=True)