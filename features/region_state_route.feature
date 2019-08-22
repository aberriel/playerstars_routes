Feature: Region State integrations tests
    Scenario: Creating a new region state
        Given I set table name and the adapter class as RegionState
        Given The request has json body
        """
        {
            "name": "BRONZE",
            "minimum_bet" : 1234,
            "states":["ES", "RJ", "MG"]
        }
        """
        When post request is made to /api/region-state
        Then The response should have status success
        Then The response should have status_code 201
        Then The saved json has body
        """
        {
            "name": "BRONZE",
            "minimum_bet" : 1234,
            "states":["ES", "RJ", "MG"]
        }
        """
        Then I delete the test entry

    Scenario: Getting a region state from the database
        Given I set table name and the adapter class as RegionState
        Given I save a new entry to the database with json body
        """
        {
            "name": "BRONZE",
            "minimum_bet" : 1234,
            "states":["AC", "BA", "RJ"],
            "entity_id":"id123"
        }
        """
        When get request is made with id id123 to /api/region-state
        Then The response should have status success
        Then The response should have status_code 200
        Then The retrived json has body
        """
        {
            "name": "BRONZE",
            "minimum_bet" : 1234,
            "states":["AC", "BA", "RJ"],
            "entity_id":"id123"
        }
        """
        Then I delete the test entry

    Scenario: Recovering all regions state from the database
        Given I set table name and the adapter class as RegionState
        Given I emptied the database
        Given I save a new entry to the database with json body
        """
        {
            "name": "BRONZE",
            "minimum_bet" : 1234,
            "states":["AC", "BA", "RJ"],
            "entity_id":"id123"
        }
        """
        Given I save a new entry to the database with json body
        """
        {
            "name": "SILVER",
            "minimum_bet" : 1234,
            "states":["ES", "PE", "SP"],
            "entity_id":"id12345"
        }
        """
        When get request is made to /api/region-state
        Then The response should have status success
        Then The retrived json has body
        """
        {
            "id123": {
             "name": "BRONZE",
             "minimum_bet" : 1234,
             "states":["AC", "BA", "RJ"],
             "entity_id":"id123"
        },

             "id12345": {
             "name": "SILVER",
             "minimum_bet" : 1234,
             "states":["ES", "PE", "SP"],
             "entity_id":"id12345"
        }
        }
        """
        Then I delete the test entry

