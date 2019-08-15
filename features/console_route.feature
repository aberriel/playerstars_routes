Feature: Console integrations tests
    Scenario: Creating a new console
        Given The request has json body
        """
        {
            "name": "Super Selminho",
            "logo_path": "/images/ss.png",
            "tag_name": "nick#1",
            "games" : []
        }
        """
        When post request is made to /api/console
        Then The response has status success
        Then The response has status code 200
#        Then The saved json has body
#        """
#        {
#            "name": "Super Nintendo",
#            "logo_path": "/images/ss.png",
#            "tag_name": "nick#1",
#            "games" : []
#        }
#        """
#        Then I reset the dynamodb mock

