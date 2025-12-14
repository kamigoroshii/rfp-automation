# 🎬 SmartBid Control Tower - Demo Tiers

## 📺 Demo Components (Tiered Approach)

---

### **Tier 1: Core Automation Pipeline** ⚡
*Must-Have Features - The Foundation (10-12 min)*

#### 1.1 Sales Agent - RFP Discovery
- **Email monitoring** (Gmail IMAP integration)
- **90-day deadline filter** (auto-discard old RFPs)
- **Go/No-Go scoring** (TimeScore + ValueScore + FitScore)
- **Demo**: Show 2 RFPs discovered → 1 qualified, 1 rejected
- **Endpoint**: `POST /agents/sales/intake-email`
- **Database**: Show `rfp_tickets` table with status progression

#### 1.2 Document Agent - Dual-Stream Processing
- **PDF parsing** (extract text, tables, metadata)
- **Spec extraction** (voltage, cores, area, insulation type)
- **Structured output**: `rfp_scope_items` table
- **Demo**: Upload RFP PDF → Show parsed specifications
- **Endpoint**: `POST /agents/document/extract/{ticket_id}`

#### 1.3 Technical Agent - Spec Match Table
- **Top-3 product matching** per scope item
- **SpecMatch% calculation** (75-85% accuracy)
  - Voltage match: 20%
  - Conductor size: 20%
  - Insulation type: 20%
  - Conductor material: 20%
  - Standards: 20%
- **Demo**: Show match results with color-coded scores
- **Wireframe**: [05_product_matching.png](data/ppt_charts/wireframes/05_product_matching.png)
- **Database**: `rfp_oem_matches` table

#### 1.4 Pricing Agent - Price Bands
- **3 pricing strategies**:
  - 🔴 Aggressive: 0.95× market median (5% below)
  - 🔵 Balanced: 1.00× market median (market rate)
  - 🟡 Conservative: 1.10× market median (10% premium)
- **Historical analysis**: Query past tender data
- **Demo**: Show price breakdown with all 3 bands
- **Wireframe**: [06_pricing_breakdown.png](data/ppt_charts/wireframes/06_pricing_breakdown.png)
- **Endpoint**: `POST /agents/pricing/calculate/{ticket_id}`

#### 🎯 Tier 1 Output
✅ **End-to-End Demo**: Email → Parsed Specs → Matched Products → 3 Price Options  
✅ **Time**: 2.5 days (vs 7 days manual)  
✅ **Charts**: [chart5_today_vs_smartbid.png](data/ppt_charts/chart5_today_vs_smartbid.png), [chart3_cycle_time_reduction.png](data/ppt_charts/chart3_cycle_time_reduction.png)

---

### **Tier 2: Quality Assurance & Intelligence** 🛡️
*Advanced Features - Validation Layer (5-7 min)*

#### 2.1 Auditor Agent - Red-Team Audit
- **Completeness checks**:
  - ✓ All required tests specified
  - ✓ Missing technical clauses flagged
  - ✓ Delivery terms validated
- **Hallucination detection**:
  - Flag SKUs not in product catalog
  - Detect price anomalies (>20% deviation from historical)
  - Verify standards compliance
- **Demo**: Show flagged issues in audit report
- **Status**: VALIDATED ✅ or FLAGGED ⚠️
- **Endpoint**: `POST /agents/auditor/validate/{ticket_id}`
- **Database**: Show audit_flags table

#### 2.2 Learning Agent - Weights Update
- **Continuous improvement from outcomes**:
  - Analyze win/loss patterns from `tender_outcomes`
  - Adjust spec matching weights per segment
  - Optimize pricing multipliers based on win rates
- **Demo**: Show before/after weight adjustments
- **Metrics tracked**:
  - Win rate by client type (government vs private)
  - Average match accuracy trends
  - Pricing competitiveness scores
- **Config table**: `pricing_config_segments`
- **Endpoint**: `POST /agents/learning/train`

#### 📊 Tier 2 Output
✅ **Quality Gates**: 98% accuracy (vs 70% manual)  
✅ **Self-Improving**: Weights adapt based on win/loss feedback  
✅ **Charts**: [chart8_automation_heatmap.png](data/ppt_charts/chart8_automation_heatmap.png) (quality vs automation)

