import fastapi
import connection

app = fastapi.FastAPI()


@app.get("/")
def hello_world_root():
    return {"TBL": "productlines"}

@app.get('/list-productlines')
def list_productlines():
    productlines_list = []
    mycursor = connection.mydb.cursor(dictionary=True)
    sql_get_all = "select * from classicmodels.productlines"
    mycursor.execute(sql_get_all)
    for productlines in mycursor:
        productlines_list.append(productlines)
    mycursor.close()
    return {'ProductLines': productlines_list }

@app.get('/get-productlines/{productline}')
def get_productlines(
    productline: str = fastapi.Path(...,
        description="Fill with productline name")):
    productlines_list = []
    mycursor = connection.mydb.cursor(dictionary=True)
    sql_get_productline = "select * from classicmodels.productlines where productline = '%s'" % (productline)
    mycursor.execute(sql_get_productline)
    for productlines in mycursor:
        productlines_list.append(productlines)
    mycursor.close()
    return {'ProductLines': productlines_list }

@app.get('/get-productlines-textdescription/{textdescription}')
def get_productlines_textdescription( textdescription: str):
    if len(textdescription) <= 5:
        return {'textdescription': 'Fill with textdescription with more then 5 characters'}
    productlines_list = []
    mycursor = connection.mydb.cursor(dictionary=True)
    sql_get_productline = "select * from classicmodels.productlines where textdescription like '%%%s%%'" % (textdescription)
    mycursor.execute(sql_get_productline)
    for productlines in mycursor:
        productlines_list.append(productlines)
    mycursor.close()
    return {'ProductLines': productlines_list }

@app.post('/productlines/{productline}/{textdescription}/{htmldescription}/{image}')
def create_productline( productline: str, textdescription: str, htmldescription: str, image: str):
    if len(productline) <= 3:
        return {'Productline name': '03 characteres or more'}
    mycursor = connection.mydb.cursor(dictionary=True)
    sql_get = "SELECT productline from classicmodels.productlines where productline = '" + productline + "'"
    mycursor.execute(sql_get)
    productlines_str = ''
    for productlines_cursor in mycursor:
        productlines_str = productlines_cursor['productline']
    mycursor.close()
    productlines_str = str(productlines_str)

    sql_insert = """ INSERT INTO classicmodels.productlines (productline,textdescription,htmldescription,image)  VALUES   ('%s', '%s','%s','%s') ; """ % ( productline,textdescription,htmldescription,image )
    #print(sql_insert)
    mycursor2 = connection.mydb.cursor()
    mycursor2.execute(sql_insert)
    mycursor2.execute("COMMIT;")
    mycursor2.close()
    return {'Productline': "Inserted - "+str(productline) }

@app.delete('/productlines/{productline}')
def delete_productline( productline: str ):
    mycursor = connection.mydb.cursor(dictionary=True)
    sql_get = "SELECT productline from classicmodels.productlines where productline = '"+productline+"'"
    mycursor.execute(sql_get)
    productlines_str = ''
    for productlines_cursor in mycursor:
        productlines_str = productlines_cursor['productline']
    mycursor.close()
    if productlines_str == '':
        return {'Message': 'productline Doesn´t exist'}
    else:
        mycursor_del = connection.mydb.cursor(dictionary=True)
        sql_del = "DELETE from classicmodels.productlines where productline = '"+productline+"'"
        mycursor_del.execute(sql_del)
        mycursor_del.execute("COMMIT;")
        mycursor_del.close()
        return {'Message': 'Productline deleted successfully - '+str(productlines_str)}

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
        #print(sql_update)
        mycursor2 = connection.mydb.cursor()
        mycursor2.execute(sql_update)
        mycursor2.execute("COMMIT;")
        mycursor2.close()
        return {'Offices': "Atualizado - " + str(officeCode)}