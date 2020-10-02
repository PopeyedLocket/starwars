# starwars
Red Hat Technical Assessment - Data Engineer

`asdasdf  
zxcvzxcvz  
feytkjh  
nnnnn`


### Install

clone github repo:
`git clone git@github.com:PopeyedLocket/starwars-characters.git`

install mysql:
`sudo apt-get install mysql-server`

install python mysql connector:
`sudo apt-get install mysql-server`

create the MySQL server user the python script will access the MySQL database with:
`sudo mysql -u root`
`mysql> USE mysql;`
`mysql> CREATE USER '<YOUR_NEW_USERNAME>'@'localhost' IDENTIFIED BY '<YOUR_NEW_PASSWORD>';`
`mysql> GRANT ALL PRIVILEGES ON *.* TO '<YOUR_NEW_USERNAME>'@'localhost';`
`mysql> FLUSH PRIVILEGES;`
`mysql> exit;`
`service mysql restart`



### Usage

run setup.py to pull the data from ​https://swapi.dev/
`python setup.py -u <YOUR_NEW_USERNAME> -p <YOUR_NEW_PASSWORD>`

then run task_one.py to output a list of films with which characters where in each film:
​`python task_one.py -u luke -p MbsuUtMMY2fN6Uq4`



### Uninstall

delete the MySQL server user:
`sudo mysql -u root`
`mysql> USE mysql;`
`mysql> DROP USER '<YOUR_NEW_USERNAME>'@'localhost'`
`mysql> exit;`
`service mysql restart`

delete the github repo:
`rm -rf /path/to/repo/starwars-characters/`
