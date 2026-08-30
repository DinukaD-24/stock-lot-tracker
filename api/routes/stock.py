from fastapi import APIRouter, Depends

from api.schemas import LotOut, StockOut
from core.warehouse import Warehouse

#Router for handling inventory and stock reporting routes
router = APIRouter(tags=["issue"])

def get_warehouse() -> Warehouse:
    #Helper to grab our shared warehouse and import inside the function to prevent circular import bugs with api/main.py
    from api.main import get_warehouse as _get
    return _get()

#GET /stock returrns summary reports (balance, value, average cost)for all registered items
@router.get("/stock", response_model=list[StockOut])
def get_stock(wh: Warehouse = Depends(get_warehouse)):
    result = []

    #loop through every item and calculate current stock levels and monetary value
    for item in wh.list_items():
        result.append(
            StockOut(
                code=item.code,
                name=item.name,
                balance=wh.balance(item.code),
                stock_value=wh.stock_value(item.code),
                average_cost=wh.average_cost(item.code),
            )
        )
    return result

#GET / stock/{code}/lots gets all individual batch records for specific item code
@router.get("/stock/{code}/lots", response_model=list[LotOut])
def get_stock_lots(code: str, wh: Warehouse = Depends(get_warehouse)):
    #lots_for() will raise ItemNotFOundError if the item code does not exist
    # Our global error handler in main.py automatically turns that into a 400 error response
    lots = wh.lots_for(code)

    return [
        LotOut(
            lot_number=lot.lot_number,
            item_code=lot.item_code,
            quantity_received=lot.quantity_received,
            unit_cost=lot.unit_cost,
            received_date=lot.received_date,
            quantity_remaining=lot.quantity_remaining,
        )
        for lot in lots
    ]

