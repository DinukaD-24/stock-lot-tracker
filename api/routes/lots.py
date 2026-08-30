from fastapi import APIRouter, Depends

from api import db
from api.schemas import LotOut, LotReceive
from core.models import Lot
from core.warehouse import Warehouse

#APIRouter groups all stock shipment(lot) endpoints together
router = APIRouter(tags=["lots"])

def get_warehouse() -> Warehouse:
    #import inside the function to prevent circular import bugs with api/main.py
    from api.main import get_warehouse as _get
    return _get()

#POST /lots registers a new incoming stock shipment batch (statuscode 201 means "Created")
@router.post("/lots", response_model=LotOut, status_code=201)
def receive_lot(payload: LotReceive, wh: Warehouse = Depends(get_warehouse)):
    #create a dmoain Lot object from the incoming API request data
    lot = Lot(
        lot_number=payload.lot_number,
        item_code=payload.item_code,
        quantity_received=payload.quantity_received,
        unit_cost=payload.unit_cost,
        received_date=payload.received_date,
    )

    #1.add shipment to in-memory warehouse (will error if product code doesn't exist)
    wh.receive(lot)

    #2.save batch to SQLite database only after memory check succeeds
    db.save_lot(lot)

    #Return full lot details back to the client, including quantity_remaining
    return LotOut(
        lot_number=lot.lot_number,
        item_code=lot.item_code,
        quantity_received=lot.quantity_received,
        unit_cost=lot.unit_cost,
        received_date=lot.received_date,
        quantity_remaining=lot.quantity_remaining,
    )