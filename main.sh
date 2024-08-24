#!/bin/bash

if [ -z "${MODULE}" ]; then
    echo "Error: MODULE is not defined"
    exit 1
fi

source /home/kelly_je_kim/venv/kellyenv/bin/activate

(cd /home/kelly_je_kim/project_fishing && ./execute_module.sh)

