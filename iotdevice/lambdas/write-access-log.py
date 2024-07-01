import boto3

def lambda_handler(event, context):
    logId = event["logId"]
    tagId = event["tagId"]
    deviceId = event["deviceId"]
    timestamp = event["timestamp"]

    device_table = boto3.resource('dynamodb').Table('Devices')
    access_log_table = boto3.resource('dynamodb').Table('AccessLog')
    
    try:
        device = device_table.get_item(Key={"deviceId": deviceId})
        
        if "Item" not in device:
            return {
                "error": True,
                "success": False,
                "message": "Unknown device"
            }
            
        if "userId" not in device["Item"] or not device["Item"]["userId"]:
            return {
                "error": True,
                "success": False,
                "message": "No access to the device"
            }  
        
        access_log_table.put_item(
            Item={
                "logId": logId,
                "tagId": tagId,
                "userId": device["Item"]["userId"],
                "deviceId": deviceId,
                "timestamp": timestamp
            }    
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
        "message": "AccessLog added"
    }

