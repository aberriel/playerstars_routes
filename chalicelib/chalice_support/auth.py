from chalice import CognitoUserPoolAuthorizer, CORSConfig

cupauth = CognitoUserPoolAuthorizer(
    'playerstars',
    provider_arns=['arn:aws:cognito-idp:us-east-1:230639242520:userpool/us-east-1_kOuqOxe1b'])

cors = CORSConfig(allow_origin='*',
                  allow_headers=['Content-Type',
                                 'X-Amz-Date',
                                 'Authorization',
                                 'X-Api-Key',
                                 'X-Amz-Security-Token',
                                 'Content-Range'],
                  expose_headers=['Content-Range'])
