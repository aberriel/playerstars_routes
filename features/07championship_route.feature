Feature: Championship integration tests
    Scenario: Creating a new championship for players
        Given I set DYNAMODB_URL as http://localhost:8000
        Given I set table name and the adapter class as Console
        Given I save a new entry to the database with json body
        """
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
            "name": "Blizzard"
        }
        """
        Given I save a new entry to the database with json body
        """
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
            "name": "Steam"
        }
        """
        Given I save a new entry to the database with json body
        """
        {
            "entity_id": "3",
            "logo_path": "/images/ss.png",
            "name": "Origin"
        }
        """
        Given I set table name and the adapter class as Player
        Given I save a new entry to the database with json body
        """
        {
            "entity_id": "c2e38849-49b7-48e8-a477-f5618358f429",
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
            "blue_star_balance": 203,
            "consoles": [
                {
                    "entity_id": "3",
                    "logo_path": "/images/ss.png",
                    "name": "Origin",
                    "tag_name": "testeorigin"
                }
            ],
            "entity_id": "cea2d165-3528-4bce-8c0b-2d3775693c95",
            "golden_star_balance": 299,
            "player_status": "OFFLINE",
            "points": 200,
            "star_transactions": [
                {
                    "coin_type": "GOLDEN_STAR",
                    "operation_date": "2019-11-22T20:44:08.231379",
                    "operation_type": "DEBIT",
                    "source": "FINANCIAL_TRANSACTION",
                    "source_id": "Convert Stars",
                    "value": 1
                },
                {
                    "coin_type": "BLUE_STAR",
                    "operation_date": "2019-11-22T20:44:08.231379",
                    "operation_type": "CREDIT",
                    "source": "FINANCIAL_TRANSACTION",
                    "source_id": "Convert Stars",
                    "value": 3
                }
            ],
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
                    "tag_name": "xi"
                }
            ],
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
                "profile_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADEAAAA7CAYAAADSB2J6AAAAAXNSR0IArs4c6QAABNpJREFUaAXVmW2IVFUYx9vM3dooSy1TS5css+yFUDP7kEQpCoLoEoWftkCx+hBEEkEQ9aWCBImgD+JHPygVSAW92maxuoZZrJqF9rZpGb2QllaW2+9Xe2fVnZl7ZubcOzN/+DEz557zPM+5595znnOm5Yz4asHkDBgPEwY/v+PzIPi5AwYgmnQYS3dgqBMWwyE4AAYudkYmwjjYBC/B29AQuokoXoc+WAVXQjl53XrWt53t6yZH8XH4Fh6AM6ESWd92ttdO7joLjxugB86v0bvtHZXNEPPxLhuWjj6BN6CtbM3wi9rphteg0hGlSeV6hiZHwNGIKe29A9rPVJ1Y3wvtGXnRrvb1k4kc5l2wKBPrQ0a1r59MHqsuDG+BPKSfriwc9WL0tiwMF7Gpn21FymsqcpX9BUbWZCW8sX70p99UjUit8X+FZXz8AaYKeegETq4Fp96P0hyGvjxXY8i1IU/txNn0EIehnTB5M5HLU0nimOqzkk70p1qLW8GcynQ+VaGdOI6ls1Otxa2gP/2mKrQTwUOb6jG8gqPgJipVoZ34HksXp1qLW8HpNWonPsRgXgtdciv0p99oOg9LZq7nRrNY3pB+DkPQXiX0cbID22Ee5KH5OHEU7EhUafgzCF3lq3Wuff3oLxN5OrEiE8tDRpfz1c1RZpqNZWeMSRl50K729ZOp7sW6w31hZC/a81BN+7nIfbAOXZBi6BKM7INnYxirxMYjVDafuqaSRkXq2l47jxW5lkvRErwcgrUwpkKP1red7bVTV12E96fhR1gPd0IrFJPlXree9W1n+5rUUlProca+lHNgKdwKHfAXuBv8E9rArNROfAnvwcuwFX6FmlRtJzzoWgiu4HNhMvhi7ofPwcBctJLg7Yj8AxfAVJgCl8MX0A1vwltgnUx1Gdafgx9gM6wCT7WrvRmmPY7go9ADrhGrwdkqukZj8QX4GZ4A72IWugqjvieedKwBE88oWoyVA+AcXvNLGBjReOo9D1/D/MA2Jau5FnwFPvf10AKcute+r1rnK2joTFLp/F+tv1LtOrgwAMtLVShV/tBgw7GlKuRcPhF/3tDgvGomlV1Fx0EjaTLBOCtOSwvKuX0HdKVVrNP1B/HbDWWn9Iep4ManUeW60gsl3492LjpcHdDIuo7g+sGsYZh8aV4dVtqYBe8TVmex0DyFvr3YhQYsswPvnh7XFRQchLIvzOmN6vh7JL5NTf6bQUcMBnIPn+b3zfI4nSDWG8AsufAnjEPjEt9MuotgNyUBmyn+BuckBU3yaWZ9GFqdd2+BrXAMmkluC/bALDsxE7ZDM+oDgp5jJ1zgJjRjD4jZBe+4sbsV/Any2vDoM5Z8pGYkxtzjuntzD90sWkegLgunrG0rKRgAO+T826hyb/EUbIPWYkGaXG0Ah2kj3A2NMPWOJY77wRMW7/6TULjRpwwFFxL5J+MiWApz4VPoAROvj8GzIkctC/lXlxufWXAzzAYPDl6BF8GOHIGCSnWiUIEvjoQvj+uJ3AhjoA/sUP9JfMN3F07XnN/B9CCRM2E7aE8mgY+GGKSBTwcnmr1gQuoj0wu7oeShWkgnaD9Moyi5Hnz8nAwSLuW7GYBBekf/hqODv03a/G4H7agJp5NJgieIBrsfTu48P+srXzyPLQvPbxbh/AtzHtmMLsW1OQAAAABJRU5ErkJggg==",
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
                    "tag_name": "lbliz"
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
                    "tag_name": "leste"
                },
                {
                    "entity_id": "3",
                    "logo_path": "/images/ss.png",
                    "name": "Origin",
                    "tag_name": "leog"
                }
            ],
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
            "owner": "c2e38849-49b7-48e8-a477-f5618358f429",
            "is_open": true,
            "price_to_enter": 3,
            "members": ["ecc4a0c8-329a-41e9-a069-a76fc27abb69"],
            "championship_type": "Player",
            "max_members": 4,
            "start_datetime": "2019-12-10T13:25:07+00:00"
        }
        """
        When post request is made to /championship
