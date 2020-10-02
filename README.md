# starwars
Red Hat Technical Assessment - Data Engineer



### Install

clone repo with: git clone git@github.com:PopeyedLocket/starwars-characters.git

install mysql with: sudo apt-get install mysql-server

install python mysql connector with: sudo apt-get install mysql-server

run these commands to create the MySQL server user the python script will access the MySQL database with:
sudo mysql -u root
mysql> USE mysql;
mysql> CREATE USER '<YOUR_NEW_USERNAME>'@'localhost' IDENTIFIED BY '<YOUR_NEW_PASSWORD>';
mysql> GRANT ALL PRIVILEGES ON *.* TO '<YOUR_NEW_USERNAME>'@'localhost';
`mysql> FLUSH PRIVILEGES;`
mysql> exit;
service mysql restart



# Usage

Run the following python script to pull the data from ​https://swapi.dev/

python setup.py -u <YOUR_NEW_USERNAME> -p <YOUR_NEW_PASSWORD>

ex:

python setup.py -u luke -p MbsuUtMMY2fN6Uq4



Then run the following script to output a list of films and which characters where in each film:

​python task_one.py -u luke -p MbsuUtMMY2fN6Uq4



### Uninstall

`sudo mysql -u root`

mysql> USE mysql;
mysql> DROP USER '<YOUR_NEW_USERNAME>'@'localhost'
mysql> exit;
service mysql restart

then delete the github repo: rm -rf /path/to/repo/starwars-characters/
