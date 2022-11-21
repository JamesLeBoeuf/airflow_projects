import airflow
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta, date

import requests
import boto3
import logging
import pandas as pd
import json
import os

AWS_ACCESS_KEY = Variable.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = Variable.get('AWS_SECRET_KEY')
AWS_REGION_NAME = Variable.get('AWS_REGION_NAME')
AWS_BUCKET_NAME = Variable.get('AWS_BUCKET_NAME')
API_ENDPOINT = Variable.get('API_ENDPOINT')
CURRENT_DATE = date.today()
CURRENT_DIR = os.getcwd()

# Create aws session
my_session = boto3.Session(
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_KEY,
    region_name = AWS_REGION_NAME
)

s3_client = my_session.client('s3')

# Grabs data from api endpoint and saves to csv in ouput folder
def save_to_csv():
    
    # Get data from API
    res = requests.get(API_ENDPOINT)

    # api result to json
    response = res.json()

    # JSON response is single quotes. Need to change to double
    normalized_json = pd.json_normalize(response['result'])
    
    # Create dataframe
    df = pd.DataFrame(normalized_json)

    # save to csv
    df.to_csv(os.path.join(CURRENT_DIR,rf'output/test.csv'), index=False, sep=',') 


# Upload csv to s3
def upload_to_s3():

    # Create bucket
    s3_client.create_bucket(Bucket=AWS_BUCKET_NAME)

    FULL_FILE_PATH = rf'output/test.csv'

    # upload_file
    s3_client.upload_file(FULL_FILE_PATH, AWS_BUCKET_NAME, f'input/test.csv')


# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1)
}

create_table_sql = """
        CREATE TABLE IF NOT EXISTS business (
        primary_id SERIAL PRIMARY KEY,
        id VARCHAR NOT NULL,
        licenseNumber VARCHAR NOT NULL,
        legalName VARCHAR,
        tradeName VARCHAR,
        licenseType VARCHAR,
        streetAddress VARCHAR,
        city VARCHAR,
        county VARCHAR,
        licenseExpiryDate VARCHAR,
        zip VARCHAR,
        phone VARCHAR,
        email VARCHAR,
        hours VARCHAR,
        dataSourceName VARCHAR,
        discloseAddress VARCHAR);
        """
upload_to_postgres_sql = f"SELECT \
        aws_s3.table_import_from_s3( \
            'business', \
            'id, licenseNumber, legalName, tradeName, licenseType, streetAddress, city, county, licenseExpiryDate, zip, phone, email, hours, dataSourceName, discloseAddress', \
            '(format csv, HEADER true)', \
            '{AWS_BUCKET_NAME}', \
            'input/test.csv', \
            '{AWS_REGION_NAME}' \
        );"

dag = DAG(
    'intermediary_data_storage_dag',
    start_date = datetime(2021, 1, 1),
    max_active_runs = 1,
    schedule_interval = '@daily',
    default_args = default_args,
    catchup = False
)

generate_file_task = PythonOperator(
    task_id = 'generate_file',
    python_callable = save_to_csv,
    dag = dag
)

upload_file_task = PythonOperator(
    task_id = 'upload_file',
    python_callable = upload_to_s3,
    dag = dag
)

create_pg_table_task = PostgresOperator(
    task_id = 'create_pg_table',
    sql = create_table_sql,
    dag = dag
)

s3_upload_to_postgres_task = PostgresOperator(
    task_id = "upload_dol_data_to_postgres",
    postgres_conn_id = "postgres_default",
    sql = upload_to_postgres_sql,
    dag = dag
)

dummy_task = DummyOperator(
    task_id = 'dummy_task',
    retries = 3,
    dag = dag
)

generate_file_task >> upload_file_task >> create_pg_table_task >> s3_upload_to_postgres_task >> dummy_task