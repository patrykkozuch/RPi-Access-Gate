import boto3

CLIENT_ID = ''

def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    
    try:
        username = event['email']
        code = event['code']
        client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            ConfirmationCode=code,
            ForceAliasCreation=False,
        )
    except client.exceptions.UserNotFoundException:
        return {"error": True, "success": False, "message": "Username doesnt exists"}
    except client.exceptions.ExpiredCodeException:
        return {"error": True, "success": False, "message": "Provided code has expired"}
    except client.exceptions.CodeMismatchException:
        return {"error": True, "success": False, "message": "Invalid Verification code"}
    except client.exceptions.NotAuthorizedException:
        return {"error": True, "success": False, "message": "User is already confirmed"}
    except Exception as e:
        return {"error": True, "success": False, "message": f"Unknown error {e.__str__()} "}

    return {"error": False, "success": True, "message": "User confirmed successfully"}
