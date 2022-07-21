import pymongo
import json
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
##To insert in specified collection in DB:
mydb = myclient["Grocery"]
mycollection = mydb["BigBasket"]
'''mydict = { "Brand": "iD Fresho","Product":"Idly Dosa Batter+non","Quantity":"Combo 2 Items","Price":"Rs 146.88"}
insrt_dta = mycollection.insert_one(mydict)
print(insrt_dta.inserted_id)'''


with open('04_07_2002_data.json') as file:
    file_data = json.load(file)

if isinstance(file_data, list):
    mycollection.insert_many(file_data)  
else:
    mycollection.insert_one(file_data)


  