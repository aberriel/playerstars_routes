Feature: Player integrations tests
    Scenario: Creating a new player
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Player
        Given The request has json body
        """
        {
            "user":{
                "name": "Anselmo Lira",
                "email": "playerstars@playerstars.com.br",
                "date_birth": "16/12/1986",
                "street": "Rua José de Figueiredo",
                "street_number": "192",
                "street_complement": "Blocos 29, 30",
                "neighborhood": "Barra da Tijuca",
                "city": "Rio de Janeiro",
                "state": "Rio de Janeiro",
                "country": "Brasil",
                "postal_code": "22333-000",
                "phone_number": "(21) 99663-6963",
                "cpf": "123.456.789-00",
                "nickname": "anselmo.lira"
            },
            "favorites": [],
            "blue_star_balance": 123,
            "golden_star_balance": 4321,
            "consoles": [
                {
                    "entity_id": "1",
                    "name": "PS 4",
                    "logo_path": "/images/ps4.png",
                    "tag_name": "007"
            },
                {
                    "entity_id": "11",
                    "name": "Xbox",
                    "logo_path": "/images/xbox.png",
                    "tag_name": "mario",
                    "games": []
                }
            ],
            "states_regions": [],
            "countries_regions": []
        }
        """
        When post request is made to /player
        Then The response should have status success
        Then The response should have status_code 201
        Then The saved json has body
        """
         {
          "terms": true,
          "golden_star_balance": 300,
          "player_status": "OFFLINE",
          "consoles": [
            {
              "name": "PS 4",
              "entity_id": "1",
              "logo_path": "/images/ps4.png",
              "tag_name": "007",
              "games": []
            },
            {
              "name": "Xbox",
              "entity_id": "11",
              "logo_path": "/images/xbox.png",
              "tag_name": "mario",
              "games": []
            }
          ],
          "user": {
            "date_birth": "1986-12-16",
            "country": "Brasil",
            "street_complement": "Blocos 29, 30",
            "city": "Rio de Janeiro",
            "street": "Rua José de Figueiredo",
            "name": "Anselmo Lira",
            "nickname": "anselmo.lira",
            "cpf": "123.456.789-00",
            "street_number": "192",
            "phone_number": "(21) 99663-6963",
            "state": "Rio de Janeiro",
            "neighborhood": "Barra da Tijuca",
            "postal_code": "22333-000",
            "email": "playerstars@playerstars.com.br",
            "profile_image": null
          },
          "points": 200,
          "blue_star_balance": 200,
          "purchases": [],
          "star_reservations": [],
          "star_transactions": [],
          "states_regions": [],
          "countries_regions": [],
          "favorites": []
        }
        """
        Then I delete the test entry

    Scenario: Getting a player from the database
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Player
        Given I save a new entry to the database with json body
        """
        {
          "entity_id": "id123",
          "terms": true,
          "golden_star_balance": 300,
          "player_status": "OFFLINE",
          "consoles": [
            {
              "name": "PS 4",
              "entity_id": "1",
              "logo_path": "/images/ps4.png",
              "tag_name": "007",
              "games": []
            },
            {
              "name": "Xbox",
              "entity_id": "11",
              "logo_path": "/images/xbox.png",
              "tag_name": "mario",
              "games": []
            }
          ],
          "user": {
            "date_birth": "1986-12-16",
            "country": "Brasil",
            "street_complement": "Blocos 29, 30",
            "city": "Rio de Janeiro",
            "street": "Rua José de Figueiredo",
            "name": "Anselmo Lira",
            "nickname": "anselmo.lira",
            "cpf": "123.456.789-00",
            "street_number": "192",
            "phone_number": "(21) 99663-6963",
            "state": "Rio de Janeiro",
            "neighborhood": "Barra da Tijuca",
            "postal_code": "22333-000",
            "email": "playerstars@playerstars.com.br",
            "profile_image": null
          },
          "points": 200,
          "blue_star_balance": 200,
          "purchases": [],
          "star_reservations": [],
          "star_transactions": [],
          "states_regions": [],
          "countries_regions": [],
          "favorites": []
        }
        """
        When get request is made with id id123 to /player
        Then The response should have status success
        Then The response should have status_code 200
        Then The retrived json has body
        """
        {
            "entity_id": "id123",
            "favorites": [],
            "blue_star_balance": 200,
            "points": 200,
            "purchases": [],
            "star_reservations": [],
            "star_transactions": [],
            "golden_star_balance": 300,
            "states_regions": [],
            "terms": true,
            "user": {
                "date_birth": "1986-12-16",
                "country": "Brasil",
                "street_complement": "Blocos 29, 30",
                "city": "Rio de Janeiro",
                "street": "Rua José de Figueiredo",
                "name": "Anselmo Lira",
                "nickname": "anselmo.lira",
                "cpf": "123.456.789-00",
                "street_number": "192",
                "phone_number": "(21) 99663-6963",
                "state": "Rio de Janeiro",
                "neighborhood": "Barra da Tijuca",
                "postal_code": "22333-000",
                "email": "playerstars@playerstars.com.br",
                "profile_image": null
            },
            "countries_regions": [],
            "player_status": "OFFLINE",
            "consoles": [
                {
                    "entity_id": "1",
                    "logo_path": "/images/ps4.png",
                    "name": "PS 4",
                    "tag_name": "007",
                    "games": []
                },
                {
                    "entity_id": "11",
                    "logo_path": "/images/xbox.png",
                    "name": "Xbox",
                    "tag_name": "mario",
                    "games": []
                }
            ]
        }
        """
        Then I delete the test entry

    Scenario: Recovering all players from the database
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Player
        Given I save a new entry to the database with json body
        """
        {
          "entity_id": "id123",
          "terms": true,
          "golden_star_balance": 300,
          "player_status": "OFFLINE",
          "consoles": [
            {
              "name": "PS 4",
              "entity_id": "1",
              "logo_path": "/images/ps4.png",
              "tag_name": "007",
              "games": []
            },
            {
              "name": "Xbox",
              "entity_id": "11",
              "logo_path": "/images/xbox.png",
              "tag_name": "mario",
              "games": []
            }
          ],
          "user": {
            "date_birth": "1986-12-16",
            "country": "Brasil",
            "street_complement": "Blocos 29, 30",
            "city": "Rio de Janeiro",
            "street": "Rua José de Figueiredo",
            "name": "Anselmo Lira",
            "nickname": "anselmo.lira",
            "cpf": "123.456.789-00",
            "street_number": "192",
            "phone_number": "(21) 99663-6963",
            "state": "Rio de Janeiro",
            "neighborhood": "Barra da Tijuca",
            "postal_code": "22333-000",
            "email": "playerstars@playerstars.com.br",
            "profile_image": null
          },
          "points": 200,
          "blue_star_balance": 200,
          "purchases": [],
          "star_reservations": [],
          "star_transactions": [],
          "states_regions": [],
          "countries_regions": [],
          "favorites": []
        }
        """
        Given I save a new entry to the database with json body
        """
        {
          "entity_id": "id1234",
          "terms": true,
          "golden_star_balance": 300,
          "player_status": "OFFLINE",
          "consoles": [
            {
              "name": "PS 4",
              "entity_id": "1",
              "logo_path": "/images/ps4.png",
              "tag_name": "007",
              "games": []
            },
            {
              "name": "Xbox",
              "entity_id": "11",
              "logo_path": "/images/xbox.png",
              "tag_name": "mario",
              "games": []
            }
          ],
          "user": {
            "date_birth": "1986-12-16",
            "country": "Brasil",
            "street_complement": "Blocos 29, 30",
            "city": "Rio de Janeiro",
            "street": "Rua José de Figueiredo",
            "name": "Anselmo Lira",
            "nickname": "anselmo.lira",
            "cpf": "123.456.789-00",
            "street_number": "192",
            "phone_number": "(21) 99663-6963",
            "state": "Rio de Janeiro",
            "neighborhood": "Barra da Tijuca",
            "postal_code": "22333-000",
            "email": "playerstars@playerstars.com.br",
            "profile_image": null
          },
          "points": 200,
          "blue_star_balance": 200,
          "purchases": [],
          "star_reservations": [],
          "star_transactions": [],
          "states_regions": [],
          "countries_regions": [],
          "favorites": []
        }
        """
        When get request is made to /player
        Then The response should have status success
        Then The retrived json has body
        """
        [{
                "entity_id": "id123",
                "favorites": [],
                "blue_star_balance": 200,
                "points": 200,
                "purchases": [],
                "star_reservations": [],
                "golden_star_balance": 300,
                "star_transactions": [],
                "states_regions": [],
                "terms": true,
                "user": {
                    "date_birth": "1986-12-16",
                    "country": "Brasil",
                    "street_complement": "Blocos 29, 30",
                    "city": "Rio de Janeiro",
                    "street": "Rua José de Figueiredo",
                    "name": "Anselmo Lira",
                    "nickname": "anselmo.lira",
                    "cpf": "123.456.789-00",
                    "street_number": "192",
                    "phone_number": "(21) 99663-6963",
                    "state": "Rio de Janeiro",
                    "neighborhood": "Barra da Tijuca",
                    "postal_code": "22333-000",
                    "email": "playerstars@playerstars.com.br",
                    "profile_image": null
                },
                "countries_regions": [],
                "player_status": "OFFLINE",
                "consoles": [
                    {
                        "entity_id": "1",
                        "logo_path": "/images/ps4.png",
                        "name": "PS 4",
                        "tag_name": "007",
                        "games": []
                    },
                    {
                    "entity_id": "11",
                    "logo_path": "/images/xbox.png",
                    "name": "Xbox",
                    "tag_name": "mario",
                    "games": []
                }
                ]
            },{
                "entity_id": "id1234",
                "terms": true,
                "favorites": [],
                "blue_star_balance": 200,
                "points": 200,
                "purchases": [],
                "star_reservations": [],
                "golden_star_balance": 300,
                "states_regions": [],
                "star_transactions": [],
                "user": {
                    "date_birth": "1986-12-16",
                    "country": "Brasil",
                    "street_complement": "Blocos 29, 30",
                    "city": "Rio de Janeiro",
                    "street": "Rua José de Figueiredo",
                    "name": "Anselmo Lira",
                    "nickname": "anselmo.lira",
                    "cpf": "123.456.789-00",
                    "street_number": "192",
                    "phone_number": "(21) 99663-6963",
                    "state": "Rio de Janeiro",
                    "neighborhood": "Barra da Tijuca",
                    "postal_code": "22333-000",
                    "email": "playerstars@playerstars.com.br",
                    "profile_image": null
                },
                "countries_regions": [],
                "player_status": "OFFLINE",
                "consoles": [
                    {
                        "entity_id": "1",
                        "logo_path": "/images/ps4.png",
                        "name": "PS 4",
                        "tag_name": "007",
                        "games": []
                    },
                    {
                    "entity_id": "11",
                    "logo_path": "/images/xbox.png",
                    "name": "Xbox",
                    "tag_name": "mario",
                    "games": []
                }
                ]
            }
        ]
        """
        Then I delete the test entry

### Pendente PUT e DELETE
