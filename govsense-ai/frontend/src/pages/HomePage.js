import React from 'react';
import { Link } from 'react-router-dom';
import { BarChart3, Zap, Globe, ArrowRight } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center py-12">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          GovSense AI
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          AI-Powered Governance Platform transforming citizen service delivery
          for Maharashtra's 125 million citizens
        </p>
        <div className="flex justify-center space-x-4">
          <Link to="/dashboard" className="btn-primary flex items-center space-x-2">
            <span>View Dashboard</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link to="/submit" className="btn-secondary flex items-center space-x-2">
            <span>Submit Request</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <Link to="/dashboard" className="card hover:shadow-lg transition-shadow">
          <div className="flex items-center justify-center w-12 h-12 bg-primary-100 rounded-lg mb-4">
            <BarChart3 className="w-6 h-6 text-primary-600" />
          </div>
          <h3 className="text-xl font-bold mb-2">Predictive Dashboard</h3>
          <p className="text-gray-600 mb-4">
            Forecast service demand 30-90 days ahead using Vertex AI and get
            AI-generated actionable insights.
          </p>
          <div className="text-primary-600 font-medium flex items-center">
            Explore Feature 1 <ArrowRight className="w-4 h-4 ml-2" />
          </div>
        </Link>

        <Link to="/submit" className="card hover:shadow-lg transition-shadow">
          <div className="flex items-center justify-center w-12 h-12 bg-success-100 rounded-lg mb-4">
            <Zap className="w-6 h-6 text-success-600" />
          </div>
          <h3 className="text-xl font-bold mb-2">Smart Prioritization</h3>
          <p className="text-gray-600 mb-4">
            AI categorization with Gemini Pro, multi-factor scoring, and
            intelligent routing in real-time.
          </p>
          <div className="text-success-600 font-medium flex items-center">
            Explore Feature 2 <ArrowRight className="w-4 h-4 ml-2" />
          </div>
        </Link>

        <Link to="/public" className="card hover:shadow-lg transition-shadow">
          <div className="flex items-center justify-center w-12 h-12 bg-warning-100 rounded-lg mb-4">
            <Globe className="w-6 h-6 text-warning-600" />
          </div>
          <h3 className="text-xl font-bold mb-2">Public Transparency</h3>
          <p className="text-gray-600 mb-4">
            Real-time performance metrics, impact stories, and open data API
            for complete transparency.
          </p>
          <div className="text-warning-600 font-medium flex items-center">
            Explore Feature 3 <ArrowRight className="w-4 h-4 ml-2" />
          </div>
        </Link>
      </div>

      {/* Stats */}
      <div className="bg-primary-700 text-white rounded-lg p-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-4xl font-bold mb-2">60%</div>
            <div className="text-primary-200">Faster Response</div>
          </div>
          <div>
            <div className="text-4xl font-bold mb-2">85%</div>
            <div className="text-primary-200">Completion Rate</div>
          </div>
          <div>
            <div className="text-4xl font-bold mb-2">48h</div>
            <div className="text-primary-200">Avg Resolution</div>
          </div>
          <div>
            <div className="text-4xl font-bold mb-2">4.2/5</div>
            <div className="text-primary-200">Satisfaction</div>
          </div>
        </div>
      </div>

      {/* Tech Stack */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-6 text-center">Built with Google Cloud</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div>
            <div className="font-bold text-lg mb-2">Gemini Pro</div>
            <div className="text-sm text-gray-600">NLP & Insights</div>
          </div>
          <div>
            <div className="font-bold text-lg mb-2">Vertex AI</div>
            <div className="text-sm text-gray-600">ML Models</div>
          </div>
          <div>
            <div className="font-bold text-lg mb-2">BigQuery</div>
            <div className="text-sm text-gray-600">Data Warehouse</div>
          </div>
          <div>
            <div className="font-bold text-lg mb-2">Cloud IAM/VPC</div>
            <div className="text-sm text-gray-600">Security</div>
          </div>
        </div>
      </div>
    </div>
  );
}
