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

If MySQL-python installation fails install 'default-libmysqlclient-dev' or 'libmysqlclient-dev'

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

If everything works restore the database

```bash
$ mysql -u foss -p fossamrita < dump.sql
```

Then migrate the db to complete the restore.

```bash
$ python manage.py migrate
```

