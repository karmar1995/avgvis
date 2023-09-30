#!/bin/bash

export PYTHONPATH=`pwd`
python3 ./tms/test_utils/tms_cli/tms_cli.py "$@" tms/test_utils/testGraph.json
