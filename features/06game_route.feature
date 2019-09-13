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
        Then I delete the test game entry

    Scenario: Getting a game from the database
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Console
        Given I save a new entry to the database with json body
        """
        {
            "name": "Super Nintendo",
            "games": [
                {
                    "name": "ZELDA",
                    "entity_id": "0123456",
                    "logo_path": "images/zelda.jpg"
                },
                {
                    "name": "fifa",
                    "entity_id": "0123",
                    "logo_path": "images/fifa.jpg"
                }
            ],
            "entity_id": "f8a1cad8-b3db-459b-9f27-aaca8b783d3d",
            "logo_path": "/images/sn.png",
            "tag_name": "nick#1"
        }
        """
        When get request is made with id 0123456 to /game
        Then The response should have status success
        Then The response should have status_code 200
        Then The retrived json has body
        """
         {
           "name": "ZELDA",
           "logo_path": "images/zelda.jpg",
           "entity_id": "0123456"
        }
        """
        Then I delete the test game entry

    Scenario: Getting all games from one console from the database
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Console
        Given I save a new entry to the database with json body
        """
        {
            "name": "Super Nintendo",
            "games": [
                {
                    "name": "ZELDA",
                    "entity_id": "0123456",
                    "logo_path": "images/zelda.jpg"
                },
                {
                    "name": "fifa",
                    "entity_id": "0123",
                    "logo_path": "images/fifa.jpg"
                }
            ],
            "entity_id": "789",
            "logo_path": "/images/sn.png",
            "tag_name": "nick#1"
        }
        """
        When get request is made with id 789 to /game/console
        Then The response should have status success
        Then The response should have status_code 200
        Then The retrived json has body
        """
        [
                {
                    "name": "ZELDA",
                    "entity_id": "0123456",
                    "logo_path": "images/zelda.jpg"
                },
                {
                    "name": "fifa",
                    "entity_id": "0123",
                    "logo_path": "images/fifa.jpg"
                }
        ]
        """
        Then I delete the test game entry

    Scenario: Updating a game in database
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Console
        Given I save a new entry to the database with json body
        """
        {
          "name": "XBOX",
          "games": [{

              "entity_id": "1e9ec",
              "name": "SONIC",
              "logo_path": "images/sonic.jpg"
          }],
          "entity_id": "403d8e91-8e4a-4833-bdf3-68aa105a99aa",
          "logo_path": "/images/xb.png",
          "tag_name": "nick#12"
        }
        """
        Given The request has json body
        """
        {
	        "entity_id": "1e9ec",
            "name": "NOME_ALTERADO",
            "logo_path": "images/sonic.jpg",
	        "consoles":[{
		        "name": "XBOX",
		        "entity_id": "403d8e91-8e4a-4833-bdf3-68aa105a99aa",
		        "logo_path": "/images/xb.png",
		        "tag_name": "nick#12"
	        }]
        }
        """
        When put request is made with id 1e9ec to /game
        Then The response should have status success
        Then The response should have status_code 200
        Then The updated game entry json has body
        """
        {
          "name": "XBOX",
          "games": [{

              "entity_id": "1e9ec",
              "name": "NOME_ALTERADO",
              "logo_path": "images/sonic.jpg"
          }],
          "entity_id": "403d8e91-8e4a-4833-bdf3-68aa105a99aa",
          "logo_path": "/images/xb.png",
          "tag_name": "nick#12"
        }
        """
        Then I delete the test game entry
