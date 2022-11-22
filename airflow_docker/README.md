# Overview
Dockerfile that will build python3.10 with Airflow latest (2.4.3). Also included in the build is postgres and amazon apache-airflow extensions.

## Setup
1. Clone repo
2. Change any user credentials in entrypoint.sh file or leave as default
3. Build docker image
  - ```docker build -t <IMAGE-NAME>:<TAG> -f Dockerfile . --no-cache```
4. Visit http://0.0.0.0:8080 or http://localhost:8080 to test

## Alternative Setup
1. This image was pushed to Docker Hub so if you'd like to pull it visit:
  - https://hub.docker.com/repository/docker/jamesleboeuf/airflow
