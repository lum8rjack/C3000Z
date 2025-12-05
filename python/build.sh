#!/bin/bash

docker build -t c3000z .

# Run using the following command
#docker run --rm -v $(pwd)/<your config file>.xml:/app/config.xml c3000z
