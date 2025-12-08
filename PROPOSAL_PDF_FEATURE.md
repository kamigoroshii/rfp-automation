# Proposal PDF Generation Feature

## Overview
Add a "Generate Proposal PDF" button that appears when RFP status is "completed". The button downloads a PDF with all proposal details.

## Frontend Changes

### 1. Add Download Icon Import
In `frontend/src/pages/RFPDetail.jsx`, line 5-12, add `Download` to imports:

```jsx
import {
  ArrowLeft,
  Calendar,
  ExternalLink,
  CheckCircle,
  AlertTriangle,
  TrendingUp,
  DollarSign,
  Package,
  Clock,
  FileText,
  Download,  // ADD THIS
  X
} from 'lucide-react';
```

### 2. Add Button After "Submit Feedback"
After line 116 (Submit Feedback button), add:

```jsx
{status === 'completed' && (
  <button
    onClick={async () => {
      try {
        const response = await fetch(`/api/rfp/${rfp_id}/proposal-pdf`);
        if (!response.ok) throw new Error('Failed to generate PDF');
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Proposal_${rfp_id}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        toast.success('Proposal PDF generated successfully!');
      } catch (error) {
        console.error('Error generating PDF:', error);
        toast.error('Failed to generate proposal PDF');
      }
    }}
    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
  >
    <Download size={18} />
    Generate Proposal PDF
  </button>
)}
```

## Backend Changes

### Create PDF Generator Endpoint
Create `orchestrator/api/routes/pdf_generator.py`:

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import logging

from orchestrator.services.rfp_service import RFPService

router = APIRouter()
logger = logging.getLogger(__name__)
rfp_service = RFPService()

@router.get("/{rfp_id}/proposal-pdf")
async def generate_proposal_pdf(rfp_id: str):
    """Generate proposal PDF for completed RFPpython"""
    try:
        # Get RFP data
        rfp = await rfp_service.get_rfp(rfp_id)
        
        if not rfp:
            raise HTTPException(status_code=404, detail="RFP not found")
        
        if rfp.get('status') != 'completed':
            raise HTTPException(status_code=400, detail="RFP must be completed to generate proposal")
        
        # Create PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Title
        p.setFont("Helvetica-Bold", 24)
        p.drawString(50, height - 50, "RFP Proposal")
        
        # RFP Details
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, height - 100, f"RFP ID: {rfp_id}")
        
        p.setFont("Helvetica", 12)
        y = height - 130
        
        # Title
        p.drawString(50, y, f"Title: {rfp.get('title', 'N/A')}")
        y -= 25
        
        # Bid Amount
        estimate = rfp.get('total_estimate', 0)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, f"Proposed Bid Amount: ₹{estimate:,.2f}")
        y -= 35
        
        # Recommended Product
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Recommended Product:")
        y -= 20
        p.setFont("Helvetica", 11)
        p.drawString(70, y, rfp.get('recommended_sku', 'N/A'))
        y -= 30
        
        # Scope
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Scope:")
        y -= 20
        p.setFont("Helvetica", 10)
       
        scope = rfp.get('scope', '')
        if len(scope) > 100:
            scope = scope[:100] + "..."
        p.drawString(70, y, scope)
        y -= 30
        
        # Product Matches
        matches = rfp.get('matches', [])
        if matches:
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, y, "Product Selection:")
            y -= 20
            
            for i, match in enumerate(matches[:5], 1):  # Show top 5
                p.setFont("Helvetica", 10)
                score = match.get('match_score', 0) * 100
                p.drawString(70, y, f"{i}. {match.get('product_name', 'N/A')} - Match: {score:.0f}%")
                y -= 15
                
        p.showPage()
        p.save()
        
        buffer.seek(0)
        
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=Proposal_{rfp_id}.pdf"}
        )
        
    except Exception as e:
        logger.error(f"Error generating proposal PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### Add to main.py
In `orchestrator/api/main.py`, add:

```python
from orchestrator.api.routes import pdf_generator

app.include_router(pdf_generator.router, prefix="/api/rfp", tags=["pdf"])
```

### Install ReportLab
Add to `requirements.txt`:
```
reportlab>=4.0.0
```

Then run:
```bash
pip install reportlab
```

## How It Works

1. User opens a completed RFP
2. "Generate Proposal PDF" button appears (green button)
3. Click button → calls `/api/rfp/{rfp_id}/proposal-pdf`
4. Backend generates PDF with:
   - RFP title and ID
   - **Bid amount** (total_estimate)
   - **Recommended product** (recommended_sku)
   - Scope of work
   - Top 5 product matches with scores
5. PDF downloads automatically as `Proposal_{rfp_id}.pdf`

The PDF contains all the key proposal details ready for submission!
