// frontend/src/components/StockTable.tsx
import Link from "next/link";
import type { StockLine } from "@/lib/api";

export function StockTable({
  stock,
  isFiltered = false,
}: {
  stock: StockLine[];
  isFiltered?: boolean;
}) {
  if (stock.length === 0) {
    return (
      <p className="text-gray-500 mt-4">
        {isFiltered
          ? "No items match your search."
          : "No stock on hand. Add items and receive lots to see them here."}
      </p>
    );
  }

  return (
    <table className="w-full mt-4 border-collapse">
      <thead>
        <tr className="text-left border-b">
          <th className="py-2 pr-4">Code</th>
          <th className="py-2 pr-4">Name</th>
          <th className="py-2 pr-4">Balance</th>
          <th className="py-2 pr-4">Stock Value</th>
          <th className="py-2 pr-4">Avg. Cost</th>
        </tr>
      </thead>
      <tbody>
        {stock.map((line) => (
          <tr key={line.code} className="border-b">
            <td className="py-2 pr-4">
              <Link href={`/stock/${line.code}`} className="underline">
                {line.code}
              </Link>
            </td>
            <td className="py-2 pr-4">{line.name}</td>
            <td className="py-2 pr-4">{line.balance}</td>
            <td className="py-2 pr-4">{line.stock_value}</td>
            <td className="py-2 pr-4">{line.average_cost ?? "—"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}