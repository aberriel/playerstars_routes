from chalice import CognitoUserPoolAuthorizer, CORSConfig
from chalicelib.settings import Settings


authorizer = CognitoUserPoolAuthorizer(
    'playerstars',
    provider_arns=[Settings.COGNITO_USERPOOL_ARN])

cors = CORSConfig(allow_origin='*',
                  allow_headers=['Content-Type',
                                 'X-Amz-Date',
                                 'Authorization',
                                 'X-Api-Key',
                                 'X-Amz-Security-Token',
                                 'Content-Range'],
                  expose_headers=['Content-Range'])
