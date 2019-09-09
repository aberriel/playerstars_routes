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
	"user": {
		"name": "Anselmo Lira",
		"email": "playerstars@playerstars.com.br",
		"birth_date": "16/12/1986",
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
	"consoles": [{
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

            "entity_id": "id0001",
            "favorites": [],
            "blue_star_balance": 123,
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
#### Request Model:
    {}

#### Response Model:
===================
## Status Code : 200
===================
    {
        "status": "success",
        "data": [{
    
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
            "consoles": [{
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
