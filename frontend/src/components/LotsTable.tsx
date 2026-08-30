// frontend/src/components/LotsTable.tsx
import type { Lot } from "@/lib/api";

export function LotsTable({ lots }: { lots: Lot[] }) {
  if (lots.length === 0) {
    return (
      <p className="text-gray-500 mt-4">
        No lots received yet for this item.
      </p>
    );
  }

  return (
    <table className="w-full mt-4 border-collapse">
      <thead>
        <tr className="text-left border-b">
          <th className="py-2 pr-4">Lot #</th>
          <th className="py-2 pr-4">Received</th>
          <th className="py-2 pr-4">Qty Received</th>
          <th className="py-2 pr-4">Unit Cost</th>
          <th className="py-2 pr-4">Remaining</th>
        </tr>
      </thead>
      <tbody>
        {lots.map((lot) => (
          <tr key={lot.lot_number} className="border-b">
            <td className="py-2 pr-4">{lot.lot_number}</td>
            <td className="py-2 pr-4">{lot.received_date}</td>
            <td className="py-2 pr-4">{lot.quantity_received}</td>
            <td className="py-2 pr-4">{lot.unit_cost}</td>
            <td className="py-2 pr-4">{lot.quantity_remaining}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}