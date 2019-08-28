Feature: Region Country integrations tests
    Scenario: Creating a new region country
        Given I set table name and the adapter class as RegionCountry
        Given The request has json body
        """
        {
            "name": "Gold",
            "minimum_bet" : 1234,
            "countries":[
                "Brasil",
                "Venezuela",
                "Cuba"
                ]
        }
        """
        When post request is made to /region-country
        Then The response should have status success
        Then The response should have status_code 201
        Then The saved json has body
        """
        {
            "name": "Gold",
            "countries": [
                      "Brasil",
                      "Venezuela",
                      "Cuba"
            ],
            "minimum_bet": 1234
        }
        """
        Then I delete the test entry

    Scenario: Getting a region country from the database
        Given I set table name and the adapter class as RegionCountry
        Given I save a new entry to the database with json body
        """
        {
             "name": "Gold",
             "countries": [
                    "Brasil",
                    "Venezuela",
                    "Cuba"
             ],
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
            "countries": [
                    "Brasil",
                    "Venezuela",
                    "Cuba"
            ],
            "entity_id": "id123",
            "minimum_bet": 1234
        }
        """
        Then I delete the test entry

    Scenario: Recovering all regions country from the database
        Given I set table name and the adapter class as RegionCountry
        Given I emptied the database
        Given I save a new entry to the database with json body
        """
        {
             "name": "Gold",
             "countries": [
                    "Brasil",
                    "Venezuela",
                    "Cuba"
             ],
             "entity_id": "9e29",
             "minimum_bet": 1234
        }
        """
        Given I save a new entry to the database with json body
        """
        {
             "name": "Silver",
             "countries": [
                    "Equador",
                    "Chile",
                    "Argentina"
             ],
             "entity_id": "946b",
             "minimum_bet": 12345
        }
        """
        When get request is made to /region-country
        Then The response should have status success
        Then The retrived json has body
        """
        {
            "946b": {
            "minimum_bet": 12345,
            "entity_id": "946b",
            "countries": [
                "Equador",
                "Chile",
                "Argentina"
            ],
            "name": "Silver"
        },
        "9e29": {
            "minimum_bet": 1234,
            "entity_id": "9e29",
            "countries": [
                "Brasil",
                "Venezuela",
                "Cuba"
            ],
            "name": "Gold"
        }
        }
        """
        Then I delete the test entry

    Scenario: Updating a region country in database
        Given I set table name and the adapter class as RegionCountry
        Given I save a new entry to the database with json body
         """
         {
             "name": "Silver",
             "countries": [
                    "Equador",
                    "Chile",
                    "Argentina"
             ],
             "entity_id": "946b",
             "minimum_bet": 12345
         }
         """
        Given The request has json body
         """
         {
             "name": "Bronze",
             "countries": [
                    "Equador",
                    "Mexico",
                    "Argentina"
             ],
             "entity_id": "946b",
             "minimum_bet": 12345
         }
         """
        When put request is made with id 946b to /region-country
        Then The response should have status success
        Then The response should have status_code 200
        Then The updated entry json has body
        """
        {
            "name": "Bronze",
             "countries": [
                    "Equador",
                    "Mexico",
                    "Argentina"
             ],
             "entity_id": "946b",
             "minimum_bet": 12345
        }
        """
        Then I delete the test entry


## FICA FALTANDO O DELETE
