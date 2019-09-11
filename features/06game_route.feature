Feature: Game integrations tests
    Scenario: Creating a new game
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Console
        Given I save a new entry to the database with json body
        """
        {
            "entity_id":"id00123",
            "name": "Super Nintendo",
            "logo_path": "/images/sn.png",
            "tag_name": "nick#1",
            "games" : []
        }
        """
        Given The request has json body
        """
            {
            "name": "Sonic",
            "logo_path": "images/sonic.jpg",
            "consoles": [{
                "name": "Super Nintendo",
                "entity_id":"id00123",
                "logo_path": "/images/sn.png",
                "tag_name": "nick#1"
                }]
            }
        """
        When post request is made to /game
        Then The response should have status success
        Then The response should have status_code 201
        Then The saved jsons has body
        """
        {
            "name": "Super Nintendo",
            "games": [
                {
                "logo_path": "images/sonic.jpg",
                "name": "Sonic"
                }
            ],
            "tag_name": "nick#1",
            "logo_path": "/images/sn.png"
        }
        """
        Then I delete the test entry

#    Scenario: Getting a game from the database
#        Given I set table name and the adapter class as Console
#        Given I save a new entry to the database with json body
#        """
#        {
#            "name": "Super Nintendo",
#            "games": [
#                {
#                    "name": "ZELDA",
#                    "entity_id": "0123456",
#                    "logo_path": "images/zelda.jpg"
#                },
#                {
#                    "name": "fifa",
#                    "entity_id": "0123",
#                    "logo_path": "images/fifa.jpg"
#                }
#            ],
#            "entity_id": "f8a1cad8-b3db-459b-9f27-aaca8b783d3d",
#            "logo_path": "/images/sn.png",
#            "tag_name": "nick#1"
#        }
#        """
#        When get request is made with id 0123456 to /game
#        Then The response should have status success
#        Then The response should have status_code 200
#        Then The retrived json has body
#        """
#         {
#           "name": "ZELDA",
#           "logo_path": "images/zelda.jpg",
#           "consoles": [{
#                "entity_id": "f8a1cad8-b3db-459b-9f27-aaca8b783d3d",
#                "name": "Super Nintendo",
#                "logo_path": "/images/sn.png",
#                "tag_name": "nick#1"
#                }]
#        """
#        Then  I delete the test entry
#
