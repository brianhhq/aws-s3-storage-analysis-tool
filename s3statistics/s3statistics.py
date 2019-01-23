import boto3
import datetime
import multiprocessing as mp


class S3Statistics:
    client = {}
    cw = {}
    stats = []
    aws_access_key_id = ''
    aws_secret_access_key = ''
    region_name = ''

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name='ap-southeast-2'):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.cw = boto3.client(
            'cloudwatch',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )
        self.client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )

    def get_statistics_by_bucket(self, bucket):
        now = datetime.datetime.now()
        result = {
            'Name': bucket['Name'],
            'CreationDate': str(bucket['CreationDate'])
        }
        response_size = self.cw.get_metric_statistics(
            Namespace='AWS/S3',
            MetricName='BucketSizeBytes',
            Dimensions=[
                {'Name': 'BucketName', 'Value': bucket['Name']},
                {'Name': 'StorageType', 'Value': 'StandardStorage'}
            ],
            Statistics=['Average'],
            Period=3600,
            StartTime=(now-datetime.timedelta(days=2)).isoformat(),
            EndTime=now.isoformat()
        )
        result['Total Size'] = response_size["Datapoints"][0]['Average']

        response_num_of_files = self.cw.get_metric_statistics(
            Namespace='AWS/S3',
            MetricName='NumberOfObjects',
            Dimensions=[
                {'Name': 'BucketName', 'Value': bucket['Name']},
                {'Name': 'StorageType', 'Value': 'AllStorageTypes'}
            ],
            Statistics=['Average'],
            Period=3600,
            StartTime=(now-datetime.timedelta(days=2)).isoformat(),
            EndTime=now.isoformat()
        )
        result['Number of Files'] = response_num_of_files["Datapoints"][0]['Average']
        return result

    def get_s3_statistics(self):
        pool = mp.Pool(4)
        buckets = self.client.list_buckets()
        for bucket in buckets['Buckets']:
            stat = pool.apply_async(self.get_statistics_by_bucket, [bucket])
            self.stats.append(stat.get())
        pool.close()
        return self.stats
