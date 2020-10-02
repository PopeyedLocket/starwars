import argparse
import random
import requests
import json
import mysql.connector
import sys
from constants import *
from setup import connect_to_mysql_server



''' get_starwars_table_data()

	Description:
		Get the data from the table in the local MySQL database.

	Arguments:
		conn ..... CMySQLConnection ... connection to database (required: else weak connection error)
		cursor ... CMySQLCursor ....... cursor object to interact with database

	Returns:
		characters ... list of dictionaries ... each list element is a row in the table,
		                                        each key is the column name, and the value is the table cell's value
	'''
def get_starwars_table_data(conn, cursor):

	# get Characters table
	cursor.execute("SELECT * FROM %s" % TABLE_NAME)
	columns = [col[0] for col in cursor.description]
	characters = [dict(zip(columns, row)) for row in cursor.fetchall()] # convert list of tuples to list of dicts

	# terminate connection
	conn.close()

	return characters

''' output_films_and_characters()

	Description:
		Create a list of dictionaries of the films and characters
		Print it to the console and return it.

	Arguments:
		characters ... list of dictionaries ... each list element is a row in the table,
		                                        each key is the column name, and the value is the table cell's value
		verbose ...... boolean ................ print the return values to the console.
		                                        optional argument with default value of False

	Returns:
		output ... list of dictionaries ... each dictionary has key: film, value: list of character in that film

	'''
def output_films_and_characters(characters, verbose=False):
	output = []
	films = list(characters[0].keys())[2:]
	for film_title in films:
		characters_in_film = list(filter(lambda c_dct : c_dct[film_title] == 1, characters))
		characters_in_film = list(map(lambda c_dct : c_dct['name'], characters_in_film))
		output.append({
			'film'      : film_title.replace('_', ' '),
			'character' : characters_in_film
		})
	if verbose:
		print(json.dumps(output, indent=4))
	return output

''' task_one()
	
	Description:
		Connect to the MySQL database, get the data in the table,
		and output and return the data.

	Arguments:
		username ... string .... optional argument with default value None. If None, parse from script arguments
		pasword .... string .... optional argument with default value None. If None, parse from script arguments
		verbose ... boolean ... print the return values to the console.
		                        optional argument with default value of False

	Returns:
		output ... list of dictionaries ... each dictionary has key: film, value: list of character in that film
		                                    returns None if failed to connect to database
	'''
def task_one(username=None, password=None, verbose=True):

	# verify the argments provided connect to the mysql server
	conn, cursor = connect_to_mysql_server(
		username=username,
		password=password,
		clear_db=False)
	if conn == None or cursor == None:
		return None

	# get the data from the database
	characters = get_starwars_table_data(conn, cursor)

	# print and return the data to the console
	output = output_films_and_characters(characters, verbose=verbose)
	return output



if __name__ == '__main__':

	output = task_one()


