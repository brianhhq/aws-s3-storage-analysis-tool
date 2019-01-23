#!/usr/bin/env python3
import logging
import os
import boto3
import ast
import multiprocessing as mp

LOG = logging.getLogger()
LOG.addHandler(logging.StreamHandler())


def get_price(location='Asia Pacific (Sydney)', volumeType='Standard'):
    pricing_client = boto3.client('pricing', region_name='us-east-1')
    results = pricing_client.get_products(
        ServiceCode='AmazonS3',
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': location
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'volumeType',
                'Value': volumeType
            },
        ]
    )
    price_list = ast.literal_eval(results['PriceList'][0])

    price = price_list['terms']['OnDemand']['5QVJMK36NJC9G6DC.JRTCKXETXF']['priceDimensions'] \
        ['5QVJMK36NJC9G6DC.JRTCKXETXF.PGHJ3S3EYE']['pricePerUnit']['USD']
    return float(price)


def get_statistics_by_bucket(bucket):
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
    price = get_price()
    result['Cost'] = str(result['Total Size'] * price) + " USD"
    return result


def get_s3_statistics():
    stats = []
    client = boto3.client('s3')
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
