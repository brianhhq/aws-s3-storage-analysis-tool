#!/usr/bin/env python3
import boto3
import multiprocessing as mp


def get_bucket_info(bucket):
    total_size = 0
    num_of_files = 0
    result = {
        'Name': bucket['Name'],
        'CreationDate': str(bucket['CreationDate'])
    }
    session = boto3.session.Session()
    s3_session = session.resource('s3')
    b = s3_session.Bucket(result['Name'])
    for item in b.objects.all():
        num_of_files += 1
        total_size += item.size
    result['Number of Files'] = num_of_files
    result['Total Size'] = total_size / 1000000000
    return result


if __name__ == "__main__":
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    pool = mp.Pool(4)
    results = []
    for bucket_item in response['Buckets']:
        r = pool.apply_async(get_bucket_info, [bucket_item])
        results.append(r.get())
    pool.close()
    print(results)
