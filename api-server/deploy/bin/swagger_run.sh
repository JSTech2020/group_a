#!/bin/bash

if [ "$PROJECT_DIR" = "" ]; then
PROJECT_DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )/../..
fi

sudo docker run -p 8080:8080 -v $PROJECT_DIR/api/dist:/swagger -e SWAGGER_JSON=/swagger/swagger.json swaggerapi/swagger-ui