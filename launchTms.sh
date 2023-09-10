#!/bin/bash

export PYTHONPATH=/home/kmarszal/Documents/dev/avgvis
python ./tms/test_utils/tms_cli/tms_cli.py "$@" tms/test_utils/testGraph.json
