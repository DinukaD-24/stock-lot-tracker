from fastapi import APIRouter, Depends

from api import db
from api.schemas import ItemCreate,ItemOut
from core.models import Product, StockItem
from core.warehouse import Warehouse

#APIRouter groups related URL routes together (all item related endpoints)
router = APIRouter(tags=["items"])

def get_warehouse() -> Warehouse:
    #import inside the function to prevent circular import bugs with api/main.py
    from api.main import get_warehouse as _get
    return _get()

#POST / items registersa new ittem (status code 201 eans "Created")
@router.post("/items", response_model=ItemOut, status_code=201)
def create_item(payload: ItemCreate, wh: Warehouse = Depends(get_warehouse)):
    #if a selling price was provided, treat it as a sellabe Product; otherwise standard StockItem
    if payload.selling_price is not None:
        item = Product(payload.code, payload.name, payload.unit, payload.selling_price)
    else:
        item = StockItem(payload.code, payload.name, payload.unit)

    #1. Try adding iin-memory warehouse (will thorw an error if item code is a duplicate)
    wh.add_item(item)

    #2. Only write to SQLite database after in-memory check succeeds
    db.save_item(item)

    return ItemOut(
        code=item.code,
        name=item.name,
        unit=item.unit,
        selling_price=getattr(item, "selling_price", None),
    )

#GET /items returns a list of all items currently in the warehouse catalog
@router.get("/items", response_model=list[ItemOut])
def list_items(wh: Warehouse = Depends(get_warehouse)):
    #converst every item object in our memory list into an ItemOut JSON schema
    return [
        ItemOut(
            code=i.code,
            name=i.name,
            unit=i.unit,
            selling_price=getattr(i, "selling_price", None),
        )
        for i in wh.list_items()
    ]