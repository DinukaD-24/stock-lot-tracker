// frontend/src/components/ReceiveLotForm.tsx
"use client";

import { useState } from "react";
import { receiveLot, ApiError } from "@/lib/api";

export function ReceiveLotForm({
  itemCode,
  onReceived,
}: {
  itemCode: string;
  onReceived: () => void;
}) {
  const [lotNumber, setLotNumber] = useState("");
  const [quantity, setQuantity] = useState("");
  const [unitCost, setUnitCost] = useState("");
  const [receivedDate, setReceivedDate] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await receiveLot({
        lot_number: lotNumber,
        item_code: itemCode,
        quantity_received: quantity,
        unit_cost: unitCost,
        received_date: receivedDate,
      });
      setLotNumber("");
      setQuantity("");
      setUnitCost("");
      setReceivedDate("");
      onReceived();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to receive lot");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="border rounded p-4">
      <h3 className="font-semibold mb-2">Receive Stock</h3>
      <div className="flex flex-wrap gap-2 items-end">
        <div>
          <label className="block text-sm text-gray-600">Lot Number</label>
          <input
            value={lotNumber}
            onChange={(e) => setLotNumber(e.target.value)}
            required
            className="border rounded px-2 py-1"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-600">Quantity</label>
          <input
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            required
            className="border rounded px-2 py-1 w-24"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-600">Unit Cost</label>
          <input
            value={unitCost}
            onChange={(e) => setUnitCost(e.target.value)}
            required
            className="border rounded px-2 py-1 w-24"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-600">Received Date</label>
          <input
            type="date"
            value={receivedDate}
            onChange={(e) => setReceivedDate(e.target.value)}
            required
            className="border rounded px-2 py-1"
          />
        </div>
        <button
          type="submit"
          disabled={submitting}
          className="bg-black text-white rounded px-4 py-1 disabled:opacity-50"
        >
          {submitting ? "Receiving..." : "Receive"}
        </button>
      </div>
      {error && <p className="text-red-600 text-sm mt-2">{error}</p>}
    </form>
  );
}