#        Then The response should have status success
#        Then The response should have status_code 201
#        Then The saved championship has body
#        """
#        {
#            "owner": {
#                "member_category": "owner",
#                "member": "c2e38849-49b7-48e8-a477-f5618358f429",
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
#            "entity_id": "9d085436-3c5e-47e1-b493-0e8a571f2aff",
#            "members": [
#                {
#                    "member_category": "member",
#                    "member": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
#                    "member_status": "Invited",
#                    "invitation_code": "1234",
#                    "member_type": "Player",
#                    "last_status_change_date": "2019-11-27T17:48:40.643826",
#                    "current_or_last_duel": null,
#                    "member_name": "Arnaud"
#                },
#                {
#                    "member_category": "owner",
#                    "member": "c2e38849-49b7-48e8-a477-f5618358f429",
#                    "member_status": "Member",
#                    "invitation_code": null,
#                    "member_type": "Player",
#                    "last_status_change_date": "2019-11-27T17:49:13.370766",
#                    "current_or_last_duel": null,
#                    "member_name": "teste"
#                }
#            ],
#            "championship_type": "Player",
#            "console": {
#                "logo_path": "/images/ss.png",
#                "tag_name": null,
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
#                "name": "Blizzard",
#                "entity_id": "2"
#            },
#            "start_datetime": "2019-11-30T19:30:35",
#            "status": "Provisioning",
#            "name": "Brazucas",
#            "is_open": true,
#            "balance": 0,
#            "max_members": 4,
#            "game": {
#                "logo_path": "/images/hearthstone.jpg",
#                "name": "Hearthstone",
#                "points": 0,
#                "entity_id": "a8b7c2e4-7d89-4a24-965b-7c201e4bbe37"
#            },
#            "price_to_enter": 2
#        }
#        """
#        Given I set table name and the adapter class as Notification
#        Then The saved json has body
#        """
#        {
#            "championship_id": "123",
#            "duel_id": null,
#            "notification_type": "CHAMPIONSHIP_INVITE_PLAYER",
#            "status": "CREATED",
#            "team_id": null,
#            "entity_id": "5f7e4875-9d08-411a-b8e0-3225e801e1e1",
#            "player_id": "ecc4a0c8-329a-41e9-a069-a76fc27abb69",
#            "creation_datetime": "2019-11-28T01:18:35.838175"
#        }
#        """
#        Then I delete the test entry
#        Given I set table name and the adapter class as Championship
#        Then I delete the test entry
