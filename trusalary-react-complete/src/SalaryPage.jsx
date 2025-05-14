import React from "react";

export default function SalaryPage() {
  return (
    <div className="bg-white text-gray-800 font-sans min-h-screen">
      <header className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-blue-700 tracking-tight">TruSalary</h1>
        <nav className="space-x-6 text-sm">
          <a href="/" className="hover:underline">Home</a>
          <a href="/salaries" className="hover:underline">Browse Salaries</a>
          <a href="/contact" className="hover:underline">Contact</a>
        </nav>
      </header>

      <main className="px-4 py-12 max-w-5xl mx-auto">
        <div className="text-center mb-10">
          <h2 className="text-4xl font-bold mb-3 leading-tight text-gray-900">
            Software Engineer Salaries in Austin, TX
          </h2>
          <p className="text-gray-500 text-sm">
            Based on 312 verified job postings from the last 30 days
          </p>
        </div>

        <section className="mb-12 text-center">
          <div className="inline-block bg-blue-50 rounded-lg px-6 py-5 shadow">
            <div className="text-sm text-blue-700 font-semibold">TruSalary (Median)</div>
            <div className="text-3xl font-bold text-blue-900 mt-1">$127,500</div>
          </div>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-12">
          <StatCard label="Salary Range" value="$105,000 – $155,000" />
          <StatCard label="Average Salary" value="$129,200" />
          <StatCard label="Listings Analyzed" value="312" />
        </section>

        <section className="mb-12 bg-gray-50 p-6 rounded shadow">
          <h3 className="font-semibold text-lg mb-3">Why This Data Matters</h3>
          <ul className="list-disc pl-6 text-sm text-gray-700 space-y-2">
            <li>We use real salaries from active employer job listings</li>
            <li>No self-reported or anonymous sources</li>
            <li>Data refreshes weekly to reflect actual market trends</li>
          </ul>
        </section>

        <section className="mb-10">
          <h3 className="text-xl font-semibold mb-4">Recent Software Engineer Listings</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left border">
              <thead className="bg-gray-100 text-xs uppercase text-gray-600">
                <tr>
                  <th className="p-2">Company</th>
                  <th className="p-2">Title</th>
                  <th className="p-2">Salary</th>
                  <th className="p-2">Location</th>
                  <th className="p-2">Posted</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t">
                  <td className="p-2">Google</td>
                  <td className="p-2">Software Engineer</td>
                  <td className="p-2">$135K</td>
                  <td className="p-2">Austin, TX</td>
                  <td className="p-2">3 days ago</td>
                </tr>
                <tr className="border-t">
                  <td className="p-2">Amazon</td>
                  <td className="p-2">Frontend Engineer</td>
                  <td className="p-2">$128K</td>
                  <td className="p-2">Austin, TX</td>
                  <td className="p-2">2 days ago</td>
                </tr>
                <tr className="border-t">
                  <td className="p-2">Dell</td>
                  <td className="p-2">Backend Developer</td>
                  <td className="p-2">$125K</td>
                  <td className="p-2">Austin, TX</td>
                  <td className="p-2">1 day ago</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <div className="text-center text-sm text-gray-600">
          Want to search another role? Head back to the <a href="/" className="text-blue-600 underline">homepage</a>
        </div>
      </main>

      <footer className="mt-20 py-6 text-center text-xs text-gray-500 border-t">
        &copy; {new Date().getFullYear()} TruSalary — Built with real data
      </footer>
    </div>
  );
}

function StatCard({ label, value }) {
  return (
    <div className="bg-white border rounded shadow p-5 text-center">
      <div className="text-gray-500 text-sm">{label}</div>
      <div className="text-xl font-bold text-gray-800">{value}</div>
    </div>
  );
}
