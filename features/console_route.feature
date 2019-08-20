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

    Scenario: Recovering all consoles from the database
        Given I set table name and the adapter class as Console
        Given I emptied the database
        Given I save a new entry to the database with json body
        """
        {
            "entity_id": "id1234",
            "name": "NINTENDO",
            "logo_path": "/images/nintendo.png",
            "tag_name": "nick#2",
            "games" : []
        }
        """
        Given I save a new entry to the database with json body
        """
        {
            "entity_id": "id12345",
            "name": "Xbox",
            "logo_path": "/images/xbox.png",
            "tag_name": "nick#3",
            "games" : []
        }
        """
        When get request is made to /api/console
        Then The response should have status success
        Then The retrived json has body
        """
        {
            "id1234":{
            "entity_id": "id1234",
            "name": "NINTENDO",
            "logo_path": "/images/nintendo.png",
            "tag_name": "nick#2",
            "games" : []
        },
            "id12345":{
            "entity_id": "id12345",
            "name": "Xbox",
            "logo_path": "/images/xbox.png",
            "tag_name": "nick#3",
            "games" : []
        }

        }
        """
        Then I delete the test entry

    Scenario: Updating a console in database
        Given I set table name and the adapter class as Console
        Given I save a new entry to the database with json body
        """
        {
            "entity_id": "id1234",
            "name": "Xbox",
            "logo_path": "/images/xbox.png",
            "tag_name": "nick#1",
            "games" : []
        }
        """
        Given The request has json body
        """
        {
            "entity_id": "id1234",
            "name": "Xbox4",
            "logo_path": "/images/xbox4.png",
            "tag_name": "nick#1",
            "games" : []
        }
        """
        When put request is made with id id1234 to /api/console
        Then The response should have status success
        Then The response should have status_code 200
        Then The updated entry json has body
        """
        {
            "entity_id": "id1234",
            "name": "Xbox4",
            "logo_path": "/images/xbox4.png",
            "tag_name": "nick#1",
            "games" : []
        }
        """
        Then I delete the test entry

    Scenario: Deleting a console in database
        Given I set table name and the adapter class as Console
        Given I save a new entry to the database with json body
        """
        {
            "entity_id": "id12345",
            "name": "PS4",
            "logo_path": "/images/ps4.png",
            "tag_name": "nick#3",
            "games" : []
        }
        """
        When delete request is made with id id12345 to /api/console
        Then The response should have status success
        Then The response should have status_code 200
        Then I delete the test entry

