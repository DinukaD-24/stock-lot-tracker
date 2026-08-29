# Pydantic schemas set up the shape of JSON data coming into and going out of our API.
# Keeping these separate from core/models.py means we can change API responses 
# without breaking our core warehouse code.

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


# ---------- items ----------

# Schema for when a user sends JSON to create a new item
class ItemCreate(BaseModel):
    code: str  # Product code like "KBD" or "MOUSE"
    name: str  # Full item name
    unit: str  # Unit of measurement like "pcs" or "box"
    # Optional means this field can be a Decimal or left blank (None)
    selling_price: Optional[Decimal] = Field(
        default=None, description="If set, item is treated as a sellable Product"
    )


# Schema for returning item details back to the user in an API response
class ItemOut(BaseModel):
    code: str
    name: str
    unit: str
    selling_price: Optional[Decimal] = None


# ---------- lots ----------

# Schema for receiving a new stock shipment batch
class LotReceive(BaseModel):
    lot_number: str  # Batch tracking ID like "LOT-001"
    item_code: str
    # gt=0 means "greater than 0" — prevents receiving 0 or negative quantities
    quantity_received: Decimal = Field(gt=0)
    # ge=0 means "greater than or equal to 0" — allows free stock (cost=0) but not negative
    unit_cost: Decimal = Field(ge=0)
    received_date: date


# Schema for returning batch details, including current remaining stock
class LotOut(BaseModel):
    lot_number: str
    item_code: str
    quantity_received: Decimal
    unit_cost: Decimal
    received_date: date
    quantity_remaining: Decimal  # Keeps track of how much stock is left in this batch


# ---------- issuing ----------

# Schema for requesting stock to be removed/sold from the warehouse
class IssueRequest(BaseModel):
    item_code: str
    quantity: Decimal = Field(gt=0)  # Must request at least 1 or more units


# Helper schema showing how much was taken from a specific batch (used in IssueResponse)
class IssueBreakdownLine(BaseModel):
    lot_number: str
    quantity: Decimal
    unit_cost: Decimal


# Schema sent back after issuing stock to show total taken and which batches were used (FIFO)
class IssueResponse(BaseModel):
    item_code: str
    quantity_issued: Decimal
    breakdown: list[IssueBreakdownLine]  # Nested list showing batch-by-batch deductions


# ---------- stock reporting ----------

# Schema for returning total warehouse inventory summaries
class StockOut(BaseModel):
    code: str
    name: str
    balance: Decimal  # Total stock units left across all batches
    stock_value: Decimal  # Total money value of remaining stock
    average_cost: Optional[Decimal] = None  # Average cost per unit (None if stock balance is 0)