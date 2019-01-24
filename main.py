#!/usr/bin/env python3
import logging
import os
from s3statistics import S3Statistics

LOG = logging.getLogger()
LOG.addHandler(logging.StreamHandler())

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', '')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '')


def main():
    """
    Entry point function
    :return:
    """
    s3_stats = S3Statistics(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    results = s3_stats.get_s3_statistics()
    print(results)


if __name__ == "__main__":
    """
    Entry point of a program
    """
    try:
        if os.environ['DEBUG'] == "true":
            LOG.setLevel(logging.DEBUG)
    except KeyError:
        pass
    main()
