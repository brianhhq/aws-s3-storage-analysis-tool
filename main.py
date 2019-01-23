#!/usr/bin/env python3
import boto3
import multiprocessing as mp


get_last_modified = lambda obj: int(obj.last_modified.strftime('%s'))

s3 = boto3.client('s3')


def get_bucket_info(bucket):
    total_size = 0
    num_of_files = 0
    last_modified_strftime = 0
    type_size = {
        'STANDARD': 0,
        'STANDARD_IA': 0,
        'ONEZONE_IA': 0,
        'REDUCED_REDUNDANCY': 0,
        'GLACIER': 0
    }
    result = {
        'Name': bucket['Name'],
        'CreationDate': str(bucket['CreationDate'])
    }

    session = boto3.session.Session()
    s3_session = session.resource('s3')
    b = s3_session.Bucket(result['Name'])

    object_summary_iterator = b.objects.all()
    for obj in object_summary_iterator:
        type_size[obj.storage_class] += obj.size
        total_size += obj.size
        num_of_files += 1
        if int(obj.last_modified.strftime('%s')) > last_modified_strftime:
            result['LastModified'] = str(obj.last_modified)

    result['Number of Files'] = num_of_files
    result['Total Size'] = total_size / 1000000000
    result['Size by Type'] = type_size
    return result


if __name__ == "__main__":
    response = s3.list_buckets()
    pool = mp.Pool(4)
    results = []
    for bucket_item in response['Buckets']:
        r = pool.apply_async(get_bucket_info, [bucket_item])
        results.append(r.get())
    pool.close()
    print(results)
