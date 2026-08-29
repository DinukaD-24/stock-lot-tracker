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

def test_issue_fifo_spans_two_lots(warehouse):
    warehouse.receive(
        Lot("L1", "WIDGET", Decimal("10"), Decimal("2.00"), date(2026, 1, 1))
    )
    warehouse.receive(
        Lot("L2", "WIDGET", Decimal("10"), Decimal("3.00"), date(2026, 1, 5))
    )

    breakdown = warehouse.issue("WIDGET", Decimal("15"))

    assert len(breakdown) == 2
    assert breakdown[0]["lot_number"] == "L1"
    assert breakdown[0]["quantity"] == Decimal("10")
    assert breakdown[0]["unit_cost"] == Decimal("2.00")
    assert breakdown[1]["lot_number"] == "L2"
    assert breakdown[1]["quantity"] == Decimal("5")
    assert breakdown[1]["unit_cost"] == Decimal("3.00")
    assert warehouse.balance("WIDGET") == Decimal("5")

def test_issue_partial_consumption_of_last_lot(warehouse):
    warehouse.receive(
        Lot("L1", "WIDGET", Decimal("5"), Decimal("2.00"), date(2026, 1, 1))
    )
    warehouse.receive(
        Lot("L2", "WIDGET", Decimal("20"), Decimal("3.00"), date(2026, 1, 5))
    )

    breakdown = warehouse.issue("WIDGET", Decimal("8"))

    assert breakdown[0]["quantity"] == Decimal("5")
    assert breakdown[1]["quantity"] == Decimal("3")

    lots = warehouse.lots_for("WIDGET")
    l1 = next(l for l in lots if l.lot_number == "L1")
    l2 = next(l for l in lots if l.lot_number == "L2")
    assert l1.quantity_remaining == Decimal("0")
    assert l2.quantity_remaining == Decimal("17")

def test_issue_exact_full_balance_empties_all_lots(warehouse):
    warehouse.receive(
        Lot("L1", "WIDGET", Decimal("4"), Decimal("1.00"), date(2026, 1, 1))
    )
    warehouse.receive(
        Lot("L2", "WIDGET", Decimal("6"), Decimal("1.50"), date(2026, 1, 2))
    )

    warehouse.issue("WIDGET", Decimal("10"))

    assert warehouse.balance("WIDGET") == Decimal("0")

def test_issue_insufficient_stock_raises_and_state_unchanged(warehouse):
    warehouse.receive(
        Lot("L1", "WIDGET", Decimal("5"), Decimal("2.00"), date(2026, 1, 1))
    )

    with pytest.raises(InsufficientStockError):
        warehouse.issue("WIDGET", Decimal("100"))

    assert warehouse.balance("WIDGET") == Decimal("5")
    lots = warehouse.lots_for("WIDGET")
    assert lots[0].quantity_remaining == Decimal("5")

def test_stock_value_across_lots_different_costs(warehouse):
    warehouse.receive(
        Lot("L1", "WIDGET", Decimal("10"), Decimal("2.00"), date(2026, 1, 1))
    )
    warehouse.receive(
        Lot("L2", "WIDGET", Decimal("5"), Decimal("4.00"), date(2026, 1, 2))
    )

    assert warehouse.stock_value("WIDGET") == Decimal("40.00")