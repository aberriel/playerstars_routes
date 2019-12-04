Feature: Championship integration
    Scenario: Creating a new championship for players
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Player
        Given I save a new entry to the database with json body
        """
        {
            "entity_id": "8ad1635f-2263-4dda-879a-bd24b5d9732f",
            "favorites": [
                "cea2d165-3528-4bce-8c0b-2d3775693c95",
                "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
                "9069e8a9-1b05-48d2-a988-20b4db85745f"
            ],
            "blue_star_balance": 200,
            "golden_star_balance": 300,
            "states_regions": [],
            "star_transactions": [],
            "user": {
                "country": "Brazil",
                "nickname": "teste",
                "postal_code": "22233112",
                "profile_image": null,
                "city": "cidae",
                "cpf": "341.398.354-78",
                "date_birth": "2019-11-13",
                "email": "d1904781@urhen.com",
                "name": "teste1",
                "neighborhood": "bairri",
                "phone_number": "11111111111",
                "state": "rj",
                "street": "ruq",
                "street_complement": "333",
                "street_number": "3"
            },
            "consoles": [
                {
                    "entity_id": "2",
                    "games": [
                        {
                            "entity_id": "a8b7c2e4-7d89-4a24-965b-7c201e4bbe37",
                            "logo_path": "/images/hearthstone.jpg",
                            "name": "Hearthstone"
                        },
                        {
                            "entity_id": "6086715d-8f78-41a3-810d-d15f42439005",
                            "logo_path": "/images/overwatch-e1464700106237.jpg",
                            "name": "Overwatch"
                        },
                        {
                            "entity_id": "8b348817-8f75-4246-917c-48e0e433efda",
                            "logo_path": "/images/wow_NAAao0m.jpg",
                            "name": "World of Warcraft"
                        }
                    ],
                    "logo_path": "/images/ss.png",
                    "name": "Blizzard",
                    "tag_name": "testebli"
                },
                {
                    "entity_id": "4",
                    "games": [
                        {
                            "entity_id": "396a0d86-a1c4-4d8d-9419-f382c426d5eb",
                            "logo_path": "https://www.pcgamesn.com/wp-content/CSGO-tips.jpg",
                            "name": "CS.GO"
                        },
                        {
                            "entity_id": "0f185dbc-2fca-4e2d-b9b8-c21c8276cca0",
                            "logo_path": "/images/lol.jpg",
                            "name": "League of Legends"
                        },
                        {
                            "entity_id": "5c7f74b2-30ef-4280-a10a-c810d23374e7",
                            "logo_path": "https://steamcdn-a.akamaihd.net/steam/apps/570/header.jpg",
                            "name": "Dota 2"
                        }
                    ],
                    "logo_path": "/images/ss.png",
                    "name": "Steam",
                    "tag_name": "testesteam"
                },
                {
                    "entity_id": "3",
                    "logo_path": "/images/ss.png",
                    "name": "Origin",
                    "tag_name": "testeorigin"
                }
            ],
            "player_status": "OFFLINE",
            "points": 200,
            "terms": true
        }
        """
        Given I save a new entry to the database with json body
        """
        {
            "blue_star_balance": 200,
            "consoles": [
                {
                    "entity_id": "2",
                    "games": [
                        {
                            "entity_id": "a8b7c2e4-7d89-4a24-965b-7c201e4bbe37",
                            "logo_path": "/images/hearthstone.jpg",
                            "name": "Hearthstone"
                        },
                        {
                            "entity_id": "6086715d-8f78-41a3-810d-d15f42439005",
                            "logo_path": "/images/overwatch-e1464700106237.jpg",
                            "name": "Overwatch"
                        },
                        {
                            "entity_id": "8b348817-8f75-4246-917c-48e0e433efda",
                            "logo_path": "/images/wow_NAAao0m.jpg",
                            "name": "World of Warcraft"
                        }
                    ],
                    "logo_path": "/images/ss.png",
                    "name": "Blizzard",
                    "tag_name": "leobliz"
                },
                {
                    "entity_id": "4",
                    "games": [
                        {
                            "entity_id": "396a0d86-a1c4-4d8d-9419-f382c426d5eb",
                            "logo_path": "https://www.pcgamesn.com/wp-content/CSGO-tips.jpg",
                            "name": "CS.GO"
                        },
                        {
                            "entity_id": "0f185dbc-2fca-4e2d-b9b8-c21c8276cca0",
                            "logo_path": "/images/lol.jpg",
                            "name": "League of Legends"
                        },
                        {
                            "entity_id": "5c7f74b2-30ef-4280-a10a-c810d23374e7",
                            "logo_path": "https://steamcdn-a.akamaihd.net/steam/apps/570/header.jpg",
                            "name": "Dota 2"
                        }
                    ],
                    "logo_path": "/images/ss.png",
                    "name": "Steam",
                    "tag_name": "leosteam"
                },
                {
                    "entity_id": "3",
                    "logo_path": "/images/ss.png",
                    "name": "Origin",
                    "tag_name": "leogin"
                }
            ],
            "entity_id": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
            "favorites": [
                "dddb5eb2-c2bd-4078-af8a-5b098a4db934"
            ],
            "golden_star_balance": 300,
            "player_status": "OFFLINE",
            "points": 200,
            "terms": true,
            "user": {
                "city": "Rio De Janeiro",
                "country": "Brazil",
                "cpf": "10610015710",
                "date_birth": "2016-11-21",
                "email": "leonardo.arnaud@stormsec.com.br",
                "name": "Leonardo B. Arnaud",
                "neighborhood": "Guaratiba",
                "nickname": "Arnaud",
                "phone_number": "11111111111",
                "postal_code": "23033100",
                "state": "RJ",
                "street": "Rua Lassance",
                "street_complement": "30",
                "street_number": "30"
            }
        }
        """
        Given The request has json body
        """
        {
            "name": "Brazucas",
            "game": {
                "entity_id": "a8b7c2e4-7d89-4a24-965b-7c201e4bbe37",
                "logo_path": "/images/hearthstone.jpg",
                "name": "Hearthstone"
            },
            "console": {
                "entity_id": "2",
                "games": [
                    {
                        "entity_id": "a8b7c2e4-7d89-4a24-965b-7c201e4bbe37",
                        "logo_path": "/images/hearthstone.jpg",
                        "name": "Hearthstone"
                    },
                    {
                        "entity_id": "6086715d-8f78-41a3-810d-d15f42439005",
                        "logo_path": "/images/overwatch-e1464700106237.jpg",
                        "name": "Overwatch"
                    },
                    {
                        "entity_id": "8b348817-8f75-4246-917c-48e0e433efda",
                        "logo_path": "/images/wow_NAAao0m.jpg",
                        "name": "World of Warcraft"
                    }
                ],
                "logo_path": "/images/ss.png",
                "name": "Blizzard"
            },
            "owner": "8ad1635f-2263-4dda-879a-bd24b5d9732f",
            "is_open": true,
            "price_to_enter": 3,
            "members": ["ecc4a0c8-329a-41e9-a069-a76fc27abb69"],
            "championship_type": "Player",
            "max_members": 4,
            "start_datetime": "2019-12-10T13:25:07+00:00",
            "mounted_keys": false,
            "balance": 0
        }
        """
        Given I set table name and the adapter class as Championship
        When post request is made to /championship
        Then The response should have status success
        Then The response should have status_code 201
        Then The saved championship has body
        """
        {
            "owner": {
                "member_category": "owner",
                "member": "8ad1635f-2263-4dda-879a-bd24b5d9732f",
                "member_status": "Member",
                "invitation_code": null,
                "member_type": "Player",
                "last_status_change_date": "2019-11-27T17:49:13.370766",
                "current_or_last_duel": null,
                "member_name": "teste"
            },
            "duels": [],
            "mounted_keys": false,
            "finish_datetime": null,
            "members": [
                {
                    "member_category": "member",
                    "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
                    "member_status": "Invited",
                    "invitation_code": "1234",
                    "member_type": "Player",
                    "last_status_change_date": "2019-11-27T17:48:40.643826",
                    "current_or_last_duel": null,
                    "member_name": "Arnaud"
                },
                {
                    "member_category": "owner",
                    "member": "8ad1635f-2263-4dda-879a-bd24b5d9732f",
                    "member_status": "Member",
                    "invitation_code": null,
                    "member_type": "Player",
                    "last_status_change_date": "2019-11-27T17:49:13.370766",
                    "current_or_last_duel": null,
                    "member_name": "teste"
                }
            ],
            "championship_type": "Player",
            "console": {
                "logo_path": "/images/ss.png",
                "tag_name": null,
                "entity_id" : "123",
                "games": [
                    {
                        "logo_path": "/images/hearthstone.jpg",
                        "name": "Hearthstone",
                        "points": 0,
                        "entity_id": "a8b7c2e4-7d89-4a24-965b-7c201e4bbe37"
                    },
                    {
                        "logo_path": "/images/overwatch-e1464700106237.jpg",
                        "name": "Overwatch",
                        "points": 0,
                        "entity_id": "6086715d-8f78-41a3-810d-d15f42439005"
                    },
                    {
                        "logo_path": "/images/wow_NAAao0m.jpg",
                        "name": "World of Warcraft",
                        "points": 0,
                        "entity_id": "8b348817-8f75-4246-917c-48e0e433efda"
                    }
                ],
                "name": "Blizzard"
            },
            "status": "Provisioning",
            "name": "Brazucas",
            "is_open": true,
            "balance": 0,
            "max_members": 4,
            "game": {
                "entity_id": "123",
                "logo_path": "/images/hearthstone.jpg",
                "name": "Hearthstone",
                "points": 0
            },
            "price_to_enter": 3
        }
        """
        Then I clean the Championship table
        Given I set table name and the adapter class as Notification
        Then The follow notification is saved in the database
        """
        {
            "championship_id": "schrubles",
            "duel_id": null,
            "notification_type": "CHAMPIONSHIP_INVITE_PLAYER",
            "status": "CREATED",
            "team_id": null,
            "player_id": "ecc4a0c8-329a-41e9-a069-a76fc27abb69"
        }
        """
        Then I clean the Notification table
        Given I set table name and the adapter class as Player
        Then I clean the Player table
