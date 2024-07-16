import boto3
from datetime import datetime
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')

s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

today = datetime.today().strftime('%Y-%m-%d')
parquet_file = f'dados_{today}.parquet'

directory_name = 'parquet'
bucket_name = 'bucketfiap'
s3_path = f'{directory_name}/dados_{today}.parquet'

try:
    s3_client.upload_file(parquet_file, bucket_name, s3_path)
    print("Upload bem-sucedido!")
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == 'SignatureDoesNotMatch':
        print(f"Erro de assinatura: {e}")
    else:
        print(f"Erro ao fazer upload: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")