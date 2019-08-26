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

    Scenario: Getting a user-admin from the database
        Given I set table name and the adapter class as UserAdmin
        Given I save a new entry to the database with json body
        """
        {
            "name": "Duarte",
            "email": "dudu_jpa@playerstars.com.br",
            "entity_id": "id123"
        }
        """
        When get request is made with id id123 to /api/user-admin
        Then The response should have status success
        Then The response should have status_code 200
        Then The retrived json has body
        """
        {
            "name": "Duarte",
            "email": "dudu_jpa@playerstars.com.br",
            "entity_id": "id123"
        }
        """
        Then  I delete the test entry

    Scenario: Recovering all users admin from the database
        Given I set table name and the adapter class as UserAdmin
        Given I emptied the database
        Given I save a new entry to the database with json body
        """
        {
            "name": "Duarte",
            "email": "dudu_jpa@playerstars.com.br",
            "entity_id": "id123"
        }
        """
        Given I save a new entry to the database with json body
        """
        {
            "name": "Anselmo",
            "email": "barriel_jpa@playerstars.com.br",
            "entity_id": "id12345"
        }
        """
        When get request is made to /api/user-admin
        Then The response should have status success
        Then The retrived json has body
        """
        [
            {
                "name": "Duarte",
                "email": "dudu_jpa@playerstars.com.br",
                "entity_id": "id123"
            },
            {
                "name": "Anselmo",
                "email": "barriel_jpa@playerstars.com.br",
                "entity_id": "id12345"
            }

        ]
        """
        Then I delete the test entry
