# twitoff-aaron-5

## Installation

Download the repo and navigate there from the command line:

```sh
git clone git@github.com:s2t2/twitoff-15.git
cd twitoff-15
```

## Setup

Setup and activate a virtual environment:

```sh
pipenv install
pipenv shell
```

Setup the database:

```sh
# Windows users can omit the "FLASK_APP=web_app" part...

FLASK_APP=web_app flask db init #> generates app/migrations dir

# run both when changing the schema:
FLASK_APP=web_app flask db migrate #> creates the db (with "alembic_version" table)
FLASK_APP=web_app flask db upgrade #> creates the specified tables
```

## Usage

Run the web app:

```sh
FLASK_APP=web_app flask run
```
=======
>>>>>>> 3e1dc06b932e2ec885a47d67683de9ee6c2f7d33
