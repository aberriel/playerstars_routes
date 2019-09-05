Player Stars 
============

##Formato de JSON para rotas
=======================
# # PLAYER ROUTE ## 
=======================


## POST 
# ROTA: "/player/"

#### Request Model:
    {
        "name": "Anselmo Lira",
        "nickname": "anselmo.lira",
        "birth_date": "16/12/1986",
        "cpf": "123.456.789-00",
        "email": "playerstars@playerstars.com.br",
        "phone_number": "(21) 99663-6963",
        "street": "Rua José de Figueiredo",
        "street_number": "192",
        "street_complement": "Blocos 29, 30",
        "neighborhood": "Barra da Tijuca",
        "city": "Rio de Janeiro",
        "state": "Rio de Janeiro",
        "country": "Brasil",
        "postal_code": "22333-000",
        "promo_code": "ABC123",
        "profile_image": "ACCBB4762CF23AA35690CC",
        "favorites":[],
        "blue_star_balance":123,
        "golden_star_balance":  4321,
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
        ]
    }

#### Response Model:
====================
## Status Code : 201
====================

    {
        "status": "success",
        "data": "id0001"
    }

## GET
# ROTA: "/player/{entity_id}"

## DADO QUE EU JA TENHA SALVO O SEGUINTE JSON:
    
    {
        "entity_id": "id0001",
        "favorites": [],
        "blue_star_balance": 123,
        "golden_star_balance": 4321,
        "states_regions": [],
        "user": {
            "group": "player",
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
        "player_status": "PlayerStatus.OFFLINE",
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


#### Response Model:
====================
## Status Code : 200
====================

    {
         "status": "success",
         "data": {

            "entity_id": "id0001",
            "favorites": [],
            "blue_star_balance": 123,
            "golden_star_balance": 4321,
            "states_regions": [],
            "user": {
                "group": "player",
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
            "player_status": "PlayerStatus.OFFLINE",
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
    }

## GET All 
# ROTA : "/player/'

## DADO QUE EU JA TENHA SALVO O SEGUINTE JSON:
    
    {
        "entity_id": "id0001",
        "favorites": [],
        "blue_star_balance": 123,
        "golden_star_balance": 4321,
        "states_regions": [],
        "user": {
            "group": "player",
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
        "player_status": "PlayerStatus.OFFLINE",
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

#### Response Model:
===================
## Status Code : 200
===================
    
    {
         "status": "success",
         "data": {

            "entity_id": "id0001",
            "favorites": [],
            "blue_star_balance": 123,
            "golden_star_balance": 4321,
            "states_regions": [],
            "user": {
                "group": "player",
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
            "player_status": "PlayerStatus.OFFLINE",
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
    }
    
