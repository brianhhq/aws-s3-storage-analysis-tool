#!/usr/bin/env python3
import logging
import os
import boto3
import datetime
import multiprocessing as mp

LOG = logging.getLogger()
LOG.addHandler(logging.StreamHandler())
cw = boto3.client('cloudwatch', region_name='ap-southeast-2')
client = boto3.client('s3')


def get_statistics_by_bucket(bucket):
    now = datetime.datetime.now()
    result = {
        'Name': bucket['Name'],
        'CreationDate': str(bucket['CreationDate'])
    }
    response_size = cw.get_metric_statistics(
        Namespace='AWS/S3',
        MetricName='BucketSizeBytes',
        Dimensions=[
            {'Name': 'BucketName', 'Value': bucket['Name']},
            {'Name': 'StorageType', 'Value': 'StandardStorage'}
        ],
        Statistics=['Average'],
        Period=3600,
        StartTime=(now - datetime.timedelta(days=2)).isoformat(),
        EndTime=now.isoformat()
    )
    if len(response_size["Datapoints"]) > 0 :
        result['Total Size'] = response_size["Datapoints"][0]['Average']
    response_num_of_files = cw.get_metric_statistics(
        Namespace='AWS/S3',
        MetricName='NumberOfObjects',
        Dimensions=[
            {'Name': 'BucketName', 'Value': bucket['Name']},
            {'Name': 'StorageType', 'Value': 'AllStorageTypes'}
        ],
        Statistics=['Average'],
        Period=3600,
        StartTime=(now - datetime.timedelta(days=2)).isoformat(),
        EndTime=now.isoformat()
    )
    if len(response_num_of_files["Datapoints"]) > 0:
        result['Number of Files'] = response_num_of_files["Datapoints"][0]['Average']

    return result


def get_s3_statistics():
    stats = []
    pool = mp.Pool(4)
    buckets = client.list_buckets()
    for bucket in buckets['Buckets']:
        stat = pool.apply_async(get_statistics_by_bucket, [bucket])
        stats.append(stat.get())
    pool.close()
    return stats


def main():
    results = get_s3_statistics()
    print(results)


if __name__ == "__main__":
    try:
        if os.environ['DEBUG'] == "true":
            LOG.setLevel(logging.DEBUG)
    except KeyError:
        pass
    main()
