import React, { useEffect, useState } from 'react';
import { Mail, FileText, Download, Calendar, User, Paperclip, Eye, CheckCircle, Clock } from 'lucide-react';
import { Link } from 'react-router-dom';
import { emailAPI } from '../services/api';

const EmailInbox = () => {
    const [emails, setEmails] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all'); // all, processed, pending
    const [stats, setStats] = useState({
        total: 0,
        processed: 0,
        pending: 0,
        attachments: 0
    });

    useEffect(() => {
        loadEmails();
    }, []);

    const loadEmails = async () => {
        try {
            setLoading(true);

            // Get emails from API
            const response = await emailAPI.getEmails();
            const emailsData = response.data.emails || [];

            // Transform API data to match UI format
            const transformedEmails = emailsData.map(email => ({
                id: email.email_id,
                subject: email.subject,
                sender: email.sender,
                received_at: email.received_at,
                body_preview: email.body ? email.body.substring(0, 200) + '...' : 'No content',
                attachments: email.attachments || [],
                rfp_created: email.processed,
                rfp_id: email.rfp_id,
                status: email.processed ? 'processed' : 'pending'
            }));

            setEmails(transformedEmails);

            // Set stats
            setStats({
                total: response.data.total || 0,
                processed: response.data.processed_count || 0,
                pending: response.data.pending_count || 0,
                attachments: transformedEmails.reduce((sum, e) => sum + (e.attachments?.length || 0), 0)
            });

        } catch (error) {
            console.error('Error loading emails:', error);
            // Fallback to empty state on error
            setEmails([]);
            setStats({ total: 0, processed: 0, pending: 0, attachments: 0 });
        } finally {
            setLoading(false);
        }
    };

    const filteredEmails = emails.filter(email => {
        if (filter === 'all') return true;
        if (filter === 'processed') return email.status === 'processed';
        if (filter === 'pending') return email.status === 'pending';
        return true;
    });

    const formatFileSize = (bytes) => {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    };

    const getStatusBadge = (status) => {
        if (status === 'processed') {
            return (
                <span className="inline-flex items-center gap-1 px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">
                    <CheckCircle size={14} />
                    Processed
                </span>
            );
        }
        return (
            <span className="inline-flex items-center gap-1 px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs font-medium">
                <Clock size={14} />
                Pending
            </span>
        );
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
            {/* Header */}
            <div>
                <div className="flex items-center gap-3 mb-2">
                    <Mail className="text-primary" size={32} />
                    <h2 className="text-3xl font-bold text-text">Email Inbox</h2>
                </div>
                <p className="text-text-light">RFPs discovered from email monitoring</p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white rounded-lg shadow-md p-6">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-text-light text-sm">Total Emails</span>
                        <Mail className="text-blue-500" size={20} />
                    </div>
                    <div className="text-3xl font-bold text-text">{stats.total}</div>
                </div>

                <div className="bg-white rounded-lg shadow-md p-6">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-text-light text-sm">Processed</span>
                        <CheckCircle className="text-green-500" size={20} />
                    </div>
                    <div className="text-3xl font-bold text-green-600">
                        {stats.processed}
                    </div>
                    <div className="text-xs text-text-light mt-1">RFPs created</div>
                </div>

                <div className="bg-white rounded-lg shadow-md p-6">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-text-light text-sm">Attachments</span>
                        <Paperclip className="text-purple-500" size={20} />
                    </div>
                    <div className="text-3xl font-bold text-purple-600">
                        {stats.attachments}
                    </div>
                    <div className="text-xs text-text-light mt-1">PDFs downloaded</div>
                </div>
            </div>

            {/* Filter */}
            <div className="bg-white rounded-lg shadow-md p-4">
                <div className="flex items-center gap-4">
                    <span className="text-sm font-medium text-text">Filter:</span>
                    <div className="flex gap-2">
                        <button
                            onClick={() => setFilter('all')}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'all'
                                ? 'bg-primary text-white'
                                : 'bg-gray-100 text-text hover:bg-gray-200'
                                }`}
                        >
                            All ({emails.length})
                        </button>
                        <button
                            onClick={() => setFilter('processed')}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'processed'
                                ? 'bg-green-600 text-white'
                                : 'bg-gray-100 text-text hover:bg-gray-200'
                                }`}
                        >
                            Processed ({emails.filter(e => e.status === 'processed').length})
                        </button>
                        <button
                            onClick={() => setFilter('pending')}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'pending'
                                ? 'bg-yellow-600 text-white'
                                : 'bg-gray-100 text-text hover:bg-gray-200'
                                }`}
                        >
                            Pending ({emails.filter(e => e.status === 'pending').length})
                        </button>
                    </div>
                </div>
            </div>

            {/* Email List */}
            <div className="space-y-4">
                {filteredEmails.length === 0 ? (
                    <div className="bg-white rounded-lg shadow-md p-12 text-center">
                        <Mail className="mx-auto text-gray-300 mb-4" size={48} />
                        <p className="text-text-light">No emails found</p>
                    </div>
                ) : (
                    filteredEmails.map((email) => (
                        <div
                            key={email.id}
                            className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6"
                        >
                            <div className="flex items-start justify-between mb-4">
                                <div className="flex-1">
                                    <div className="flex items-center gap-3 mb-2">
                                        <h3 className="text-lg font-bold text-text">{email.subject}</h3>
                                        {getStatusBadge(email.status)}
                                    </div>

                                    <div className="flex items-center gap-4 text-sm text-text-light mb-3">
                                        <div className="flex items-center gap-2">
                                            <User size={16} />
                                            <span>{email.sender}</span>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <Calendar size={16} />
                                            <span>{new Date(email.received_at).toLocaleString()}</span>
                                        </div>
                                    </div>

                                    <p className="text-text-light text-sm mb-4">{email.body_preview}</p>

                                    {/* Attachments */}
                                    {email.attachments.length > 0 && (
                                        <div className="mb-4">
                                            <div className="flex items-center gap-2 mb-2">
                                                <Paperclip size={16} className="text-text-light" />
                                                <span className="text-sm font-medium text-text">
                                                    {email.attachments.length} Attachment{email.attachments.length > 1 ? 's' : ''}
                                                </span>
                                            </div>
                                            <div className="space-y-2">
                                                {email.attachments.map((attachment, idx) => (
                                                    <div
                                                        key={idx}
                                                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200"
                                                    >
                                                        <div className="flex items-center gap-3">
                                                            <FileText className="text-red-500" size={20} />
                                                            <div>
                                                                <div className="text-sm font-medium text-text">{attachment.filename}</div>
                                                                <div className="text-xs text-text-light">{formatFileSize(attachment.size)}</div>
                                                            </div>
                                                        </div>
                                                        <div className="flex items-center gap-2">
                                                            <a
                                                                href={`http://localhost:8003/uploads/${attachment.filename}`}
                                                                target="_blank"
                                                                rel="noopener noreferrer"
                                                                className="p-2 hover:bg-gray-200 rounded-lg transition-colors text-text-light hover:text-primary"
                                                                title="View"
                                                            >
                                                                <Eye size={18} />
                                                            </a>
                                                            <a
                                                                href={`http://localhost:8003/uploads/${attachment.filename}`}
                                                                download
                                                                className="p-2 hover:bg-gray-200 rounded-lg transition-colors text-text-light hover:text-primary"
                                                                title="Download"
                                                            >
                                                                <Download size={18} />
                                                            </a>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* RFP Link */}
                                    {email.rfp_created && email.rfp_id && (
                                        <div className="flex items-center gap-2 p-3 bg-green-50 border border-green-200 rounded-lg">
                                            <CheckCircle className="text-green-600" size={20} />
                                            <span className="text-sm text-green-800">
                                                RFP Created:
                                            </span>
                                            <Link
                                                to={`/rfp/${email.rfp_id}`}
                                                className="text-sm font-medium text-primary hover:underline"
                                            >
                                                {email.rfp_id}
                                            </Link>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>

            {/* Info Box */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-start gap-3">
                    <Mail className="text-blue-600 flex-shrink-0 mt-1" size={20} />
                    <div>
                        <h4 className="font-semibold text-blue-900 mb-1">Email Monitoring Active</h4>
                        <p className="text-sm text-blue-800">
                            The system automatically checks your email inbox every hour for new RFPs.
                            Emails with PDF attachments are processed automatically, and RFP entries are created.
                        </p>
                        <p className="text-sm text-blue-800 mt-2">
                            <strong>PDFs are saved to:</strong> <code className="bg-blue-100 px-2 py-1 rounded">data/uploads/</code>
                        </p>
                        <p className="text-sm text-blue-800 mt-2 font-medium">
                            Last Checked: Just now
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default EmailInbox;
