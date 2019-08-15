Feature: Console integrations tests
    Scenario: Creating a new console
        Given I set table name and the adapter class as Console
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

    Scenario: Getting a console from the database
        Given I set table name and the adapter class as Console
        Given I save a new entry to the database with json body
        """
        {
            "entity_id": "id123",
            "name": "Super Selminho",
            "logo_path": "/images/ss.png",
            "tag_name": "nick#1",
            "games" : []
        }
        """
        When get request is made with id id123 to /api/console
        Then The response should have status success
        Then The response should have status_code 200
        Then The retrived json has body
        """
        {
            "entity_id": "id123",
            "name": "Super Selminho",
            "logo_path": "/images/ss.png",
            "tag_name": "nick#1",
            "games" : []
        }
        """
        Then I delete the test entry
