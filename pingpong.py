from game.determine_winner import find_winner
from game.helpers import csv_to_json
from config import *
from database import *

import os
import uuid
import shutil

from flask import Flask, jsonify, request, session
import pandas

app = Flask(__name__)


@app.route('/')
def index():
	return jsonify({"documentation" :"https://documenter.getpostman.com/view/1206388/pingpong/6taa56p"})

@app.route('/api/start', methods=['POST'])
def start_match():
	restart= request.args.get('restart')
	if restart:
		db.tinydb.purge_tables()
		return jsonify({'success': "cleared the database and restarted the match"})
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


@app.route('/api/player/online', methods=['POST'])
@validate_match
def add_player_info():
	try:
		form_data = request.get_json()
		print(form_data)
		username = form_data.get('username')
		try:
			result = add_user(request)
			return jsonify({"result":result})
		except Exception as e:
			return jsonify({"error": str(e)})
		return jsonify({"result": get_user_data(request)})
	except:
		return jsonify({'error': 'username and type not passed'})


@app.route('/api/player/online', methods=['GET'])
@validate_match
def get_players():
	users = db.users.find({})
	return jsonify({'users': list(users)})

######################
# refree apis
######################
@app.route('/api/refree/game', methods=['POST'])
def create_match():
	"""
	Create a match
	request:
	takes: post data
	round: int
	matches: []
	"""
	post_data = None
	users_available = csv_to_json(DATA_FILE)
	try:
		post_data = request.get_json()
	except:
		pass
	if not post_data:
		return jsonify({'error': 'matches not added'})

	if not post_data.get('round'):
		return jsonify({'error': 'round param in body required!'})

	# get all users
	all_players = set()
	all_players_db = set()

	for u in users_available:
		all_players_db.add(u['Player Name'])

	for match in post_data['matches']:
		player1 = match['player1']
		player2 = match['player2']
		all_players.add(player2)
		all_players.add(player1)
		if not player1 or not player2:
			return jsonify({'error': 'player1 or player2 not added', 'data': match})

	if (all_players <= all_players_db) == False:
		return jsonify({
				'error': 'some players are not available',
				'availablePlayers': list(all_players_db),
				'sentPlayers': list(all_players)
			})

	try:
		all_players = list(all_players)
		game_round = int(post_data.get('round'))
		game = games_collection.find_one({'round': game_round})
		if game:
			return jsonify({'error ': 'game has already been decided! can\'t change until you restart'})
		print('\n'*10)
		print(list(all_players_db))
		## check if required players match and length of selected players match
		if game_round == 1:
			if len(all_players) != 8:
				return jsonify({'error ': 'need 8 player for round 1', 'players': all_players})
			games_collection.insert_one(post_data)
			return jsonify({'success': "successfully added players!"})
		elif game_round == 2:
			if len(all_players) != 4:
				return jsonify({'error ': 'need 4 player for round 2', 'players': all_players})
			games_collection.insert_one(post_data)
			return jsonify({'success': "successfully added players!"})
		elif game_round == 3:
			if len(all_players) != 2:
				return jsonify({'error ': 'need 2 player for round 3', 'players': all_players})
			games_collection.insert_one(post_data)
			return jsonify({'success': "successfully added players!"})
		else:
			return jsonify({'error': "all matches only have 3 rounds."})
	except Exception as e:
		return jsonify({'error': str(e)})

	# games_collection.update()
	# return jsonify(save_match_to_db(request))
	return jsonify({})


######################
# matches apis
######################
@app.route('/api/matches/<match_round>')
def get_matches(match_round):
	"""Get matches and their winners"""
	matches = list(db.games.find({}))
	return jsonify({'data': matches})

@app.route('/api/match/winner', methods=['GET'])
def get_winner():
	player1 = request.args.get('player1') or 'Chandler'
	player2 = request.args.get('player2') or 'Colwin'
	players_data = pandas.read_csv(DATA_FILE)
	winner = find_winner(player1, player2, players_data)
	return jsonify({'winner': winner})

if __name__=='__main__':
	app.run(debug=True)