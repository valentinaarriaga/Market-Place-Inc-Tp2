from fastapi import FastAPI, HTTPException

app = FastAPI(title="Catalog Service")

products = [
    {"id": 1, "name": "Notebook Lenovo", "price": 850000},
    {"id": 2, "name": "Mouse Logitech", "price": 25000},
    {"id": 3, "name": "Teclado Redragon", "price": 70000},
]

@app.get("/health")
def health():
    return {"status": "ok", "service": "catalog"}

@app.get("/products")
def get_products():
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Producto no encontrado")