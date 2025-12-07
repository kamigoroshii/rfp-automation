# 📡 SmartBid API Contract

**Version:** 1.0  
**Last Updated:** December 7, 2025  
**Base URL:** `http://localhost:8000/api`

---

## 🔐 Authentication

All requests require JWT token in header:
```
Authorization: Bearer <token>
```

---

## 📋 Standard Response Format

### Success Response
```json
{
  "status": "success",
  "data": { ... },
  "message": "Operation completed",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

### Error Response
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Missing required field: client_name",
    "details": { ... }
  },
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

## 🎫 RFP Management Endpoints

### 1. List All RFPs
```
GET /api/rfp/list
```

**Query Parameters:**
- `status` (optional): Filter by status (NEW, ANALYZING, MATCHED, PRICED, REVIEWED, APPROVED, REJECTED)
- `client_type` (optional): Filter by client type (government, private, repeat)
- `days_until_due` (optional): Filter by urgency
- `page` (optional, default: 1): Page number
- `limit` (optional, default: 20): Items per page
- `sort_by` (optional, default: "go_no_go_score"): Sort field
- `sort_order` (optional, default: "desc"): asc or desc

**Response:**
```json
{
  "status": "success",
  "data": {
    "rfps": [
      {
        "ticket_id": "uuid",
        "rfp_title": "33kV XLPE Cable Supply for Metro Project",
        "client_name": "Delhi Metro Rail Corporation",
        "client_type": "government",
        "project_type": "transmission",
        "due_date": "2025-03-15T23:59:59Z",
        "days_until_due": 45,
        "go_no_go_score": 87.5,
        "status": "MATCHED",
        "discovered_at": "2025-12-01T10:30:00Z",
        "estimated_value": 1500000.00,
        "currency": "INR"
      }
    ],
    "pagination": {
      "total": 150,
      "page": 1,
      "limit": 20,
      "pages": 8
    }
  },
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 2. Get RFP Details
```
GET /api/rfp/{ticket_id}
```

**Path Parameters:**
- `ticket_id` (required): UUID of the RFP ticket

**Response:**
```json
{
  "status": "success",
  "data": {
    "ticket": {
      "ticket_id": "uuid",
      "rfp_title": "33kV XLPE Cable Supply for Metro Project",
      "source_type": "web",
      "source_url": "https://example.com/tender",
      "client_name": "Delhi Metro Rail Corporation",
      "client_type": "government",
      "project_type": "transmission",
      "due_date": "2025-03-15T23:59:59Z",
      "days_until_due": 45,
      "go_no_go_score": 87.5,
      "rfp_raw_text": "Full RFP text...",
      "status": "MATCHED",
      "discovered_at": "2025-12-01T10:30:00Z",
      "created_at": "2025-12-01T10:30:00Z",
      "updated_at": "2025-12-03T14:20:00Z"
    },
    "scope_items": [
      {
        "item_id": "uuid",
        "item_number": 1,
        "description": "3 Core XLPE Insulated, Armoured Cable",
        "quantity": 5000,
        "unit": "meters",
        "voltage_kv": 33.0,
        "cores": 3,
        "area_sqmm": 185.0,
        "insulation_type": "XLPE",
        "conductor_material": "Copper",
        "armour_type": "SWA",
        "temp_rating": 90,
        "standards": ["IEC 60502-2", "IS 7098"]
      }
    ],
    "matches": [
      {
        "item_id": "uuid",
        "sku": "XLPE-33KV-3C-185",
        "product_name": "33kV 3C 185mm² XLPE Cable",
        "match_rank": 1,
        "spec_match_pct": 95.0,
        "voltage_match": true,
        "size_match": true,
        "insulation_match": true,
        "conductor_match": true,
        "standards_match": true
      }
    ],
    "pricing": {
      "total_value": 1500000.00,
      "currency": "INR",
      "selected_strategy": "balanced",
      "line_items": [
        {
          "item_id": "uuid",
          "sku": "XLPE-33KV-3C-185",
          "quantity": 5000,
          "unit_price": 250.00,
          "material_cost": 1250000.00,
          "testing_cost": 125000.00,
          "delivery_cost": 75000.00,
          "margin_pct": 15.0,
          "total_price": 1450000.00,
          "aggressive_price": 1377500.00,
          "balanced_price": 1450000.00,
          "conservative_price": 1595000.00
        }
      ]
    }
  },
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 3. Submit New RFP
```
POST /api/rfp/submit
```

**Request Body:**
```json
{
  "rfp_title": "Supply of 11kV XLPE Cables",
  "source_type": "manual",
  "rfp_text": "Full RFP text or specifications...",
  "client_name": "ABC Power Company",
  "client_type": "private",
  "project_type": "distribution",
  "due_date": "2025-04-30T23:59:59Z"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "ticket_id": "uuid",
    "rfp_title": "Supply of 11kV XLPE Cables",
    "status": "NEW",
    "go_no_go_score": null,
    "created_at": "2025-12-07T10:30:00Z"
  },
  "message": "RFP submitted successfully. Processing will begin shortly.",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 4. Update RFP Status
```
PUT /api/rfp/{ticket_id}/status
```

**Request Body:**
```json
{
  "status": "APPROVED",
  "notes": "Approved for bidding"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "ticket_id": "uuid",
    "status": "APPROVED",
    "updated_at": "2025-12-07T10:30:00Z"
  },
  "message": "Status updated successfully",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 5. Submit Feedback
```
POST /api/rfp/{ticket_id}/feedback
```

**Request Body:**
```json
{
  "outcome": "WON",
  "our_total_price": 1450000.00,
  "competitor_price": 1520000.00,
  "feedback_notes": "Won due to better pricing and faster delivery",
  "lessons_learned": "Client valued delivery speed over price"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "outcome_id": "uuid",
    "ticket_id": "uuid",
    "outcome": "WON",
    "created_at": "2025-12-07T10:30:00Z"
  },
  "message": "Feedback recorded successfully",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 6. Delete RFP
```
DELETE /api/rfp/{ticket_id}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "ticket_id": "uuid",
    "deleted": true
  },
  "message": "RFP deleted successfully",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

## 🤖 Sales Agent Endpoints

### 1. Intake from URL
```
POST /api/agents/sales/intake-url
```

**Request Body:**
```json
{
  "url": "https://example.com/tender/12345",
  "source_type": "web",
  "client_type": "government",
  "project_type": "transmission"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "job_id": "uuid",
    "ticket_id": "uuid",
    "rfp_title": "Extracted title",
    "due_date": "2025-04-30T23:59:59Z",
    "days_until_due": 85,
    "go_no_go_score": 75.0,
    "status": "NEW"
  },
  "message": "RFP discovered and queued for processing",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 2. Intake from Email
```
POST /api/agents/sales/intake-email
```

**Request Body (multipart/form-data):**
- `email_body`: Email text
- `attachments`: File uploads (PDF, DOC, etc.)
- `sender`: Email sender
- `subject`: Email subject

**Response:**
```json
{
  "status": "success",
  "data": {
    "tickets": [
      {
        "ticket_id": "uuid",
        "rfp_title": "Extracted from attachment",
        "status": "NEW"
      }
    ]
  },
  "message": "Email processed, 1 RFP found",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 3. List Sales Tickets
```
GET /api/agents/sales/tickets
```

**Query Parameters:**
- `days_range` (optional, default: 7): Show tickets from last N days
- `min_score` (optional): Minimum go_no_go_score

**Response:**
```json
{
  "status": "success",
  "data": {
    "tickets": [
      {
        "ticket_id": "uuid",
        "rfp_title": "...",
        "go_no_go_score": 85.0,
        "days_until_due": 45,
        "discovered_at": "2025-12-07T09:00:00Z"
      }
    ],
    "stats": {
      "total_discovered": 25,
      "qualified": 18,
      "rejected": 7,
      "avg_score": 72.5
    }
  },
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

## 🔧 Technical Agent Endpoints

### 1. Extract Scope
```
POST /api/agents/technical/extract-scope/{ticket_id}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "ticket_id": "uuid",
    "scope_items": [
      {
        "item_id": "uuid",
        "item_number": 1,
        "description": "3 Core XLPE Cable",
        "quantity": 5000,
        "unit": "meters",
        "voltage_kv": 33.0,
        "cores": 3,
        "area_sqmm": 185.0,
        "insulation_type": "XLPE",
        "conductor_material": "Copper",
        "armour_type": "SWA",
        "temp_rating": 90,
        "standards": ["IEC 60502-2"]
      }
    ],
    "extraction_confidence": 0.92
  },
  "message": "Scope extracted successfully",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 2. Match Products
```
POST /api/agents/technical/match-products/{ticket_id}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "ticket_id": "uuid",
    "matches": [
      {
        "item_id": "uuid",
        "top_matches": [
          {
            "sku": "XLPE-33KV-3C-185",
            "product_name": "33kV 3C 185mm² XLPE Cable",
            "match_rank": 1,
            "spec_match_pct": 95.0,
            "match_details": {
              "voltage_match": true,
              "size_match": true,
              "insulation_match": true,
              "conductor_match": true,
              "standards_match": true
            }
          },
          {
            "sku": "XLPE-33KV-3C-240",
            "match_rank": 2,
            "spec_match_pct": 85.0
          },
          {
            "sku": "XLPE-33KV-4C-185",
            "match_rank": 3,
            "spec_match_pct": 80.0
          }
        ]
      }
    ]
  },
  "message": "Product matching completed",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 3. Get Matches
```
GET /api/agents/technical/matches/{ticket_id}
```

**Response:** Same as Match Products response

---

## 💰 Pricing Agent Endpoints

### 1. Calculate Pricing
```
POST /api/agents/pricing/calculate/{ticket_id}
```

**Request Body (optional):**
```json
{
  "strategy": "balanced",
  "margin_override": 15.0
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "ticket_id": "uuid",
    "total_value": 1500000.00,
    "currency": "INR",
    "selected_strategy": "balanced",
    "line_items": [
      {
        "item_id": "uuid",
        "sku": "XLPE-33KV-3C-185",
        "quantity": 5000,
        "unit_price": 250.00,
        "material_cost": 1250000.00,
        "testing_cost": 125000.00,
        "delivery_cost": 75000.00,
        "margin_pct": 15.0,
        "total_price": 1450000.00,
        "price_bands": {
          "aggressive": 1377500.00,
          "balanced": 1450000.00,
          "conservative": 1595000.00
        }
      }
    ],
    "historical_comparison": {
      "similar_tenders": 5,
      "avg_unit_price": 245.00,
      "median_unit_price": 250.00,
      "price_position": "at_market"
    }
  },
  "message": "Pricing calculated successfully",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 2. Get Pricing Breakdown
```
GET /api/agents/pricing/breakdown/{ticket_id}
```

**Response:** Same as Calculate Pricing response with additional details

---

### 3. Apply Pricing Strategy
```
POST /api/agents/pricing/apply-strategy/{ticket_id}
```

**Request Body:**
```json
{
  "strategy": "aggressive"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "ticket_id": "uuid",
    "strategy_applied": "aggressive",
    "total_value": 1377500.00,
    "discount_pct": 5.0
  },
  "message": "Pricing strategy applied",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

## 🔍 Auditor Agent Endpoints

### 1. Validate RFP
```
POST /api/agents/auditor/validate/{ticket_id}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "ticket_id": "uuid",
    "validation_status": "VALIDATED",
    "checks": {
      "completeness": {
        "passed": true,
        "missing_items": [],
        "score": 100
      },
      "price_anomaly": {
        "passed": true,
        "outliers": [],
        "avg_deviation_pct": 2.5
      },
      "compliance": {
        "passed": true,
        "issues": [],
        "standards_met": ["IEC 60502-2", "IS 7098"]
      }
    },
    "flagged_issues": [],
    "recommendations": [
      "Consider adding warranty clause",
      "Delivery timeline is tight"
    ]
  },
  "message": "Validation completed",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 2. Get Audit Report
```
GET /api/agents/auditor/report/{ticket_id}
```

**Response:** Same as Validate response with full audit history

---

## 📊 Learning Agent Endpoints

### 1. Train Model
```
POST /api/agents/learning/train
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "training_completed": true,
    "outcomes_analyzed": 50,
    "segments_updated": 3,
    "improvements": {
      "spec_weights": {
        "government_transmission": {
          "voltage_weight": 0.22,
          "size_weight": 0.21,
          "insulation_weight": 0.19,
          "conductor_weight": 0.20,
          "standards_weight": 0.18
        }
      },
      "pricing_multipliers": {
        "aggressive": 0.93,
        "balanced": 1.00,
        "conservative": 1.12
      }
    }
  },
  "message": "Model training completed",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 2. Get Insights
