# starwars
Red Hat Technical Assessment - Data Engineer



### Install

clone github repo:<br/>
`git clone git@github.com:PopeyedLocket/starwars-characters.git`

install mysql if not already installed:<br/>
`sudo apt-get install mysql-server`

install python library requirements:<br/>
`pip3 install -r requirements.txt`

create the MySQL server username and password that the python script will use to access the database:<br/>
```
sudo mysql -u root
mysql> USE mysql;
mysql> CREATE USER '<YOUR_NEW_USERNAME>'@'localhost' IDENTIFIED BY '<YOUR_NEW_PASSWORD>';
mysql> GRANT ALL PRIVILEGES ON *.* TO '<YOUR_NEW_USERNAME>'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> exit;
service mysql restart
```



### Usage

run setup.py to pull the data from ​https://swapi.dev/ and save it to database<br/>
```
cd starwars/src/
python setup.py -u <YOUR_NEW_USERNAME> -p <YOUR_NEW_PASSWORD>
```

then run task_one.py to output a list of starwars films and which characters where in each film:<br/>
​`python task_one.py -u luke -p MbsuUtMMY2fN6Uq4`



### Testing

Open starwars/tests/test_constants.py and change VALID_USERNAME and VALID_PASSWORD to <YOUR_NEW_USERNAME> and <YOUR_NEW_PASSWORD> respectively.

run Unit Test with:<br/>
```
cd starwars/tests/
coverage run function_unittests.py
```

Get Unittest Code Coverage with:<br/>
```
coverage report -m --include=/path/to/repo/src/*
OR
coverage report -m --include=../src/*
```

Run end-to-end Test with:<br/>
`python project_end_to_end_tests.py`



### Uninstall

delete the MySQL server user:<br/>
```
sudo mysql -u root
mysql> USE mysql;
mysql> DROP USER '<YOUR_NEW_USERNAME>'@'localhost'
mysql> exit;
service mysql restart
```

delete the github repo:<br/>
`rm -rf /path/to/repo/starwars/`

