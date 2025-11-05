import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BarChart3, FileText, Globe, Home } from 'lucide-react';

// Pages
import HomePage from './pages/HomePage';
import PredictiveDashboard from './pages/PredictiveDashboard';
import SubmitRequest from './pages/SubmitRequest';
import TrackRequest from './pages/TrackRequest';
import PublicPortal from './pages/PublicPortal';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          {/* Navigation */}
          <nav className="bg-primary-700 text-white shadow-lg">
            <div className="container mx-auto px-4">
              <div className="flex items-center justify-between h-16">
                <Link to="/" className="flex items-center space-x-2">
                  <BarChart3 className="w-8 h-8" />
                  <span className="text-xl font-bold">GovSense AI</span>
                </Link>
                
                <div className="flex space-x-6">
                  <Link 
                    to="/" 
                    className="flex items-center space-x-1 hover:text-primary-200 transition-colors"
                  >
                    <Home className="w-4 h-4" />
                    <span>Home</span>
                  </Link>
                  <Link 
                    to="/dashboard" 
                    className="flex items-center space-x-1 hover:text-primary-200 transition-colors"
                  >
                    <BarChart3 className="w-4 h-4" />
                    <span>Dashboard</span>
                  </Link>
                  <Link 
                    to="/submit" 
                    className="flex items-center space-x-1 hover:text-primary-200 transition-colors"
                  >
                    <FileText className="w-4 h-4" />
                    <span>Submit Request</span>
                  </Link>
                  <Link 
                    to="/public" 
                    className="flex items-center space-x-1 hover:text-primary-200 transition-colors"
                  >
                    <Globe className="w-4 h-4" />
                    <span>Public Portal</span>
                  </Link>
                </div>
              </div>
            </div>
          </nav>

          {/* Main Content */}
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/dashboard" element={<PredictiveDashboard />} />
              <Route path="/submit" element={<SubmitRequest />} />
              <Route path="/track/:trackingId?" element={<TrackRequest />} />
              <Route path="/public" element={<PublicPortal />} />
            </Routes>
          </main>

          {/* Footer */}
          <footer className="bg-gray-800 text-white mt-16">
            <div className="container mx-auto px-4 py-8">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div>
                  <h3 className="text-lg font-bold mb-4">GovSense AI</h3>
                  <p className="text-gray-400">
                    AI-Powered Governance Platform transforming citizen service delivery
                    for Maharashtra.
                  </p>
                </div>
                <div>
                  <h3 className="text-lg font-bold mb-4">Quick Links</h3>
                  <ul className="space-y-2 text-gray-400">
                    <li><Link to="/dashboard" className="hover:text-white">Predictive Dashboard</Link></li>
                    <li><Link to="/submit" className="hover:text-white">Submit Request</Link></li>
                    <li><Link to="/public" className="hover:text-white">Public Portal</Link></li>
                  </ul>
                </div>
                <div>
                  <h3 className="text-lg font-bold mb-4">Technology</h3>
                  <p className="text-gray-400">
                    Built with Google Cloud: Gemini Pro, Vertex AI, BigQuery
                  </p>
                  <p className="text-gray-400 mt-2 text-sm">
                    GenAI Exchange Hackathon 2024
                  </p>
                </div>
              </div>
              <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
                <p>&copy; 2024 GovSense AI - Government of Maharashtra. All rights reserved.</p>
              </div>
            </div>
          </footer>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
