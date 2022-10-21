#!/bin/bash
#
# Script Name: run.sh
#
# Author: James LeBoeuf
# Date : 10/20/2022
#
# Description: The following script is for python script setup
#
# Run Information: This script is run based on user demand and it not
#                  automatic. There is no cron job associated.
#
# Error Log: Any errors or output associated with the script can be
#            found in /log folder

# SET VARIABLES
DATE_TIME=`date '+%b %d %Y %H:%M:%S'`
SHELL_SCRIPT_NAME='run'
VENV_NAME='venv'
PROJECT_NAME='python_s3_snowflake'
CURRENT_DIR=$(pwd)
LOGS_DIR=${CURRENT_DIR}/log
LOG_FILE=${LOGS_DIR}/${SHELL_SCRIPT_NAME}.log

echo "[JOB:] PYTHON SCRIPT SETUP"

# SET LOG RULES
echo "[PROCESS:] SETTING LOG RULES"
exec 2> >(tee ${LOG_FILE} >&2)

# Activate python3
echo "[PROCESS:] ACTIVATING VIRTUALENV"
source ${VENV_NAME}/bin/activate

# Run python script
echo "[PROCESS:] RUNNING PYTHON SCRIPT"
python3 run.py


RETURN_CODE=$?
if [[ ${RETURN_CODE} != 0 ]]; then
    echo "[ERROR]: PYTHON SCRIPT ERROR"
    echo "[ERROR]: [CODE]: ${RETURN_CODE}"
    exit 1
else
    echo "[SUCCESS]: PYTHON SCRIPT SETUP COMPLETE"
fi

echo "[JOB]: PYTHON SCRIPT SETUP COMPLETED SUCCESSFULLY"

deactivate

exit 0
