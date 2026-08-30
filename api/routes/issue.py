from fastapi import APIRouter, Depends

from api import db
from api.schemas import IssueBreakdownLine, IssueRequest, IssueResponse
from core.warehouse import Warehouse

#Router for handling stock issuing routes
router = APIRouter(tags=["issue"])

def get_warehouse() -> Warehouse:
    #Helper to grab our shared warehouse and import inside the function to prevent circular import bugs with api/main.py
    from api.main import get_warehouse as _get
    return _get()

#POST /issue handles removing/selling stock using FIFO logic
@router.post("/issue", response_model=IssueResponse)
def issue_stock(payload: IssueRequest, wh: Warehouse = Depends(get_warehouse)):
    #1.deduct stock in memory (raises error automaticaly if not enough stock or item missing)
    breakdown = wh.issue(payload.item_code, payload.quantity)

    #2.update SQLite DB remaining stock for each batch that was used
    for line in breakdown:
        db.update_lot_remaining(line["lot_number"], line["quantity_remaining_after"])

        #return summary showing totla issued and lot by lot breakdown
        return IssueResponse(
            item_code=payload.item_code,
            quantity_issued=payload.quantity,
            breakdown=[
                IssueBreakdownLine(
                    lot_number=line["lot_number"],
                    quantity=line["quantity"],
                    unit_cost=line["unit_cost"],
                )
                for line in breakdown
            ],
        )