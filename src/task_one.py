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

def get_starwars_tables(conn, cursor):

	# get Characters table
	cursor.execute("SELECT * FROM Characters")
	columns = [col[0] for col in cursor.description]
	characters = [dict(zip(columns, row)) for row in cursor.fetchall()] # convert list of tuples to list of dicts

	# get Films table
	cursor.execute("SELECT * FROM Films")
	columns = [col[0] for col in cursor.description]
	films = [dict(zip(columns, row)) for row in cursor.fetchall()]

	# terminate connection
	conn.close()

	return characters, films

def output_films_and_characters(films, characters):
	output = []
	for f_dct in films:
		characters_in_film = []
		for c_dct in characters:
			films_with_character = list(map(lambda film_id : int(film_id), c_dct['films'].split(',')))
			if f_dct['film_id'] in films_with_character:
				characters_in_film.append(c_dct['name'])
		output.append({
			'film'      : f_dct['title'],
			'character' : characters_in_film})
	print(json.dumps(output, indent=4))

def task_one():

	# verify the argments provided connect to the mysql server
	conn, cursor = connect_to_mysql_server()

	# get the data from the database
	characters, films = get_starwars_tables(conn, cursor)

	# print the data to the console
	output_films_and_characters(films, characters)



if __name__ == '__main__':

	task_one()

