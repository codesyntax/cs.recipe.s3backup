import boto3
import botocore
import os
import logging
import sys


def _setup_logging():
    root_logger = logging.getLogger()
    log_format = '%(name)s: %(message)s'
    buildout_handler = logging.StreamHandler(sys.stdout)
    buildout_handler.setFormatter(logging.Formatter(log_format))
    root_logger.propagate = False
    root_logger.addHandler(buildout_handler)
    log = logging.getLogger('backup')
    log.setLevel(logging.INFO)


def backup(filepaths=[],
           directories=[],
           AWS_ACCESS_KEY_ID=None,
           AWS_SECRET_ACCESS_KEY=None,
           AWS_BUCKET_NAME=None,
           overwrite=False):

    _setup_logging()
    log = logging.getLogger('backup')

    s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        s3.meta.client.head_bucket(Bucket=AWS_BUCKET_NAME)
        bucket = s3.Bucket(AWS_BUCKET_NAME)
        for filepath in filepaths:
            filename = os.path.basename(filepath)
            if not overwrite:
                if filename in [item.key for item in bucket.objects.all()]:
                    log.warning('Item {} already exists. Not overwriten.'.format(filepath))
                    continue
            s3.Object(AWS_BUCKET_NAME, filename).put(Body=open(filepath, 'rb'))
            log.info('Item {} copied.'.format(filepath))

        for directory in directories:
            for root, dirs, files in os.walk(directory):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    s3.Object(AWS_BUCKET_NAME, filename).put(Body=open(filepath, 'rb'))
        return 0

    except botocore.exceptions.ClientError as e:
        log.exception(e)
        log.error('Bucket does not exist')
        return 1
