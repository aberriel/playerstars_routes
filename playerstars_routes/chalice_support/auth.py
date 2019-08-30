from chalice import CognitoUserPoolAuthorizer, CORSConfig

cupauth = CognitoUserPoolAuthorizer(
    'aunelive',
    provider_arns=['arn:aws:cognito-idp:us-east-1:778654367758:'
                   'userpool/us-east-1_WRpRjf9tI'])

cors = CORSConfig(allow_origin='*',
                  allow_headers=['Content-Type', 'X-Amz-Date', 'Authorization',
                                 'X-Api-Key', 'X-Amz-Security-Token'])
