import boto3

CLIENT_ID = ''


def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    
    for field in ['email', 'password', 'code']:
        if not event.get(field):
            return {
                "error": True,
                "success": False,
                "message": f"Field {field} is required"
            }
    
    
    try:
        username = event['email']
        password = event['password']
        code = event['code']
        client.confirm_forgot_password(
            ClientId=CLIENT_ID,
            Username=username,
            ConfirmationCode=code,
            Password=password,
        )
    except client.exceptions.UserNotFoundException as e:
        return {
            "error": True,
            "success": False,
            "message": "Username doesnt exists"
        }

    except client.exceptions.CodeMismatchException as e:
        return {
            "error": True,
            "success": False,
            "message": "Invalid Verification code"
        }

    except client.exceptions.NotAuthorizedException as e:
        return {
            "error": True,
            "success": False,
            "message": "User is already confirmed"
        }

    except Exception as e:
        return {
            "error": True,
            "success": False,
            "message": f"Unknown error {e.__str__()}"
        }

    return {
        "error": False,
        "success": True,
        "message": "Password has been changed successfully"
    }
