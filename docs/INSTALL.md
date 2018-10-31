# Installation Instructions

## 1. Install Pre-Requisites
The project require the following packages to be installed in your system :- 
* **`pip`** - popular python package manager used to install project dependencies. 
* **`python-dev`** - for compiling python extention modules  
* **`virtualenvwrapper`** - wrappers for creating and deleting virtual environments

```bash
sudo apt-get install python-pip python-dev
sudo -H pip install virtualenvwrapper
```
## 2. Get the Repository
You may clone the project file for the amfoss website directly from https://github.com/amfoss/website. However, it is recommended that you fork the repository and work on it, so that you will be able to send pull requests.

After cloning, you should move to the development branch (or create a branch derieved from development branch) to work on the development branch.

```bash
git clone https://github.com/amfoss/fosswebsite.git
cd ./fosswebsite
git checkout development
```
## 3. Setup Development Environment
Set the work environment path, and use the `virtualenwrapper` to create an virtual environment for the project.

### 3.1 Set the Work Environment Path
```bash
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
```
### 3.2 Create an Environment
```bash
mkvirtualenv --python=`which python3` foss
```
### 3.3 Work on the Environment
```bash
workon foss
```
## 4. Install Project Requirements
For working on the project, we need to install some project dependencies. All the requirements are listed in the [`requirements.txt`](./requirements.txt) file inside the `docs` directory.

```bash
pip install -r docs/requirements.txt
```
## 5. Create `local_settings.py`
Create the file `local_settings.py` inside the fosswebsite subdirectory.
```bash
touch fosswebsite/local_settings.py
```
## 6. Setup Database
In the development branch, we run django using the default sqlite3 database. To setup django tables in the database, we perform migrations. 

```bash
python manage.py makemigrations
python manage.py migrate
```

Collect all the static project files for fast serving
```bash
python manage.py collectstatic
```
## 7. Create an Admin Account
Create a superuser account for managing the django project admin interface.
```bash
python manage.py createsuperuser
```
## 8. Run Server
Run your project locally and view changes.
```bash
python manage.py runserver
```
