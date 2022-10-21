#!/bin/bash
#
# Script Name: init.sh
#
# Author: James LeBoeuf
# Date : 10/20/2022
#
# Description: The following script is for system setup
#              i.e. 'pip install'
#
# Run Information: This script is run based on user demand and it not
#                  automatic. There is no cron job associated.
#
# Important: Don’t store your Python scripts and your requirements.txt
# file inside your Python virtual environment.

# SET VARIABLES
DATE_TIME=`date '+%b %d %Y %H:%M:%S'`
VENV_NAME='venv'
PROJECT_NAME='python_s3_snowflake'

# UPDATE SYSTEM
echo "[PROCESS:] UPDATING SYSTEM"
sudo apt-get update

# UPGRADE SYSTEM
echo "[PROCESS:] UPGRADING SYSTEM"
sudo apt upgrade -y

# Install python 3
echo "[PROCESS:] INSTALLING PYTHON3"
sudo apt install python3.8 -y

# Install aws-cli
echo "[PROCESS:] INSTALLING AWS-CLI"
sudo apt install awscli -y

# pip3 is not installed on the server by default.
echo "[PROCESS:] INSTALLING PIP3"
sudo apt install python3-pip -y

# Install virtualenv
echo "[PROCESS:] INSTALLING VIRTUALENV"
sudo apt install python3-virtualenv -y

# Now that virtualenv is installed, create a virtual environment
echo "[PROCESS:] CREATING VIRTUALENV"
virtualenv -p python3 ${VENV_NAME}

# Before installing or using packages in your new Python virtual environment, you need to activate it.
echo "[PROCESS:] ACTIVATING VIRTUALENV"
source ${VENV_NAME}/bin/activate

# Install requirements from .txt file
echo "[PROCESS:] INSTALLING REQUIREMENTS"
pip3 install -r requirements.txt

# Deactivate
echo "[PROCESS:] DEACTIVATING VIRTUALENV"
deactivate

# chmod for run.sh script
echo "[PROCESS:] CHANGE PERMISSIONS ON RUN SCRIPT"
chmod a+x run.sh

# Make log directory
echo "[PROCESS:] CREATE LOG DIRECTORY"
mkdir -p log
