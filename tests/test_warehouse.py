#Tests for warehouse FIFO logic, validation and all clculations

from datetime import date
from decimal import Decimal

import pytest

from core.exceptions import (DuplicateItemError, InsufficientStockError, InvalidQuantityError, ItemNotFoundError,)

from core.models import Lot, StockItem
from core.warehouse import Warehouse

@pytest.fixture
def warehouse():
    wh = Warehouse()
    wh.add_item(StockItem(code="WIDGET", name="Widget", unit="pcs"))
    return wh

def test_add_item_duplicate_code_raises(warehouse):
    with pytest.raises(DuplicateItemError):
        warehouse.add_item(StockItem(code="WIDGET", name="Widget Again", unit="pcs"))

def test_receive_rejects_negative_quantity(warehouse):
    with pytest.raises(InvalidQuantityError):
        warehouse.receive(Lot(
            lot_number="L1",
            item_code="WIDGET",
            quantity_received=Decimal("-5"),
            unit_cost=Decimal("2.00"),
            received_date=date(2026, 1, 1),
        ))

def test_receive_rejects_negative_cost(warehouse):
    with pytest.raises(InvalidQuantityError):
        warehouse.receive(Lot(
            lot_number="L1",
            item_code="WIDGET",
            quantity_received=Decimal("10"),
            unit_cost=Decimal("-2.00"),
            received_date=date(2026, 1, 1),
        )
        )

def test_receive_unknown_item_raises(warehouse):
    with pytest.raises(ItemNotFoundError):
        warehouse.receive(Lot(
            lot_number="L1",
            item_code="DOES_NOT_EXIST",
            quantity_received=Decimal("10"),
            unit_cost=Decimal("2.00"),
            received_date=date(2026, 1, 1),
        ))