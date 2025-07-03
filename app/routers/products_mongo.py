from fastapi import APIRouter, HTTPException
from app.db.models.product import Product, products_schema
#db connection
from db.client import client
from db.client import products_collection
from bson.objectid import ObjectId

router = APIRouter(prefix="/products-mongo", tags=["products_mongo"])

#get all orders
@router.get("/", response_model=list[Product])
async def get_products():
    #parse the response to a list of products using the schema
    return products_schema(products_collection.find())


#add new product - test data
#{
    #"id": "testIdtetettetet",
    #"name": "another python product",
    #"price": "12.54",
    #"description": "a python product description for this produict"
#}

#add a new order
@router.post("/")
async def add_product(product: Product):
    #see if the product name already exists
    find_product = await get_product_by_name(product.name)
    #if product does not exist, create it
    if find_product is None:
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
    else:
        raise HTTPException(status_code=400, detail="Product already exists")
    

#get product by name
async def get_product_by_name(product_name: str):
    product = products_collection.find_one({"name": product_name})
    if product is None:
       return None
    return Product(id=str(product["_id"]), name=product["name"], price=product["price"], description=product["description"])


#get product by id
@router.get("/{product_id}")
async def get_product(product_id: str):
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        return Product(id=str(product["_id"]), name=product["name"], price=product["price"], description=product["description"])


#updated product by id
@router.put("/{product_id}")
async def update_product(product_id: str, product: Product):
    product_response = products_collection.find_one({"_id": ObjectId(product_id)})
    if product_response is None:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        try:
            #update the product
            products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": {"name": product.name, "price": product.price, "description": product.description}})
            #get the updated product
            edited_product = products_collection.find_one({"_id": ObjectId(product_id)})
            #return the updated product
            return Product(id=str(edited_product["_id"]), name=edited_product["name"], price=edited_product["price"], description=edited_product["description"])
        except:
            raise HTTPException(status_code=400, detail="Product not found")


#remove product by id
@router.delete("/{product_id}/remove")
async def remove_product(product_id: str):
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        products_collection.delete_one({"_id": ObjectId(product_id)})
        return {"message": "Product deleted"}
    