---

### **Tier 3: Command Center & Intelligence** 🎮
*Premium Features - User Experience (5-7 min)*

#### 3.1 Bid Co-Pilot - RAG Chatbot
- **Conversational AI** over entire knowledge base:
  - RFP documents
  - Product datasheets
  - Historical pricing data
  - Past tender outcomes
- **Demo queries**:
  - "What's the recommended SKU for 11kV XLPE cable?"
  - "Show me pricing for similar Maharashtra State tenders"
  - "What type tests are required per IS 7098?"
- **Context-aware responses** with citations
- **Wireframe**: [08_bid_copilot.png](data/ppt_charts/wireframes/08_bid_copilot.png)
- **Tech**: Qdrant vector search + Gemini LLM
- **Endpoint**: `POST /agents/copilot/chat`

#### 3.2 Kanban Dashboard - Status Board
- **Visual workflow** (Kanban-style):
  ```
  NEW → ANALYZING → MATCHED → PRICED → REVIEWED → APPROVED
  ```
- **Drag-and-drop** cards for status updates
- **Real-time metrics**:
  - Cards in each stage
  - Bottleneck detection
  - SLA warnings (deadline approaching)
- **Wireframe**: [01_dashboard.png](data/ppt_charts/wireframes/01_dashboard.png) + [02_rfp_list.png](data/ppt_charts/wireframes/02_rfp_list.png)
- **Tech**: React DnD + WebSockets for real-time updates

#### 3.3 Queue Visualization - System Health
- **Redis queue monitoring**:
  - Queue depth (pending RFPs)
  - Processing throughput (RFPs/hour)
  - Agent utilization (busy/idle)
- **Agent status indicators**:
  - 🟢 Active | 🟡 Busy | 🔴 Error | ⚪ Idle
- **Performance charts**:
  - Processing time distribution
  - Error rate trends
  - Capacity utilization
- **Live logs**: Stream processing events
- **Wireframe**: [07_analytics.png](data/ppt_charts/wireframes/07_analytics.png)

#### 🏆 Tier 3 Output
✅ **User Experience**: Intuitive interface for sales teams  
✅ **Transparency**: Full visibility into AI decision-making  
✅ **Control**: Human-in-the-loop approval workflow  
✅ **Charts**: [chart1_monthly_rfp_volume.png](data/ppt_charts/chart1_monthly_rfp_volume.png), [chart4_win_rate_improvement.png](data/ppt_charts/chart4_win_rate_improvement.png)

---

## 🎭 Demo Execution Plan

### **Option A: Full Demo (20-25 min)**
```
├─ Problem Statement (2 min)
├─ Tier 1: Core Pipeline (10 min)
│  ├─ Scout discovery → Dual-stream → Match → Price
│  └─ Live: Process 1 RFP end-to-end
├─ Tier 2: QA & Learning (5 min)
│  ├─ Red-team audit results
│  └─ Learning agent weight evolution
├─ Tier 3: Command Center (5 min)
│  ├─ RAG chatbot Q&A
│  ├─ Kanban board walkthrough
│  └─ Queue visualization
└─ Impact Metrics + Q&A (3 min)
```

### **Option B: Quick Demo (12-15 min)**
```
├─ Problem Statement (2 min)
├─ Tier 1 ONLY (8 min) - Full pipeline demo
└─ Impact Metrics + Q&A (2 min)
```

### **Option C: Feature Showcase (15-18 min)**
```
├─ Problem Statement (2 min)
├─ Tier 1: Highlights (5 min) - Key features only
├─ Tier 2: Audit (3 min) - Red-team demo
├─ Tier 3: Co-Pilot (3 min) - RAG chatbot
└─ Impact Metrics + Q&A (2 min)
```

---

## 📋 Pre-Demo Checklist

### Tier 1 Setup
- [ ] Backend running on `http://127.0.0.1:8000`
- [ ] Sample RFP email ready in inbox
- [ ] Test PDF uploaded: "Supply of 11kV XLPE Cables"
- [ ] `oem_skus` table populated (at least 20 products)
- [ ] `historical_tender_lines` seeded (past 12 months)
- [ ] Redis queue operational

