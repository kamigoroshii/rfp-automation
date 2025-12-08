# Complete Proposal PDF Feature - V2 (Iframe Display)

## Backend: Comprehensive PDF Generator

Create `orchestrator/api/routes/pdf_generator.py`:

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import logging
from datetime import datetime

from orchestrator.services.rfp_service import RFPService

router = APIRouter()
logger = logging.getLogger(__name__)
rfp_service = RFPService()

@router.get("/{rfp_id}/proposal-pdf")
async def generate_proposal_pdf(rfp_id: str):
    """Generate comprehensive proposal PDF for completed RFP"""
    try:
        # Get RFP data
        rfp = await rfp_service.get_rfp(rfp_id)
        
        if not rfp:
            raise HTTPException(status_code=404, detail="RFP not found")
        
        if rfp.get('status') != 'completed':
            raise HTTPException(status_code=400, detail="RFP must be completed")
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Container for PDF elements
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#556B2F'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#556B2F'),
            spaceAfter=12
        )
        
        # Title
        elements.append(Paragraph("BUSINESS PROPOSAL", title_style))
        elements.append(Paragraph(f"RFP #{rfp_id}", styles['Heading3']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Generated Date
        elements.append(Paragraph(
            f"<i>Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}</i>",
            styles['Normal']
        ))
        elements.append(Spacer(1, 0.4*inch))
        
        # === SECTION 1: RFP DETAILS ===
        elements.append(Paragraph("1. RFP INFORMATION", heading_style))
        
        rfp_info = [
            ['RFP Title:', rfp.get('title', 'N/A')],
            ['RFP ID:', rfp_id],
            ['Source:', rfp.get('source', 'N/A')],
            ['Discovered On:', datetime.fromisoformat(str(rfp.get('discovered_at', ''))).strftime('%B %d, %Y') if rfp.get('discovered_at') else 'N/A'],
            ['Deadline:', datetime.fromisoformat(str(rfp.get('deadline', ''))).strftime('%B %d, %Y') if rfp.get('deadline') else 'N/A'],
            ['Status:', rfp.get('status', 'N/A').upper()],
        ]
        
        t = Table(rfp_info, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5F5F5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.3*inch))
        
        # === SECTION 2: FINANCIAL PROPOSAL ===
        elements.append(Paragraph("2. FINANCIAL PROPOSAL", heading_style))
        
        estimate = rfp.get('total_estimate', 0)
        financial_data = [
            ['Description', 'Amount (INR)'],
            ['Total Bid Amount', f"₹ {estimate:,.2f}"],
            ['Tax (if applicable)', 'As per regulations'],
            ['Payment Terms', '30 days from delivery'],
        ]
        
        t = Table(financial_data, colWidths=[3*inch, 3*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#556B2F')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, 1), 12),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.3*inch))
        
        # === SECTION 3: SCOPE OF WORK ===
        elements.append(Paragraph("3. SCOPE OF WORK", heading_style))
        scope_text = rfp.get('scope', 'Not specified')
        elements.append(Paragraph(scope_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # === SECTION 4: RECOMMENDED SOLUTION ===
        elements.append(Paragraph("4. RECOMMENDED SOLUTION", heading_style))
        elements.append(Paragraph(
            f"<b>Primary Product:</b> {rfp.get('recommended_sku', 'N/A')}",
            styles['Normal']
        ))
        
        match_score = rfp.get('match_score', 0) * 100
        elements.append(Paragraph(
            f"<b>Match Confidence:</b> {match_score:.1f}%",
            styles['Normal']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Product Matches
        matches = rfp.get('matches', [])
        if matches and len(matches) > 0:
            elements.append(Paragraph("<b>Alternative Products:</b>", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            match_data = [['#', 'Product Name', 'SKU', 'Match %', 'Price (₹)']]
            for i, match in enumerate(matches[:10], 1):  # Top 10
                match_data.append([
                    str(i),
                    match.get('product_name', 'N/A')[:40],
                    match.get('sku', 'N/A'),
                    f"{match.get('match_score', 0)*100:.0f}%",
                    f"₹{match.get('price', 0):,.2f}" if match.get('price') else 'N/A'
                ])
            
            t = Table(match_data, colWidths=[0.4*inch, 2.5*inch, 1*inch, 0.8*inch, 1*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6B8E23')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            elements.append(t)
        elements.append(Spacer(1, 0.3*inch))
        
        # === SECTION 5: TECHNICAL SPECIFICATIONS ===
        if rfp.get('specifications'):
            elements.append(Paragraph("5. TECHNICAL SPECIFICATIONS", heading_style))
            specs = rfp.get('specifications', [])
            if isinstance(specs, list):
                for spec in specs[:15]:  # Limit to 15
                    elements.append(Paragraph(f"• {spec}", styles['Normal']))
            else:
                elements.append(Paragraph(str(specs), styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
        
        # === SECTION 6: TESTING REQUIREMENTS ===
        if rfp.get('testing_requirements'):
            elements.append(Paragraph("6. TESTING & QUALITY REQUIREMENTS", heading_style))
            elements.append(Paragraph(rfp.get('testing_requirements', 'Standard tests apply'), styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
        
        # === SECTION 7: DELIVERY TERMS ===
        elements.append(Paragraph("7. DELIVERY & TIMELINE", heading_style))
        delivery_data = [
            ['Delivery Timeline:', '30-45 days from order confirmation'],
            ['Delivery Location:', 'As specified in RFP'],
            ['Warranty:', '12 months from delivery'],
            ['Support:', '24/7 technical support'],
        ]
        
        t = Table(delivery_data, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.4*inch))
        
        # Footer
        elements.append(Paragraph(
            "<i>This proposal is valid for 90 days from the date of generation.</i>",
            styles['Normal']
        ))
        elements.append(Paragraph(
            "<i>All prices are subject to applicable taxes and regulations.</i>",
            styles['Normal']
        ))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename=Proposal_{rfp_id}.pdf"}
        )
        
    except Exception as e:
        logger.error(f"Error generating proposal PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

## Frontend: Button with Iframe Modal

Update `frontend/src/pages/RFPDetail.jsx`:

### 1. Add state for proposal PDF:
```jsx
const [proposalPdfUrl, setProposalPdfUrl] = useState('');
const [proposalPdfOpen, setProposalPdfOpen] = useState(false);
```

### 2. Add button (after Submit Feedback button, around line 116):
```jsx
{status === 'completed' && (
  <button
    onClick={() => {
      setProposalPdfUrl(`http://localhost:8003/api/rfp/${rfp_id}/proposal-pdf`);
      setProposalPdfOpen(true);
    }}
    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
  >
    <Download size={18} />
    Generate Proposal PDF
  </button>
)}
```

### 3. Add iframe modal (at end of component, before closing div):
```jsx
{/* Proposal PDF Modal */}
{proposalPdfOpen && (
  <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
    <div className="bg-white rounded-lg shadow-2xl w-full max-w-5xl h-[90vh] flex flex-col">
      <div className="flex items-center justify-between p-4 border-b">
        <h3 className="text-lg font-bold">Proposal Document - {rfp_id}</h3>
        <button
          onClick={() => setProposalPdfOpen(false)}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <X size={20} />
        </button>
      </div>
      <div className="flex-1 p-4">
        <iframe
          src={proposalPdfUrl}
          className="w-full h-full border-0 rounded"
          title="Proposal PDF"
        />
      </div>
      <div className="p-4 border-t flex justify-end gap-3">
        <a
          href={proposalPdfUrl}
          download={`Proposal_${rfp_id}.pdf`}
          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
        >
          Download PDF
        </a>
        <button
          onClick={() => setProposalPdfOpen(false)}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
        >
          Close
        </button>
      </div>
    </div>
  </div>
)}
```

## Setup Instructions

1. Install ReportLab:
```bash
pip install reportlab
```

2. Add router to `orchestrator/api/main.py`:
```python
from orchestrator.api.routes import pdf_generator
app.include_router(pdf_generator.router, prefix="/api/rfp", tags=["pdf"])
```

3. Restart backend server

## What the PDF Contains (ALL Details):

1. **RFP Information** - Title, ID, Source, Dates, Status
2. **Financial Proposal** - Bid amount, taxes, payment terms
3. **Scope of Work** - Complete description
4. **Recommended Solution** - Primary product + match score
5. **Alternative Products** - Top 10 matches with prices
6. **Technical Specifications** - Full spec list
7. **Testing Requirements** - Quality standards
8. **Delivery Terms** - Timeline, warranty, support

The PDF appears in a **large iframe modal** with download option!
