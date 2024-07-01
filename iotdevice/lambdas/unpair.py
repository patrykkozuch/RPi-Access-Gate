import boto3
import datetime

from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    userId = event["sub"]
        
    if not event.get("deviceId"):
        return {
            "error": True,
            "success": False,
            "message": "Field deviceId is required"
        }
        
    deviceId = event["deviceId"]

    devices_table = boto3.resource('dynamodb').Table('Devices')

    deviceKey = { "deviceId": deviceId }

    try:
        device = devices_table.get_item(Key=deviceKey)
        
        if 'Item' not in device or 'userId' not in device['Item'] or userId != device['Item']['userId']:
            return {
                "error": True,
                "success": False,
                "message": "No access to device"
            }
        
        devices_table.update_item(
            Key=deviceKey,
            AttributeUpdates={
                "userId": {
                    "Action": "DELETE"
                },
                "key": {
                    "Action": "DELETE"
                },
                "paired": {
                    "Action": "DELETE"
                }
            }
        )
        
        return {
            "error": False,
            "success": True,
            "message": "Unpaired"
        }   
        
    except Exception as e:
        return {
            "error": True,
            "success": False,
            "message": str(e)
        }
