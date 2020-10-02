import argparse
import random
import requests
import json
import mysql.connector
import sys



HOSTNAME = 'localhost'
DB_NAME = 'starwars_db'



def connect_to_mysql_server():

	# parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--user',     help='username of mysql database')
	parser.add_argument('-p', '--password', help='password to mysql database')
	args = parser.parse_args()

	# connect to mysql server, abort if connection fails
	conn = mysql.connector.connect(
		host=HOSTNAME,
		user=args.user,
		password=args.password)
	if conn == None:
		print('Failed to connect to MySQL Server.')
		sys.exit()

	# set database
	cursor = conn.cursor()
	cursor.execute("USE %s" % DB_NAME)

	return conn, cursor

def get_starwars_table(conn, cursor):

	# get Characters table
	cursor.execute("SELECT * FROM Characters")
	columns = [col[0] for col in cursor.description]
	characters = [dict(zip(columns, row)) for row in cursor.fetchall()] # convert list of tuples to list of dicts

	# terminate connection
	conn.close()

	return characters

def output_films_and_characters(characters):
	output = []
	films = list(characters[0].keys())[2:]
	for film_title in films:
		characters_in_film = list(filter(lambda c_dct : c_dct[film_title] == 1, characters))
		characters_in_film = list(map(lambda c_dct : c_dct['name'], characters_in_film))
		output.append({
			'film'      : film_title.replace('_', ' '),
			'character' : characters_in_film
		})
	print(json.dumps(output, indent=4))

def task_one():

	# verify the argments provided connect to the mysql server
	conn, cursor = connect_to_mysql_server()

	# get the data from the database
	characters = get_starwars_table(conn, cursor)

	# print the data to the console
	output_films_and_characters(characters)



if __name__ == '__main__':

	task_one()

