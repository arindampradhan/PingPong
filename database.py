from tinymongo import TinyMongoClient
from flask import session, jsonify
from functools import wraps
from game.helpers import csv_to_json
from config import *
import pandas
from game.determine_winner import find_winner

# /tmp is accessible in lambda
connection = TinyMongoClient(DB_PATH)
db = connection[DBNAME]
users_collection = db.users
matches_collection = db.matches
games_collection = db.games

def add_refree(form_data):
    started = db.match_start.find({'start': True})
    match_id = started['_id']
    is_refree_present = len(list(db.refree.find({})))
    if is_refree_present:
        return {'error': 'refree already present'}
    db.refree.insert_one({'match_id': match_id, 'data':form_data})
    return {'success': 'Successfully added refree', 'match_id': match_id}

def add_user(request):
    """add user to db"""

    # get data
    form_data = request.get_json()
    username = form_data.get('username')
    player_type = form_data.get('type').lower()
    # check form data present
    if not username:
        return {'error': 'username cannot be empty'}
    if not player_type:
        return {'error': 'type cannot be empty'}
    if player_type == 'refree':
        return add_refree(form_data)

    # find if user exists in available list
    users_available = csv_to_json(DATA_FILE)
    exists = False
    for u in users_available:
        if u.get('Player Name').lower() == username.lower():
            exists = True
    if not exists:
        return {'error': 'username is not available for match'}

    # CHECK IF USER IS ADDED TO DB
    if not users_collection.find_one({"username": username}):
        users_collection.insert_one(
                {"username": username}
            )
        return {'success': "Successfully added user online!"}
    else:
        return {'error': 'user already present!'}

def get_user_data(request):
    """get user data"""
    if not request.args.get('username'):
        return get_all_user()
    record = users_collection.find_one({'username': request.args.get('username')})
    return [record]

def get_all_user():
    """Get all users"""
    record = users_collection.find({})
    return list(record)

def save_match_to_db(request):
    """Save matches to database"""
    form_data = request.get_json()
    if not form_data.get('matches'):
        return {'error': "matches not added"}
    if not form_data.get('round'):
        return {'error': "round not added"}
    try:
        record = matches_collection.insert_one(form_data)
        return {'success': "successfully saved details!"}
    except Exception as e:
        return {'error': str(e)}


def get_player_matches(match_round):
    matches = matches_collection.find({'round': match_round})
    return list(matches)


def validate_match(f):
    """Validate apis for different cases."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        started = db.match_start.find({'start': True})
        if not dict(started):
            return jsonify({"error": 'match not started yet!'})
        return f(*args, **kwargs)
    return decorated_function

def all_players_loggedin(f):
    """Validate apis for different cases."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db_all_users = list(db.users.find({}))
        users_available = csv_to_json(DATA_FILE)
        print(users_available)
        # get player names
        u1 = set([usr['Player Name'].lower() for usr in users_available])
        u2 = set([usr['username'].lower() for usr in db_all_users])
        if u1 != u2:
            return jsonify({"error": "all users are not online!", "active":list(u2), "all": list(u1)})

        return f(*args, **kwargs)
    return decorated_function


def get_matches_by_round(match_round):
    """Get matches and their winners"""
    if match_round > 3:
        return {'error': 'round cannot be greater than 3'}
    matches = db.games.find_one({"round": match_round})
    if not matches:
        return {'error': 'Round not yet started by the refree!'}
    players_data = pandas.read_csv(DATA_FILE)
    # winner
    winners = []
    for match in matches['matches']:
        player1 = match['player1'].title()
        player2 = match['player2'].title()
        winner = find_winner(player1, player2, players_data)
        message = '{} vs {}'.format(player1, player2)
        winners.append({'winner':winner, 'message':message})
    return {'data': matches, 'winners': winners}


def get_players_status(username):
    """Get status of the matches by player names"""
    try:
        games = db.games.find({})
        statuses = []
        players_data = pandas.read_csv(DATA_FILE)

        for game in games:
            for match in game['matches']:
                player1 = match['player1']
                player2 = match['player2']
                winner = find_winner(player1, player2, players_data)
                stat = None
                if winner == username:
                    stat = 'won'
                else:
                    stat = 'lose'
                if username == player2 or username == player1:
                    status = {
                        'match': '{} vs {}'.format(player1,player2),
                        'status': stat
                    }
                    statuses.append(status)

        return {'status': statuses}
    except Exception as e:
        return {'error': str(e)}

