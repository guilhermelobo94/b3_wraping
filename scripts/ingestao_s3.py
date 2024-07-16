import boto3
import os
from datetime import datetime

s3_client = boto3.client(
    's3',
    aws_access_key_id='fiap_b3',
    aws_secret_access_key='fiap_b3@',
    region_name='us-east-1'
)

today = datetime.today().strftime('%Y-%m-%d')

parquet_file = f'dados_{today}.parquet'

s3_client = boto3.client('s3')

directory_name = 'parquet_data'

bucket_name = 'bucket_fiap'

s3_path = f'{directory_name}/dados_{today}.parquet'


s3_client.upload_file(parquet_file, bucket_name, s3_path)

os.remove(parquet_file)

print(f'Arquivo {parquet_file} enviado para s3://{bucket_name}/{s3_path}')