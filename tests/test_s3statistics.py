import unittest
import logging
import os
from s3statistics import S3Statistics

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

    # def test_get_statistics_by_bucket(self):
    #     s3_stats = S3Statistics(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    #     stat = s3_stats.get_statistics_by_bucket()
    #     self.assertTrue(1 == 1)
    #
    # def test_get_s3_statistics(self):
    #     s3_stats = S3Statistics(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    #     stats = s3_stats.get_s3_statistics()
    #     self.assertTrue(1 == 1)
