#!/bin/sh

set -e

usage() {
  echo "Usage: $0 <local_dir> <volume_name>"
  exit 1
}

if [ $# -ne 2 ]; then
  usage
fi

LOCAL_DIR=$1
VOLUME_NAME=$2

if [ ! -d "${LOCAL_DIR}" ]; then
  echo "Error: ${LOCAL_DIR} does not exist or is not a directory."
  exit 1
fi

WIN_LOCAL_DIR=$(cd "${LOCAL_DIR}" && pwd -W)

MSYS_NO_PATHCONV=1 docker run --rm \
  -v "${VOLUME_NAME}:/data" \
  -v "${WIN_LOCAL_DIR}:/src" \
  alpine sh -c "mkdir -p /data && cp -R /src/. /data/"

echo "Files from ${LOCAL_DIR} have been copied to the Docker volume ${VOLUME_NAME}."
