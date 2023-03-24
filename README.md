# ufdl-backend
User-Friendly Deep Learning (UFDL) - backend system.

## Requirements

* Python 3.8 (including development headers)

  ```commandline
  sudo apt-get install python3.8 python3.8-dev libpython3.8-dev
  ```

* essential build environment

  ```commandline
  sudo apt-get install build-essential
  ```

* additional libraries

  ```commandline
  sudo apt-get install libsm6 libxrender1 virtualenv
  ```

* when using a MySQL backend ensure that `mysql_config` is present

  ```commandline
  sudo apt-get install libmysqlclient-dev
  ```


## Scripts

* `dev_init.sh` - for setting up the virtual environment `venv.dev` that runs a
  developer instance. You may want to adjust the parameters in the automatically 
  generated file `./venv.dev/lib/python3.7/site-packages/ufdl/api_site/secret.py`
  (like `DEBUG` and `ALLOWED_HOSTS`). Use `-h` for outputting the help screen.
* `dev_reset.sh` - simply resets the database state (the virtual environment must exist)
* `dev_start.sh` - launches the developer instance from the `venv.dev` virtual
  environment on [http://localhost:8000](http://localhost:8000), unless the IP
  address and port to bind to is provided as argument (e.g., `0.0.0.0:8000`)


## Environment variables

The following environment variables can be used to 

* `UFDL_DATABASE_TYPE` - the database to use for the backend (`sqlite3|postgresql`, default: `sqlite3`)
* `UFDL_POSTGRESQL_HOST` - host for PostgreSQL DB
* `UFDL_POSTGRESQL_USER` - user for PostgreSQL DB
* `UFDL_POSTGRESQL_PASSWORD` - password for PostgreSQL DB


## Docker

See [here](docker/) for more scripts or [documentation](https://ufdl.cms.waikato.ac.nz/getting-started/#docker-compose-docker).


## API documentation

For API documentation see:
* [repository](https://github.com/waikato-ufdl/ufdl-api)
* [website](https://waikato-ufdl.github.io/ufdl-api/)
