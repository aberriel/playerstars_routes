Feature: Player integrations tests
    Scenario: Creating a new player
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Player
        Given The request has json body
        """
        {
            "user":{
                "entity_id": "id0123",
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
                "nickname": "anselmo.lira",
                "profile_image": "ACCBB4762CF23AA35690CC"
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
            "favorites": [],
            "blue_star_balance": 123,
            "golden_star_balance": 4321,
            "states_regions": [],
            "user": {
                "country": "Brasil",
                "nickname": "anselmo.lira",
                "postal_code": "22333-000",
                "profile_image": "ACCBB4762CF23AA35690CC",
                "city": "Rio de Janeiro",
                "address": "Rua José de Figueiredo 192, Blocos 29, 30 - Barra da Tijuca",
                "name": "Anselmo Lira",
                "phone_number": "(21) 99663-6963",
                "cpf": "123.456.789-00",
                "state": "Rio de Janeiro",
                "date_birth": "1986-12-16",
                "email": "playerstars@playerstars.com.br"
            },
            "countries_regions": [],
            "player_status": "OFFLINE",
            "star_transactions": [],
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

    Scenario: Getting a player from the database
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Player
        Given I save a new entry to the database with json body
        """
        {
            "entity_id": "id123",
            "favorites": [],
            "blue_star_balance": 123,
            "golden_star_balance": 4321,
            "states_regions": [],
            "star_transactions": [],
            "user": {
                "country": "Brasil",
                "nickname": "anselmo.lira",
                "postal_code": "22333-000",
                "profile_image": null,
                "city": "Rio de Janeiro",
                "address": "Rua José de Figueiredo 192, Blocos 29, 30 - Barra da Tijuca",
                "name": "Anselmo Lira",
                "phone_number": "(21) 99663-6963",
                "entity_id": "54321",
                "cpf": "123.456.789-00",
                "state": "Rio de Janeiro",
                "date_birth": "1986-12-16",
                "email": "playerstars@playerstars.com.br"
            },
            "countries_regions": [],
            "games": [],
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
        When get request is made with id id123 to /player
        Then The response should have status success
        Then The response should have status_code 200
        Then The retrived json has body
        """
        {
            "entity_id": "id123",
            "favorites": [],
            "blue_star_balance": 123,
            "star_transactions": [],
            "golden_star_balance": 4321,
            "states_regions": [],
            "user": {
                "country": "Brasil",
                "nickname": "anselmo.lira",
                "postal_code": "22333-000",
                "profile_image": null,
                "city": "Rio de Janeiro",
                "address": "Rua José de Figueiredo 192, Blocos 29, 30 - Barra da Tijuca",
                "name": "Anselmo Lira",
                "phone_number": "(21) 99663-6963",
                "entity_id": "54321",
                "cpf": "123.456.789-00",
                "state": "Rio de Janeiro",
                "date_birth": "1986-12-16",
                "email": "playerstars@playerstars.com.br"
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
            "favorites": [],
            "blue_star_balance": 123,
            "golden_star_balance": 4321,
            "states_regions": [],
            "star_transactions": [],
            "user": {
                "entity_id": "id2345",
                "country": "Brasil",
                "nickname": "anselmo.lira",
                "postal_code": "22333-000",
                "profile_image": null,
                "city": "Rio de Janeiro",
                "address": "Rua José de Figueiredo 192, Blocos 29, 30 - Barra da Tijuca",
                "name": "Anselmo Lira",
                "phone_number": "(21) 99663-6963",
                "entity_id": "54321",
                "cpf": "123.456.789-00",
                "state": "Rio de Janeiro",
                "date_birth": "1986-12-16",
                "email": "playerstars@playerstars.com.br"
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
        Given I save a new entry to the database with json body
        """
        {
            "entity_id": "id123456",
            "favorites": [],
            "blue_star_balance": 123,
            "golden_star_balance": 4321,
            "states_regions": [],
            "star_transactions": [],
            "user": {
                "entity_id": "it983",
                "country": "Canada",
                "nickname": "Dudu",
                "postal_code": "22333-000",
                "profile_image": null,
                "city": "Toronto",
                "address": "Rua XV, Class A, 30 ",
                "name": "Duarte",
                "phone_number": "(21) 99663-6963",
                "entity_id": "54321234",
                "cpf": "123.000.789-00",
                "state": "CCAA",
                "date_birth": "1986-12-16",
                "email": "playerstars@playerstars.com.br"
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
        When get request is made to /player
        Then The response should have status success
        Then The retrived json has body
        """
        [{
                "entity_id": "id123",
                "favorites": [],
                "blue_star_balance": 123,
                "golden_star_balance": 4321,
                "star_transactions": [],
                "states_regions": [],
                "user": {
                    "country": "Brasil",
                    "nickname": "anselmo.lira",
                    "postal_code": "22333-000",
                    "profile_image": null,
                    "city": "Rio de Janeiro",
                    "address": "Rua José de Figueiredo 192, Blocos 29, 30 - Barra da Tijuca",
                    "name": "Anselmo Lira",
                    "phone_number": "(21) 99663-6963",
                    "entity_id": "54321",
                    "cpf": "123.456.789-00",
                    "state": "Rio de Janeiro",
                    "date_birth": "1986-12-16",
                    "email": "playerstars@playerstars.com.br"
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
                "entity_id": "id123456",
                "favorites": [],
                "blue_star_balance": 123,
                "golden_star_balance": 4321,
                "states_regions": [],
                "star_transactions": [],
                "user": {
                    "country": "Canada",
                    "nickname": "Dudu",
                    "postal_code": "22333-000",
                    "profile_image": null,
                    "city": "Toronto",
                    "address": "Rua XV, Class A, 30 ",
                    "name": "Duarte",
                    "phone_number": "(21) 99663-6963",
                    "entity_id": "54321234",
                    "cpf": "123.000.789-00",
                    "state": "CCAA",
                    "date_birth": "1986-12-16",
                    "email": "playerstars@playerstars.com.br"
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

## Pendente PUT e DELETE
