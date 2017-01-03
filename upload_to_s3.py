import sys
from sys import argv

import boto
from boto.s3.key import Key

AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXX'
AWS_SECRET_ACCESS_KEY = 'XXXXXXXXXXXXX'
S3_HOST = 's3-ap-southeast-1.amazonaws.com'
BASE_URL = 'http://xyz.com'


def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()


def get_file_public_url(base_url, bucket_key, cache_control='max-age=2592000,public'):
    metadata = bucket_key.metadata
    metadata['Cache-Control'] = cache_control
    return base_url + bucket_key.key


def upload_to_s3_bucket(aws_key_id, aws_secret_key, bucket_name, source_file, destination, s3_host=S3_HOST):
    print("Starting upload...")
    conn = boto.connect_s3(aws_key_id, aws_secret_key, host=s3_host)
    k = Key(conn.get_bucket(bucket_name))
    k.key = '/' + destination
    upload_file = k.set_contents_from_filename(source_file, policy='public-read', cb=percent_cb, num_cb=10)
    if upload_file:
        return k
    else:
        return False


script, bucket_name, source_file, destination = argv
try:
    if upload_to_s3_bucket(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, bucket_name, source_file, destination):
        public_url = get_file_public_url(BASE_URL, k)
        print("File upload successfully. Your public URL is:-")
        print(public_url)
    else:
        raise Exception
except Exception as e:
    print("Upload failed.")
    print("Error: " + str(e))
