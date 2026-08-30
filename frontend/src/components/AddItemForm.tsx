// frontend/src/components/AddItemForm.tsx
"use client";

import { useState } from "react";
import { createItem, ApiError } from "@/lib/api";

export function AddItemForm({ onCreated }: { onCreated: () => void }) {
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [unit, setUnit] = useState("");
  const [sellingPrice, setSellingPrice] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await createItem({
        code,
        name,
        unit,
        selling_price: sellingPrice || undefined,
      });
      setCode("");
      setName("");
      setUnit("");
      setSellingPrice("");
      onCreated(); // tell the parent page to refresh the list
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to create item");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-wrap gap-2 items-end">
      <div>
        <label className="block text-sm text-gray-600">Code</label>
        <input
          value={code}
          onChange={(e) => setCode(e.target.value)}
          required
          className="border rounded px-2 py-1"
        />
      </div>
      <div>
        <label className="block text-sm text-gray-600">Name</label>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="border rounded px-2 py-1"
        />
      </div>
      <div>
        <label className="block text-sm text-gray-600">Unit</label>
        <input
          value={unit}
          onChange={(e) => setUnit(e.target.value)}
          required
          placeholder="pcs, kg..."
          className="border rounded px-2 py-1"
        />
      </div>
      <div>
        <label className="block text-sm text-gray-600">Selling Price (optional)</label>
        <input
          value={sellingPrice}
          onChange={(e) => setSellingPrice(e.target.value)}
          placeholder="e.g. 9.99"
          className="border rounded px-2 py-1"
        />
      </div>
      <button
        type="submit"
        disabled={submitting}
        className="bg-black text-white rounded px-4 py-1 disabled:opacity-50"
      >
        {submitting ? "Adding..." : "Add Item"}
      </button>
      {error && <p className="text-red-600 text-sm w-full">{error}</p>}
    </form>
  );
}