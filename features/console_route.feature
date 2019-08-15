Feature: Console integrations tests
    Scenario: Creating a new console
        Given I set table name as Console
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
        Then The response should have status success
        Then The response should have status_code 201
        Then The saved json has body
        """
        {
            "name": "Super Selminho",
            "logo_path": "/images/ss.png",
            "tag_name": "nick#1",
            "games" : []
        }
        """
        Then I delete the test entry

