Player Stars 
============

##Formato de JSON para rota
=======================
# # PLAYER ROUTE ## 
=======================


## POST 
# ROTA: "/player/"

#### Request Model:
    {
	"points": 200,
	"blue_star_balance": 15,
	"consoles": [{
		"entity_id": "1",
		"logo_path": "/images/ss.png",
		"name": "Playstation 4",
		"sync": true,
		"tag_name": "Leoplay4"
	}],
	"countries_regions": [{
        "name": "NA",
        "minimum_bet" : 1234,
        "countries":["EUA", "Mexico", "Canada"],
        "entity_id":"id123"
     }],
	"states_regions": [{
        "name": "Sudeste",
        "minimum_bet" : 123,
        "states":["RJ", "MG", "SP"],
        "entity_id":"id123"
     }],
	"favorites": ["ght232141-3a12-5t67-19ehdufasuu"],
	"golden_star_balance": 0,
	"star_transactions": [{
		"value": 2, 
		"operation_date": "2019-08-21T13:11:07+00:00", 
		"coin_type": "GOLDEN_STAR", 
		"operation_type": "DEBIT", 
		"source": "DUEL", 
		"source_id": "68dc45c5-43eb-4351-bead-4319aba7af85"
	}],
	"purchases": [{
		"value": "1050", 
		"star_value": "3", 
		"purchase_type": "GOLDEN_STAR_PURCHASE", 
		"purchase_datetime": "2017-11-21T09:58:00+00:00", 
		"payment": {
			"code": "schrubles123", 
			"payment_datetime": "2017-11-22T09:58:00+00:00",
			"payment_type": "PAGSEGURO",
			"transactions": []
		}
		}],
	"user": {
		"city": "Rio de Janeiro",
		"country": "Brasil",
		"cpf": "09022715043",
		"date_birth": "13/09/2019",
		"email": "wapilejig@mail-guru.net",
		"name": "Dada",
		"neighborhood": "Guaratiba",
		"nickname": "leobarnaud",
		"phone_number": "11111111111",
		"postal_code": "23575275",
		"profile_image": "",
		"state": "RJ",
		"street": "Rua pablin",
		"street_complement": "Quadra 3",
		"street_number": "2"
	}
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
#### Request Model:
    {}
    
#### Response Model:
====================
## Status Code : 200
====================
    {
        "status": "success",
        "data": {
            "states_regions": [
                {
                    "name": "Sudeste",
                    "minimum_bet": 123,
                    "states": [
                        "RJ",
                        "MG",
                        "SP"
                    ],
                    "entity_id": "id123"
                }
            ],
            "countries_regions": [
                {
                    "name": "NA",
                    "minimum_bet": 1234,
                    "countries": [
                        "EUA",
                        "Mexico",
                        "Canada"
                    ],
                    "entity_id": "id123"
                }
            ],
            "points": 200,
            "star_transactions": [
                {
                    "operation_date": "2019-08-21T13:11:07+00:00",
                    "source": "DUEL",
                    "coin_type": "GOLDEN_STAR",
                    "operation_type": "DEBIT",
                    "source_id": "68dc45c5-43eb-4351-bead-4319aba7af85",
                    "value": 2
                }
            ],
            "entity_id": "acbf5816-3a14-4bf1-a0d3-19efda0151d0",
            "golden_star_balance": 0,
            "consoles": [
                {
                    "games": [],
                    "entity_id": "1",
                    "name": "Playstation 4",
                    "logo_path": "/images/ss.png",
                    "tag_name": "Leoplay4"
                }
            ],
            "favorites": [
                "ght232141-3a12-5t67-19ehdufasuu"
            ],
            "user": {
                "email": "wapilejig@mail-guru.net",
                "nickname": "leobarnaud",
                "postal_code": "23575275",
                "address": "Rua pablin 2, Quadra 3 - Guaratiba",
                "country": "Brasil",
                "cpf": "09022715043",
                "name": "Dada",
                "city": "Rio de Janeiro",
                "phone_number": "11111111111",
                "state": "RJ",
                "date_birth": "2019-09-13",
                "profile_image": null
            },
            "blue_star_balance": 15,
            "player_status": "OFFLINE",
            "purchases": [
                {
                    "star_value": 3,
                    "purchase_datetime": "2017-11-21T09:58:00+00:00",
                    "payment": {
                        "code": "schrubles123",
                        "payment_type": "PAGSEGURO",
                        "payment_datetime": "2017-11-22T09:58:00+00:00"
                    },
                    "purchase_type": "GOLDEN_STAR_PURCHASE",
                    "value": 1050
                }
            ]
        }
    }

## GET All 
# ROTA : "/player/'
#### Request Model:
    {}

#### Response Model:
===================
## Status Code : 200
===================


    {
        "status": "success",
        "data": [{
            "states_regions": [
                {
                    "name": "Sudeste",
                    "minimum_bet": 123,
                    "states": [
                        "RJ",
                        "MG",
                        "SP"
                    ],
                    "entity_id": "id123"
                }
            ],
            "countries_regions": [
                {
                    "name": "NA",
                    "minimum_bet": 1234,
                    "countries": [
                        "EUA",
                        "Mexico",
                        "Canada"
                    ],
                    "entity_id": "id123"
                }
            ],
            "points": 200,
            "star_transactions": [
                {
                    "operation_date": "2019-08-21T13:11:07+00:00",
                    "source": "DUEL",
                    "coin_type": "GOLDEN_STAR",
                    "operation_type": "DEBIT",
                    "source_id": "68dc45c5-43eb-4351-bead-4319aba7af85",
                    "value": 2
                }
            ],
            "entity_id": "acbf5816-3a14-4bf1-a0d3-19efda0151d0",
            "golden_star_balance": 0,
            "consoles": [
                {
                    "games": [],
                    "entity_id": "1",
                    "name": "Playstation 4",
                    "logo_path": "/images/ss.png",
                    "tag_name": "Leoplay4"
                }
            ],
            "favorites": [
                "ght232141-3a12-5t67-19ehdufasuu"
            ],
            "user": {
                "email": "wapilejig@mail-guru.net",
                "nickname": "leobarnaud",
                "postal_code": "23575275",
                "address": "Rua pablin 2, Quadra 3 - Guaratiba",
                "country": "Brasil",
                "cpf": "09022715043",
                "name": "Dada",
                "city": "Rio de Janeiro",
                "phone_number": "11111111111",
                "state": "RJ",
                "date_birth": "2019-09-13",
                "profile_image": null
            },
            "blue_star_balance": 15,
            "player_status": "OFFLINE",
            "purchases": [
                {
                    "star_value": 3,
                    "purchase_datetime": "2017-11-21T09:58:00+00:00",
                    "payment": {
                        "code": "schrubles123",
                        "payment_type": "PAGSEGURO",
                        "payment_datetime": "2017-11-22T09:58:00+00:00"
                    },
                    "purchase_type": "GOLDEN_STAR_PURCHASE",
                    "value": 1050
                }
            ]
        }]
    }


##Formato de JSON para rota
=======================
# # CONSOLE ROUTE ## 
=======================


## POST 
# ROTA: "/console/"

#### Request Model:

    {
        "name": "Super Selminho",
        "logo_path": "/images/ss.png",
        "tag_name": "nick#1",
        "games" : []
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
# ROTA: "/console/{entity_id}"
#### Request Model:
    {}
    
#### Response Model:
====================
## Status Code : 200
====================

    {
        "status": "success",
        "data": {
            "entity_id ": "id123 ",
            "name": "Super Selminho",
            "logo_path": "/images/ss.png",
            "tag_name": "nick#1",
            "games": []
        }
    }

## GET All 
# ROTA : "/console/'

#### Request Model:
    {}

#### Response Model:
===================
## Status Code : 200
===================
    {
         "status": "success",
         "data":[{
                  
            "entity_id": "id123",
            "name": "Super Selminho",
            "logo_path": "/images/ss.png",
            "tag_name": "nick#1",
            "games" : []
         }]
    }


## PUT
# ROTA : "/console/{entity_id}"

## DADO O SEGUINTE CONSOLE SALVO:

    {              
        "entity_id": "id123",
        "name": "Super Selminho",
        "logo_path": "/images/ss.png",
        "tag_name": "nick#1",
        "games" : []
    }


#### Request Model:
    {
        "entity_id": "id123",
        "name": "XBOX", 
        "logo_path": "/images/xb.png",
        "tag_name": "nick#1",
        "games" : []
    }

#### Response Model:
===================
## Status Code : 200
===================
    {
         "status": "success",
         "data":"id123"
         
    }
    
## DELETE
# ROTA : "/console/{entity_id}" 

#### Request Model:
    { }

#### Response Model:
===================
## Status Code : 200
===================

    {
         "status": "success",
         "data":"id123"  
    }   
    
##Formato de JSON para rota
=======================
# # USER ROUTE ## 
=======================


## POST 
# ROTA: "/user-admin/"

#### Request Model:
    {
     
        "name": "Anselmo Lira",
        "email": "playerstars@playerstars.com.br"
    
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
# ROTA: "/user-admin/{entity_id}"
#### Request Model:
    {}
    
#### Response Model:
====================
## Status Code : 200
====================

    {
        "status": "success",
        "data":{
            
            "name": "Duarte",
            "email": "dudu_jpa@playerstars.com.br",
            "entity_id": "id123"
               
        }
    }

## GET All 
# ROTA : "/user-admin/'

#### Request Model:
    {}

#### Response Model:
===================
## Status Code : 200
===================

    {
         "status": "success",
         "data":[{
            "entity_id": "id123",
            "name": "Duarte",
            "email": "dudu_jpa@playerstars.com.br"
         }]
    }


## PUT
# ROTA : "/user-admin/{entity_id}"

## DADO O SEGUINTE CONSOLE SALVO:

    {
        "name": "Duarte",
        "email": "dudu_jpa@playerstars.com.br",
        "entity_id": "id123"
    }


#### Request Model:
    {
        "entity_id": "id123",
        "name": "name_alterado",
        "email": "email_alterado_put@playerstars.com.br"
    }

#### Response Model:
===================
## Status Code : 200
===================
    {
         "status": "success",
         "data":"id123"   
    }


## DELETE

##Formato de JSON para rota
=======================
# # REGION COUNTRY ROUTE ## 
=======================


## POST 
# ROTA: "/region-country/"

#### Request Model:

    {
            "name": "Gold",
            "minimum_bet" : 1234,
            "countries":[
                "Brasil",
                "Venezuela",
                "Cuba"
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
# ROTA: "/region-country/{entity_id}"
#### Request Model:
    {}
    
#### Response Model:
====================
## Status Code : 200
====================

    {
         "status": "success",
         "data": {
            "name": "Gold",
            "countries": [
                    "Brasil",
                    "Venezuela",
                    "Cuba"
            ],
            "entity_id": "id0001",
            "minimum_bet": 1234
         }
    }


## GET All 
# ROTA : "/region-country/'

#### Request Model:
    {}

#### Response Model:
===================
## Status Code : 200
===================

    {
         "status": "success",
         "data":[{
            "name": "Gold",
            "countries": [
                    "Brasil",
                    "Venezuela",
                    "Cuba"
            ],
            "entity_id": "id0001",
            "minimum_bet": 1234
        }]
    }


## PUT
# ROTA : "/region-country/{entity_id}"

## DADO O SEGUINTE CONSOLE SALVO:

    {
         "name": "Silver",
         "countries": [
                "Equador",
                "Chile",
                "Argentina"
         ],
         "entity_id": "id0001",
         "minimum_bet": 1234
    }


#### Request Model:
    {
        "name": "nome_alterado",
         "countries": [
                "Equador",
                "Chile",
                "Argentina"
         ],
         "entity_id": "id0001",
         "minimum_bet": 1234
    }

#### Response Model:
===================
## Status Code : 200
===================
    {
         "status": "success",
         "data":"id0001"   
    }
    
    
## DELETE    


##Formato de JSON para rota
=======================
# # REGION STATE ROUTE ## 
=======================


## POST 
# ROTA: "/region-state/"

#### Request Model:
    {
        "name": "Gold",
        "minimum_bet" : 1234,
        "states":[
            "RJ",
            "ES",
            "SP"
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
# ROTA: "/region-state/{entity_id}"
#### Request Model:
    {}
    
#### Response Model:
====================
## Status Code : 200
====================

    {
         "status": "success",
         "data": {
            "name": "Gold",
            "states":[
                "RJ",
                "ES",
                "SP"
                ]
            ],
            "entity_id": "id0001",
            "minimum_bet": 1234
         }
    }


## GET All 
# ROTA : "/region-state/'

#### Request Model:
    {}

#### Response Model:
===================
## Status Code : 200
===================
    {
         "status": "success",
         "data":[{
            "name": "Gold",
            "states":[
                "RJ",
                "ES",
                "SP"
                ]
            ],
            "entity_id": "id0001",
            "minimum_bet": 1234
        }]
    }


## PUT
# ROTA : "/region-state/{entity_id}"

## DADO O SEGUINTE CONSOLE SALVO:

    {
         "name": "Silver",
         "states":[
                "RJ",
                "ES",
                "SP"
                ]
         ],
         "entity_id": "id0001",
         "minimum_bet": 1234
    }


#### Request Model:
    {
        "name": "nome_alterado",
         "states":[
                "RJ",
                "ES",
                "SP"
                ]
         ],
         "entity_id": "id0001",
         "minimum_bet": 1234
    }

#### Response Model:
===================
## Status Code : 200
===================
    {
         "status": "success",
         "data":"id0001"   
    }
    
    
## DELETE
