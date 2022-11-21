

# Overview

The purpose of this project is to show how to use Airflow to take JSON data from an API endpoint and insert it into a Postgres database.

## How it works

![Basic Dag Flow](./basic_dag_flow.png)

## Built With

* Postgres
* Airflow
* Python
* S3
* EC2

## Prerequisites
* AWS RDS Postgres instance
* AWS EC2 instance
* AWS S3 bucket

### Setup
#### Setting up EC2 on AWS
Requirements
* Size: t2 medium
* * Newer versions of Airflow are quite large and will choke out on t2 micro and t2 small.
* Platform: Ubuntu
* Security Group Settings: add port 8080
* * This allows to access airflow's webserver

Upgrade/update system & install pip & python
* ```sudo apt update```
* ```sudo apt upgrade -y```
* Oftentimes when upgrading an instance, it's recommended to reboot the instance.
* ```sudo apt install python3-pip -y```
* ```sudo apt install python3.10-venv```

Create virtual environment before installing airflow and airflow dependencies
* ```python3 -m venv airflow-venv```
* ```source airflow-venv/bin/activate```

Install airflow and airflow dependencies
* ```sudo apt install -y build-essential libssl-dev libffi-dev python3-dev libpq-dev```
* ```pip3 install psycopg2```
* ```pip3 install apache-airflow```
* ```pip3 install apache-airflow-providers-postgres[amazon]```
* ```pip3 install apache-airflow-providers-amazon```

Check if airflow was installed successfully by running
* ```airflow```
* If command not found, reboot instance & reconnect via ssh

Initialising Airflow
* ```export AIRFLOW_HOME=~/airflow```
* ```airflow db init```
* ```
    airflow users create \
       --username admin \
       --password admin \
       --firstname firstname \
       --lastname lastname \
       --role Admin \
       --email test@airflow.com
    ```

#### Setting up RDS Postgres
Requirements
* Port: 5432
* Connect RDS Instance via PGAdmin or DBeaver. Run command to create s3 extension
* * ```CREATE EXTENSION aws_s3 CASCADE;```
