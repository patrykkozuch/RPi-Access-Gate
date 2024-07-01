import base64
import boto3
import datetime

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def get_timestamp():
    return datetime.datetime.now().isoformat()


def lambda_handler(event, context):
    for field in ["deviceId", "data"]:
        if event.get(field) is None:
            return {
                "message": f"{field} is required",
                "success": False,
                "error": True
            }

    data = event["data"]
    data = base64.b64decode(data)

    device_id = event["deviceId"]

    pairing_table = boto3.resource('dynamodb').Table('PairingRequests')
    device_table = boto3.resource('dynamodb').Table('Devices')
    
    device = device_table.get_item(Key={"deviceId": device_id})
    request = pairing_table.get_item(Key={"deviceId": device_id})

    if "Item" not in device:
        return {
            "error": True,
            "success": False,
            "message": "Unknown device."
        }
        
    if "userId" in device["Item"] and device["Item"]["userId"]:
        return {
            "error": True,
            "success": False,
            "message": "Already paired"
        }

    if "Item" not in request:
        pairing_table.put_item(
            Item={
                'deviceId': device_id,
                'data': data
            }
        )
    elif "key" not in request["Item"] or "iv" not in request["Item"]:
        pairing_table.update_item(
            Key={
                "deviceId": device_id
            },
            AttributeUpdates={
                "data": {
                    "Value": data,
                    "Action": "PUT"
                }
            }
        )
    else:
        try:
            pairing_request = request["Item"]
            key = pairing_request["key"].value
            iv = pairing_request["iv"].value
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            plaintext = unpad(cipher.decrypt(data), 16).decode('utf-8')
    
            if plaintext == device_id:
                device_table = boto3.resource('dynamodb').Table('Devices')
                device_table.update_item(
                    Key={
                    "deviceId": device_id
                    },
                    AttributeUpdates={
                        "userId": {
                            "Value": pairing_request["userId"],
                            "Action": "PUT"
                        },
                        "key": {
                            "Value": key,
                            "Action": "PUT"
                        },
                        "paired": {
                            "Value": get_timestamp(),
                            "Action": "PUT"
                        }
                    }
                )
                
                pairing_table.delete_item(Key={"deviceId": device_id})
    
                return {
                    "error": False,
                    "success": True,
                    "message": "Paired"
                }
        except:
            pairing_table.update_item(
                 Key={
                    "deviceId": device_id
                },
                AttributeUpdates={
                    "data": {
                        "Value": data,
                        "Action": "PUT"
                    },
                    "userId": {
                        "Action": "DELETE"
                    },
                    "key": {
                        "Action": "DELETE"
                    },
                    "iv": {
                        "Action": "DELETE"
                    }
                }
            )
            
            return {
                "error": False,
                "success": True,
                "message": "OK"
            }

        pairing_table.delete_item(Key={"deviceId": device_id})

        return {
            "error": True,
            "success": False,
            "message": "Invalid key."
        }

            
    return {
        "error": False,
        "success": True,
        "message": "OK"
    }
