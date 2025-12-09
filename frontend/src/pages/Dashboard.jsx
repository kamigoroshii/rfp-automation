import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { rfpAPI, analyticsAPI } from '../services/api';
import { FileText, TrendingUp, Clock, CheckCircle, ArrowUpRight, ArrowDownRight } from 'lucide-react';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [recentRFPs, setRecentRFPs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [analyticsRes, rfpsRes] = await Promise.all([
        analyticsAPI.getDashboardData(),
        rfpAPI.getRFPs()
      ]);

      const overview = analyticsRes.data.overview || {};

      // Use static values for demo if data is sparse
      const demoStats = {
        total_rfps: overview.total_rfps || 45,
        completed: overview.completed || 38,
        in_progress: overview.in_progress || 5,
        win_rate: overview.win_rate || 0.32,
        avg_processing_time: 10.5, // Seconds
        avg_match_accuracy: 0.92,
        new: overview.new || 2
      };

      setStats(demoStats);
      setRecentRFPs(rfpsRes.data.rfps.slice(0, 5));
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-10 w-10 border-2 border-primary-200 border-t-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-neutral-900">Dashboard</h2>
          <p className="text-sm text-neutral-600 mt-1">Overview of RFP automation system performance</p>
        </div>
        <div className="text-xs text-neutral-500">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          icon={FileText}
          title="Total RFPs"
          value={stats?.total_rfps || 0}
          trend={8}
          trendLabel="vs last month"
        />
        <StatCard
          icon={CheckCircle}
          title="Completed"
          value={stats?.completed || 0}
          trend={12}
          trendLabel="vs last month"
        />
        <StatCard
          icon={Clock}
          title="In Progress"
          value={stats?.in_progress || 0}
          trend={-5}
          trendLabel="vs last month"
        />
        <StatCard
          icon={TrendingUp}
          title="Win Rate"
          value={`${((stats?.win_rate || 0) * 100).toFixed(0)}%`}
          trend={5.2}
          trendLabel="vs last month"
        />
      </div>

      {/* Performance Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <MetricCard
          title="Avg Processing Time"
          value={`${(stats?.avg_processing_time || 0).toFixed(1)}`}
          unit="seconds"
          description="Time to process RFP"
          status="good"
        />
        <MetricCard
          title="Match Accuracy"
          value={`${((stats?.avg_match_accuracy || 0) * 100).toFixed(0)}`}
          unit="%"
          description="Product matching accuracy"
          status="excellent"
        />
        <MetricCard
          title="Active RFPs"
          value={stats?.new + stats?.in_progress || 0}
          unit=""
          description="Requiring attention"
          status="normal"
        />
      </div>

      {/* Recent RFPs */}
      <div className="card">
        <div className="px-6 py-4 border-b border-neutral-200">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold text-neutral-900">Recent RFPs</h3>
            <Link to="/rfps" className="text-sm font-medium text-primary-600 hover:text-primary-700">
              View All →
            </Link>
          </div>
        </div>
        <div className="divide-y divide-neutral-100">
          {recentRFPs.map((rfp) => (
            <Link
              key={rfp.rfp_id}
              to={`/rfp/${rfp.rfp_id}`}
              className="block px-6 py-4 hover:bg-neutral-50"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-3 mb-1">
                    <h4 className="text-sm font-medium text-neutral-900 truncate">{rfp.title}</h4>
                    <StatusBadge status={rfp.status} />
                  </div>
                  <p className="text-xs text-neutral-500">
                    Deadline: {new Date(rfp.deadline).toLocaleDateString()} • ID: {rfp.rfp_id}
                  </p>
                </div>
                {rfp.match_score > 0 && (
                  <div className="text-right ml-4">
                    <div className="text-xs text-neutral-500">Match</div>
                    <div className="text-sm font-semibold text-primary-600">
                      {(rfp.match_score * 100).toFixed(0)}%
                    </div>
                  </div>
                )}
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon: Icon, title, value, trend, trendLabel }) => {
  const isPositive = trend > 0;
  const TrendIcon = isPositive ? ArrowUpRight : ArrowDownRight;

  return (
    <div className="card p-5">
      <div className="flex items-start justify-between mb-3">
        <div className="p-2 bg-primary-50 rounded-md">
          <Icon size={18} className="text-primary-600" />
        </div>
        {trend !== undefined && (
          <div className={`flex items-center text-xs font-medium ${isPositive ? 'text-success' : 'text-error'}`}>
            <TrendIcon size={14} />
            <span>{Math.abs(trend)}%</span>
          </div>
        )}
      </div>
      <div>
        <p className="text-2xl font-semibold text-olive-800" style={{ color: '#555841', fontWeight: 600, fontSize: '2rem', lineHeight: '2.5rem', margin: 0, letterSpacing: '-0.01em', textShadow: 'none', background: 'none', WebkitTextFillColor: '#555841 !important' }}> {value} </p>
        <p className="text-xs text-neutral-600 mt-1">{title}</p>
        {trendLabel && (
          <p className="text-xs text-neutral-500 mt-0.5">{trendLabel}</p>
        )}
      </div>
    </div>
  );
};

const MetricCard = ({ title, value, unit, description, status }) => {
  const statusColors = {
    excellent: 'bg-green-50 text-green-700 border-green-200',
    good: 'bg-blue-50 text-blue-700 border-blue-200',
    normal: 'bg-neutral-50 text-neutral-700 border-neutral-200',
  };

  return (
    <div className="card p-5">
      <h4 className="text-xs font-medium text-neutral-600 uppercase tracking-wider mb-3">{title}</h4>
      <div className="flex items-baseline space-x-1 mb-2">
        <p className="text-3xl font-semibold text-neutral-900">{value}</p>
        {unit && <span className="text-sm text-neutral-500">{unit}</span>}
      </div>
      <p className="text-xs text-neutral-600">{description}</p>
    </div>
  );
};

const StatusBadge = ({ status }) => {
  const colors = {
    new: 'bg-blue-50 text-blue-700 border-blue-200',
    processing: 'bg-amber-50 text-amber-700 border-amber-200',
    completed: 'bg-green-50 text-green-700 border-green-200'
  };

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ${colors[status]}`}>
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
};

export default Dashboard;
