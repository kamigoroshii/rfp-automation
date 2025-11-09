import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Layout
import Layout from './components/Layout/Layout';

// Pages
import Dashboard from './pages/Dashboard';
import RFPList from './pages/RFPList';
import RFPDetail from './pages/RFPDetail';
import SubmitRFP from './pages/SubmitRFP';
import Analytics from './pages/Analytics';
import Products from './pages/Products';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/rfps" element={<RFPList />} />
          <Route path="/rfp/:id" element={<RFPDetail />} />
          <Route path="/submit" element={<SubmitRFP />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/products" element={<Products />} />
        </Routes>
      </Layout>
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </Router>
  );
}

export default App;
