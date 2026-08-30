// frontend/src/app/items/page.tsx
"use client";

import { useEffect, useState, useCallback } from "react";
import { getItems, ApiError, type Item } from "@/lib/api";
import { ItemsTable } from "@/components/ItemsTable";
import { AddItemForm } from "@/components/AddItemForm";

export default function ItemsPage() {
  const [items, setItems] = useState<Item[] | null>(null); // null = loading
  const [error, setError] = useState<string | null>(null);

  const loadItems = useCallback(async () => {
    setError(null);
    try {
      const data = await getItems();
      setItems(data);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to load items");
    }
  }, []);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  return (
    <main className="min-h-screen p-8 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Items</h1>

      <AddItemForm onCreated={loadItems} />

      {error && (
        <p className="text-red-600 mt-4">
          Could not load items: {error}
        </p>
      )}

      {items === null && !error && (
        <p className="text-gray-500 mt-4">Loading items…</p>
      )}

      {items !== null && <ItemsTable items={items} />}
    </main>
  );
}