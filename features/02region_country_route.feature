Feature: Region Country integrations tests
    Scenario: Creating a new region country
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Region_Country
        Given The request has json body
        """
        {
            "name": "Gold",
            "countries": ["Brasil", "Venezuela", "Cuba"],
            "minimum_bet": 1234
        }
        """
        When post request is made to /region-country
        Then The response should have status success
        Then The response should have status_code 201
        Then The saved json has body
        """
        {
            "name": "Gold",
            "countries": ["Brasil", "Venezuela", "Cuba"],
            "minimum_bet": 1234
        }
        """
        Then I delete the test entry

    Scenario: Getting a region country from the database
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Region_Country
        Given I save a new entry to the database with json body
        """
        {
            "name": "Gold",
            "countries": ["Brasil", "Venezuela", "Cuba"],
            "entity_id": "id123",
            "minimum_bet": 1234
        }
        """
        When get request is made with id id123 to /region-country
        Then The response should have status success
        Then The response should have status_code 200
        Then The retrived json has body
        """
        {
            "name": "Gold",
            "countries": ["Brasil","Venezuela","Cuba"],
            "entity_id": "id123",
            "minimum_bet": 1234
        }
        """
        Then I delete the test entry

    Scenario: Recovering all regions country from the database
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Region_Country
        Given I emptied the database
        Given I save a new entry to the database with json body
        """
        {
             "name": "BRONZE",
             "minimum_bet" : 1234,
             "countries":["brazil", "mexico", "canada"],
             "entity_id":"id123"
        }
        """
        Given I save a new entry to the database with json body
        """
        {
             "name": "SILVER",
             "minimum_bet" : 1234,
             "countries":["japan", "argentina", "venezuela"],
             "entity_id":"id12345"
        }
        """
        When get request is made to /region-country
        Then The response should have status success
        Then The retrived json has body
        """
        [{
             "name": "BRONZE",
             "minimum_bet" : 1234,
             "countries":["brazil", "mexico", "canada"],
             "entity_id":"id123"
          },{

             "name": "SILVER",
             "minimum_bet" : 1234,
             "countries":["japan", "argentina", "venezuela"],
             "entity_id":"id12345"
            }
        ]
        """
        Then I delete the test entry

    Scenario: Updating a region country in database
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Region_Country
        Given I save a new entry to the database with json body
         """
         {
             "name": "BRONZE",
             "minimum_bet" : 1234,
             "countries":["brazil", "mexico", "canada"],
             "entity_id":"id123"
         }
         """
        Given The request has json body
         """
         {
            "name": "ALTEREI_NOME",
             "minimum_bet" : 1234,
             "countries":["brazil", "mexico", "canada"],
             "entity_id":"id123"
         }
         """
        When put request is made with id 946b to /region-country
        Then The response should have status success
        Then The response should have status_code 200
        Then The updated entry json has body
        """
        {
            "name": "ALTEREI_NOME",
             "minimum_bet" : 1234,
             "countries":["brazil", "mexico", "canada"],
             "entity_id":"id123"
        }
        """
        Then I delete the test entry


### FICA FALTANDO O DELETE
