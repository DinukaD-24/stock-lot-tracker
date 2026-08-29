"""Custom exceptions for the stock lot tracker core package to handle warehouse business rules"""

#Base exception class for all stock tracker business errors
class StockError(Exception):
    pass

#Raise this exception when quantity or cost is negative or 0
class InvalidQuantityError(StockError):
    pass

#Raise this exceptin when trying to add a code of an item that already exists
class DuplicateItemError(StockError):
    pass

#Raise this exception when searching for an  item code that doesn't exist
class ItemNotFoundError(StockError):
    pass

#Raise this exception when requesting more stock than available on hand
class InsufficientStockError(StockError):
    pass
