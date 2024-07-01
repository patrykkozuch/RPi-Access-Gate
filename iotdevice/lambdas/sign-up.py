import boto3

CLIENT_ID = ''


def lambda_handler(event, context):
    for field in ["email", "password"]:
        if not event.get(field):
            return {
                "error": True, 
                "success": False, 
                'message': f"Field {field} is required"
            }

    email = event["email"]
    password = event['password']

    client = boto3.client('cognito-idp')
    try:
        client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': "email",
                    'Value': email
                }
            ],
            ValidationData=[
                {
                    'Name': "email",
                    'Value': email
                }
            ]
        )

    except client.exceptions.UsernameExistsException as e:
        return {
            "error": True,
            "success": False,
            "message": "This username already exists"
        }

    except client.exceptions.InvalidPasswordException as e:
        return {
            "error": True,
            "success": False,
            "message": "Password should have Caps, Special chars and Numbers"
        }

    except Exception as e:
        return {
            "error": True,
            "success": False,
            "message": str(e)
        }

    return {
        "error": False,
        "success": True,
        "message": "Please confirm your signup, check Email for validation code",
    }
