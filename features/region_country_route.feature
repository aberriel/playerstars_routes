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
        When post request is made to /api/region-country
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
        When get request is made with id id123 to /api/region-country
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
