#!/bin/bash

docker-compose up --build

./scripts/copy_files_to_volume.sh ./src/frontend/media authentication_media_volume
./scripts/copy_files_to_volume.sh ./src/frontend/static authentication_static_volume
./scripts/copy_files_to_volume.sh ./src/frontend/pages authentication_pages_volume

echo "Initialization complete."