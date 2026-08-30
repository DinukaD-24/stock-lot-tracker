// frontend/src/components/NavBar.tsx
import Link from "next/link";

export function NavBar() {
  return (
    <nav className="border-b px-8 py-4 flex gap-6 items-center">
      <Link href="/" className="font-bold">
        Stock Lot Tracker
      </Link>
      <Link href="/items" className="text-gray-600 hover:text-black">
        Items
      </Link>
      <Link href="/stock" className="text-gray-600 hover:text-black">
        Stock
      </Link>
    </nav>
  );
}