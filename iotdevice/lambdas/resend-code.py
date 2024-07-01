import boto3

CLIENT_ID = ''

def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    try:
        username = event['email']
        client.resend_confirmation_code(
            ClientId=CLIENT_ID,
            Username=username,
        )
    except client.exceptions.UserNotFoundException:
        return {"error": True, "success": False, "message":   "Username doesnt exists"}
        
    except client.exceptions.InvalidParameterException:
        return {"error": True, "success": False, "message": "User is already confirmed"}
    
    except Exception as e:
        return {"error": True, "success": False, "message": f"Unknown error {e.__str__()} "}
      
    return  {"error": False, "success": True}
