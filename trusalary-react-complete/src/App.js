import React from 'react';
import HomePage from './HomePage';
import SalaryPage from './SalaryPage';

function App() {
  const showSeoPage = window.location.pathname.includes('/salaries/');
  return showSeoPage ? <SalaryPage /> : <HomePage />;
}

export default App;
