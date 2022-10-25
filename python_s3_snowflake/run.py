import requests
import pandas as pd
import numpy as np
import os
import boto3
import json
from dotenv import load_dotenv
import logging
from datetime import date, datetime

# Enable more error logging
# logging.basicConfig(level=logging.DEBUG)

# take environment variables from .env.
load_dotenv()

current_date = date.today()
current_time = datetime.now()

CURRENT_DIR = os.getcwd()
CSV_FILENAME = os.getenv('CSV_FILENAME')
API_URL = os.getenv('API_URL')
MANUFACTURER = os.getenv('MANUFACTURER')
DISTRIBUTOR = os.getenv('DISTRIBUTOR')
LAB = os.getenv('LAB')
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
REGION_NAME = os.getenv('REGION_NAME')
BUCKET_NAME = os.getenv('BUCKET_NAME')

# Create aws session
my_session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION_NAME
)

# Create s3 resource and s3 client
s3 = my_session.resource('s3')
s3_client = my_session.client('s3')

api_requests_dictionary = {
    'distributor': {
        'filename': f'distributor-0-10000_{current_time}.csv',
        'params': {
            'keyword': 'all',
            'skip': 0,
            'take': 10000,
            'discipline': 0,
            'status': 'all',
            'type': 'distributor',
            'profession': 'all'
        }
    },

    # NOTE: Have to break up request because api request limit is 10000
    'manufacturer_1': {
        'filename': f'manufacturer-0-10000_{current_time}.csv',
        'params': {
            'keyword': 'all',
            'skip': 0,
            'take': 10000,
            'discipline': 0,
            'status': 'all',
            'type': 'manufacturer',
            'profession': 'all'
        }
    },
    'manufacturer_2': {
        'filename': f'manufacturer-10000-20000_{current_time}.csv',
        'params': {
            'keyword': 'all',
            'skip': 10000,
            'take': 20000,
            'discipline': 0,
            'status': 'all',
            'type': 'manufacturer',
            'profession': 'all'
        }
    },

    'lab': {
        'filename': f'lab-0-10000_{current_time}.csv',
        'params': {
            'keyword': 'all',
            'skip': 0,
            'take': 10000,
            'discipline': 0,
            'status': 'all',
            'type': 'laboratory',
            'profession': 'all'
        }
    }
}

def request_save_upload():
    for attr, value in api_requests_dictionary.items():
        response = requests.get(
            API_URL,
            params=value['params']
        )

        # api result to json
        response = response.json()

        # JSON response is single quotes. Need to change to double
        normalized_json = pd.json_normalize(response['result'])

        # Create dataframe
        df = pd.DataFrame(normalized_json)

        # save to csv
        df.to_csv(os.path.join(CURRENT_DIR,rf'output/{value["filename"]}'), index=False, sep=',')

        FULL_FILE_PATH = rf'output/{value["filename"]}'

        # save to json
        # df.to_json(os.path.join(CURRENT_DIR,FULL_FILE_PATH), orient="records", lines=True)

        # Create bucket
        s3_client.create_bucket(Bucket=BUCKET_NAME)

        # Upload file into s3
        s3_client.upload_file(FULL_FILE_PATH, BUCKET_NAME, f'input/{current_date.year}/{current_date.month}/{current_date.day}/{value["filename"]}')

request_save_upload()
