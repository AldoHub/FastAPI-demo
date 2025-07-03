from fastapi import APIRouter, HTTPException
from app.db.models.product import Product
#db connection
from db.client import client
from db.client import products_collection
from bson.objectid import ObjectId
import pprint

router = APIRouter(prefix="/orders", tags=["orders"])

#get all orders
@router.get("/")
async def get_orders():
    return []

#add a new order
@router.post("/")
async def add_product(product: Product):
    product_dict = dict(product)
    #remove the id from the product dict
    product_dict.pop("id")
    new_product =  products_collection.insert_one(product_dict)
    #get the product id
    new_product_id = new_product.inserted_id
    
    #find the created product
    created_product = products_collection.find_one({"_id": ObjectId(new_product_id)})
    created_product_dict = dict(created_product)
    #return the new product - set the object id as a string
    return Product(id=str(created_product_dict["_id"]), name=created_product_dict["name"], price=created_product_dict["price"], description=created_product_dict["description"])

    