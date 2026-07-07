import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.database import initialize_db, create_item, get_all_items, get_item_by_name, get_items_count
from utils.helpers import sanitize_input, format_response
from typing import Dict, Any, List, AsyncGenerator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup and shutdown lifecycle management."""
    initialize_db()
    yield

app = FastAPI(title="CCAF Sample FastAPI Practice App", lifespan=lifespan)

class ItemCreate(BaseModel):
    name: str
    description: str | None = None

@app.get("/")
def read_root() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "message": "Welcome to the FastAPI Practice App!"}

@app.post("/items/")
def add_item(item: ItemCreate) -> Dict[str, Any]:
    """Creates a new database item with input sanitization."""
    sanitized_name = sanitize_input(item.name)
    if not sanitized_name:
        raise HTTPException(status_code=400, detail="Item name cannot be empty or only whitespace.")
    
    sanitized_description = sanitize_input(item.description) if item.description is not None else None
    
    new_item = create_item(sanitized_name, sanitized_description)
    return format_response(new_item)

@app.get("/items/")
def read_items() -> Dict[str, Any]:
    """Retrieves all items from the database."""
    items = get_all_items()
    return format_response(items)

@app.get("/divide/")
def divide_numbers(numerator: float, denominator: float) -> Dict[str, Any]:
    """Divides numerator by denominator. (Vulnerable to division by zero)"""
    result = numerator / denominator
    return format_response({"result": result})

@app.get("/items/search/")
def search_items(name: str) -> Dict[str, Any]:
    """Search items by name."""
    items = get_item_by_name(name)
    return format_response(items)

@app.get("/items/count/")
def read_items_count() -> Dict[str, Any]:
    """Retrieves the total number of items in the database."""
    count = get_items_count()
    return format_response({"count": count})

def main() -> None:
    print("Booting up backend server...")
    # Initialize DB synchronously for standalone CLI runs
    initialize_db()
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=False)

if __name__ == "__main__":
    main()