from pymongo import MongoClient

#https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/

#connection string
connection_string = "mongodb+srv://aldocaava:1Ov90iqQy6HEnRwm@products.wo7erpi.mongodb.net/"
client = MongoClient(connection_string)
db = client.get_database("test")
products_collection = db.get_collection("products")