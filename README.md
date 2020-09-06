# ufdl-backend
User-Friendly Deep Learning (UFDL) - backend system.

## Requirements

* Python 3.7 or 3.8 (including development headers)

  ```commandline
  sudo apt-get install python3.7 python3.7-dev libpython3.7-dev
  ```

  or

  ```commandline
  sudo apt-get install python3.8 python3.8-dev libpython3.8-dev
  ```

* essential build environment

  ```commandline
  sudo apt-get install build-essential
  ```

## Scripts

* `dev_init.sh` - for setting up the virtual environment `venv.dev` that runs a
  developer instance. You may want to adjust the parameters in the automatically 
  generated file `./venv.dev/lib/python3.7/site-packages/ufdl/api_site/secret.py`
  (like `DEBUG` and `ALLOWED_HOSTS`).
* `dev_reset.sh` - simply resets the database state (the virtual environment must exist)
* `dev_start.sh` - launches the developer instance from the `venv.dev` virtual
  environment on [http://localhost:8000](http://localhost:8000), unless the IP
  address and port to bind to is provided as argument (e.g., `0.0.0.0:8000`)

## API documentation

For API documentation see:
* [repository](https://github.com/waikato-ufdl/ufdl-api)
* [website](https://waikato-ufdl.github.io/ufdl-api/)


## Job templates

* The migrations look for `.json` files in the `migrations/job_templates` directory.
* Use the [template_to_json.py](ufdl/core_app/migrations/job_templates/raw/template_to_json.py)
  script to convert any text file into dummy JSON output (`body` element) for copy/pasting into an
  actual template.
* Compound fields get split on the `|`:

  * framework: `name|version`
  * input: `name|type|options`
  * parameter: `name|type|default`
  
* Currently supported types for compound fields `input` and `parameter`:
  
  * bool
  * int
  * float
  * str
  * dataset
  * model (for selecting pretrained models)
  * joboutput (specifies the job output `type` in the `options` field of parameters)


## Job execution

Jobs that were created from job templates get executed using the 
[Job launcher framework](https://github.com/waikato-ufdl/ufdl-job-launcher) 
on worker nodes.
