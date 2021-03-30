# UFDL backend

Docker image for running the UFDL backend development server.

By mapping a local Django SQlite database (`db.sqlite3`) and storage 
backend (`fs`) into the container, the state of the server is persistent
between runs of the container.
 

## Docker

### Quick start

* Log into registry using *public* credentials:

  ```commandline
  docker login -u public -p public public.aml-repo.cms.waikato.ac.nz:443 
  ```

* Pull and run image (adjust volume mappings `-v`):

  ```commandline
  docker run \
    --net=host \
    -p 8000:8000 \
    -v /local/dir/ufdl-backend/venv.dev/lib/python3.7/site-packages/ufdl/db.sqlite3:/ufdl/ufdl-backend/venv.dev/lib/python3.7/site-packages/ufdl/db.sqlite3 \
    -v /local/dir/ufdl-backend/fs:/fs \
    -it public.aml-repo.cms.waikato.ac.nz:443/ufdl/ufdl_backend:latest \
    /ufdl/ufdl-backend/venv.dev/bin/python -m ufdl.api_site.scripts.manage runserver 0.0.0.0:8000
  ```

* If need be, remove all containers and images from your system:

  ```commandline
  docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q) && docker system prune -a
  ```


### Build local image

* Build the image from Docker file (from within /path_to/ufdl/image_classification/docker/1.14)

  ```commandline
  docker build -t ufdl_backend .
  ```

* Run the container

  ```commandline
  docker run \
    --net=host \
    -p 8000:8000 \
    -v /local/dir/ufdl-backend/venv.dev/lib/python3.7/site-packages/ufdl/db.sqlite3:/ufdl/ufdl-backend/venv.dev/lib/python3.7/site-packages/ufdl/db.sqlite3 \
    -v /local/dir/ufdl-backend/fs:/fs \
    -it ufdl_backend \
    /ufdl/ufdl-backend/venv.dev/bin/python -m ufdl.api_site.scripts.manage runserver 0.0.0.0:8000
  ```
  * `-p X:Y` maps local port X to container port Y 
  * `-v /local/dir:/container/dir` maps a local disk directory into a directory inside the container
    (only maps files if the file already exists inside the container)

### Pre-built images

* Build

  ```commandline
  docker build -t ufdl/ufdl_backend:latest .
  ```
  
* Tag

  ```commandline
  docker tag \
    ufdl/ufdl_backend:latest \
    public-push.aml-repo.cms.waikato.ac.nz:443/ufdl/ufdl_backend:latest
  ```
  
* Push

  ```commandline
  docker push public-push.aml-repo.cms.waikato.ac.nz:443/ufdl/ufdl_backend:latest
  ```
  If error "no basic auth credentials" occurs, then run (enter username/password when prompted):
  
  ```commandline
  docker login public-push.aml-repo.cms.waikato.ac.nz:443
  ```
  
* Pull

  If image is available in aml-repo and you just want to use it, you can pull using following command and then [run](#run).

  ```commandline
  docker pull public.aml-repo.cms.waikato.ac.nz:443/ufdl/ufdl_backend:latest
  ```
  If error "no basic auth credentials" occurs, then run (enter username/password when prompted):
  
  ```commandline
  docker login public.aml-repo.cms.waikato.ac.nz:443
  ```
  Then tag by running:
  
  ```commandline
  docker tag \
    public.aml-repo.cms.waikato.ac.nz:443/ufdl/ufdl_backend:latest \
    ufdl/ufdl_backend:latest
  ```

* <a name="run">Run</a>

  ```commandline
  docker run \
    --net=host \
    -p 8000:8000 \
    -v /local/dir/ufdl-backend/venv.dev/lib/python3.7/site-packages/ufdl/db.sqlite3:/ufdl/ufdl-backend/venv.dev/lib/python3.7/site-packages/ufdl/db.sqlite3 \
    -v /local/dir/ufdl-backend/fs:/fs \
    -it ufdl/ufdl_backend:latest \
    /ufdl/ufdl-backend/venv.dev/bin/python -m ufdl.api_site.scripts.manage runserver 0.0.0.0:8000
  ```
  * `-p X:Y` maps local port X to container port Y 
  * `-v /local/dir:/container/dir` maps a local disk directory into a directory inside the container
    (only maps files if the file already exists inside the container)