### Tier 2 Setup
- [ ] Auditor agent configured with rules
- [ ] Sample flagged RFP ready (price anomaly or missing spec)
- [ ] `tender_outcomes` table has win/loss data
- [ ] Learning agent trained with initial weights

### Tier 3 Setup
- [ ] Qdrant vector database loaded with documents
- [ ] RAG chatbot tested with 5 sample queries
- [ ] Frontend dashboard accessible
- [ ] WebSocket server running for real-time updates
- [ ] Queue monitoring charts rendering

### Presentation Assets
- [ ] All 13 charts in `data/ppt_charts/`
- [ ] All 8 wireframes in `data/ppt_charts/wireframes/`
- [ ] Backup screenshots/videos
- [ ] Impact metrics slide ready

---

## 🎯 Key Messages Per Tier

### Tier 1: "Automation at Scale"
- **65% faster**: 7 days → 2.5 days
- **16x capacity**: 3 → 50 RFPs/day
- **85% match accuracy**: AI-powered product selection

### Tier 2: "Intelligence & Quality"
- **98% accuracy**: Red-team validation catches errors
- **Self-improving**: Learns from every win/loss
- **Risk mitigation**: Hallucination detection

### Tier 3: "Human-AI Collaboration"
- **Natural language**: Ask questions, get instant answers
- **Full transparency**: See every decision step
- **Workflow control**: Kanban board for team coordination

---

## 💰 Business Impact Summary

| Metric | Before (Manual) | After (SmartBid) | Improvement |
|--------|----------------|------------------|-------------|
| **Response Time** | 7 days | 2.5 days | **65% faster** |
| **Capacity** | 3 RFPs/day | 50 RFPs/day | **16x more** |
| **Win Rate** | 18% | 32% | **+14 points** |
| **Error Rate** | 10% | 1% | **90% reduction** |
| **Revenue Captured** | ₹120 Cr | ₹1,323 Cr | **11x growth** |
| **Manual Effort** | 288 hrs/month | 3 hrs/month | **99% automated** |

**ROI**: From 5% market capture → 55% with SmartBid  
**Chart**: [chart13_waterfall_revenue.png](data/ppt_charts/chart13_waterfall_revenue.png)

---

## 🎬 Demo Script Template

```markdown
[TIER 1 - 10 MIN]
"Let me show you how SmartBid automates the entire RFP workflow..."

1. Scout Agent: "We monitor Gmail 24/7. Here's an RFP that just arrived."
   → Show email → Click "Process" → Status: NEW

2. Document Agent: "AI extracts specifications from the PDF."
   → Show parsed specs table → Highlight: 11kV, 3-core, 240 sq.mm

3. Technical Agent: "Find Top-3 matching products from our catalog."
   → Show match table → 85%, 72%, 68% scores → Select XLPE-11KV-240-CU

4. Pricing Agent: "Generate pricing with 3 strategies."
   → Show price breakdown → Toggle Aggressive/Balanced/Conservative
   → Highlight: "2.9% above historical median"

Result: "Complete proposal ready in 2.5 days vs 7 days manual."

[TIER 2 - 5 MIN]
5. Auditor: "Red-team checks for errors."
   → Show audit report → Flag: "Price 22% above median - Review!"
   
6. Learning Agent: "System improves from every tender."
   → Show weight evolution chart → "Win rate improved 14 points"

[TIER 3 - 5 MIN]
7. Co-Pilot: "Ask me anything about this RFP."
   → Type: "What tests are required?"
   → AI: "Type test and routine test per IS 7098, estimated ₹4.04L"

8. Dashboard: "Full visibility for your team."
   → Show Kanban board → 24 RFPs in progress
   → Show queue: 5 pending, 2 processing, 17 completed today

[IMPACT - 2 MIN]
"Bottom line: 11x revenue growth, 65% faster, 16x capacity."
→ Show waterfall chart → ₹120 Cr → ₹1,323 Cr
```

---

**Status**: ✅ Ready for demo execution  
**Next Steps**: Choose demo length (Option A/B/C) and rehearse script
