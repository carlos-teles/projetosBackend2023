import requests
import pprint
from json2table import convert

def convert_and_write( jsonobj, filename ):
    build_direction = "LEFT_TO_RIGHT"
    table_attributes = {"style": "width:100%"}
    html = convert(jsonobj, build_direction=build_direction, table_attributes=table_attributes)
    file = open("htmlmovie/%s.html" % (filename), "w")
    file.write(html)
    file.close()

#response1 = requests.get("https://www.omdbapi.com/?apikey=XXXXX&t=the%20terminator")
#convert_and_write( response1.json(), "the-terminator" )

response1 = requests.get("https://www.omdbapi.com/?apikey=XXXXX&t=the%20matrix")
convert_and_write( response1.json(), "the-matrix" )

response2 = requests.get("https://www.omdbapi.com/?apikey=XXXXX&t=dune")
convert_and_write( response2.json(), "dune" )
