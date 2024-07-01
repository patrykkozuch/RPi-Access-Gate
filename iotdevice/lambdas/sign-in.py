import boto3

USER_POOL_ID = ''
CLIENT_ID = ''

def initiate_auth(client, username, password):
    try:
        resp = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            }
        )
    except client.exceptions.NotAuthorizedException:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotConfirmedException:
        return None, "User is not confirmed"
    except Exception as e:
        return None, e.__str__()
    return resp, None


def lambda_handler(event, context):
    client = boto3.client('cognito-idp')

    for field in ["email", "password"]:
        if event.get(field) is None:
            return {
                "error": True,
                "success": False,
                "message": f"{field} is required",
                "data": None
            }

    email = event['email']
    password = event['password']

    resp, msg = initiate_auth(client, email, password)

    if msg is not None:
        return {
            "message": msg,
            "error": True,
            "success": False,
            "data": None
        }

    if resp and resp.get("AuthenticationResult"):
        return {
            "message": "success",
            "error": False,
            "success": True,
            "data": {
                "id_token": resp["AuthenticationResult"]["IdToken"],
                "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                "access_token": resp["AuthenticationResult"]["AccessToken"],
                "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
                "token_type": resp["AuthenticationResult"]["TokenType"]
            }
        }
        
    return {
        "message": "Unknown error.",
        "error": True,
        "success": False,
        "data": None
    }
