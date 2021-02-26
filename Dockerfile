FROM python:3.9.1-alpine
LABEL maintainer="Social Systems SRE Team <sre@socialsystems.com>"

# Build arguments
ARG SRC_DIR="/usr/src/sereno"
ARG USER="socialsystems"
ARG USER_ID=101
ARG USER_GROUP="socialsystems"
ARG USER_GROUP_ID=101
ARG USER_HOME="/home/${USER}"

# Create a non-root user and group, and create source dir
RUN addgroup -S -g ${USER_GROUP_ID} ${USER_GROUP} \
    && adduser -S -u ${USER_ID} -h ${USER_HOME} -G ${USER_GROUP} ${USER} \
    && mkdir -p ${SRC_DIR}

# Add source files
ADD . ${SRC_DIR}/

# Install sereno
WORKDIR ${SRC_DIR}
RUN python3 setup.py install

# Set the user and work directory
USER ${USER_ID}
WORKDIR ${USER_HOME}

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/sereno"]
