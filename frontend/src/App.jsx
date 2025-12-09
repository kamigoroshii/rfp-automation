import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { AuthProvider, useAuth } from './context/AuthContext';

// Layout
import Layout from './components/Layout/Layout';

// Pages
import Dashboard from './pages/Dashboard';
import RFPList from './pages/RFPList';
import RFPDetail from './pages/RFPDetail';
import SubmitRFP from './pages/SubmitRFP';
import Analytics from './pages/Analytics';
import Products from './pages/Products';
import AuditorDashboard from './pages/AuditorDashboard';
import EmailInbox from './pages/EmailInbox';
import IngestRFPs from './pages/IngestRFPs';
import Login from './pages/Login';
import LandingPage from './pages/LandingPage';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

const PublicRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  if (user) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

const AdminRoute = ({ children }) => {
  const { user } = useAuth();

  if (user?.role !== 'admin') {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<PublicRoute><LandingPage /></PublicRoute>} />
          <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
          <Route path="/*" element={
            <ProtectedRoute>
              <Layout>
                <Routes>
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/ingest" element={<IngestRFPs />} />
                  <Route path="/rfps" element={<RFPList />} />
                  <Route path="/rfp/:id" element={<RFPDetail />} />
                  <Route path="/submit" element={<SubmitRFP />} />
                  <Route path="/analytics" element={<Analytics />} />
                  <Route path="/products" element={<Products />} />
                  <Route path="/auditor" element={
                    <AdminRoute>
                      <AuditorDashboard />
                    </AdminRoute>
                  } />
                  <Route path="/emails" element={<EmailInbox />} />
                </Routes>
              </Layout>
            </ProtectedRoute>
          } />
        </Routes>
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
    </AuthProvider>
  );
}

export default App;
