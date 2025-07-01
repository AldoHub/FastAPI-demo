from fastapi import APIRouter

#add the prefix to the router and set the response for 404 in cae the product is not found
router = APIRouter(prefix="/products", tags=["products"], responses={404: {"description": "Product not found"}})

products = ["product1", "product2", "product3"]

#get products
@router.get("/")
async def get_products():
    return products;

#get product by id
@router.get("/{product_id}")
async def get_product(product_id: int):
    return products[product_id]