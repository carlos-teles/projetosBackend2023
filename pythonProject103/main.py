"""from fastapi import FastAPI, Path"""
import fastapi
import connection

#print(connection.mydb)
#print("connection.mydb")
app = fastapi.FastAPI()


@app.get("/")
def hello_world_root():
    return {"Turma": "Backend"}

"""
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
"""

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
    mycursor.close()
    officeCode = str(officeCode)

    sql_insert = """ INSERT INTO offices (officeCode,city,phone,addressLine1,addressLine2,state,country,postalCode,territory)  VALUES   ('%s', '%s','%s','%s','%s','%s','%s','%s','%s') ; """ % ( officeCode,  city, phone, addressLine1, addressLine2, state, country, postalCode,  territory )
    #print(sql_insert)
    mycursor2 = connection.mydb.cursor()
    mycursor2.execute(sql_insert)
    mycursor2.execute("COMMIT;")
    mycursor2.close()
    return {'Offices': "Inserido - "+str(officeCode) }

@app.delete('/office/{officeCode}')
def delete_office( officeCode: str ):
    mycursor = connection.mydb.cursor(dictionary=True)
    sql_get = "SELECT officeCode from classicmodels.offices where officeCode = "+officeCode+""
    mycursor.execute(sql_get)
    officeCode = ''
    for offices in mycursor:
        officeCode = offices['officeCode']
    mycursor.close()
    if officeCode == '':
        return {'Message': 'Office Nao existe'}
    else:
        mycursor_del = connection.mydb.cursor(dictionary=True)
        sql_del = "DELETE from classicmodels.offices where officeCode = "+officeCode+""
        mycursor_del.execute(sql_del)
        mycursor_del.execute("COMMIT;")
        mycursor_del.close()
        return {'Message': 'Office deleted successfully - '+str(officeCode)}

@app.put('/office/{officeCode}/{city}/{phone}/{addressLine1}/{addressLine2}/{state}/{country}/{postalCode}/{territory}')
def update_office( officeCode: str, city: str, phone: str, addressLine1: str, addressLine2: str, state: str, country: str, postalCode: str,  territory: str ):
    mycursor = connection.mydb.cursor(dictionary=True)
    sql_get = "SELECT officeCode from classicmodels.offices where officeCode = "+officeCode+""
    mycursor.execute(sql_get)
    officeCode = ''
    for offices in mycursor:
        officeCode = offices['officeCode']
    mycursor.close()
    if officeCode == '':
        return {'Message': 'Office Nao existe'}
    else:
        sql_update = """ UPDATE offices SET  city = '%s', phone = '%s' , addressLine1  = '%s',addressLine2  = '%s',state  = '%s' ,country  = '%s' , postalCode = '%s',
        territory = '%s' where officeCode = %s ; """ % (
        city, phone, addressLine1, addressLine2, state, country, postalCode, territory, officeCode)
        print(sql_update)
        mycursor2 = connection.mydb.cursor()
        mycursor2.execute(sql_update)
        mycursor2.execute("COMMIT;")
        mycursor2.close()
        return {'Offices': "Atualizado - " + str(officeCode)}