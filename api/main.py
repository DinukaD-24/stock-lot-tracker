from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api import db
from core.exceptions import StockError
from core.warehouse import Warehouse

#Global varable to hold ur single warehouse object in memory while the app runs
_warehouse: Warehouse | None = None

def get_warehouse() -> Warehouse:
    #routes will call this helper function to grab the loaded warehouse instance
    assert _warehouse is not None, "Warehouse not initialised"
    return _warehouse

@asynccontextmanager
async def lifespan(app: FastAPI):
    #everything bfore 'yield' runs when API starts up 
    global _warehouse
    db.init_db() #make sure database tables exist
    _warehouse = db.load_warehouse() #pull saved DB rows into our memeory object

    yield #the app stays runing here...

    #anything placed after 'yield' runs when the server stops
    #we dont need code here because SQLite saves changes instantly on every write

app = FastAPI(title="Stock Lot Tracker API", lifespan=lifespan)

@app.exception_handler(StockError)
def handle_stock_error(request, exc: StockError):
    #catch any custom business logic errors (like ItemNotFounError) and send back a standard 400 reponse
    return JSONResponse(status_code=400, content={"detail": str(exc)})

@app.get("/health")
def health_check():
    #simple check toconfirm the server is running
    return {"status": "ok"}

#Import routes down here so they can safely use get_warehouse without circular import bugs
from api.routes import issue, items, lots, stock #noqa: E402

app.include_router(items.router)
app.include_router(lots.router)
app.include_router(issue.router)
app.include_router(stock.router)
