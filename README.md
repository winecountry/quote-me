# quote_me
### The daily quote recommender

## Set up local database

    $ createdb quote_db
    $ psql -d quote_db -f db_init.sql

### Seed the database

* Open `/daily_quote/views.py`
* Uncomment the first line in the `index` view so that you see


    def index(req):
        seed(with_quotes=True)
        ...
    
* In a terminal, run


    $ python manage.py runserver

* Make a get request to `localhost:8000`
* Go back to `views.py` and comment out the first line again


    def index(req):
        # seed(with_quotes=True)
        ...

## Run the app

    $ python manage.py runserver
