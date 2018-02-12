```bash
$ sudo apt install mysql-server
```


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
mysql> GRANT ALL PRIVILEGES ON *.* TO 'finley'@'localhost'
    ->     WITH GRANT OPTION;
```

logout using ctrl+d and login again using the new user
```bash
$ mysql -u foss -p
```

If everything works restore the database

```bash
$ mysql -u foss -p fossamrita < dump.sql
```