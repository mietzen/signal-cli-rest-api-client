#!/bin/bash

source signal-cli-rest-api-client/bin/activate
python ./signal-cli-rest-api-client.py "$@"

exit 0
