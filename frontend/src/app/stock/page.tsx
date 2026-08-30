// frontend/src/app/stock/page.tsx
"use client";

import { useEffect, useState, useMemo } from "react";
import { getStock, ApiError, type StockLine } from "@/lib/api";
import { StockTable } from "@/components/StockTable";

export default function StockPage() {
  const [stock, setStock] = useState<StockLine[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const data = await getStock();
        setStock(data);
      } catch (err) {
        setError(err instanceof ApiError ? err.message : "Failed to load stock");
      }
    }
    load();
  }, []);

  const filtered = useMemo(() => {
    if (!stock) return [];
    const q = query.trim().toLowerCase();
    if (!q) return stock;
    return stock.filter(
      (line) =>
        line.code.toLowerCase().includes(q) ||
        line.name.toLowerCase().includes(q)
    );
  }, [stock, query]);

  return (
    <main className="min-h-screen p-8 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Stock on Hand</h1>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search by code or name..."
        className="border rounded px-2 py-1 w-full max-w-sm"
      />

      {error && (
        <p className="text-red-600 mt-4">Could not load stock: {error}</p>
      )}

      {stock === null && !error && (
        <p className="text-gray-500 mt-4">Loading stock…</p>
      )}

      {stock !== null && (
        <StockTable stock={filtered} isFiltered={query.trim().length > 0} />
       )}
       
    </main>
  );
}