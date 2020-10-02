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
	cursor = conn.cursor()
	cursor.execute("show databases")
	current_dbs = [row[0] for row in cursor.fetchall()]
	if DB_NAME in current_dbs:
		cursor.execute("DROP DATABASE %s" % DB_NAME)

	# create and set database
	cursor.execute("CREATE DATABASE %s" % DB_NAME)
	cursor.execute("USE %s" % DB_NAME)

	return conn, cursor

def pull_starwars_data():

	# create dictionary of all starwars films
	response = requests.get(FILMS_URL)
	all_films = {
		f['url'] : {
			'id'    : f['url'].split('/')[-2], # index of film (starting at 1)
			'title' : f['title']
		} \
		for f in json.loads(response.text)['results']}

	# NOTE: the get request returns: <Response [404]> {"detail":"Not found"}
	# for the following indeces:
	invalid_indeces = [17, 84, 85, 86, 87]
	valid_indeces = [i for i in range(1, 87+1) if i not in invalid_indeces]
	characters = {}
	for i in random.sample(valid_indeces, 15):
		response = requests.get(CHARACTER_URL.format(character_index=i))
		data = json.loads(response.text)
		film_ids = [all_films[film_url]['id'] for film_url in data['films']]
		characters[data['name']] = {'character_id' : i, 'film_ids' : film_ids}

	# just keep the film_id and the title for the mysql db
	all_films = {f['id'] : f['title'] for f in all_films.values()}

	return characters, all_films

def save_starwars_data(conn, cursor, characters, all_films):

	# create Films table with columns: [film_id, title], and insert all_films data into it
	cursor.execute("CREATE TABLE Films (film_id INT(3) PRIMARY KEY, title VARCHAR(50))")
	cursor.execute("INSERT INTO Films (film_id, title) VALUES " + \
		", ".join(["(%s, \"%s\")" % (film_id, title) \
			for film_id, title in all_films.items()]))

	# create Charcters table with columns: [name, films], and insert characters into it
	cursor.execute("CREATE TABLE Characters (character_id INT(3) NOT NULL, name VARCHAR(50), films VARCHAR(50), PRIMARY KEY (character_id))")
	# print("INSERT INTO Characters (name, films) VALUES " + \
	# 	", ".join(["(\"%s\", \"%s\")" % (name, ','.join(films)) \
	# 		for name, films in characters.items()]))
	cursor.execute("INSERT INTO Characters (character_id, name, films) VALUES " + \
		", ".join(["(%s, \"%s\", \"%s\")" % (dct['character_id'], name, ','.join(dct['film_ids'])) \
			for name, dct in characters.items()]))

	# commit inserts and terminate connection
	conn.commit()
	conn.close()



if __name__ == '__main__':

	# verify the argments provided connect to the mysql server
	conn, cursor = connect_to_mysql_server()

	# pull data from starwars API
	characters, all_films = pull_starwars_data()
	# # print(json.dumps(characters, indent=4))
	# # print(json.dumps(all_films, indent=4))

	# save data in mysql database
	save_starwars_data(conn, cursor, characters, all_films)


