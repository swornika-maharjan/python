from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
import certifi
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

# MongoDB Atlas connection — replace with your actual Atlas URI
MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())
db = client["mydb"]
collection = db["items"]

# Request model
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = None

# Helper to serialize MongoDB document 
def item_serializer(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item.get("description"),
        "price": item.get("price"),
    }

# POST - Create item
@app.post("/items/")
async def create_item(item: Item):
    result = await collection.insert_one(item.model_dump())
    new_item = await collection.find_one({"_id": result.inserted_id})
    return item_serializer(new_item)

# GET - Get item by ID
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    item = await collection.find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_serializer(item)

# GET - Get all items
@app.get("/items/")
async def read_all_items():
    items = []
    async for item in collection.find():
        items.append(item_serializer(item)) 
    return items

# DELETE - Delete item by ID
@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = await collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}