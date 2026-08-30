// frontend/src/lib/api.ts

// Backend server URL — uses environment variable if defined, otherwise defaults to local FastAPI port
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

//Custom error class so frontend components can easily check status codes (like 400 or 500)
export class ApiError extends Error {
    constructor(message: string, public status: number) {
        super(message);
        this.name = "ApiError";
    }
}

//Main helper function to send fetch requests to our API endpoints
async function request<T>(path: string, options?: RequestInit): Promise<T> {
    const res = await fetch(`${API_URL}${path}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options?.headers ?? {}),
        },
        cache: "no-store", // Disables browser caching so stock levels are always live and accurate
    });

    if (!res.ok) {
        let detail = `Request failed with status ${res.status}`;
        try {
        // Try parsing standard JSON error body returned by FastAPI exception handlers
        const body = await res.json();
        if (body?.detail) detail = body.detail;
        } catch {
        // If error response isn't JSON format, stick to default error text
        }
        throw new ApiError(detail, res.status);
    }

    // Convert response to text first so empty responses (like status 204) don't break JSON.parse
    const text = await res.text();
    return text ? (JSON.parse(text) as T) : (undefined as T);
}

//Types matching backend JSON schemas

export type Item = {
  code: string;
  name: string;
  unit: string;
  selling_price?: string | null;
};

export type Lot = {
  lot_number: string;
  item_code: string;
  quantity_received: string;
  unit_cost: string;
  received_date: string;
  quantity_remaining: string;
};

export type StockLine = {
  code: string;
  name: string;
  balance: string;
  stock_value: string;
  average_cost: string | null;
};

export type IssueBreakdownLine = {
  lot_number: string;
  quantity: string;
  unit_cost: string;
};

export type IssueResult = {
  item_code: string;
  quantity_issued: string;
  breakdown: IssueBreakdownLine[];
};


//API functions used by UI pages
// Fetch list of all registered catalog items
export function getItems(): Promise<Item[]> {
  return request<Item[]>("/items");
}

// Register a new item in the warehouse
export function createItem(payload: {
  code: string;
  name: string;
  unit: string;
  selling_price?: string;
}): Promise<Item> {
  return request<Item>("/items", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

// Fetch total stock summary table (balances, values, average costs)
export function getStock(): Promise<StockLine[]> {
  return request<StockLine[]>("/stock");
}

// Fetch individual batches/lots recorded for a specific item code
export function getStockLots(code: string): Promise<Lot[]> {
  return request<Lot[]>(`/stock/${encodeURIComponent(code)}/lots`);
}

// Log a new incoming shipment batch into warehouse memory
export function receiveLot(payload: {
  lot_number: string;
  item_code: string;
  quantity_received: string;
  unit_cost: string;
  received_date: string;
}): Promise<Lot> {
  return request<Lot>("/lots", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

// Deduct/sell stock out of the warehouse using FIFO logic
export function issueStock(payload: {
  item_code: string;
  quantity: string;
}): Promise<IssueResult> {
  return request<IssueResult>("/issue", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}