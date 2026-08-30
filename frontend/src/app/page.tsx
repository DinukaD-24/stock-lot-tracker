export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-2xl font-bold">Stock Lot Tracker</h1>
      <p className="text-gray-600 mt-2">
        Go to <a href="/items" className="underline">Items</a> or{" "}
        <a href="/stock" className="underline">Stock</a>.
      </p>
    </main>
  );
}