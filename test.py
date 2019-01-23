import boto3
import datetime

now = datetime.datetime.now()

client = boto3.client('ce')


response = client.get_cost_and_usage(
    TimePeriod={
        'Start': '2019-01-01',
        'End': '2019-01-22'
    },
    Granularity='MONTHLY',
    Metrics=[
        'BlendedCost',
    ],
    Filter={
        "Dimensions": {
            "Key": "SERVICE",
            "Values": [
                "Amazon Simple Storage Service"
            ]
        }
    }
)

print(response)
