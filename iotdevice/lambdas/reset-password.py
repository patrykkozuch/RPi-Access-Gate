import boto3

CLIENT_ID = ''


def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    
    if not event.get('email'):
        return {
            "error": True,
            "success": False,
            "message": "Field email is required."
        }
    
    try:
        username = event['email']
        client.forgot_password(
            ClientId=CLIENT_ID,
            Username=username
        )
    except client.exceptions.UserNotFoundException:
        return {
            "error": True,
            "success": False,
            "message": "Username doesnt exists"
        }

    except client.exceptions.CodeMismatchException:
        return {
            "error": True,
            "success": False,
            "message": "Invalid Verification code"
        }

    except client.exceptions.NotAuthorizedException:
        return {
            "error": True,
            "success": False,
            "message": "User is already confirmed"
        }

    except Exception as e:
        return {
            "error": True,
            "success": False,
            "message": f"Uknown error {e.__str__()}"
        }

    return {
        "error": False,
        "success": True,
        "message": f"Please check your registered email for validation code"
    }
