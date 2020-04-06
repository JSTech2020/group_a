#!/bin/bash


if [ "$PROJECT_DIR" = "" ]; then
PROJECT_DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )/../..
fi

docker build \
    -t frontend \
    -f $PROJECT_DIR/deploy/docker/Dockerfile \
    $PROJECT_DIR

