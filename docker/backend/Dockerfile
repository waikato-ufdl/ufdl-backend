# Ubuntu 22.04 with Python 3.10
ARG DOCKER_REGISTRY=public.aml-repo.cms.waikato.ac.nz:443/

# ================== #
# Setup the build OS #
# ================== #
FROM ${DOCKER_REGISTRY}ubuntu:jammy AS build_os
ARG PYTHON=python3.10
RUN \
    # Make sure that we aren't prompted for timezone information
    export DEBIAN_FRONTEND=noninteractive && \
    # Install necessary tools for the build
    apt-get update && \
    apt-get install -y --no-install-recommends git-core libglib2.0-0 libsm6 libxrender-dev libxrender1 libxext6 wget libpq-dev && \
    apt-get install -y build-essential ${PYTHON} ${PYTHON}-dev lib${PYTHON}-dev virtualenv && \
    # Make the root UFDL directory
    mkdir /ufdl
WORKDIR /ufdl

# ==================== #
# Backend Installation #
# ==================== #
FROM build_os AS backend
ARG UFDL_BACKEND_CACHE_INVALIDATION
RUN \
    # Clone the required repos
    git clone https://github.com/waikato-ufdl/ufdl-json-messages.git && \
    git clone https://github.com/waikato-ufdl/ufdl-job-types.git && \
    git clone https://github.com/waikato-ufdl/ufdl-job-contracts.git

COPY ufdl-api-site/ /ufdl/ufdl-backend/ufdl-api-site/
COPY ufdl-core-app/ /ufdl/ufdl-backend/ufdl-core-app/
COPY ufdl-html-client-app/ /ufdl/ufdl-backend/ufdl-html-client-app/
COPY ufdl-image-classification-app/ /ufdl/ufdl-backend/ufdl-image-classification-app/
COPY ufdl-spectrum-classification-app/ /ufdl/ufdl-backend/ufdl-spectrum-classification-app/
COPY ufdl-image-segmentation-app/ /ufdl/ufdl-backend/ufdl-image-segmentation-app/
COPY ufdl-object-detection-app/ /ufdl/ufdl-backend/ufdl-object-detection-app/
COPY ufdl-speech-app/ /ufdl/ufdl-backend/ufdl-speech-app/
COPY dev_init.sh /ufdl/ufdl-backend/

RUN \
    # Run the dev-init script, no prompts, and don't try and reset the database
    cd /ufdl/ufdl-backend && \
    ./dev_init.sh -y -r

# ======================== #
# HTML Client Installation #
# ======================== #
FROM build_os AS frontend
ARG NODE_VERSION=v15.12.0
ARG UFDL_FRONTEND_BRANCH=main
ARG UFDL_FRONTEND_CACHE_INVALIDATION
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
    git checkout $UFDL_FRONTEND_BRANCH && \
    npm install . && \
    npm run rebuild

# ======================== #
# Final Image Construction #
# ======================== #
FROM ${DOCKER_REGISTRY}ubuntu:jammy
ARG PYTHON=python3.10

# Setup the base run-time OS
RUN \
    # Make sure that we aren't prompted for timezone information
    export DEBIAN_FRONTEND=noninteractive && \
    # Install necessary tools for the build
    apt-get update && \
    #apt-get install -y --no-install-recommends git-core libglib2.0-0 libsm6 libxrender-dev libxrender1 libxext6 postgresql wget libpq-dev && \
    apt-get install -y --no-install-recommends postgresql && \
    #apt-get install -y build-essential ${PYTHON} ${PYTHON}-dev lib${PYTHON}-dev virtualenv && \
    apt-get install -y build-essential ${PYTHON} && \
    # Clean up the apt cache
    rm -rf /var/lib/apt/lists/* && \
    # Make the root UFDL directory
    mkdir /ufdl

# Copy over artifacts from backend and frontend builds
COPY --from=backend /ufdl/ufdl-backend/venv.dev /ufdl/ufdl-backend/venv.dev
COPY --from=frontend /ufdl/ufdl-frontend-ts/build /ufdl/static

# Copy in run-time scripts
COPY dev_reset.sh dev_start.sh /ufdl/ufdl-backend/

# Link the HTML client into the static file server
RUN ln -s /ufdl/static /ufdl/ufdl-backend/venv.dev/lib/${PYTHON}/site-packages/ufdl/html_client_app/static

# Add default values for the Postgres environment
ENV UFDL_DATABASE_TYPE=postgresql
ENV UFDL_POSTGRESQL_USER=ufdl
ENV UFDL_POSTGRESQL_PASSWORD=ufdl
ENV UFDL_POSTGRESQL_HOST=localhost

# Copy the Bash init script to the image. This will start the Redis server
# and source the backend's Python venv
COPY docker/backend/bash.bashrc /etc/bash.bashrc

# Start in the root dir of the backend
WORKDIR /ufdl/ufdl-backend

ENTRYPOINT ["./venv.dev/bin/python", "-m", "ufdl.api_site.scripts.run"]

CMD ["-b", "0.0.0.0"]
