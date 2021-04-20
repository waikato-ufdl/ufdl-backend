# UFDL Database

Docker image for running a PostgreSQL database for UFDL.
 

## Docker

### Quick start

* Log into registry using *public* credentials:

  ```commandline
  docker login -u public -p public public.aml-repo.cms.waikato.ac.nz:443 
  ```

* Create a volume to persist the database data:

  ```commandline
  docker volume create ufdl-postgres-volume
  ```

* Pull and run image:

  ```commandline
  docker run \
    -p 5432:5432/tcp \
    -v ufdl-postgres-volume:/var/lib/postgresql/10/main \
    public.aml-repo.cms.waikato.ac.nz:443/ufdl/ufdl_postgres:latest
  ```

* If need be, remove all containers and images from your system:

  ```commandline
  docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q) && docker system prune -a
  ```


### Build local image

* Build the image from Docker file (from within /path_to/ufdl/docker/database)

  ```commandline
  docker build -t ufdl_postgres .
  ```


* Create a volume to persist the database data:

  ```commandline
  docker volume create ufdl-postgres-volume
  ```

* Run the container

  ```commandline
  docker run \
    -p 5432:5432/tcp \
    -v ufdl-postgres-volume:/var/lib/postgresql/10/main \
    ufdl_postgres
  ```
  * `-p X:Y` maps local port X to container port Y 
  * `-v volume-name:/container/dir` maps a volume into a directory inside the container
    (only maps files if the file already exists inside the container)

### Pre-built images

* Build

  ```commandline
  docker build -t ufdl/ufdl_postgres:latest .
  ```
  
* Tag

  ```commandline
  docker tag \
    ufdl/ufdl_postgres:latest \
    public-push.aml-repo.cms.waikato.ac.nz:443/ufdl/ufdl_postgres:latest
  ```
  
* Push

  ```commandline
  docker push public-push.aml-repo.cms.waikato.ac.nz:443/ufdl/ufdl_postgres:latest
  ```
  If error "no basic auth credentials" occurs, then run (enter username/password when prompted):
  
  ```commandline
  docker login public-push.aml-repo.cms.waikato.ac.nz:443
  ```
  
* Pull

  If image is available in aml-repo and you just want to use it, you can pull using following command and then [run](#run).

  ```commandline
  docker pull public.aml-repo.cms.waikato.ac.nz:443/ufdl/ufdl_postgres:latest
  ```
  If error "no basic auth credentials" occurs, then run (enter username/password when prompted):
  
  ```commandline
  docker login public.aml-repo.cms.waikato.ac.nz:443
  ```
  Then tag by running:
  
  ```commandline
  docker tag \
    public.aml-repo.cms.waikato.ac.nz:443/ufdl/ufdl_postgres:latest \
    ufdl/ufdl_postgres:latest
  ```

* Create a volume to persist the database data:

  ```commandline
  docker volume create ufdl-postgres-volume
  ```

* <a name="run">Run</a>

  ```commandline
  docker run \
    -p 5432:5432/tcp \
    -v ufdl-postgres-volume:/var/lib/postgresql/10/main \
    ufdl/ufdl_postgres:latest
  ```
  * `-p X:Y` maps local port X to container port Y 
  * `-v volume-name:/container/dir` maps a volume into a directory inside the container
    (only maps files if the file already exists inside the container)
