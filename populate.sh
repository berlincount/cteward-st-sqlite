curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/prices/1
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/prices/2
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/prices/3
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/prices/4
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/prices/5
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/prices/6
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/prices/7
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/prices/8
curl -X POST -H 'Content-type: application/json' http://hoschi:14339/api/prices -d '{"id": 1, "displayName":"Clubmate 0,5 - Member", "amount": 1, "amount_unit":"Flaschen", "price":1.30, "price_unit":"EUR"}'
curl -X POST -H 'Content-type: application/json' http://hoschi:14339/api/prices -d '{"id": 2, "displayName":"Clubmate 0,5 - Alien",  "amount": 1, "amount_unit":"Flaschen", "price":2.00, "price_unit":"EUR"}'
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/tariffs/1
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/tariffs/2
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/tariffs/3
curl -X POST -H 'Content-type: application/json' http://hoschi:14339/api/tariffs -d '{"id": 1, "displayName":"Standard"}'
curl -X POST -H 'Content-type: application/json' http://hoschi:14339/api/tariffs -d '{"id": 2, "displayName":"Member Only"}'
curl -X POST -H 'Content-type: application/json' http://hoschi:14339/api/tariffs -d '{"id": 3, "displayName":"Party"}'
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/items/1
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/items/2
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/items/3
curl -X DELETE -H 'Content-type: application/json' http://hoschi:14339/api/items/4
curl -X POST -H 'Content-type: application/json' http://hoschi:14339/api/items -d '{"id": 1, "displayName": "Clubmate   ", "tariff_id": 1, "price_id":  1, "meta": "{\"x\":0,\"y\":0,\"col\":1}"}'
curl -X POST -H 'Content-type: application/json' http://hoschi:14339/api/items -d '{"id": 2, "displayName": "Clubmate   ", "tariff_id": 1, "price_id":  2, "meta": "{\"x\":1,\"y\":0,\"col\":2}"}'
curl -X POST -H 'Content-type: application/json' http://hoschi:14339/api/items -d '{"id": 3, "displayName": "12345678901", "tariff_id": 1, "price_id":  1, "meta": "{\"x\":0,\"y\":0,\"col\":0}"}'
curl -X POST -H 'Content-type: application/json' http://hoschi:14339/api/items -d '{"id": 4, "displayName": "12345678901", "tariff_id": 1, "price_id":  1, "meta": "{\"x\":0,\"y\":0,\"col\":0}"}'
