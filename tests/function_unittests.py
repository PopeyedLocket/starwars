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



class Unittester(unittest.TestCase):



    #################### setup.py functions #####################

    # assert that the connection is made with valid credentials
    def test_connect_to_mysql_server1(self):
       conn, cursor = connect_to_mysql_server(
          username=VALID_USERNAME,
          password=VALID_PASSWORD)
       assert(conn != None and cursor != None)

    # assert that the connection is not made with invalid credentials
    def test_connect_to_mysql_server2(self):
       invalid_username = 'asdfasdfasdf'
       invalid_password = 'qwerqwerqwer'
       conn, cursor = connect_to_mysql_server(
          username=invalid_username,
          password=invalid_password)
       assert(conn == None and cursor == None)

    # assert that when a connection is successfully made, it results in a new empty database
    def test_connect_to_mysql_server3(self):
       conn, cursor = connect_to_mysql_server(
          username=VALID_USERNAME,
          password=VALID_PASSWORD)
       cursor.execute("SHOW DATABASES")
       current_dbs = [row[0] for row in cursor.fetchall()]
       assert(DB_NAME not in current_dbs)

    # assert that the returned data is of the proper format
    def test_pull_starwars_data1(self):
       characters, all_films = pull_starwars_data(verbose=False)
       assert(all_films == TEST_ALL_FILMS)
       assert(len(characters.keys()) == NUM_CHARACTERS)
       first_character_name = list(characters.keys())[0]
       first_character_data = characters[first_character_name]
       assert(isinstance(first_character_name, str))
       assert(isinstance(first_character_data, dict))
       assert(isinstance(first_character_data['character_id'], int))
       assert(isinstance(first_character_data['films_with_character'], list))

    # assert that the MySQL table has the proper format and number of rows 
    def test_save_starwars_data1(self):
       conn, cursor = connect_to_mysql_server(
          username=VALID_USERNAME,
          password=VALID_PASSWORD,
          clear_db=True)
       characters, all_films = pull_starwars_data(verbose=False)
       save_starwars_data(conn, cursor, characters, all_films, verbose=False)

       # connect_to_mysql_server is used again here (with clear_db=False though) because coverage looses the connection:
       # mysql.connector.errors.OperationalError: 2055: Lost connection to MySQL server at 'localhost:3306', system error: Connection not available.
       conn, cursor = connect_to_mysql_server(
          username=VALID_USERNAME,
          password=VALID_PASSWORD,
          clear_db=False)
       cursor.execute("SELECT * FROM %s" % TABLE_NAME)
       columns = [col[0] for col in cursor.description]
       characters = [dict(zip(columns, row)) for row in cursor.fetchall()] # convert list of tuples to list of dicts

       assert(len(characters) == NUM_CHARACTERS)
       assert(columns == TEST_TABLE_COLUMNS)




     
    #################### task_one.py functions ##################

    # assert that data returned is of the proper format
    def test_get_starwars_table_data(self):
        conn, cursor = connect_to_mysql_server(
            username=VALID_USERNAME,
            password=VALID_PASSWORD,
            clear_db=False)
        characters = get_starwars_table_data(conn, cursor)
        assert(len(characters) == NUM_CHARACTERS)
        first_character_data = characters[0]
        assert(isinstance(first_character_data, dict))
        for k, v in first_character_data.items():
            if k == "name":
                assert(isinstance(v, str))
            else: # k = "character_id" or a film title (booleans stored as TINYINT in MySQL)
                assert(isinstance(v, int))

    # assert that the output is of the proper format
    def test_output_films_and_characters(self):
        conn, cursor = connect_to_mysql_server(
            username=VALID_USERNAME,
            password=VALID_PASSWORD,
            clear_db=False)
        characters = get_starwars_table_data(conn, cursor)
        output = output_films_and_characters(characters, verbose=True)
        assert(isinstance(output, list))
        first_film = output[0]
        assert(isinstance(first_film, dict))
        first_films_characters = first_film['character']
        assert(isinstance(first_films_characters, list))




def suite():
    suite = unittest.TestSuite()
    suite.addTests(
       unittest.TestLoader().loadTestsFromTestCase(Unittester))
    return suite

''' Testing and Code coverage with Python
    
    run Test with:
      coverage run function_unittests.py
    
    Get Code Coverage with:
      coverage report -m --include=/path/to/repo/src/*
      coverage report -m --include=../src/*
    
    Source:
        https://developer.ibm.com/recipes/tutorials/testing-and-code-coverage-with-python/

    '''
if __name__ == '__main__':

    unittest.TextTestRunner(verbosity=1).run(suite())


