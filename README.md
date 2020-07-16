# ufdl-backend
User-Friendly Deep Learning (UFDL) - backend system.

## Scripts

* `dev_init.sh` - for setting up the virtual environment `venv.dev` that runs a
  developer instance. You may want to adjust the parameters in the automatically 
  generated file `./venv.dev/lib/python3.7/site-packages/ufdl/api_site/secret.py`
  (like `DEBUG` and `ALLOWED_HOSTS`).
* `dev_reset.sh` - simply resets the database state (the virtual environment must exist)
* `dev_start.sh` - launches the developer instance from the `venv.dev` virtual
  environment on [http://localhost:8000](http://localhost:8000), unless the IP
  address and port to bind to is provided as argument (e.g., `0.0.0.0:8000`)
