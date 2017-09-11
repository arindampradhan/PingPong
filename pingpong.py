from game.determine_winner import find_winner
from game.helpers import csv_to_json
from config import *
from db import *

from flask import Flask, jsonify, request, session
import pandas

app = Flask(__name__)

@app.route('/')
def index():
	return jsonify({"documentation" :"https://documenter.getpostman.com/view/1206388/pingpong/6taa56p"})

@app.route('/api/start', methods=['POST'])
@app.route('/api/restart', methods=['POST'])
def start_match():
	db.match_start.insert_one({'start': True})
	return jsonify({'success': 'started the match'})

######################
# player apis
######################
@app.route('/api/player/', methods=['GET'])
@validate_match
def player_info():
	if request.method == 'GET':
		j = csv_to_json(DATA_FILE)
		return jsonify({'players': j})
	else:
		return jsonify({'error': 'method not allowed!'})


@app.route('/api/player/add', methods=['POST'])
@validate_match
def add_player_info():
	form_data = request.get_json()
	username = form_data.get('username')
	try:
		result = add_user(request)
		return jsonify({"result":result})
	except Exception as e:
		return jsonify({"error": str(e)})
	return jsonify({"result": get_user_data(request)})



@app.route('/api/player/online')
@validate_match
def get_players():
	users = db.users.find({})
	return jsonify({'users': list(users)})

######################
# refree apis
######################
@app.route('/api/refree/game', methods=['POST'])
def create_match():
	return jsonify(save_match_to_db(request))


######################
# matches apis
######################
@app.route('/api/matches/<round>')
def get_matches(round):
	matches = get_player_matches(round)
	return jsonify({'round': round, 'matches': matches})


@app.route('/api/matches/<round>/winners')
def get_winners(round):
	matches = get_player_matches(round)
	return jsonify(matches)

@app.route('/api/match/winner', methods=['GET'])
def get_winner():
	player1 = request.args.get('player1') or 'Chandler'
	player2 = request.args.get('player2') or 'Colwin'
	players_data = pandas.read_csv(DATA_FILE)
	winner = find_winner(player1, player2, players_data)
	return jsonify({'winner': winner})

if __name__=='__main__':
	app.run(debug=True)