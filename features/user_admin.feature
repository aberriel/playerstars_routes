Feature: Console integrations tests
    Scenario: Creating a new user admin
        Given I set table name and the adapter class as UserAdmin
        Given The request has json body
        """
        {
            "name": "Duarte",
            "email": "dudu_jpa@playerstars.com.br"
        }
        """
        When post request is made to /api/user-admin
        Then The response should have status success
        Then The response should have status_code 201
        Then The saved json has body
        """
        {
            "name": "Duarte",
            "email": "dudu_jpa@playerstars.com.br"
        }
        """
        Then I delete the test entry
            
