# Ubuntu 18.04 with Python 3.7
ARG DOCKER_REGISTRY=public.aml-repo.cms.waikato.ac.nz:443/
FROM ${DOCKER_REGISTRY}ubuntu:bionic

# Add default values for the Postgres environment
ARG UFDL_POSTGRESQL_DATABASE=ufdl
ARG UFDL_POSTGRESQL_USER=ufdl
ARG UFDL_POSTGRESQL_PASSWORD=ufdl

# ======== #
# OS Setup #
# ======== #
RUN \
    # Make sure that we aren't prompted for timezone information
    export DEBIAN_FRONTEND=noninteractive && \
    # Install necessary tools for the build
    apt-get update && \
    apt-get install -y --no-install-recommends git-core libglib2.0-0 libsm6 libxrender-dev libxrender1 libxext6 postgresql wget && \
    # Clean up the apt cache
    rm -rf /var/lib/apt/lists/*

# ====================== #
# Add UFDL user/database #
# ====================== #
RUN \
    su -c "/usr/lib/postgresql/10/bin/pg_ctl -D /etc/postgresql/10/main start" postgres && \
    su -c "psql -c \"CREATE DATABASE ufdl;\"" postgres && \
    su -c "psql -c \"CREATE USER $UFDL_POSTGRESQL_USER WITH ENCRYPTED PASSWORD '$UFDL_POSTGRESQL_PASSWORD';\"" postgres && \
    su -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE ufdl TO $UFDL_POSTGRESQL_USER;\"" postgres && \
    su -c "/usr/lib/postgresql/10/bin/pg_ctl -D /etc/postgresql/10/main stop" postgres

# ======================== #
# Add Server Configuration #
# ======================== #
COPY postgresql.conf /etc/postgresql/10/main/postgresql.conf

# =============== #
# Add HBA Entries #
# =============== #
RUN \
    # Remove the existing configuration
    rm -f /etc/postgresql/10/main/pg_hba.conf && \
    # Add a fresh file
    touch /etc/postgresql/10/main/pg_hba.conf && \
    # Insert entries for the postgres user and the configured ufdl user
    echo "local all postgres peer" > /etc/postgresql/10/main/pg_hba.conf && \
    echo "local $UFDL_POSTGRESQL_DATABASE $UFDL_POSTGRESQL_USER md5" >> /etc/postgresql/10/main/pg_hba.conf && \
    echo "host $UFDL_POSTGRESQL_DATABASE $UFDL_POSTGRESQL_USER all md5" >> /etc/postgresql/10/main/pg_hba.conf

# Copy the Bash init script to the image. This will start the Redis server
# and source the backend's Python venv
COPY bash.bashrc /etc/bash.bashrc

# =========================== #
# Fix Missing Directory Error #
# =========================== #
RUN \
    mkdir -p /var/run/postgresql/10-main.pg_stat_tmp && \
    chown -R postgres:postgres /var/run/postgresql/10-main.pg_stat_tmp

EXPOSE 5432

VOLUME /var/lib/postgresql/10/main

USER postgres

ENTRYPOINT ["/usr/lib/postgresql/10/bin/postgres", "-D", "/etc/postgresql/10/main"]
