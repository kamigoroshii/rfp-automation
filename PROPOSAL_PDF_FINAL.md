# Enhanced Proposal PDF Modal - V3

## Updated Frontend Code

Replace the PDF modal section in `frontend/src/pages/RFPDetail.jsx`:

```jsx
{/* Proposal PDF Modal */}
{proposalPdfOpen && (
  <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
    <div className="bg-white rounded-lg shadow-2xl w-full max-w-5xl h-[90vh] flex flex-col">
      {/* Header with Download Icon */}
      <div className="flex items-center justify-between p-4 border-b bg-gradient-to-r from-green-50 to-green-100">
        <div>
          <h3 className="text-lg font-bold text-gray-800">Business Proposal</h3>
          <p className="text-sm text-gray-600">RFP #{rfp_id} - {title}</p>
        </div>
        <div className="flex items-center gap-2">
          {/* Download Icon Button */}
          <a
            href={proposalPdfUrl}
            download={`Proposal_${rfp_id}.pdf`}
            className="p-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
            title="Download PDF"
          >
            <Download size={20} />
          </a>
          {/* Close Button */}
          <button
            onClick={() => setProposalPdfOpen(false)}
            className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
          >
            <X size={20} />
          </button>
        </div>
      </div>
      
      {/* PDF Iframe */}
      <div className="flex-1 p-4 bg-gray-50">
        <iframe
          src={proposalPdfUrl}
          className="w-full h-full border-0 rounded shadow-inner"
          title="Proposal PDF"
        />
      </div>
      
      {/* Footer with Send Mail Button */}
      <div className="p-4 border-t bg-white flex justify-between items-center">
        <button
          onClick={() => setProposalPdfOpen(false)}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
        >
          Close
        </button>
        
        {/* Send Mail Button */}
        <a
          href={`https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(
            rfpData.source_email || rfpData.source || ''
          )}&su=${encodeURIComponent(
            `Business Proposal for RFP #${rfp_id} - ${title || 'RFP Submission'}`
          )}&body=${encodeURIComponent(
            `Dear Sir/Madam,\n\nPlease find attached our comprehensive business proposal for RFP #${rfp_id}.\n\nRFP Title: ${title}\nProposed Amount: ₹${rfpData.total_estimate?.toFixed(2) || 'N/A'}\n\nWe look forward to your positive response.\n\nBest Regards,\nYour Company Name\n\nNote: Please download the attached proposal PDF for complete details.`
          )}`}
          target="_blank"
          rel="noopener noreferrer"
          className="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all shadow-md flex items-center gap-2 font-medium"
        >
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
            <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
          </svg>
          Send via Gmail
        </a>
      </div>
    </div>
  </div>
)}
```

## Backend: Add Email to RFP Response

Update `orchestrator/services/rfp_service.py` to extract and return source email:

In the `get_rfp` method, ensure the response includes:
```python
async def get_rfp(self, rfp_id: str) -> dict:
    # ... existing code ...
    
    # Extract email from source if available
    source_email = ''
    if rfp_data.get('source'):
        # Try to extract email from source string
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, str(rfp_data.get('source', '')))
        if emails:
            source_email = emails[0]
    
    rfp_data['source_email'] = source_email
    return rfp_data
```

## Alternative: Use Database Email Field

If you store emails in the `emails` table linked to RFPs, modify to fetch:

```python
# Query to get email associated with RFP
cursor.execute("""
    SELECT e.sender_email, e.sender_name
    FROM emails e
    JOIN rfps r ON r.source LIKE '%' || e.subject || '%'
    WHERE r.rfp_id = %s
    LIMIT 1
""", (rfp_id,))

email_row = cursor.fetchone()
if email_row:
    rfp_data['source_email'] = email_row[0]
    rfp_data['source_name'] = email_row[1]
```

## Complete Features:

### Top Right:
- ✅ **Download Icon** - Single click to download PDF

### Bottom:
- ✅ **Send via Gmail button** with:
  - **To:** Email from RFP source
  - **Subject:** "Business Proposal for RFP #{id} - {title}"
  - **Body:** Pre-written professional message including:
    - RFP details
    - Proposed amount
    - Request to review
    - Note about PDF attachment

### Gmail Compose Opens With:
```
To: [source_email from RFP]
Subject: Business Proposal for RFP #RFP-001 - Cable Supply Tender

Body:
Dear Sir/Madam,

Please find attached our comprehensive business proposal for RFP #RFP-001.

RFP Title: Cable Supply Tender
Proposed Amount: ₹12,50,000.00

We look forward to your positive response.

Best Regards,
Your Company Name

Note: Please download the attached proposal PDF for complete details.
```

### Visual Design:
- Green download button (top-right)
- Blue gradient "Send via Gmail" button (bottom-right)
- Professional gray "Close" button (bottom-left)
- Email icon on send button
- Hover effects and shadows

The user can click "Send via Gmail" and Gmail will open in a new tab with everything pre-filled! 📧✨
