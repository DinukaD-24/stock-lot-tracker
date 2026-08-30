// frontend/src/components/IssueStockForm.tsx
"use client";

import { useState } from "react";
import { issueStock, ApiError, type IssueResult } from "@/lib/api";

export function IssueStockForm({
  itemCode,
  onIssued,
}: {
  itemCode: string;
  onIssued: () => void;
}) {
  const [quantity, setQuantity] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastResult, setLastResult] = useState<IssueResult | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLastResult(null);
    setSubmitting(true);
    try {
      const result = await issueStock({ item_code: itemCode, quantity });
      setLastResult(result);
      setQuantity("");
      onIssued();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to issue stock");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="border rounded p-4 mt-4">
      <h3 className="font-semibold mb-2">Issue Stock (FIFO)</h3>
      <div className="flex gap-2 items-end">
        <div>
          <label className="block text-sm text-gray-600">Quantity</label>
          <input
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            required
            className="border rounded px-2 py-1 w-24"
          />
        </div>
        <button
          type="submit"
          disabled={submitting}
          className="bg-black text-white rounded px-4 py-1 disabled:opacity-50"
        >
          {submitting ? "Issuing..." : "Issue"}
        </button>
      </div>
      {error && <p className="text-red-600 text-sm mt-2">{error}</p>}
      {lastResult && (
        <div className="text-sm text-green-700 mt-2">
          Issued {lastResult.quantity_issued} from{" "}
          {lastResult.breakdown.length} lot(s):{" "}
          {lastResult.breakdown
            .map((b) => `${b.quantity} @ ${b.unit_cost} (${b.lot_number})`)
            .join(", ")}
        </div>
      )}
    </form>
  );
}