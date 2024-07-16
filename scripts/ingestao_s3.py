import boto3
from datetime import datetime
from botocore.exceptions import ClientError

s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIAQDRB6H65UPQSE2LJ',
    aws_secret_access_key='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',
    region_name='us-east-1'
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
