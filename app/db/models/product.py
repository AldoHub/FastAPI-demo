from pydantic import BaseModel

#users entity
class Product(BaseModel):
    id: str | None
    name: str
    price: float
    description: str
    

def products_schema(products) -> list[Product]:
    #return an array of products
    return [Product(id=str(product["_id"]), name=product["name"], price=product["price"], description=product["description"]) for product in products]