// frontend/src/app/stock/[code]/page.tsx
"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import { getStockLots, ApiError, type Lot } from "@/lib/api";
import { LotsTable } from "@/components/LotsTable";
import { ReceiveLotForm } from "@/components/ReceiveLotForm";
import { IssueStockForm } from "@/components/IssueStockForm";

export default function StockDetailPage() {
  const params = useParams<{ code: string }>();
  const code = params.code;

  const [lots, setLots] = useState<Lot[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadLots = useCallback(async () => {
    setError(null);
    try {
      const data = await getStockLots(code);
      setLots(data);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to load lots");
    }
  }, [code]);

  useEffect(() => {
    loadLots();
  }, [loadLots]);

  return (
    <main className="min-h-screen p-8 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Lots for {code}</h1>

      {error && <p className="text-red-600 mb-4">{error}</p>}

      {lots === null && !error && (
        <p className="text-gray-500 mb-4">Loading lots…</p>
      )}

      {lots !== null && <LotsTable lots={lots} />}

      <div className="mt-6 space-y-4">
        <ReceiveLotForm itemCode={code} onReceived={loadLots} />
        <IssueStockForm itemCode={code} onIssued={loadLots} />
      </div>
    </main>
  );
}