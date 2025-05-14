import React from "react";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white text-gray-800">
      <header className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-blue-700">TruSalary</h1>
        <nav className="space-x-6 text-sm">
          <a href="/" className="hover:underline">Home</a>
          <a href="/about" className="hover:underline">About</a>
          <a href="/contact" className="hover:underline">Contact</a>
        </nav>
      </header>

      <main className="text-center px-4 py-20">
        <h2 className="text-4xl font-bold mb-4 leading-tight">
          Find Real Salaries for Real Jobs — Instantly
        </h2>
        <p className="text-lg text-gray-600 mb-8 max-w-xl mx-auto">
          TruSalary uses verified salary data pulled directly from real job postings — no surveys, no self-submissions, no guesswork.
        </p>

        <div className="flex flex-col md:flex-row gap-4 justify-center max-w-2xl mx-auto mb-10">
          <input type="text" placeholder="Job Title" className="w-full md:w-1/3 px-4 py-3 border rounded" />
          <input type="text" placeholder="Location" className="w-full md:w-1/3 px-4 py-3 border rounded" />
          <button className="bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700">
            Search
          </button>
        </div>

        <p className="text-sm text-gray-500">
          No accounts. No popups. Just real-time salary insights from jobs posted this week.
        </p>
      </main>

      <section className="bg-gray-50 py-16">
        <h3 className="text-2xl font-semibold mb-6 text-center">Why TruSalary is Different</h3>
        <div className="max-w-4xl mx-auto grid md:grid-cols-3 gap-6 text-center text-sm px-6">
          <div className="bg-white p-6 rounded shadow">
            <h4 className="font-bold text-lg mb-2">📌 Real Job Postings</h4>
            <p>We only use job listings published by actual employers — no anonymous reports.</p>
          </div>
          <div className="bg-white p-6 rounded shadow">
            <h4 className="font-bold text-lg mb-2">📅 Always Fresh</h4>
            <p>Data is updated constantly to reflect what employers are paying right now.</p>
          </div>
          <div className="bg-white p-6 rounded shadow">
            <h4 className="font-bold text-lg mb-2">🔒 100% Free & Transparent</h4>
            <p>No logins. No surveys. No “contribute your salary” traps. Just answers.</p>
          </div>
        </div>
      </section>

      <footer className="mt-20 py-6 text-center text-xs text-gray-500 border-t">
        &copy; {new Date().getFullYear()} TruSalary. All rights reserved.
      </footer>
    </div>
  );
}
