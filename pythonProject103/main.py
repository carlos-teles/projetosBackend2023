"""from fastapi import FastAPI, Path"""
import fastapi
import connection

#print(connection.mydb)
#print("connection.mydb")
app = fastapi.FastAPI()
menu = [  {   'id': 1,        'name': 'coffee',        'price': 2.5     },
        {        'id': 2,        'name': 'cake',        'price': 10    },
        {        'id': 3,        'name': 'tea',        'price': 3.2    },
        {        'id': 4,        'name': 'croissant',        'price': 5.79    }
]

@app.get("/")
def hello_world_root():
    return {"Turma": "Backend"}

@app.get('/get-item/{item_id}')
def get_item(
    item_id: int = fastapi.Path(...,
        description="Fill with ID of the item you want to view")):
    search = list(filter(lambda x: x["id"] == item_id, menu))
    if search == []:
        return {'Error': 'Item does not exist'}
    return {'Item': search[0]}

@app.get('/get-by-name/{item_name}')
def get_by_name( item_name: str = fastapi.Path(...,  description="Preencha com o nome") ):
    search = list(filter(lambda x: x["name"] == item_name, menu))
    if search == []:
        return {'item': 'Does not exist'}
    return {'Item': search[0]}


@app.get('/get-by-price/{item_price}')
def get_by_price( item_price: float = fastapi.Path(...,  description="Preencha com o preco") ):
    search = list(filter(lambda x: x["price"] == item_price, menu))
    if search == []:
        return {'item': 'Does not exist'}
    return {'Item': search[0]}

@app.post('/create-item/{item_id}/{item_name}/{item_price}')
def create_item(item_id: int, item_name: str, item_price: float ):
    search = list(filter(lambda x: x["id"] == item_id, menu))
    if search != []:
        return {'Error': 'Item exists'}
    item = {}
    item['id'] = item_id
    item['name'] = item_name
    item['price'] = item_price
    menu.append(item)
    return item

@app.put('/update-item/{item_id}/{item_name}/{item_price}')
def update_item(item_id: int, item_name: str, item_price: float ):
    search = list(filter(lambda x: x["id"] == item_id, menu))
    if search == []:
        return {'Item': 'Does not exist'}
    else:
        item = search
    if item_name is not None:
        search[0]['name'] = item_name
    if item_price is not None:
        search[0]['price'] = item_price
    return item

@app.delete('/delete-item/{item-id}')
def delete_item(item_id: int):
    search = list(filter(lambda x: x["id"] == item_id, menu))
    if search == []:
        return {'Item': 'Does not exist'}
    for i in range(len(menu)):
        if menu[i]['id'] == item_id:
            del menu[i]
            break
    return {'Message': 'Item deleted successfully'}

@app.get('/list-menu')
def list_menu():
    return {'Menu': menu }

@app.get('/list-offices')
def list_offices():
    offices_list = []
    mycursor = connection.mydb.cursor(dictionary=True)
    mycursor.execute("select * from classicmodels.offices")
    for offices in mycursor:
        offices_list.append(offices)
    mycursor.close()
    return {'Offices': offices_list }

@app.get('/get-office/{office_id}')
def get_office(
    office_id: int = fastapi.Path(...,
        description="Fill with ID of the item you want to view")):
    offices_list = []
    mycursor = connection.mydb.cursor(dictionary=True)
    sql_get_office_id = "select * from classicmodels.offices where officeCode = " + str(int(office_id)) + ""
    mycursor.execute(sql_get_office_id)
    for offices in mycursor:
        offices_list.append(offices)
    mycursor.close()
    return {'Offices': offices_list }

@app.get('/get-office-by-city-name/{city_name}')
def get_office_by_city_name(
    city_name: str = fastapi.Path(...,
        description="Fill with ID of the item you want to view")):
    if len(city_name) <= 3:
        return {'Office name': 'Preencher mais de tres caracteres'}
    offices_list = []
    mycursor = connection.mydb.cursor(dictionary=True)
    sql_get_office_id = "select * from classicmodels.offices where city like '" + city_name + "%'"
    mycursor.execute(sql_get_office_id)
    for offices in mycursor:
        offices_list.append(offices)
    mycursor.close()
    return {'Offices': offices_list }

@app.post('/office/{city}/{phone}/{addressLine1}/{addressLine2}/{state}/{country}/{postalCode}/{territory}')
def create_office( city: str, phone: str, addressLine1: str, addressLine2: str, state: str, country: str, postalCode: str,  territory: str ):

    if len(city) <= 3:
        return {'Office name': 'Preencher o nome da cidade com mais de tres caracteres'}
    mycursor = connection.mydb.cursor(dictionary=True)
    sql_get = "SELECT max(CAST((substring(officeCode,1)) AS DECIMAL(5,2))) as maxofficeCode from classicmodels.offices "
    mycursor.execute(sql_get)
    officeCode = 0
    for offices in mycursor:
        officeCode = int(offices['maxofficeCode']) + 1
    #print(officeCode)
    mycursor.close()
    officeCode = str(officeCode)

    sql_insert = """ INSERT INTO offices (officeCode,city,phone,addressLine1,addressLine2,state,country,postalCode,territory)  VALUES   ('%s', '%s','%s','%s','%s','%s','%s','%s','%s') ; """ % ( officeCode,  city, phone, addressLine1, addressLine2, state, country, postalCode,  territory )
    #print(sql_insert)
    mycursor2 = connection.mydb.cursor()
    mycursor2.execute(sql_insert)
    mycursor2.execute("COMMIT;")
    mycursor2.close()
    return {'Offices': "Inserido - "+str(officeCode) }