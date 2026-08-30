# Stock Lot Tracker 

Start the application with:

docker compose up --build

Then open http://localhost:3000

Run tests:

    docker compose exec api pytest

Or, if running locally:

    pytest

Make sure the virtual environment is active.

## What's finished
- Part A – Core OOP: Implemented `StockItem`, `Product`, `Lot`, and `Warehouse`, including FIFO stock issuing, custom exceptions, and no use of global state or `print()` for application logic.
- Part B – Testing: Added 11 pytest tests covering FIFO issuing, insufficient stock, input validation, stock valuation, and average cost.
- Part C – API: Added a FastAPI layer for items, lots, issuing stock, and stock information. Data is stored in SQLite, with CORS and proper 4xx error handling.
- Part D – Frontend: Built the Next.js frontend with `/items`, `/stock`, and `/stock/[code]` pages. It also includes loading, empty, and error states, along with forms for receiving and issuing stock.
- Part E – Docker: Added Docker Compose setup with a named volume for persistent data. The application can be started with a single command and was also tested from a fresh clone.

## What's not finished / known gaps
- The CORS origin is currently set to `http://localhost:3000` in the API. If `FRONTEND_PORT` is changed, the CORS configuration would also need to be updated.
- The `/stock` page doesn't currently have pagination or sorting. This is acceptable for a small dataset, but would become useful as the amount of stock grows.
- CSV export and a stock-movement audit log were not implemented. These were optional bonus features and were left out due to the available time.
- The search on `/stock` is done on the frontend, so it only searches through the items that have already been loaded.
- There is currently no CI pipeline to automatically run the tests when changes are pushed.

## Assumptions
- `Decimal` is used for money and quantities instead of `float` to avoid rounding problems. Values are rounded to 2 decimal places using `ROUND_HALF_UP` when reporting things such as stock value and average cost. Stored and intermediate values are not rounded.
- `Product.margin()` returns the difference between the selling price and cost as an amount of money, rather than a percentage.
- `average_cost()` returns `None` when there is no stock, since an average cost cannot be calculated with a zero balance.
- `issue()` is designed to be atomic. It first checks whether enough stock is available before changing any lots. If there isn't enough stock, an `InsufficientStockError` is raised and the warehouse remains unchanged.

## If I Had More Time

If I had another week to work on the project, I would:

- Add a repository layer and proper transaction handling instead of manually calling `save_x()` after each API operation.
- Move the CORS origin into an environment variable so it works correctly when the frontend port is changed.
- Add pagination and sorting to the stock page.
- Add CSV export for the current stock.
- Add a stock-movement history so receiving and issuing stock can be tracked over time.
- Set up GitHub Actions to run the test suite automatically on every push.
- Add more tests for Decimal edge cases and concurrent stock-issue scenarios.

## AI Tools Used

I used Claude to help with some of the supporting parts of the project, mainly:

- Docker Compose and Dockerfile setup
- Basic FastAPI setup, including CORS and error handling
- Basic Next.js components

The core OOP implementation, especially the `Warehouse`, `Lot`, and FIFO `issue()` logic, as well as the test suite, was written by me. I understand how these parts work and can explain the code and design decisions behind them.

## Video
https://drive.google.com/drive/folders/1FiLJr9vqRKLTN36GZJG5IEj7ixBF_7Dl?usp=sharing