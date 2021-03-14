# Aliases app

App works with *PostgresSQL*<br/> 
 - **Necessary to have created database 
   and user with rights to create tables.**
 - **Necessary to add DB_NAME, DB_USER, DB_PASSWORD 
environment variables.**

###Write the commands

1. `git clone https://github.com/ChernenkiyCode/Aliases.git`
2. `python -m venv YourDirectoryName`
3. `source YourDirectoryName/Scripts/activate`
4. `cd Aliases`
5. `pip install -r requirements.txt`
6. `python manage.py migrate`

### Using

- Run server with command `python manage.py runserver`
- Run tests with command `python manage.py test`
