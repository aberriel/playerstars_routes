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
