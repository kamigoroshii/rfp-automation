import React, { useEffect, useState } from 'react';
import { analyticsAPI } from '../services/api';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { TrendingUp, Clock, Target, DollarSign } from 'lucide-react';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const Analytics = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const response = await analyticsAPI.getDashboardData();
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error loading analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="text-center py-12">
        <p className="text-text-light">Failed to load analytics</p>
      </div>
    );
  }

  const { overview, trends, revenue } = analytics;

  // Chart configurations
  const winRateChartData = {
    labels: trends.win_rate_trend.map(d => d.month),
    datasets: [
      {
        label: 'Win Rate',
        data: trends.win_rate_trend.map(d => (d.rate * 100).toFixed(1)),
        borderColor: '#556B2F',
        backgroundColor: 'rgba(85, 107, 47, 0.1)',
        tension: 0.4,
        fill: true
      }
    ]
  };

  const processingTimeChartData = {
    labels: trends.processing_time_trend.map(d => d.month),
    datasets: [
      {
        label: 'Avg Processing Time (min)',
        data: trends.processing_time_trend.map(d => d.time),
        backgroundColor: '#6B8E23',
        borderColor: '#556B2F',
        borderWidth: 1
      }
    ]
  };

  const matchAccuracyChartData = {
    labels: trends.match_accuracy_trend.map(d => d.month),
    datasets: [
      {
        label: 'Match Accuracy',
        data: trends.match_accuracy_trend.map(d => (d.accuracy * 100).toFixed(1)),
        borderColor: '#9ACD32',
        backgroundColor: 'rgba(154, 205, 50, 0.1)',
        tension: 0.4,
        fill: true
      }
    ]
  };

  const rfpStatusChartData = {
    labels: ['Completed', 'In Progress', 'New'],
    datasets: [
      {
        data: [overview.completed, overview.in_progress, overview.new],
        backgroundColor: ['#228B22', '#DAA520', '#556B2F'],
        borderWidth: 0
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom'
      }
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-text">Analytics Dashboard</h2>
        <p className="text-text-light mt-1">Performance metrics and insights</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          icon={TrendingUp}
          title="Win Rate"
          value={`${(overview.win_rate * 100).toFixed(0)}%`}
          change="+5.2%"
          positive={true}
          color="text-success"
        />
        <MetricCard
          icon={Clock}
          title="Avg Processing Time"
          value={`${overview.avg_processing_time} min`}
          change="-12.3%"
          positive={true}
          color="text-primary"
        />
        <MetricCard
          icon={Target}
          title="Match Accuracy"
          value={`${(overview.avg_match_accuracy * 100).toFixed(0)}%`}
          change="+3.1%"
          positive={true}
          color="text-accent"
        />
        <MetricCard
          icon={DollarSign}
          title="Total RFPs"
          value={overview.total_rfps}
          change="+8 this month"
          positive={true}
          color="text-warning"
        />
      </div>

      {/* Revenue Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <RevenueCard
          title="Total Value"
          value={revenue.total_value}
          color="bg-primary"
        />
        <RevenueCard
          title="Won Value"
          value={revenue.won_value}
          color="bg-success"
        />
        <RevenueCard
          title="Pipeline Value"
          value={revenue.pipeline_value}
          color="bg-warning"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Win Rate Trend */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-text mb-4">Win Rate Trend</h3>
          <div className="h-64">
            <Line data={winRateChartData} options={chartOptions} />
          </div>
        </div>

        {/* RFP Status Distribution */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-text mb-4">RFP Status Distribution</h3>
          <div className="h-64">
            <Doughnut data={rfpStatusChartData} options={doughnutOptions} />
          </div>
        </div>

        {/* Processing Time Trend */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-text mb-4">Processing Time Trend</h3>
          <div className="h-64">
            <Bar data={processingTimeChartData} options={chartOptions} />
          </div>
        </div>

        {/* Match Accuracy Trend */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-text mb-4">Match Accuracy Trend</h3>
          <div className="h-64">
            <Line data={matchAccuracyChartData} options={chartOptions} />
          </div>
        </div>
      </div>

      {/* Performance Summary */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold text-text mb-4">Performance Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="border-l-4 border-success pl-4">
            <p className="text-sm text-text-light">Best Match Rate</p>
            <p className="text-2xl font-bold text-text mt-1">94%</p>
            <p className="text-sm text-success mt-1">Exceeds target</p>
          </div>
          <div className="border-l-4 border-primary pl-4">
            <p className="text-sm text-text-light">Fastest Processing</p>
            <p className="text-2xl font-bold text-text mt-1">12 min</p>
            <p className="text-sm text-primary mt-1">Below average</p>
          </div>
          <div className="border-l-4 border-warning pl-4">
            <p className="text-sm text-text-light">Highest Value RFP</p>
            <p className="text-2xl font-bold text-text mt-1">₹67.5L</p>
            <p className="text-sm text-text-light mt-1">22kV Cable Supply</p>
          </div>
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ icon: Icon, title, value, change, positive, color }) => (
  <div className="bg-white rounded-lg shadow-md p-6">
    <div className="flex items-center justify-between mb-2">
      <p className="text-sm text-text-light">{title}</p>
      <Icon size={20} className={color} />
    </div>
    <p className="text-3xl font-bold text-text">{value}</p>
    <p className={`text-sm mt-2 ${positive ? 'text-success' : 'text-error'}`}>
      {change} from last month
    </p>
  </div>
);

const RevenueCard = ({ title, value, color }) => (
  <div className={`${color} text-white rounded-lg shadow-md p-6`}>
    <p className="text-sm opacity-90">{title}</p>
    <p className="text-2xl font-bold mt-2">
      ₹{(value / 10000000).toFixed(2)} Cr
    </p>
    <p className="text-sm opacity-75 mt-1">
      {(value / 100000).toFixed(0)} Lakhs
    </p>
  </div>
);

export default Analytics;
