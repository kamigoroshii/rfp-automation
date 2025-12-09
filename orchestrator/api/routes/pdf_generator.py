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

@router.post("/{rfp_id}/generate-pdf")
async def generate_proposal_pdf(rfp_id: str):
    """Generate proposal PDF for completed RFP"""
    try:
        import os
        # Get RFP data
        rfp = await rfp_service.get_rfp_by_id(rfp_id)
        
        if not rfp:
            raise HTTPException(status_code=404, detail="RFP not found")
        
        # Check status (relaxed checks for testing if needed, but keeping logic)
        if rfp.get('status') != 'completed':
             raise HTTPException(status_code=400, detail="RFP must be completed to generate proposal")
        
        # Ensure uploads dir exists
        uploads_dir = os.path.join(os.getcwd(), "data", "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        
        safe_id = rfp_id.replace('/', '_').replace('\\', '_').replace(':', '')
        filename = f"proposal_{safe_id}.pdf"
        filepath = os.path.join(uploads_dir, filename)
        
        # Create PDF
        p = canvas.Canvas(filepath, pagesize=letter)
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
        p.drawString(50, y, f"Proposed Bid Amount: {estimate:,.2f} INR")
        y -= 35
        
        # Recommended Product
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Recommended Product:")
        y -= 20
        p.setFont("Helvetica", 11)
        p.drawString(70, y, str(rfp.get('recommended_sku', 'N/A')))
        y -= 30
        
        # Scope
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Scope:")
        y -= 20
        p.setFont("Helvetica", 10)
       
        scope = rfp.get('scope', '')
        if len(scope) > 400: # Truncate for PDF
            scope = scope[:400] + "..."
        
        # Simple text wrap simulation
        words = scope.split()
        line = ""
        for word in words:
            if p.stringWidth(line + " " + word, "Helvetica", 10) < 500:
                line += " " + word
            else:
                p.drawString(70, y, line.strip())
                y -= 15
                line = word
        if line:
            p.drawString(70, y, line.strip())
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
                
        p.save()
        
        # Return URL
        return {"download_url": f"/uploads/{filename}"}
        
    except Exception as e:
        logger.error(f"Error generating proposal PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{rfp_id}/generate-doc")
async def generate_proposal_doc(rfp_id: str):
    """Generate proposal Word Doc (HTML) for completed RFP"""
    try:
        import os
        rfp = await rfp_service.get_rfp_by_id(rfp_id)
        if not rfp:
            raise HTTPException(status_code=404, detail="RFP not found")
            
        uploads_dir = os.path.join(os.getcwd(), "data", "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        
        safe_id = rfp_id.replace('/', '_').replace('\\', '_').replace(':', '')
        filename = f"proposal_{safe_id}.doc"
        filepath = os.path.join(uploads_dir, filename)
        
        # Generate HTML content acting as Doc
        rows = ""
        for p in rfp.get('pricing', []):
            rows += f"<tr><td>{p.get('sku')}</td><td>{p.get('quantity')}</td><td>{p.get('unit_price')}</td><td>{p.get('total')}</td></tr>"

        content = f"""
        <html>
        <body>
            <h1>Business Proposal</h1>
            <h2>RFP: {rfp.get('title')}</h2>
            <p><strong>ID:</strong> {rfp_id}</p>
            <p><strong>Total Estimate:</strong> INR {rfp.get('total_estimate', 0):,.2f}</p>
            <hr>
            <h3>Scope</h3>
            <p>{rfp.get('scope')}</p>
            <h3>Recommendation</h3>
            <p>We recommend: <strong>{rfp.get('recommended_sku')}</strong></p>
            <h3>Pricing Breakdown</h3>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr><th>Item</th><th>Qty</th><th>Unit Price</th><th>Total</th></tr>
                {rows}
            </table>
        </body>
        </html>
        """
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        return {"download_url": f"/uploads/{filename}"}
    except Exception as e:
        logger.error(f"Error generating Doc: {e}")
        raise HTTPException(status_code=500, detail=str(e))
