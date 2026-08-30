// frontend/src/components/ItemsTable.tsx
import type { Item } from "@/lib/api";

export function ItemsTable({ items }: { items: Item[] }) {
  if (items.length === 0) {
    return (
      <p className="text-gray-500 mt-4">
        No items yet. Add one using the form above to get started.
      </p>
    );
  }

  return (
    <table className="w-full mt-4 border-collapse">
      <thead>
        <tr className="text-left border-b">
          <th className="py-2 pr-4">Code</th>
          <th className="py-2 pr-4">Name</th>
          <th className="py-2 pr-4">Unit</th>
          <th className="py-2 pr-4">Selling Price</th>
        </tr>
      </thead>
      <tbody>
        {items.map((item) => (
          <tr key={item.code} className="border-b">
            <td className="py-2 pr-4">{item.code}</td>
            <td className="py-2 pr-4">{item.name}</td>
            <td className="py-2 pr-4">{item.unit}</td>
            <td className="py-2 pr-4">
              {item.selling_price ?? "—"}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}