```
GET /api/agents/learning/insights
```

**Query Parameters:**
- `segment` (optional): Filter by segment (e.g., "government_transmission")
- `period` (optional, default: "30d"): Time period (7d, 30d, 90d)

**Response:**
```json
{
  "status": "success",
  "data": {
    "win_rate": {
      "overall": 65.5,
      "by_segment": {
        "government_transmission": 72.0,
        "private_distribution": 58.0
      }
    },
    "avg_match_accuracy": 89.5,
    "pricing_performance": {
      "aggressive_wins": 35.0,
      "balanced_wins": 45.0,
      "conservative_wins": 20.0
    },
    "recommendations": [
      "Increase aggressive pricing for private clients",
      "Focus on voltage matching for government tenders"
    ]
  },
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 3. Record Feedback
```
POST /api/agents/learning/feedback/{ticket_id}
```

**Request Body:**
```json
{
  "outcome": "WON",
  "our_price": 1450000.00,
  "competitor_price": 1520000.00,
  "notes": "Won due to better specs match"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "feedback_recorded": true,
    "outcome_id": "uuid"
  },
  "message": "Feedback recorded for learning",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

## 📈 Analytics Endpoints

### 1. Dashboard Metrics
```
GET /api/analytics/dashboard
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "active_rfps": 45,
    "win_rate": 65.5,
    "avg_processing_time_hours": 4.2,
    "total_pipeline_value": 25000000.00,
    "currency": "INR",
    "recent_activity": [
      {
        "ticket_id": "uuid",
        "action": "status_changed",
        "from_status": "MATCHED",
        "to_status": "PRICED",
        "timestamp": "2025-12-07T09:30:00Z"
      }
    ]
  },
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 2. Performance Trends
```
GET /api/analytics/trends
```

**Query Parameters:**
- `period` (optional, default: "30d"): Time period
- `metric` (optional): Specific metric to trend

**Response:**
```json
{
  "status": "success",
  "data": {
    "trends": [
      {
        "date": "2025-12-01",
        "rfps_discovered": 15,
        "rfps_won": 8,
        "win_rate": 53.3,
        "avg_score": 75.0
      }
    ]
  },
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

## 🛍️ Product Endpoints

### 1. List Products
```
GET /api/products/list
```

**Query Parameters:**
- `category` (optional): Filter by category
- `voltage_kv` (optional): Filter by voltage
- `page` (optional): Page number
- `limit` (optional): Items per page

**Response:**
```json
{
  "status": "success",
  "data": {
    "products": [
      {
        "sku": "XLPE-33KV-3C-185",
        "product_name": "33kV 3C 185mm² XLPE Cable",
        "manufacturer": "Acme Cables",
        "category": "Power Cables",
        "voltage_kv": 33.0,
        "cores": 3,
        "area_sqmm": 185.0,
        "insulation_type": "XLPE",
        "conductor_material": "Copper",
        "base_unit_price": 250.00,
        "currency": "INR",
        "stock_status": "In Stock",
        "lead_time_days": 30
      }
    ],
    "pagination": {
      "total": 50,
      "page": 1,
      "limit": 20
    }
  },
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 2. Search Products
```
GET /api/products/search
```

**Query Parameters:**
- `q` (required): Search query
- `category` (optional): Filter by category

**Response:** Same format as List Products

---

### 3. Get Categories
```
GET /api/products/categories
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "categories": [
      {
        "name": "Power Cables",
        "count": 25
      },
      {
        "name": "Control Cables",
        "count": 15
      }
    ]
  },
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

