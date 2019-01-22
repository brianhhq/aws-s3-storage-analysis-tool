#!/usr/bin/env python3
import boto3


def main():
    results=[]
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    for bucket in response['Buckets']:
        total_size = 0
        num_of_files = 0
        result = {
            'Name': bucket['Name'],
            'CreationDate': str(bucket['CreationDate'])
        }
        bucket = boto3.resource('s3').Bucket(result['Name'])
        for item in bucket.objects.all():
            num_of_files += 1
            total_size += item.size
        result['Number of Files'] = num_of_files
        result['Total Size'] = total_size / 1000000000
        results.append(result)
        print(result)
    print(results)


if __name__ == "__main__":
    main()