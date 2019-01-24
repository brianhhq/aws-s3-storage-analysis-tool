import unittest
import logging
import os
from s3statistics import S3Statistics
import json

LOG = logging.getLogger()
LOG.addHandler(logging.StreamHandler())


class S3StatisticsTestCase(unittest.TestCase):

    def setUp(self):
        try:
            if os.environ['DEBUG'] == "true":
                LOG.setLevel(logging.DEBUG)
        except KeyError:
            pass
        self.aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', '')
        self.aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

    def tearDown(self):
        """ clean up tmp files after each test """
        pass

    def test_get_price(self):
        s3_stats = S3Statistics(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
        price = s3_stats.get_price()
        self.assertTrue(price == 0.025)

    def test_get_statistics_by_bucket(self):
        expected_result = {'Name': 'brianhhq-test', 'CreationDate': '2019-01-24 04:48:52+00:00', 'LastModified': '2019-01-24 08:28:52+00:00', 'Number of Files': 1, 'Total Size': '1.143e-06 G', 'Size by Type': {'STANDARD': 1143, 'STANDARD_IA': 0, 'ONEZONE_IA': 0, 'REDUCED_REDUNDANCY': 0, 'GLACIER': 0}, 'Cost': '2.8575e-08 USD'}
        bucket = {
            'Name': 'brianhhq-test',
            'CreationDate': '2019-01-24 04:48:52+00:00'
        }
        s3_stats = S3Statistics(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
        stat = s3_stats.get_statistics_by_bucket(bucket)
        self.assertTrue(expected_result == stat)

    def test_get_s3_statistics(self):
        expected_result = [{"Name": "brianhhq-test", "CreationDate": "2019-01-24 04:48:52+00:00", "LastModified": "2019-01-24 08:28:52+00:00", "Number of Files": 1, "Total Size": "1.143e-06 G", "Size by Type": {"STANDARD": 1143, "STANDARD_IA": 0, "ONEZONE_IA": 0, "REDUCED_REDUNDANCY": 0, "GLACIER": 0}, "Cost": "2.8575e-08 USD"}]
        expected_result = json.dumps(expected_result)
        s3_stats = S3Statistics(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
        stats = s3_stats.get_s3_statistics()
        self.assertTrue(expected_result == stats)
