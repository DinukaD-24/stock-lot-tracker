from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

from core.exceptions import (DuplicateItemError, InsufficientStockError, InvalidQuantityError, ItemNotFoundError,)

from core.models import Lot, Product, StockItem

TWO_PLACES = Decimal("0.01")

def _money(value: Decimal) -> Decimal:
    #helper func to rounds moentary amounts to two decimal places using standard rounding
    return value.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

class Warehouse:
    #manages all items and stock lots in memory

    def __init__(self):
        self.items: dict[str, StockItem] = {}
        self.lots: dict[str, list[Lot]] = {} # maps item_code -> list of lots

    #Item Management
    def add_item(self, item: StockItem) -> None:
        if item.code in self._items:
            raise DuplicateItemError(f"Item code '{item.code}' already exists")
        self._items[item.code] = item
        self._lots[item.code] =[]

    def get_item(self, code: str) -> StockItem:
        item = self._items.get(code)
        if item is None:
            raise ItemNotFoundError(f"Item cide 'code' not found")
        return item

    def list_items(self) -> list[StockItem]:
        return list(self._items.values())

    #Stock receiving
    def receive(self, lot: Lot) -> None:
        #adds a new lot to an existing item's inventory
        self.get_item(lot.item_code)#raises ItemNotFoundError if item code does not exist
        self._lots[lot.item_code].append(lot)

    #Stock issuing (FIFO)
    def issue(self, code: str, quantity: Decimal) -> list[dict]:
        #issues stock using First In First Out logic
        self.get_item(code)
        quantity = Decimal(str(quantity))
        if quantity <= 0:
            raise InvalidQuantityError("Quantity to issue must be greater than zero")

        #get available lots sorted by date received (oldest first)
        available_lots = sorted(
            (lot for lot in self.lots[code] if lot.quantity_remaining > 0), 
            key=lambda lot: (lot.received_date, lot.lot_number),
        )

        #step1: verify total available stock before making changes
        total_available = sum((lot.quantity_remaining for lot in available_lots), Decimal("0"))
        if quantity > total_available:
            raise InsufficientStockError(f"Cannot issue {quantity} of '{code}'; only {total_available} on hand")

        #step2: deduct stock from oldest lots first
        remaining_to_issue = quantity
        breakdown =[]
        for lot in available_lots:
            if remaining_to_issue <= 0:
                break
            take = min(lot.quantity_remaining, remaining_to_issue)
            lot.consume(take)
            breakdown.append(
                {
                    "lot_number": lot.lot_number,
                    "quantity": take,
                    "unit_cost": lot.unit_cost,
                }
            )
            remaining_to_issue -= take

        return breakdown

    #Inventory Reporting
    def balance(self, code: str) -> Decimal:
        #caculates totola cost value of current stock on hand
        self.get_item(code)
        return sum((lot.quantity_remaining for lot in self._lots[code]), Decimal("0"))

    def stock_value(self, code: str) -> Decimal:
        #Calculates total cost value of current stock on hand
        self.get_item(code)
        total = sum((lot.quantity_remaining * lot.unit_cost for lot in self._lots[code]), Decimal("0"))

    def average_cost(self, code: str) -> Optional[Decimal]:
        #Calculates average cost per unit for current stock 
        self.get_item(code)
        bal = self.balance(code)
        if bal == 0:
            return None #no stock available to calculte average
        return _money(self.stock_value(code) / bal)

    def lots_for(self, code: str) -> list[Lot]:
        #returns all lots for an item sorted by arrival date
        self.get_item(code)
        return sorted(self._lots[code], key=lambda lot: (lot.received_date, lot.lot_number))