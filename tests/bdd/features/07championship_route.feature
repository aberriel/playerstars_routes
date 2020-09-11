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
            "is_open": true,
            "price_to_enter": 3,
            "members": ["ecc4a0c8-329a-41e9-a069-a76fc27abb69"],
            "championship_type": "Player",
            "max_members": 4,
            "start_datetime": "2034-12-10T13:25:07+00:00",
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


    Scenario: Creating a new championship for teams
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
            "consoles": [{
                "entity_id": "123",
                "name": "Super Nintendo",
                "games": [
                    {
                    "entity_id": "234",
                    "logo_path": "images/sonic.jpg",
                    "name": "Sonic",
                    "points": 0
                    }
                ],
                "tag_name": "nick#1",
                "logo_path": "/images/sn.png"
            }],
            "player_status": "OFFLINE",
            "points": 200,
            "terms": true
        }
        """
        Given I save a new entry to the database with json body
        """
        {
            "blue_star_balance": 200,
            "consoles": [{
                "entity_id": "123",
                "name": "Super Nintendo",
                "games": [
                    {
                    "entity_id": "234",
                    "logo_path": "images/sonic.jpg",
                    "name": "Sonic",
                    "points": 0
                    }
                ],
                "tag_name": "nick#1",
                "logo_path": "/images/sn.png"
            }],
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
        Given I save a new entry to the database with json body
        """
        {
            "blue_star_balance": 203,
            "consoles": [{
                "entity_id": "123",
                "name": "Super Nintendo",
                "games": [
                    {
                    "entity_id": "234",
                    "logo_path": "images/sonic.jpg",
                    "name": "Sonic",
                    "points": 0
                    }
                ],
                "tag_name": "nick#1",
                "logo_path": "/images/sn.png"
            }],
            "entity_id": "cea2d165-3528-4bce-8c0b-2d3775693c95",
            "golden_star_balance": 299,
            "player_status": "OFFLINE",
            "points": 200,
            "star_transactions": [],
            "terms": true,
            "user": {
                "city": "Rio de Janeiro",
                "country": "Brasil",
                "cpf": "144.216.417-40",
                "date_birth": "1994-10-16",
                "email": "luciano.souza@stormsec.com.br",
                "name": "LUCIANO ANDRADE DE SOUZA",
                "neighborhood": "Maria da Graça",
                "nickname": "luc16",
                "phone_number": "(021) 97496-0917",
                "postal_code": "21050-582",
                "profile_image": "http://playerstars-dev-photos.s3-website-us-east-1.amazonaws.com/cea2d165-3528-4bce-8c0b-2d3775693c95-photo.jpeg",
                "state": "RJ",
                "street": "Rua Conde de Azambuja, 140",
                "street_complement": "Ap 507",
                "street_number": "140"
            }
        }
        """
        Given I save a new entry to the database with json body
        """
        {
            "blue_star_balance": 200,
            "consoles": [{
                "entity_id": "123",
                "name": "Super Nintendo",
                "games": [
                    {
                    "entity_id": "234",
                    "logo_path": "images/sonic.jpg",
                    "name": "Sonic",
                    "points": 0
                    }
                ],
                "tag_name": "nick#1",
                "logo_path": "/images/sn.png"
            }],
            "entity_id": "9069e8a9-1b05-48d2-a988-20b4db85745f",
            "golden_star_balance": 300,
            "player_status": "OFFLINE",
            "points": 200,
            "terms": true,
            "user": {
                "city": "fduhfu",
                "country": "Brasil",
                "cpf": "123.545.456-78",
                "date_birth": "1998-02-12",
                "email": "d1236994@urhen.com",
                "name": "ximira",
                "neighborhood": "djnfdj",
                "nickname": "ximirinha",
                "phone_number": "(021) 12345-6787",
                "postal_code": "12345-678",
                "profile_image": "data:image/png;base64,iVB2",
                "state": "AL",
                "street": "kdfkdn",
                "street_complement": "hbdfhjdbfd",
                "street_number": "545"
            }
        }
        """
        Given I save a new entry to the database with json body
        """
        {
            "blue_star_balance": 200,
            "consoles": [{
                "entity_id": "123",
                "name": "Super Nintendo",
                "games": [
                    {
                    "entity_id": "234",
                    "logo_path": "images/sonic.jpg",
                    "name": "Sonic",
                    "points": 0
                    }
                ],
                "tag_name": "nick#1",
                "logo_path": "/images/sn.png"
            }],
            "entity_id": "dddb5eb2-c2bd-4078-af8a-5b098a4db934",
            "golden_star_balance": 300,
            "player_status": "OFFLINE",
            "points": 200,
            "terms": true,
            "user": {
                "city": "Rio De Janeiro",
                "country": "Brazil",
                "cpf": "10610015710",
                "date_birth": "2019-11-22",
                "email": "leonardo.arnaud.java@gmail.com",
                "name": "Leonardo B A",
                "neighborhood": "Guara",
                "nickname": "Leonardo",
                "phone_number": "11111111111",
                "postal_code": "230503",
                "state": "RJ",
                "street": "Tiba",
                "street_complement": "111",
                "street_number": "111"
            }
        }
        """
        Given I set table name and the adapter class as Team
        Given I save a new entry to the database with json body
        """
        {
          "captain": {
            "association_date": "2019-11-18T21:42:53.267340",
            "entity_id": "290f6c46-a844-4207-a0ad-bd8b080641b5",
            "member_type": "CAPTAIN",
            "player": {
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
                "consoles": [{
                    "entity_id": "123",
                    "name": "Super Nintendo",
                    "games": [
                        {
                        "entity_id": "234",
                        "logo_path": "images/sonic.jpg",
                        "name": "Sonic",
                        "points": 0
                        }
                    ],
                    "tag_name": "nick#1",
                    "logo_path": "/images/sn.png"
                }],
                "player_status": "OFFLINE",
                "points": 200,
                "terms": true
            },
            "status": "ACCEPTED"
          },
          "consoles": [{
                "entity_id": "123",
                "name": "Super Nintendo",
                "games": [
                    {
                    "entity_id": "234",
                    "logo_path": "images/sonic.jpg",
                    "name": "Sonic",
                    "points": 0
                    }
                ],
                "tag_name": "nick#1",
                "logo_path": "/images/sn.png"
            }],
          "description": "time twste",
          "entity_id": "0b878258-afdc-4a76-8af0-f26015f6a817",
          "logo_path": "http://playerstars-dev-photos.s3-website-us-east-1.amazonaws.com/0b878258-afdc-4a76-8af0-f26015f6a817-photo.jpg",
          "members": [
            {
              "association_date": "2019-11-18T21:42:53.347984",
              "entity_id": "4c332a01-c1ce-4e77-b9ef-c1f3fca0595b",
              "member_type": "MEMBER",
              "player": {
                    "blue_star_balance": 200,
                    "consoles": [{
                        "entity_id": "123",
                        "name": "Super Nintendo",
                        "games": [
                            {
                            "entity_id": "234",
                            "logo_path": "images/sonic.jpg",
                            "name": "Sonic",
                            "points": 0
                            }
                        ],
                        "tag_name": "nick#1",
                        "logo_path": "/images/sn.png"
                    }],
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
                },
              "status": "INVITED"
            }
          ],
          "name": "Teste2"
        }
        """
        Given I save a new entry to the database with json body
        """
        {
          "captain": {
            "association_date": "2019-11-18T21:42:53.267340",
            "entity_id": "300f6c46-a844-4207-a0ad-bd8b080641b5",
            "member_type": "CAPTAIN",
            "player": {
                "blue_star_balance": 203,
                "consoles": [{
                    "entity_id": "123",
                    "name": "Super Nintendo",
                    "games": [
                        {
                        "entity_id": "234",
                        "logo_path": "images/sonic.jpg",
                        "name": "Sonic",
                        "points": 0
                        }
                    ],
                    "tag_name": "nick#1",
                    "logo_path": "/images/sn.png"
                }],
                "entity_id": "cea2d165-3528-4bce-8c0b-2d3775693c95",
                "golden_star_balance": 299,
                "player_status": "OFFLINE",
                "points": 200,
                "star_transactions": [],
                "terms": true,
                "user": {
                    "city": "Rio de Janeiro",
                    "country": "Brasil",
                    "cpf": "144.216.417-40",
                    "date_birth": "1994-10-16",
                    "email": "luciano.souza@stormsec.com.br",
                    "name": "LUCIANO ANDRADE DE SOUZA",
                    "neighborhood": "Maria da Graça",
                    "nickname": "luc16",
                    "phone_number": "(021) 97496-0917",
                    "postal_code": "21050-582",
                    "profile_image": "http://playerstars-dev-photos.s3-website-us-east-1.amazonaws.com/cea2d165-3528-4bce-8c0b-2d3775693c95-photo.jpeg",
                    "state": "RJ",
                    "street": "Rua Conde de Azambuja, 140",
                    "street_complement": "Ap 507",
                    "street_number": "140"
                }
            },
            "status": "ACCEPTED"
          },
          "consoles": [{
                "entity_id": "123",
                "name": "Super Nintendo",
                "games": [
                    {
                    "entity_id": "234",
                    "logo_path": "images/sonic.jpg",
                    "name": "Sonic",
                    "points": 0
                    }
                ],
                "tag_name": "nick#1",
                "logo_path": "/images/sn.png"
            }],
          "description": "time twste",
          "entity_id": "1c878258-afdc-4a76-8af0-f26015f6a817",
          "logo_path": "http://playerstars-dev-photos.s3-website-us-east-1.amazonaws.com/0b878258-afdc-4a76-8af0-f26015f6a817-photo.jpg",
          "members": [
            {
              "association_date": "2019-11-18T21:42:53.347984",
              "entity_id": "5d332a01-c1ce-4e77-b9ef-c1f3fca0595b",
              "member_type": "MEMBER",
              "player": {
                    "blue_star_balance": 200,
                    "consoles": [{
                        "entity_id": "123",
                        "name": "Super Nintendo",
                        "games": [
                            {
                            "entity_id": "234",
                            "logo_path": "images/sonic.jpg",
                            "name": "Sonic",
                            "points": 0
                            }
                        ],
                        "tag_name": "nick#1",
                        "logo_path": "/images/sn.png"
                    }],
                    "entity_id": "9069e8a9-1b05-48d2-a988-20b4db85745f",
                    "golden_star_balance": 300,
                    "player_status": "OFFLINE",
                    "points": 200,
                    "terms": true,
                    "user": {
                        "city": "fduhfu",
                        "country": "Brasil",
                        "cpf": "123.545.456-78",
                        "date_birth": "1998-02-12",
                        "email": "d1236994@urhen.com",
                        "name": "ximira",
                        "neighborhood": "djnfdj",
                        "nickname": "ximirinha",
                        "phone_number": "(021) 12345-6787",
                        "postal_code": "12345-678",
                        "profile_image": "data:image/png;base64,iVB2",
                        "state": "AL",
                        "street": "kdfkdn",
                        "street_complement": "hbdfhjdbfd",
                        "street_number": "545"
                    }
                },
              "status": "INVITED"
            },{
              "association_date": "2019-11-18T21:42:53.347984",
              "entity_id": "6e332a01-c1ce-4e77-b9ef-c1f3fca0595b",
              "member_type": "MEMBER",
              "player": {
                    "blue_star_balance": 200,
                    "consoles": [{
                        "entity_id": "123",
                        "name": "Super Nintendo",
                        "games": [
                            {
                            "entity_id": "234",
                            "logo_path": "images/sonic.jpg",
                            "name": "Sonic",
                            "points": 0
                            }
                        ],
                        "tag_name": "nick#1",
                        "logo_path": "/images/sn.png"
                    }],
                    "entity_id": "dddb5eb2-c2bd-4078-af8a-5b098a4db934",
                    "golden_star_balance": 300,
                    "player_status": "OFFLINE",
                    "points": 200,
                    "terms": true,
                    "user": {
                        "city": "Rio De Janeiro",
                        "country": "Brazil",
                        "cpf": "10610015710",
                        "date_birth": "2019-11-22",
                        "email": "leonardo.arnaud.java@gmail.com",
                        "name": "Leonardo B A",
                        "neighborhood": "Guara",
                        "nickname": "Leonardo",
                        "phone_number": "11111111111",
                        "postal_code": "230503",
                        "state": "RJ",
                        "street": "Tiba",
                        "street_complement": "111",
                        "street_number": "111"
                    }
                },
              "status": "INVITED"
            }
          ],
          "name": "Teste3"
        }
        """
        Given The request has json body
        """
        {
            "name": "Brazucas",
            "game": {
                "entity_id": "234",
                "logo_path": "images/sonic.jpg",
                "name": "Sonic"
            },
            "console": {
                "entity_id": "123",
                "name": "Super Nintendo",
                "games": [
                    {
                    "entity_id": "234",
                    "logo_path": "images/sonic.jpg",
                    "name": "Sonic",
                    "points": 0
                    }
                ],
                "tag_name": "nick#1",
                "logo_path": "/images/sn.png"
            },
            "owner": "0b878258-afdc-4a76-8af0-f26015f6a817",
            "is_open": true,
            "price_to_enter": 3,
            "members": ["1c878258-afdc-4a76-8af0-f26015f6a817"],
            "championship_type": "Team",
            "max_members": 4,
            "start_datetime": "2034-12-10T13:25:07+00:00",
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
            "last_status_change_date": "2019-12-04T21:03:41.956231",
            "member_type": "Team",
            "member": "0b878258-afdc-4a76-8af0-f26015f6a817",
            "member_name": "Teste2",
            "member_category": "owner",
            "member_status": "Member"
          },
          "console": {
            "name": "Super Nintendo",
            "games": [
              {
                "name": "Sonic",
                "entity_id": "234",
                "logo_path": "images/sonic.jpg",
                "points": 0
              }
            ],
            "entity_id": "123",
            "logo_path": "/images/sn.png",
            "tag_name": "nick#1"
          },
          "game": {
            "name": "Sonic",
            "entity_id": "234",
            "logo_path": "images/sonic.jpg",
            "points": 0
          },
          "price_to_enter": 3,
          "is_open": true,
          "start_datetime": "2019-12-10T13:25:07+00:00",
          "members": [
            {
              "member_type": "Team",
              "invitation_code": "73d0f9c6-10ea-4cd9-b169-b8dcb9d75cd8",
              "member_status": "Invited",
              "last_status_change_date": "2019-12-04T21:03:41.972186",
              "member": "1c878258-afdc-4a76-8af0-f26015f6a817",
              "member_name": "Teste2",
              "member_category": "member"
            },
            {
              "last_status_change_date": "2019-12-04T21:03:41.956231",
              "member_type": "Team",
              "member": "0b878258-afdc-4a76-8af0-f26015f6a817",
              "member_name": "Teste2",
              "member_category": "owner",
              "member_status": "Member"
            }
          ],
          "championship_type": "Team",
          "name": "Brazucas",
          "max_members": 4,
          "entity_id": "bcda4c04-cbe2-4f70-b916-29d8de7efb35",
          "status": "Provisioning",
          "mounted_keys": false,
          "balance": 0
        }
        """
        Then I clean the Championship table
        Given I set table name and the adapter class as Notification
        Then The follow notification is saved in the database
        """
        {
            "championship_id": "ec41a3cc-1f9b-44ec-911d-54e041070d9d",
            "duel_id": null,
            "notification_type": "CHAMPIONSHIP_INVITE_TEAM",
            "status": "CREATED",
            "team_id": "1c878258-afdc-4a76-8af0-f26015f6a817",
            "player_id": "cea2d165-3528-4bce-8c0b-2d3775693c95"
        }
        """
        Then I clean the Notification table
        Given I set table name and the adapter class as Player
        Then I clean the Player table
        Given I set table name and the adapter class as Team
        Then I clean the Team table


    Scenario: Accepting a championship invitation
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
        Given I set table name and the adapter class as Championship
        Given I save a new entry to the database with json body
        """
        {
            "start_datetime": "2034-12-10T13:25:07+00:00",
            "entity_id": "champ123",
            "owner": {
                "member_category": "owner",
                "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
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
                  "member_type": "Player",
                  "invitation_code": "1234",
                  "member_status": "Invited",
                  "member": "8ad1635f-2263-4dda-879a-bd24b5d9732f",
                  "last_status_change_date": "2019-11-27T17:48:40.643826",
                  "member_name": "Arnaud",
                  "member_category": "member"
                },
                {
                  "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
                  "last_status_change_date": "2019-11-27T17:49:13.370766",
                  "member_type": "Player",
                  "member_name": "teste",
                  "member_category": "owner",
                  "member_status": "Member"
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
        Given The request has json body
        """
        {
            "invitation_code": "1234",
            "accepted": true
        }
        """
        When POST request is made to /championship/accept-invitation
        Then The response should have status success
        Then The response should have status_code 200
        Then The saved championship has body
        """
        {
            "start_datetime": "2034-12-10T13:25:07+00:00",
            "entity_id": "champ123",
            "owner": {
                "member_category": "owner",
                "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
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
                    "member": "8ad1635f-2263-4dda-879a-bd24b5d9732f",
                    "member_status": "Member",
                    "invitation_code": "1234",
                    "member_type": "Player",
                    "last_status_change_date": "2019-11-27T17:48:40.643826",
                    "current_or_last_duel": null,
                    "member_name": "Arnaud"
                },
                {
                    "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
                    "last_status_change_date": "2019-11-27T17:49:13.370766",
                    "member_type": "Player",
                    "member_name": "teste",
                    "member_category": "owner",
                    "member_status": "Member"
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
        Given I set table name and the adapter class as Player
        Then I clean the Player table
        Given I set table name and the adapter class as Championship
        Then I clean the Championship table


    Scenario: Entering an open championship
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
        Given I set table name and the adapter class as Championship
        Given I save a new entry to the database with json body
        """
        {
            "start_datetime": "2034-12-10T13:25:07+00:00",
            "entity_id": "champ123",
            "owner": {
                "member_category": "owner",
                "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
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
            "members": [{
                "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
                "last_status_change_date": "2019-11-27T17:49:13.370766",
                "member_type": "Player",
                "member_name": "teste",
                "member_category": "owner",
                "member_status": "Member"
            }],
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
        Given The request has json body
        """
        {
            "member_id": "8ad1635f-2263-4dda-879a-bd24b5d9732f",
            "member_type": "Player",
            "championship_id": "champ123"
        }
        """
        When POST request is made to /championship/join
        Then The response should have status success
        Then The response should have status_code 200
        Then The saved championship has body
        """
        {
            "start_datetime": "2034-12-10T13:25:07+00:00",
            "entity_id": "champ123",
            "owner": {
                "member_category": "owner",
                "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
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
                  "member_type": "Player",
                  "invitation_code": "1234",
                  "member_status": "Invited",
                  "member": "8ad1635f-2263-4dda-879a-bd24b5d9732f",
                  "last_status_change_date": "2019-11-27T17:48:40.643826",
                  "member_name": "Arnaud",
                  "member_category": "member"
                },
                {
                  "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
                  "last_status_change_date": "2019-11-27T17:49:13.370766",
                  "member_type": "Player",
                  "member_name": "teste",
                  "member_category": "owner",
                  "member_status": "Member"
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
        Given I set table name and the adapter class as Player
        Then I clean the Player table
        Given I set table name and the adapter class as Championship
        Then I clean the Championship table

#    Scenario: Inviting a friend to a championship
#        Given I set DYNAMODB_URL as http://localhost:8000
#        Given I set table name and the adapter class as Player
#        Given I save a new entry to the database with json body
#        """
#        {
#            "entity_id": "8ad1635f-2263-4dda-879a-bd24b5d9732f",
#            "favorites": [
#                "cea2d165-3528-4bce-8c0b-2d3775693c95",
#                "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
#                "9069e8a9-1b05-48d2-a988-20b4db85745f"
#            ],
#            "blue_star_balance": 200,
#            "golden_star_balance": 300,
#            "states_regions": [],
#            "star_transactions": [],
#            "user": {
#                "country": "Brazil",
#                "nickname": "teste",
#                "postal_code": "22233112",
#                "profile_image": null,
#                "city": "cidae",
#                "cpf": "341.398.354-78",
#                "date_birth": "2019-11-13",
#                "email": "d1904781@urhen.com",
#                "name": "teste1",
#                "neighborhood": "bairri",
#                "phone_number": "11111111111",
#                "state": "rj",
#                "street": "ruq",
#                "street_complement": "333",
#                "street_number": "3"
#            },
#            "consoles": [
#                {
#                    "entity_id": "2",
#                    "games": [
#                        {
#                            "entity_id": "a8b7c2e4-7d89-4a24-965b-7c201e4bbe37",
#                            "logo_path": "/images/hearthstone.jpg",
#                            "name": "Hearthstone"
#                        },
#                        {
#                            "entity_id": "6086715d-8f78-41a3-810d-d15f42439005",
#                            "logo_path": "/images/overwatch-e1464700106237.jpg",
#                            "name": "Overwatch"
#                        },
#                        {
#                            "entity_id": "8b348817-8f75-4246-917c-48e0e433efda",
#                            "logo_path": "/images/wow_NAAao0m.jpg",
#                            "name": "World of Warcraft"
#                        }
#                    ],
#                    "logo_path": "/images/ss.png",
#                    "name": "Blizzard",
#                    "tag_name": "testebli"
#                },
#                {
#                    "entity_id": "4",
#                    "games": [
#                        {
#                            "entity_id": "396a0d86-a1c4-4d8d-9419-f382c426d5eb",
#                            "logo_path": "https://www.pcgamesn.com/wp-content/CSGO-tips.jpg",
#                            "name": "CS.GO"
#                        },
#                        {
#                            "entity_id": "0f185dbc-2fca-4e2d-b9b8-c21c8276cca0",
#                            "logo_path": "/images/lol.jpg",
#                            "name": "League of Legends"
#                        },
#                        {
#                            "entity_id": "5c7f74b2-30ef-4280-a10a-c810d23374e7",
#                            "logo_path": "https://steamcdn-a.akamaihd.net/steam/apps/570/header.jpg",
#                            "name": "Dota 2"
#                        }
#                    ],
#                    "logo_path": "/images/ss.png",
#                    "name": "Steam",
#                    "tag_name": "testesteam"
#                },
#                {
#                    "entity_id": "3",
#                    "logo_path": "/images/ss.png",
#                    "name": "Origin",
#                    "tag_name": "testeorigin"
#                }
#            ],
#            "player_status": "OFFLINE",
#            "points": 200,
#            "terms": true
#        }
#        """
#        Given I save a new entry to the database with json body
#        """
#        {
#            "blue_star_balance": 200,
#            "consoles": [
#                {
#                    "entity_id": "2",
#                    "games": [
#                        {
#                            "entity_id": "a8b7c2e4-7d89-4a24-965b-7c201e4bbe37",
#                            "logo_path": "/images/hearthstone.jpg",
#                            "name": "Hearthstone"
#                        },
#                        {
#                            "entity_id": "6086715d-8f78-41a3-810d-d15f42439005",
#                            "logo_path": "/images/overwatch-e1464700106237.jpg",
#                            "name": "Overwatch"
#                        },
#                        {
#                            "entity_id": "8b348817-8f75-4246-917c-48e0e433efda",
#                            "logo_path": "/images/wow_NAAao0m.jpg",
#                            "name": "World of Warcraft"
#                        }
#                    ],
#                    "logo_path": "/images/ss.png",
#                    "name": "Blizzard",
#                    "tag_name": "leobliz"
#                },
#                {
#                    "entity_id": "4",
#                    "games": [
#                        {
#                            "entity_id": "396a0d86-a1c4-4d8d-9419-f382c426d5eb",
#                            "logo_path": "https://www.pcgamesn.com/wp-content/CSGO-tips.jpg",
#                            "name": "CS.GO"
#                        },
#                        {
#                            "entity_id": "0f185dbc-2fca-4e2d-b9b8-c21c8276cca0",
#                            "logo_path": "/images/lol.jpg",
#                            "name": "League of Legends"
#                        },
#                        {
#                            "entity_id": "5c7f74b2-30ef-4280-a10a-c810d23374e7",
#                            "logo_path": "https://steamcdn-a.akamaihd.net/steam/apps/570/header.jpg",
#                            "name": "Dota 2"
#                        }
#                    ],
#                    "logo_path": "/images/ss.png",
#                    "name": "Steam",
#                    "tag_name": "leosteam"
#                },
#                {
#                    "entity_id": "3",
#                    "logo_path": "/images/ss.png",
#                    "name": "Origin",
#                    "tag_name": "leogin"
#                }
#            ],
#            "entity_id": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
#            "favorites": [
#                "dddb5eb2-c2bd-4078-af8a-5b098a4db934"
#            ],
#            "golden_star_balance": 300,
#            "player_status": "OFFLINE",
#            "points": 200,
#            "terms": true,
#            "user": {
#                "city": "Rio De Janeiro",
#                "country": "Brazil",
#                "cpf": "10610015710",
#                "date_birth": "2016-11-21",
#                "email": "leonardo.arnaud@stormsec.com.br",
#                "name": "Leonardo B. Arnaud",
#                "neighborhood": "Guaratiba",
#                "nickname": "Arnaud",
#                "phone_number": "11111111111",
#                "postal_code": "23033100",
#                "state": "RJ",
#                "street": "Rua Lassance",
#                "street_complement": "30",
#                "street_number": "30"
#            }
#        }
#        """
#        Given I set table name and the adapter class as Championship
#        Given I save a new entry to the database with json body
#        """
#        {
#            "start_datetime": "2034-12-10T13:25:07+00:00",
#            "entity_id": "champ123",
#            "owner": {
#                "member_category": "owner",
#                "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
#                "member_status": "Member",
#                "invitation_code": null,
#                "member_type": "Player",
#                "last_status_change_date": "2019-11-27T17:49:13.370766",
#                "current_or_last_duel": null,
#                "member_name": "teste"
#            },
#            "duels": [],
#            "mounted_keys": false,
#            "finish_datetime": null,
#            "members": [{
#                "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
#                "last_status_change_date": "2019-11-27T17:49:13.370766",
#                "member_type": "Player",
#                "member_name": "teste",
#                "member_category": "owner",
#                "member_status": "Member"
#            }],
#            "championship_type": "Player",
#            "console": {
#                "logo_path": "/images/ss.png",
#                "tag_name": null,
#                "entity_id" : "123",
#                "games": [
#                    {
#                        "logo_path": "/images/hearthstone.jpg",
#                        "name": "Hearthstone",
#                        "points": 0,
#                        "entity_id": "a8b7c2e4-7d89-4a24-965b-7c201e4bbe37"
#                    },
#                    {
#                        "logo_path": "/images/overwatch-e1464700106237.jpg",
#                        "name": "Overwatch",
#                        "points": 0,
#                        "entity_id": "6086715d-8f78-41a3-810d-d15f42439005"
#                    },
#                    {
#                        "logo_path": "/images/wow_NAAao0m.jpg",
#                        "name": "World of Warcraft",
#                        "points": 0,
#                        "entity_id": "8b348817-8f75-4246-917c-48e0e433efda"
#                    }
#                ],
#                "name": "Blizzard"
#            },
#            "status": "Provisioning",
#            "name": "Brazucas",
#            "is_open": true,
#            "balance": 0,
#            "max_members": 4,
#            "game": {
#                "entity_id": "123",
#                "logo_path": "/images/hearthstone.jpg",
#                "name": "Hearthstone",
#                "points": 0
#            },
#            "price_to_enter": 3
#        }
#        """
#        Given The request has json body
#        """
#        {
#            "invitation_code"
#        }
#        """
#        When POST request is made to /championship/join
#        Then The response should have status success
#        Then The response should have status_code 200
#        Then The saved championship has body
#        """
#        {
#            "start_datetime": "2034-12-10T13:25:07+00:00",
#            "entity_id": "champ123",
#            "owner": {
#                "member_category": "owner",
#                "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
#                "member_status": "Member",
#                "invitation_code": null,
#                "member_type": "Player",
#                "last_status_change_date": "2019-11-27T17:49:13.370766",
#                "current_or_last_duel": null,
#                "member_name": "teste"
#            },
#            "duels": [],
#            "mounted_keys": false,
#            "finish_datetime": null,
#            "members": [
#                {
#                  "member_type": "Player",
#                  "invitation_code": "1234",
#                  "member_status": "Invited",
#                  "member": "8ad1635f-2263-4dda-879a-bd24b5d9732f",
#                  "last_status_change_date": "2019-11-27T17:48:40.643826",
#                  "member_name": "Arnaud",
#                  "member_category": "member"
#                },
#                {
#                  "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
#                  "last_status_change_date": "2019-11-27T17:49:13.370766",
#                  "member_type": "Player",
#                  "member_name": "teste",
#                  "member_category": "owner",
#                  "member_status": "Member"
#                }
#            ],
#            "championship_type": "Player",
#            "console": {
#                "logo_path": "/images/ss.png",
#                "tag_name": null,
#                "entity_id" : "123",
#                "games": [
#                    {
#                        "logo_path": "/images/hearthstone.jpg",
#                        "name": "Hearthstone",
#                        "points": 0,
#                        "entity_id": "a8b7c2e4-7d89-4a24-965b-7c201e4bbe37"
#                    },
#                    {
#                        "logo_path": "/images/overwatch-e1464700106237.jpg",
#                        "name": "Overwatch",
#                        "points": 0,
#                        "entity_id": "6086715d-8f78-41a3-810d-d15f42439005"
#                    },
#                    {
#                        "logo_path": "/images/wow_NAAao0m.jpg",
#                        "name": "World of Warcraft",
#                        "points": 0,
#                        "entity_id": "8b348817-8f75-4246-917c-48e0e433efda"
#                    }
#                ],
#                "name": "Blizzard"
#            },
#            "status": "Provisioning",
#            "name": "Brazucas",
#            "is_open": true,
#            "balance": 0,
#            "max_members": 4,
#            "game": {
#                "entity_id": "123",
#                "logo_path": "/images/hearthstone.jpg",
#                "name": "Hearthstone",
#                "points": 0
#            },
#            "price_to_enter": 3
#        }
#        """
##        Given I set table name and the adapter class as Player
##        Then I clean the Player table
##        Given I set table name and the adapter class as Championship
##        Then I clean the Championship table

