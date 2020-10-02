import argparse
import random
import requests
import json
import mysql.connector
import sys



HOSTNAME = 'localhost'
DB_NAME = 'starwars_db'
FILMS_URL = 'https://swapi.dev/api/films/'
CHARACTER_URL = 'https://swapi.dev/api/people/{character_index}/'
NUM_CHARACTERS = 15


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

	# delete database if it already exists
	# NOTE: if this wasn't here the program would have to check at each step if
	# the database, table, and rows its creating/adding already exist or not.
	cursor = conn.cursor()
	cursor.execute("show databases")
	current_dbs = [row[0] for row in cursor.fetchall()]
	if DB_NAME in current_dbs:
		cursor.execute("DROP DATABASE %s" % DB_NAME)

	# create and set database
	cursor.execute("CREATE DATABASE %s" % DB_NAME)
	cursor.execute("USE %s" % DB_NAME)

	return conn, cursor

def pull_starwars_data(verbose=False):

	# create dictionary of all starwars films
	response = requests.get(FILMS_URL)
	all_films = {
		f['url'] : f['title'] \
		for f in json.loads(response.text)['results']}
	if verbose:
		print('\nall_films = ')
		print(json.dumps(all_films, indent=4))

	# NOTE: the api returns: <Response [404]> {"detail":"Not found"}
	# for the following indeces:
	invalid_indeces = [17, 84, 85, 86, 87]
	valid_indeces = [i for i in range(1, 87+1) if i not in invalid_indeces]
	characters = {}
	for i in random.sample(valid_indeces, NUM_CHARACTERS):
		response = requests.get(CHARACTER_URL.format(character_index=i))
		data = json.loads(response.text)
		films_with_character = [all_films[film_url] for film_url in data['films']]
		characters[data['name']] = {
			'character_id'         : i,
			'films_with_character' : films_with_character}
	if verbose:
		print('\n%d characters = ' % NUM_CHARACTERS)
		print(json.dumps(characters, indent=4))

	return characters, all_films

def save_starwars_data(conn, cursor, characters, all_films, verbose=False):

	# create MySQL table: Characters
	# each row is a character
	# the primary key is the int index from swapi for each character which is alreay unique
	# the character name is the next column, its a varchar
	# and the rest of the columns are booleans for each of the film titles (with '_' replacing any spaces in the column name)
	film_columns_str = ", ".join(["%s BOOL" % title.replace(' ', '_') for title in all_films.values()])
	cmd = "CREATE TABLE Characters (character_id INT(3) NOT NULL, name VARCHAR(50), %s, PRIMARY KEY (character_id))" % film_columns_str
	cursor.execute(cmd)
	if verbose:
		print('\nMySQL CREATE statement:')
		print(cmd)

	# insert the data of the characters into the database
	film_titles_str = ', '.join(["%s" % title.replace(' ', '_') for title in all_films.values()])
	values_str = ""
	for name, dct in characters.items():
		values_str += "(%s, \'%s\'" % (dct['character_id'], name)
		for film_title in all_films.values():
			values_str += ", TRUE" if film_title in dct['films_with_character'] else ", FALSE"
		values_str += "), "
	values_str = values_str[:-2] # remove trailing comma and space
	cmd = "INSERT INTO Characters (character_id, name, %s) VALUES %s" % (film_titles_str, values_str)
	cursor.execute(cmd)
	if verbose:
		print('\nMySQL INSERT statement:')
		print(cmd, '\n')

	# commit inserts and terminate connection
	conn.commit()
	conn.close()

def setup(verbose=False):

	# verify the argments provided connect to the local mysql server
	conn, cursor = connect_to_mysql_server()

	# pull data from starwars API
	characters, all_films = pull_starwars_data(verbose=verbose)

	# save data in mysql database
	save_starwars_data(conn, cursor, characters, all_films, verbose=verbose)



if __name__ == '__main__':

	setup(verbose=True)


