import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { rfpAPI } from '../services/api';
import { Search, Filter, Calendar, AlertCircle } from 'lucide-react';
import { format, differenceInHours } from 'date-fns';

const RFPList = () => {
  const [rfps, setRfps] = useState([]);
  const [filteredRfps, setFilteredRfps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    loadRFPs();
  }, []);

  useEffect(() => {
    filterRFPs();
  }, [searchTerm, statusFilter, rfps]);

  const loadRFPs = async () => {
    try {
      const response = await rfpAPI.getRFPs();
      setRfps(response.data.rfps);
      setFilteredRfps(response.data.rfps);
    } catch (error) {
      console.error('Error loading RFPs:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterRFPs = () => {
    let filtered = rfps;

    if (searchTerm) {
      filtered = filtered.filter(rfp =>
        rfp.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        rfp.rfp_id.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (statusFilter !== 'all') {
      filtered = filtered.filter(rfp => rfp.status === statusFilter);
    }

    setFilteredRfps(filtered);
  };

  const isDeadlineSoon = (deadline) => {
    const hours = differenceInHours(new Date(deadline), new Date());
    return hours > 0 && hours <= 48;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-text">RFP List</h2>
        <p className="text-text-light mt-1">Manage and track all RFP submissions</p>
      </div>

      {/* Search and Filter */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-text-light" size={20} />
            <input
              type="text"
              placeholder="Search RFPs by title or ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <div className="flex items-center gap-2">
            <Filter size={20} className="text-text-light" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="all">All Status</option>
              <option value="new">New</option>
              <option value="processing">Processing</option>
              <option value="completed">Completed</option>
            </select>
          </div>
        </div>
      </div>

      {/* RFP Cards */}
      <div className="grid grid-cols-1 gap-4">
        {filteredRfps.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <p className="text-text-light">No RFPs found</p>
          </div>
        ) : (
          filteredRfps.map((rfp) => (
            <Link
              key={rfp.rfp_id}
              to={`/rfp/${rfp.rfp_id}`}
              className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6"
            >
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="text-xl font-bold text-text mb-1">{rfp.title}</h3>
                      <p className="text-sm text-text-light">{rfp.rfp_id}</p>
                    </div>
                    {isDeadlineSoon(rfp.deadline) && (
                      <span className="flex items-center gap-1 px-3 py-1 bg-error/20 text-error rounded-full text-sm font-medium">
                        <AlertCircle size={16} />
                        Urgent
                      </span>
                    )}
                  </div>
                  <p className="text-text-light mt-2 line-clamp-2">{rfp.scope}</p>
                  <div className="flex flex-wrap gap-2 mt-3">
                    {rfp.testing_requirements && rfp.testing_requirements.length > 0 &&
                      rfp.testing_requirements.slice(0, 3).map((req, idx) => (
                        <span key={idx} className="px-2 py-1 bg-gray-100 text-text text-xs rounded">
                          {req}
                        </span>
                      ))
                    }
                  </div>
                </div>
                <div className="lg:text-right space-y-2 lg:min-w-[200px]">
                  <StatusBadge status={rfp.status} />
                  <div className="flex items-center gap-2 text-text-light text-sm lg:justify-end">
                    <Calendar size={16} />
                    <span>Due: {format(new Date(rfp.deadline), 'MMM dd, yyyy')}</span>
                  </div>
                  {rfp.match_score > 0 && (
                    <div className="text-sm">
                      <span className="text-text-light">Match: </span>
                      <span className="font-semibold text-success">
                        {(rfp.match_score * 100).toFixed(0)}%
                      </span>
                    </div>
                  )}
                  {rfp.total_estimate > 0 && (
                    <div className="text-sm">
                      <span className="text-text-light">Estimate: </span>
                      <span className="font-semibold text-primary">
                        ₹{(rfp.total_estimate / 100000).toFixed(2)}L
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </Link>
          ))
        )}
      </div>
    </div>
  );
};

const StatusBadge = ({ status }) => {
  const colors = {
    new: 'bg-blue-100 text-blue-800',
    processing: 'bg-warning/20 text-warning',
    completed: 'bg-success/20 text-success'
  };

  return (
    <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${colors[status]}`}>
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
};

export default RFPList;
