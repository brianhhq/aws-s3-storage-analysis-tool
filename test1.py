import boto3
import ast
pricing = boto3.client('pricing', region_name='us-east-1')
results = pricing.get_products(
    ServiceCode='AmazonS3',
    Filters=[
        {
            'Type': 'TERM_MATCH',
            'Field': 'location',
            'Value': 'Asia Pacific (Sydney)'
        },

        {
            'Type': 'TERM_MATCH',
            'Field': 'volumeType',
            'Value': 'Standard'
        },

    ]
)
price_list = ast.literal_eval(results['PriceList'][0])

print(price_list['terms']['OnDemand']['5QVJMK36NJC9G6DC.JRTCKXETXF']['priceDimensions']['5QVJMK36NJC9G6DC.JRTCKXETXF.PGHJ3S3EYE']['pricePerUnit']['USD'])

# s = pricing.describe_services(ServiceCode='AmazonS3')
# print(s)
#
# response = pricing.get_attribute_values(
#     ServiceCode='AmazonS3',
#     AttributeName='productFamily'
# )
# print(response)





