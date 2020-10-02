import sys
import os
import pathlib
REPO_PATH = str(pathlib.Path(__file__).resolve().parent.parent)
SRC_PATH  = os.path.join(REPO_PATH, 'src')
sys.path.append(SRC_PATH)
from setup import *
from task_one import *
from test_constants import *
import unittest



# assert that the MySQL table has the proper format and number of rows 
def test_setup():

	setup(
		username=VALID_USERNAME,
		password=VALID_PASSWORD,
		verbose=False)

	conn, cursor = connect_to_mysql_server(
		username=VALID_USERNAME,
		password=VALID_PASSWORD,
		clear_db=False)
	cursor.execute("SELECT * FROM %s" % TABLE_NAME)
	columns = [col[0] for col in cursor.description]
	characters = [dict(zip(columns, row)) for row in cursor.fetchall()] # convert list of tuples to list of dicts

	assert(len(characters) == NUM_CHARACTERS)
	assert(columns == TEST_TABLE_COLUMNS)
	print('setup end-to-end test ...... successful')

# assert the final output is of the proper format
def test_task_one():

	output = task_one(
		username=VALID_USERNAME,
		password=VALID_PASSWORD,
		verbose=False)

	assert(isinstance(output, list))
	first_film = output[0]
	assert(isinstance(first_film, dict))
	first_films_characters = first_film['character']
	assert(isinstance(first_films_characters, list))
	print('task_one end-to-end test ... successful')



if __name__ == '__main__':

	test_setup()

	# tested after setup in order to reuse the db setup created
	test_task_one()


