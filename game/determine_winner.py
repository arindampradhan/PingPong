import pandas
import random
from random import randint
from os import path

def make_defence_array(week_player_details):
	defence_array = random.sample(range(1, 10), week_player_details['defence'])
	return defence_array

def choose_random_number():
	number = randint(0,10)
	return number

def find_week_player(player1, player2, players_data):
	defence_player_1_details = players_data[players_data['Player Name'] == player1]["Defence set length"]
	defence_player_2_details = players_data[players_data['Player Name'] == player2]["Defence set length"]
	for index, value in defence_player_1_details.items():
 		defence_player_1 = value
	for index, value in defence_player_2_details.items():
		defence_player_2 = value
	if defence_player_1 > defence_player_2:
		return player1
	else:
		return player2

def find_week_player_details(player, players_data):
	# print player
	player_details = players_data[players_data['Player Name'] == player]["Defence set length"]
	# print player_details
	for index, value in player_details.items():
		defence_player = value
	return {'player' : player, 'defence' : defence_player}

def find_winner(player1, player2, players_data):
	player1_score = 0
	player2_score = 0
	players_list = [player1, player2]
	week_player = find_week_player(player1, player2, players_data)
	week_player_details = find_week_player_details(week_player, players_data)
	strong_player = [player for player in players_list if player != week_player][0]
	counter = 0
	while (player1_score != 5) and (player2_score != 5):
		number_chosen_by_strong = choose_random_number()
		week_player_details = find_week_player_details(week_player, players_data)
		week_player_defence_list = make_defence_array(week_player_details)
		if number_chosen_by_strong in week_player_defence_list:
			if player1 == week_player:
				player1_score += 1
			else :
				player2_score +=1
			strong_player = week_player
			week_player = strong_player
		else:
			if player1 == strong_player:
				player1_score +=1
			else:
				player2_score +=1
	if player1_score > player2_score:
		return player1
	else :
		return player2

