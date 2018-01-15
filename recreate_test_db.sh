#!/usr/bin/env bash

dropdb quote_db
createdb quote_db
psql -d quote_db -f db_init.sql
python manage.py migrate
python manage.py loaddata daily_quote/fixtures/authors.json
python manage.py loaddata daily_quote/fixtures/quotes.json
