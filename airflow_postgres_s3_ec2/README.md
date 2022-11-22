

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

1. Launch new ec2 instance
    - OS Image / Platform: Ubuntu
    - Instance Type: t2.medium
        * Newer versions of Airflow are quite large and will choke out on t2 micro.
    - Add new inbound rule to ec2 Security Group
        * Custom TCP - Port 8080 - 0.0.0.0/0
            - This allows to access Airflows webserver on the ec2 instance

2. SSH into instance
    - Right click on instance, click on 'Connect'
    - Click on SSH client tab
    - Copy ssh command
        * Example: ```ssh -i "your_pem_file.pem" ubuntu@ecX-X-XXX-XXX-XX.compute-1.amazonaws.com```

3. Install dependencies on ec2 instance
    - Update system
        * ```sudo apt update```
        * ```sudo apt upgrade -y```
        * Reboot instance if needed
    - Install python & pip
        * ```sudo apt install python3-pip -y```
        * ```sudo apt install python3.10-venv```

4. Create virtual environment before installing Airflow and Airflow dependencies
    - ```python3 -m venv airflow-venv```
    - ```source airflow-venv/bin/activate```

5. Install Airflow and Airflow dependencies
    - ```sudo apt install -y build-essential libssl-dev libffi-dev python3-dev libpq-dev```
    - ```pip3 install psycopg2```
    - ```pip3 install apache-airflow```
    - ```pip3 install apache-airflow-providers-postgres[amazon]```
    - ```pip3 install apache-airflow-providers-amazon```

6. Check if Airflow was installed successfully
    - ```airflow```
    - If command not found, reboot instance & reconnect via ssh

7. Initialise Airflow
    - ```export AIRFLOW_HOME=~/airflow```
    - ```airflow db init```
    - ```
        airflow users create \
           --username admin \
           --password admin \
           --firstname firstname \
           --lastname lastname \
           --role Admin \
           --email test@airflow.com
        ```
 8. Start Airflow Webserver and scheduler
    - ```airflow webserver -p 8080 -D```
    - ```airflow scheduler -D```
    - The ```-D``` is optional. If you don't want it to be running in the background, then remove it in the above commands.

9. Log into Airflow.
    - Copy your EC2's public ipv4 DNS.
        * Should look something like ```ec2-X-XXX-XXX-XX.compute-1.amazonaws.com```
    - Go to browser and test connection. Make sure to add colon and port
        * Example: ```http://ecX-X-XXX-XXX-XX.compute-1.amazonaws.com:8080/```
    - Enter username & password into Airflow



#### Setting up RDS PostgreSQL

1. Launch RDS PostgreSQL
    - Standard Create
    - PostgreSQL
    - Instance Name
    - Port: 5432
    - Username
    - Password
    - Templates: Free Tier
    - Storage: 20 GiB

2. Copy RDS PostgreSQL endpoint
    - Example: ```asdfasdf.asdfasdfasdf.us-east-1.rds.amazonaws.com```

#### Connect RDS PostgreSQL to PGAdmin

1. Register - Server
    - NAME: rds instance name
    - HOST NAME / ADDRESS: rds endpoint
    - PORT: 5432
    - USERNAME: rds username
    - PASSWORD: rds password

2. Create aws extension
    - In PGAdmin and connected to RDS. Enter the query:
        * ```CREATE EXTENSION aws_s3 CASCADE;```

#### Create AWS S3 bucket

1. Create bucket
    - Bucket name

#### 
