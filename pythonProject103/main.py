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
    mycursor = connection.mydb.cursor()
    mycursor.execute("select * from classicmodels.offices")
    for offices in mycursor:
        offices_list.append(offices)
    return {'Offices': offices_list }