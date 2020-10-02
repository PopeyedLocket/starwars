import argparse
import random
import requests
import json
import mysql.connector
import sys
from constants import *



''' connect_to_mysql_server()

	Description:
		Create connection to local MySQL server with username and password arguments.
		Return (None, None) if connection failed. If connection succeeded, (optionally)
		delete database with DB_NAME if it currently exists. Create a new empty database,
		and return the mysql connection object and the mysql cursor object.

	Arguments:
		username ... string .... optional argument with default value None. If None, parse from script arguments
		pasword .... string .... optional argument with default value None. If None, parse from script arguments
		clear_db ... boolean ... optional argument with default value False.If True, delete/recreate the data base

	Returns:
		conn ..... CMySQLConnection ... connection to database (required: else weak connection error)
		cursor ... CMySQLCursor ....... cursor object to interact with database

	'''
def connect_to_mysql_server(username=None, password=None, clear_db=False):

	# parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--user',     help='username of mysql database')
	parser.add_argument('-p', '--password', help='password to mysql database')
	args = parser.parse_args()
	if username == None: username = args.user
	if password == None: password = args.password

	# connect to mysql server, abort if connection fails
	try:
		conn = mysql.connector.connect(
			host=HOSTNAME,
			user=username,
			password=password)
	except Exception as e:
		print('Failed to connect to MySQL Server.')
		print(e)
		return None, None

	# delete database if it already exists, and create an empty new one
	# NOTE: if the db isn't cleared the setup program would have to check at each step
	# if the database, table, and rows its creating/adding already exist or not.
	cursor = conn.cursor()
	if clear_db:
		cursor.execute("SHOW DATABASES")
		current_dbs = [row[0] for row in cursor.fetchall()]
		if DB_NAME in current_dbs:
			cursor.execute("DROP DATABASE %s" % DB_NAME)
		cursor.execute("CREATE DATABASE %s" % DB_NAME)

	# set database to use
	cursor.execute("USE %s" % DB_NAME)

	return conn, cursor

''' pull_starwars_data()

	Description:
		Get the data from the starwars api https://swapi.dev/

	Arguments:
		verbose ... boolean ... print the return values to the console.
		                        optional argument with default value of False

	Returns:
		characters ... dictionary ... keys: character name, values: dictionary:
											keys: unique character id on api,
											values: film titles the character has been in
		all_films .... dictionary ... keys: api url for film, values: film title
	'''
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

''' save_starwars_data()

	Description:
		Create the table with TABLE_NAME. Each row represents a character. The primary key is the int index
		from the swapi api which is alreay unique. The character name is the 2nd column; its a varchar. And
		the rest of the columns are booleans for each of the film titles (with '_' replacing any spaces in
		the column names). Then insert the data into said table.

	Arguments:
		conn ..... CMySQLConnection ... connection to database (required: else weak connection error)
		cursor ... CMySQLCursor ....... cursor object to interact with database
		characters ... dictionary ... keys: character name, values: dictionary:
											keys: unique character id on api,
											values: film titles the character has been in
		all_films .... dictionary ... keys: api url for film, values: film title
		verbose ... boolean ... print the return values to the console.
		                        optional argument with default value of False

	Returns:
		Nothing

	'''
def save_starwars_data(conn, cursor, characters, all_films, verbose=False):

	# create MySQL table
	film_columns_str = ", ".join(["%s BOOL" % title.replace(' ', '_') for title in all_films.values()])
	cmd = "CREATE TABLE %s (character_id INT(3) NOT NULL, name VARCHAR(50), %s, PRIMARY KEY (character_id))" % (TABLE_NAME, film_columns_str)
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
	cmd = "INSERT INTO %s (character_id, name, %s) VALUES %s" % (TABLE_NAME, film_titles_str, values_str)
	cursor.execute(cmd)
	if verbose:
		print('\nMySQL INSERT statement:')
		print(cmd, '\n')

	# commit inserts and terminate connection
	conn.commit()
	conn.close()

''' setup()

	Description:
		Create the MySQL database, pull the data from the API, create a table in the
		MySQL database, and save the data in the table.

	Arguments:
		username ... string .... optional argument with default value None. If None, parse from script arguments
		pasword .... string .... optional argument with default value None. If None, parse from script arguments
		verbose ... boolean ... print the return values to the console.
		                        optional argument with default value of False

	Returns:
		Nothing

	'''
def setup(username=None, password=None, verbose=False):

	# verify the argments provided connect to the local mysql server
	conn, cursor = connect_to_mysql_server(
		username=username,
		password=password,
		clear_db=True)
	if conn == None or cursor == None:
		return

	# pull data from starwars API
	characters, all_films = pull_starwars_data(verbose=verbose)

	# save data in mysql database
	save_starwars_data(conn, cursor, characters, all_films, verbose=verbose)



if __name__ == '__main__':

	setup(verbose=True)


