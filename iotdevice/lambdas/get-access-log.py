import boto3
import datetime
import json

from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    deviceId = event["deviceId"]
    userId = event["sub"]

    accessLogTable = boto3.resource('dynamodb').Table('AccessLog')
    devicesTable = boto3.resource('dynamodb').Table('Devices')
    
    try:
        device = devicesTable.get_item(Key={"deviceId": deviceId})    
        
        if "Item" not in device or 'userId' not in device['Item'] or userId != device['Item']['userId']:
            return {
                "error": True,
                "success": False,
                "message": "No access to device"
            }
        
        accessLog = accessLogTable.scan(
            FilterExpression=Attr('userId').eq(userId) & Attr('deviceId').eq(deviceId)
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
        "message": f"Access log for device {deviceId} retrieved successfuly",
        "data": accessLog['Items']
    }

