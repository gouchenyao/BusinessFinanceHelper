# BusinessFinanceHelper

A tool for small business on financial issues

## Tech

This tool uses a number of open source projects to work properly:

* Flask
* Sqlite

## Installation

This tool requires Pipenv and Python 3.6 to run.

Install the dependencies and dev-dependencies from Pipfile using Pipenv, initialize the database and start the server.

```sh
$ pipenv install
$ pipenv run python database.py
$ pipenv run python views.py
```