from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import asyncio

app = FastAPI(title="CI/CD Learning API")

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# Sample data
items = [
    {"id": 1, "name": "Laptop", "description": "High performance laptop"},
    {"id": 2, "name": "Mouse", "description": "Wireless mouse"},
]

@app.get("/")
async def root():
    # Adding a tiny sleep to simulate async work
    await asyncio.sleep(0.01)
    return {"message": "Welcome to the CI/CD Learning API!"}

@app.get("/items", response_model=List[Item])
async def get_items():
    await asyncio.sleep(0.01)
    return items

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    await asyncio.sleep(0.01)
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    await asyncio.sleep(0.01)
    # Check if ID already exists
    if any(i["id"] == item.id for i in items):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    
    items.append(item.dict())
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
