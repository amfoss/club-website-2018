## Development Environment
Its super easy to set up our development environment

## Collect Pre-requisites
Install `python-pip`, `python-dev` and `virtualenvwrapper`
```bash
sudo apt-get install python-pip python-dev
sudo -H pip install virtualenvwrapper
```
## Get the files
You can clone it directly from https://github.com/amfoss/website
```bash
git clone https://github.com/amfoss/fosswebsite.git
```
## Setup development environment
First, some initialization steps. Most of this only needs to be done
one time. You will want to add the command to source
`/usr/local/bin/virtualenvwrapper.sh` to your shell startup file
(`.bashrc` or `.zshrc`) changing the path to `virtualenvwrapper.sh`
depending on where it was installed by `pip`.
```bash
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
```
Lets create a virtual environment for our project
```bash
mkvirtualenv --python=`which python3` foss
workon foss
```
## Install requirements
All the requirements are mentioned in the file `requirements.txt`.

Install mysql client. 

In debian: 

```bash
sudo apt install default-libmysqlclient-dev 
```

In ubuntu: 

```bash
sudo apt install libmysqlclient-dev
```
Further install all the requirement packages from the requirements.txt file.

```bash
pip install -r docs/requirements.txt
```

## Setup database

This project is deployed using a MySQL database,so it's recommended to set up a mysql server locally to ensure compatibility.

Install mysql-server

```bash
$ sudo apt install mysql-server
```

If you are running Python3

```bash
$ pip3 install mysqlclient
```

For python2

```bash
$ pip install MySQL-python
```

If MySQL-python installation fails install 'default-libmysqlclient-dev' or 'libmysqlclient-dev' and try again.

```bash
$ sudo apt install default-libmysqlclient-dev
```

or 

```bash
$ sudo apt install libmysqlclient-dev
```

Log into mysql as root

```bash
$ sudo mysql -u root
```

Create a new user and database

create database fossamrita

```mysql
mysql> CREATE USER 'foss'@'localhost' IDENTIFIED BY 'foss@amrita';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'foss'@'localhost'
    ->     WITH GRANT OPTION;
```

where foss is the username and foss@amrita is the password.

logout using ctrl+d and login again using the new user

```bash
$ mysql -u foss -p
```

Create new database fossamrita, for avoiding this error: 'Specified key was too long; max key length is 767 bytes' in 
MariaDB just specify utf8_general_ci at creation time

```mysql
mysql> create database fossamrita default CHARACTER set utf8 default COLLATE utf8_general_ci;
```

## Use the default settings

```bash
$ cp fosswebsite/local_settings_sample.py fosswebsite/local_settings.py
```

Then migrate the db to complete the restore.

```bash
$ python manage.py migrate
```

## Create an admin account
```bash
python manage.py createsuperuser
```
## Run server
```bash
python manage.py runserver
```
