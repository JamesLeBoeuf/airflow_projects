#!/usr/bin/env bash

# Initiliase the metastore
airflow db init

# Run the scheduler in background
airflow scheduler &> /dev/null &

# Create user
airflow users create \
    --username admin \
    --password admin \
    --firstname firstname \
    --lastname lastname \
    --role Admin \
    --email test@airflow.com

# Run the web server in foreground (for docker logs)
exec airflow webserver