import boto3
import ast


class S3Statistics:
    s3_client = {}
    s3_resource = {}
    pricing_client = {}
    stats = []
    aws_access_key_id = ''
    aws_secret_access_key = ''
    region_name = ''

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name='ap-southeast-2'):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.s3_resource = boto3.resource('s3',
                                          region_name=self.region_name,
                                          aws_access_key_id=self.aws_access_key_id,
                                          aws_secret_access_key=self.aws_secret_access_key)
        self.s3_client = boto3.client('s3',
                                      region_name=self.region_name,
                                      aws_access_key_id=self.aws_access_key_id,
                                      aws_secret_access_key=self.aws_secret_access_key)
        self.pricing_client = boto3.client('pricing',
                                           region_name='us-east-1',
                                           aws_access_key_id=self.aws_access_key_id,
                                           aws_secret_access_key=self.aws_secret_access_key)

    def get_price(self, location='Asia Pacific (Sydney)', volume_type='Standard'):
        results = self.pricing_client.get_products(
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
                    'Value': volume_type
                },
            ]
        )
        price_list = ast.literal_eval(results['PriceList'][0])

        price = price_list['terms']['OnDemand']['5QVJMK36NJC9G6DC.JRTCKXETXF']['priceDimensions'] \
            ['5QVJMK36NJC9G6DC.JRTCKXETXF.PGHJ3S3EYE']['pricePerUnit']['USD']
        return float(price)

    def get_statistics_by_bucket(self, bucket):
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

        objs = self.s3_resource.Bucket(result['Name'])

        object_summary_iterator = objs.objects.all()
        for obj in object_summary_iterator:
            type_size[obj.storage_class] += obj.size
            total_size += obj.size
            num_of_files += 1
            if int(obj.last_modified.strftime('%s')) > last_modified_strftime:
                result['LastModified'] = str(obj.last_modified)
        result['Number of Files'] = num_of_files
        total_size = total_size / 1000000000
        result['Total Size'] = str(total_size) + ' G'
        result['Size by Type'] = type_size
        price = self.get_price()
        result['Cost'] = str(total_size * price) + " USD"
        return result

    def get_s3_statistics(self):
        buckets = self.s3_client.list_buckets()
        for bucket in buckets['Buckets']:
            if bucket['Name'] == 'annamonitoring' or bucket['Name'] == 'ha-cloudtrail':
                continue
            stat = self.get_statistics_by_bucket(bucket)
            self.stats.append(stat)
        pool.close()
        return self.stats
