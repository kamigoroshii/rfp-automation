# Demo Websites for RFP Web Scraping

## Overview
This directory contains demo HTML pages that simulate real tender portals for testing the RFP web scraping functionality.

## 🚀 Quick Start

1. **Start the frontend dev server:**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Access the demo index page:**
   Open: `http://localhost:5173/demos/index.html`

3. **Start testing!**

## Demo Pages

### Index Page
**File:** `index.html`  
**URL:** `http://localhost:5173/demos/index.html`

Central hub with links to all demo pages, instructions, and copy-paste URLs for quick testing.

### 1. Test Portal (Recommended for First-Time Testing)
**File:** `test-simple.html`  
**URL:** `http://localhost:5173/demos/test-simple.html`

Simple page with 3 RFPs. Clean structure, perfect for validating the scraping logic.

**Contents:**
- 3 test RFPs with basic information
- Clear `.rfp-listing` structure
- Includes testing instructions

### 2. Main Government Portal
**File:** `tenders-portal.html`  
**URL:** `http://localhost:5173/demos/tenders-portal.html`

Realistic government tender portal with multiple RFPs.

**Structure:**
- Contains 5 RFP listings with `class="rfp-listing"`
- Each listing includes: title, client, deadline, value, specs, etc.
- Structured to match the Sales Agent's scraping expectations
- Mix of urgent, high-value, and standard RFPs

### 3. Detail Pages
Individual RFP detail pages for each tender:
- `metro-rail-rfp-detail.html` - Metro cable tender (₹45 Cr, Urgent)
- `solar-modules-rfp-detail.html` - Solar module tender (₹120 Cr)
- `smart-lighting-rfp-detail.html` - Smart LED lighting (₹28 Cr)

## Testing Instructions

### Start the Frontend Dev Server
```bash
cd frontend
npm run dev
```

### Access Demo Pages
- Main Portal: http://localhost:5173/demos/tenders-portal.html
- Metro RFP Detail: http://localhost:5173/demos/metro-rail-rfp-detail.html
- Solar RFP Detail: http://localhost:5173/demos/solar-modules-rfp-detail.html

### Test Web Scraping

1. **Via Frontend UI:**
   - Go to Submit RFP page
   - Select "Web URL" submission type
   - Enter: `http://localhost:5173/demos/tenders-portal.html`
   - Click "Scrape & Process"

2. **Via API:**
   ```bash
   curl -X POST http://localhost:8005/api/sales/intake-url \
     -H "Content-Type: application/json" \
     -d '{"url": "http://localhost:5173/demos/tenders-portal.html"}'
   ```

3. **Direct Sales Agent Test:**
   ```python
   from agents.sales.agent import SalesAgent
   
   agent = SalesAgent()
   rfps = agent.discover_rfps_from_url("http://localhost:5173/demos/tenders-portal.html")
   print(f"Found {len(rfps)} RFPs")
   ```

## RFP Data Structure

Each `.rfp-listing` div contains:
- `data-rfp-id`: Unique identifier (e.g., "RFP-2025-001")
- `.rfp-title`: RFP title
- `.rfp-meta`: Client, deadline, value, location
- `.rfp-description`: Project scope
- `.rfp-specs`: Technical specifications as tags
- Badge indicating urgency/priority

## Expected Behavior

When scraped by the Sales Agent:
1. Finds all `.rfp-listing` elements
2. Extracts title, client, deadline, specs from each
3. Calculates days until deadline
4. Applies 90-day filter
5. Computes Go/No-Go score
6. Creates RFP tickets in database
7. Pushes qualified RFPs to Redis queue

## Customization

To add more demo RFPs:
1. Copy an existing `.rfp-listing` div
2. Update the data-rfp-id
3. Modify title, specs, dates, etc.
4. Ensure structure matches existing pattern

## Notes
- All deadlines are relative to current date (some urgent, some 30+ days)
- Project values range from ₹28 Cr to ₹120 Cr
- Mix of client types: Government, PSU, Private
- Various product categories: Cables, Solar, Lighting, etc.
