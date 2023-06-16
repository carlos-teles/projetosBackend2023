import requests
import pprint
from json2table import convert

def convert_and_write( jsonobj, filename ):
    build_direction = "LEFT_TO_RIGHT"
    table_attributes = {"style": "width:100%"}
    html = convert(jsonobj, build_direction=build_direction, table_attributes=table_attributes)
    file = open("html/%s.html" % (filename), "w")
    file.write(html)
    file.close()

response1 = requests.get("http://127.0.0.1:8000/list-productlines")
#pprint.pprint(response1.json())
convert_and_write( response1.json(), "productlines" )

response2 = requests.get("http://127.0.0.1:8000/get-productlines/Motorcycles")
#pprint.pprint(response2.json())
convert_and_write( response2.json(), "Motorcycles" )

response3 = requests.get("http://127.0.0.1:8000/get-productlines/Classic Cars")
convert_and_write( response3.json(), "Classic_Cars" )

response4 = requests.get("http://127.0.0.1:8000/get-productlines/Planes")
convert_and_write( response4.json(), "Planes" )

response5 = requests.get("http://127.0.0.1:8000/get-productlines-textdescription/guarantee")
convert_and_write( response5.json(), "text_desc01" )


