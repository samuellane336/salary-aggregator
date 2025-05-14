import React from "react";

export default function HomePage() {
  return (
    <div className="p-4 md:p-8 max-w-5xl mx-auto">
      {/* Header */}
      <header className="flex justify-between items-center mb-6">
        <div className="text-xl font-bold">TruSalary</div>
        <nav className="space-x-4">
          <a href="/" className="hover:underline">Home</a>
          <a href="/about" className="hover:underline">About</a>
          <a href="/contact" className="hover:underline">Contact</a>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="text-center py-12">
        <h1 className="text-3xl md:text-5xl font-bold mb-4">
          Find Real Salaries for Real Jobs — Instantly
        </h1>
        <p className="text-lg mb-6">
          Based on millions of real job postings. No surveys. No login required. Always fresh.
        </p>
        <div className="flex flex-col md:flex-row justify-center gap-4">
          <input
            type="text"
            placeholder="Job Title"
            className="border px-4 py-2 rounded-md w-full md:w-1/3"
          />
          <input
            type="text"
            placeholder="Location"
            className="border px-4 py-2 rounded-md w-full md:w-1/3"
          />
          <button className="bg-blue-600 text-white px-6 py-2 rounded-md">
            Search
          </button>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="grid md:grid-cols-3 gap-6 py-12">
        <div>
          <h3 className="font-bold text-lg mb-2">Real-Time Salary Data</h3>
          <p>Only from actual job postings. Updated daily.</p>
        </div>
        <div>
          <h3 className="font-bold text-lg mb-2">No Logins, No Paywalls</h3>
          <p>Get the information you need instantly.</p>
        </div>
        <div>
          <h3 className="font-bold text-lg mb-2">Salary Trends You Can Trust</h3>
          <p>Track how pay is changing over time.</p>
        </div>
      </section>

      {/* Popular Searches */}
      <section className="py-12">
        <h2 className="text-2xl font-bold mb-4">Popular Salary Searches</h2>
        <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
          <li><a href="/salaries/software-engineer-new-york" className="text-blue-600 hover:underline">Software Engineer Salaries in New York</a></li>
          <li><a href="/salaries/marketing-manager-los-angeles" className="text-blue-600 hover:underline">Marketing Manager Salaries in Los Angeles</a></li>
          <li><a href="/salaries/project-manager-chicago" className="text-blue-600 hover:underline">Project Manager Salaries in Chicago</a></li>
          <li><a href="/salaries/data-analyst-san-francisco" className="text-blue-600 hover:underline">Data Analyst Salaries in San Francisco</a></li>
        </ul>
        <div className="mt-4">
          <a href="/salaries" className="text-blue-600 hover:underline">View All Job Salaries →</a>
        </div>
      </section>

      {/* Explanation Section */}
      <section className="py-12">
        <h2 className="text-2xl font-bold mb-4">Why We're Different</h2>
        <ul className="list-disc pl-6 space-y-2">
          <li>We use real salaries pulled directly from employers’ postings — not anonymous employee submissions.</li>
          <li>Every listing is verified from public sources like company career pages, job boards, and employer sites.</li>
          <li>No signups, no hidden fees, no "survey your salary" popups.</li>
        </ul>
        <div className="mt-4">
          <a href="/how-we-collect" className="text-blue-600 hover:underline">Learn How We Collect Data →</a>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-100 text-center py-12 rounded-md mt-12">
        <h2 className="text-2xl font-bold mb-4">Start Searching Now — 100% Free, No Account Needed</h2>
        <div className="flex flex-col md:flex-row justify-center gap-4">
          <input
            type="text"
            placeholder="Job Title"
            className="border px-4 py-2 rounded-md w-full md:w-1/3"
          />
          <input
            type="text"
            placeholder="Location"
            className="border px-4 py-2 rounded-md w-full md:w-1/3"
          />
          <button className="bg-blue-600 text-white px-6 py-2 rounded-md">
            Search
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="text-center text-sm text-gray-500 py-8 mt-12">
        <p>
          <a href="/about" className="hover:underline">About</a> | 
          <a href="/privacy" className="hover:underline">Privacy Policy</a> | 
          <a href="/terms" className="hover:underline">Terms of Service</a> | 
          <a href="/contact" className="hover:underline">Contact Us</a>
        </p>
      </footer>
    </div>
  );
}
