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
        #print(sql_update)
        mycursor2 = connection.mydb.cursor()
        mycursor2.execute(sql_update)
        mycursor2.execute("COMMIT;")
        mycursor2.close()
        return {'Offices': "Atualizado - " + str(officeCode)}