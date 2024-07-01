import boto3

from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    userId = event["sub"]

    table = boto3.resource('dynamodb').Table('Devices')

    try:
        devices = table.scan(
            FilterExpression=Attr('userId').eq(userId)
        )
        
    except Exception as e:
        return {
            "error": True,
            "success": False,
            "message": str(e)
        }

    return {
        "error": False,
        "success": True,
        "message": "Devices retrieved successfuly",
        "data": [item['deviceId'] for item in  devices['Items']]
    }

