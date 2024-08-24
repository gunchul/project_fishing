#!/bin/bash

if [ -z "${MODULE}" ]; then
    echo "Error: MODULE is not defined"
    exit 1
fi

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

LOGFILE="log/${MODULE}_log.txt"
ERROR_LOGFILE="log/${MODULE}_log_error_at_${TIMESTAMP}.txt"

python ${MODULE}.py > ${LOGFILE} 2>&1

if [ $? -ne 0 ]; then
    python error_handle.py ${MODULE} ${LOGFILE}
    mv ${LOGFILE} ${ERROR_LOGFILE}
fi
