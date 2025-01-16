from fastapi import FastAPI, HTTPException
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

app = FastAPI()

# Cosmos DB Configuration
COSMOS_ENDPOINT = "https://localhost:8081"
COSMOS_KEY = COSMOS_KEY
DATABASE_NAME = "AdvancedDB"
CONTAINER_NAME = "Items"

# Initialize Cosmos DB Client
client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
database = client.create_database_if_not_exists(id=DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path="/category"),
    offer_throughput=400
)

# Data Models
class ItemBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    price: float
    quantity: int

class Item(ItemBase):
    id: str
    created_at: datetime
    updated_at: datetime

@app.post("/items/", response_model=Item)
async def create_item(item: ItemBase):
    new_item = {
        "id": str(uuid.uuid4()),
        "name": item.name,
        "category": item.category,
        "description": item.description,
        "price": item.price,
        "quantity": item.quantity,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    try:
        container.create_item(new_item)
        return new_item
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/items/{item_id}")
async def read_item(item_id: str, category: str):
    try:
        item = container.read_item(item_id, partition_key=category)
        return item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items/category/{category}")
async def list_items_by_category(category: str):
    query = "SELECT * FROM c WHERE c.category = @category"
    parameters = [{"name": "@category", "value": category}]
    items = list(container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    return items

@app.put("/items/{item_id}")
async def update_item(item_id: str, item: ItemBase):
    try:
        existing_item = container.read_item(item_id, partition_key=item.category)
        existing_item.update({
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "quantity": item.quantity,
            "updated_at": datetime.utcnow().isoformat()
        })
        updated_item = container.replace_item(item_id, existing_item)
        return updated_item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: str, category: str):
    try:
        container.delete_item(item_id, partition_key=category)
        return {"message": "Item deleted successfully"}
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
