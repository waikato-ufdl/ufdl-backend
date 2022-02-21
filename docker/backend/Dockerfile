# Ubuntu 18.04 with Python 3.7
ARG DOCKER_REGISTRY=public.aml-repo.cms.waikato.ac.nz:443/
FROM ${DOCKER_REGISTRY}ubuntu:bionic

ARG PYTHON=python3.7
ARG NODE_VERSION=v15.12.0

# ======== #
# OS Setup #
# ======== #
RUN \
    # Make sure that we aren't prompted for timezone information
    export DEBIAN_FRONTEND=noninteractive && \
    # Install necessary tools for the build
    apt-get update && \
    apt-get install -y --no-install-recommends git-core libglib2.0-0 libsm6 libxrender-dev libxrender1 libxext6 postgresql wget && \
    apt-get install -y build-essential ${PYTHON} ${PYTHON}-dev lib${PYTHON}-dev virtualenv && \
    # Clean up the apt cache
    rm -rf /var/lib/apt/lists/*

# ==================== #
# Backend Installation #
# ==================== #
RUN \
    # Create and change into base directory
    mkdir /ufdl && \
    cd /ufdl && \
    # Clone the required repos
    git clone https://github.com/waikato-ufdl/ufdl-json-messages.git && \
    git clone https://github.com/waikato-ufdl/ufdl-backend.git && \
    git clone https://github.com/waikato-ufdl/ufdl-job-types.git && \
    git clone https://github.com/waikato-ufdl/ufdl-job-contracts.git && \
    # Run the dev-init script, no prompts, and don't try and reset the database
    cd /ufdl/ufdl-backend && \
    ./dev_init.sh -y -r

# ======================== #
# HTML Client Installation #
# ======================== #
RUN \
    # Download and install Node.js, adding it to PATH
    cd / && \
    wget https://nodejs.org/dist/${NODE_VERSION}/node-${NODE_VERSION}-linux-x64.tar.xz && \
    tar xJf node-${NODE_VERSION}-linux-x64.tar.xz && \
    export PATH=$PATH:/node-${NODE_VERSION}-linux-x64/bin && \
    # Clone the required repos
    cd /ufdl && \
    git clone https://github.com/waikato-ufdl/ufdl-ts-client.git && \
    git clone https://github.com/waikato-ufdl/ufdl-frontend-ts.git && \
    # Build the TypeScript client
    cd /ufdl/ufdl-ts-client && \
    npm install . && \
    npm run rebuild && \
    # Build the HTML client
    cd /ufdl/ufdl-frontend-ts && \
    npm install . && \
    npm run rebuild && \
    # Copy the HTML client build into the server directory (for serving)
    cp -rf /ufdl/ufdl-frontend-ts/build /ufdl/ufdl-backend/venv.dev/lib/${PYTHON}/site-packages/ufdl/html_client_app/static && \
    # Remove Node.js and the repos as they are no longer required
    cd / && \
    rm -rf node-${NODE_VERSION}-linux-x64.tar.xz node-${NODE_VERSION}-linux-x64 && \
    cd ufdl && \
    rm -rf ufdl-ts-client ufdl-frontend-ts

# Add default values for the Postgres environment
ENV UFDL_POSTGRESQL_USER=ufdl
ENV UFDL_POSTGRESQL_PASSWORD=ufdl
ENV UFDL_POSTGRESQL_HOST=localhost

# Copy the Bash init script to the image. This will start the Redis server
# and source the backend's Python venv
COPY bash.bashrc /etc/bash.bashrc

# Start in the root dir of the backend
WORKDIR /ufdl/ufdl-backend

ENTRYPOINT ["./venv.dev/bin/python", "-m", "ufdl.api_site.scripts.manage"]

CMD ["runserver", "0.0.0.0:8000"]