## 🤝 Orchestrator Endpoints

### 1. Process Ticket
```
POST /api/orchestrator/process-ticket/{ticket_id}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "ticket_id": "uuid",
    "status": "ANALYZING",
    "workflow_started": true,
    "estimated_completion_minutes": 5
  },
  "message": "Processing started",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 2. Get Status
```
GET /api/orchestrator/status/{ticket_id}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "ticket_id": "uuid",
    "current_status": "MATCHED",
    "workflow_progress": {
      "sales_agent": "completed",
      "technical_agent": "completed",
      "pricing_agent": "in_progress",
      "auditor_agent": "pending"
    },
    "progress_pct": 60
  },
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### 3. Approve Ticket
```
POST /api/orchestrator/approve/{ticket_id}
```

**Request Body:**
```json
{
  "approver": "John Doe",
  "notes": "Approved for submission"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "ticket_id": "uuid",
    "status": "APPROVED",
    "approved_by": "John Doe",
    "approved_at": "2025-12-07T10:30:00Z"
  },
  "message": "Ticket approved",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

## ❌ Error Codes

| Code | Description |
|------|-------------|
| `VALIDATION_ERROR` | Request validation failed |
| `NOT_FOUND` | Resource not found |
| `UNAUTHORIZED` | Authentication required |
| `FORBIDDEN` | Insufficient permissions |
| `DUPLICATE_ENTRY` | Resource already exists |
| `PROCESSING_ERROR` | Agent processing failed |
| `DATABASE_ERROR` | Database operation failed |
| `EXTERNAL_API_ERROR` | External service call failed |

---

## 📝 Notes for Frontend Developer

1. **Always check `status` field** in response
2. **Use `timestamp` for caching** and "Last updated" displays
3. **Error handling**: Show `error.message` to user, log `error.details`
4. **Polling**: Use `/api/orchestrator/status/{ticket_id}` for progress updates
5. **Real-time**: WebSocket endpoint will be added later for live updates

---

**Maintained by:** Backend Team  
**Questions?** Post in #api-contract channel
