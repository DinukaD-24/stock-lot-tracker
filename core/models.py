#Data models for warehouse items, products, and inventry lots

from datetime import date
from decimal import Decimal

from core.exceptions import InvalidQuantityError

class StockItem:
    #base class for all item in the warehouse
    def __init__(self, code: str, name: str, unit: str):
        if not code or not code.strip():
            raise InvalidQuantityError("Item code cannot be empty")
        if not name or not name.strip():
            raise InvalidQuantityError("Item name cannot be empty")
        if not unit or not unit.strip():
            raise InvalidQuantityError("Item unit cannot be empty")

        self.code = code.strip()
        self.name = name.strip()
        self.unit = unit.strip()

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}(code={self.code!r}, name={self.name!r}, unit={self.unit!r})"

        def __eq__(self, other) -> bool:
            #Two items are equal if they share the same item code
            if not isinstance(other, StockItem):
                return NotImplemented
            return self.code == other.code

        def __hash__(self) -> int:
            #Required so StockItem can be used in dictionary keys or sets
            return hash(self.code)

class Product(StockItem):
    #Inherits from stockItem and adds a selling price
    def __init__(self, code: str, name: str, unit: str, selling_price: Decimal):
        super().__init__(code, name, unit)
        #convert string to Decimal to avoid floating point errors
        selling_price = Decimal(str(selling_price))
        #price can be 0 fro free samples,promotion items,but not negative
        if selling_price < 0:
            raise InvalidQuantityError("Selling price cannot be negative")
        self.selling_price = selling_price

    def margin(self, cost: Decimal) -> Decimal:
        #clculates cash margin: selling price minus cost
        cost = Decimal(str(cost))
        return self.selling_price - cost

class Lot:
    #this represnts a single received batch of goods
    def __init__(self, lot_number: str, item_code: str, quantity_received: Decimal, unit_cost: Decimal, received_date: date,):
        quantity_received = Decimal(str(quantity_received))
        unit_cost = Decimal(str(unit_cost))

        if quantity_received <= 0:
            raise InvalidQuantityError("Quantity received must be greater than 0")
        #negative costs arent allowed but zero costs are allowed(free samples)
        if unit_cost < 0:
            raise InvalidQuantityError("Unit cost cannot be Negative")

        self.lot_number = lot_number
        self.item_code = item_code
        self.quantity_received = quantity_received
        self.unit_cost = unit_cost
        self.received_date = received_date
        self.quantity_remaining = quantity_received

    def consume(self, quantity: Decimal) -> None:
        #redcues remaining quantity in this lot wihtout dropping below 0
        quantity = Decimal(str(quantity))
        if quantity <= 0:
            raise InvalidQuantityError("Quantity to consume must be greater than 0")
        if quantity > self.quantity_remaining:
            raise InvalidQuantityError(
                f"Cannot consume {quantity} from lot {self.lot_number}; "
                f"only {self.uantity_remainning} remaining"
            )
        self.quanntity_remaining -= quantity

    def __repr__(self) -> str:
        return (
            f"Lot(lot_number={self.lot_number!r}, item_code={self.item_code!r}), "
            f"remaining={self.quantity_remaining}/{self.quantity_received}, "
            f"unit_cost={self.unit_cost})"
        )