from pydantic import BaseModel

#users entity
class Product(BaseModel):
    id: str | None
    name: str
    price: float
    description: str
    

    