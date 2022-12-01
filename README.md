# django commands
## start server
python manage.py runserver 0.0.0.0:8000

## create new app
python manage.py startapp tweets(API name)

## make migration
python manage.py makemigrations

if there is no migrations folder under the app folder (e.g. tweets),
the above command will throw an error. Run the following instead:
python manage.py makemigrations tweets

Note: makemigrations compares the current model with the database, 
no modifications to database involved

# run unit tests
python manage.py test (this run all the unit tests)
python manage.py test tweets (this only runs tests under tweets)
python manage.py test tweets.api (only test the unit tests under tweets/api)
python manage.py test tweets.api.tests.TweetApiTests.test_list (only run one single specific unit test)

## make changes to database
python manage.py migrate

# Database
## login to database
mysql -uroot -pyourpassword;

## quit database
Bye
quit

## show all databases
show databases;

## select database
use twitter;

## show all tables within the database
show tables;

## show contents of a table
select * from django_migrationsl;

# Debugging
## enter interactive coding mode
python manage.py shell
## quit interactive mode
exit() 
or 
Ctrl-D

