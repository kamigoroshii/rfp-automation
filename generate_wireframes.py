"""
Generate wireframes for SmartBid Control Tower
Creates 8 key screen wireframes as PNG images
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch
from pathlib import Path

# Create output directory
output_dir = Path("data/ppt_charts/wireframes")
output_dir.mkdir(parents=True, exist_ok=True)

# Wireframe colors
COLORS = {
    'bg': '#ffffff',
    'border': '#333333',
    'header': '#2c3e50',
    'sidebar': '#ecf0f1',
    'text': '#2c3e50',
    'light_gray': '#bdc3c7',
    'card': '#f8f9fa',
    'primary': '#3498db',
    'accent': '#e74c3c'
}

def draw_header(ax, title="SmartBid Control Tower"):
    """Draw standard header"""
    header = Rectangle((0, 9), 16, 1, facecolor=COLORS['header'], edgecolor=COLORS['border'], linewidth=2)
    ax.add_patch(header)
    ax.text(0.3, 9.5, "☰ " + title, fontsize=14, fontweight='bold', color='white', va='center')
    ax.text(15.5, 9.5, "👤", fontsize=12, color='white', va='center', ha='right')

def draw_sidebar(ax):
    """Draw navigation sidebar"""
    sidebar = Rectangle((0, 0), 2, 9, facecolor=COLORS['sidebar'], edgecolor=COLORS['border'], linewidth=2)
    ax.add_patch(sidebar)
    
    menu_items = [
        ("📊", "Dashboard", 8.2),
        ("📋", "RFPs", 7.5),
        ("📦", "Products", 6.8),
        ("📈", "Analytics", 6.1),
        ("🤖", "Co-Pilot", 5.4),
        ("⚙️", "Settings", 1.0)
    ]
    
    for icon, label, y in menu_items:
        ax.text(0.3, y, icon, fontsize=10, va='center')
        ax.text(0.7, y, label, fontsize=9, va='center', color=COLORS['text'])

def draw_card(ax, x, y, w, h, title, content_lines=None):
    """Draw a card component"""
    card = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                          facecolor=COLORS['card'], edgecolor=COLORS['border'],
                          linewidth=1.5)
    ax.add_patch(card)
    ax.text(x + 0.2, y + h - 0.3, title, fontsize=9, fontweight='bold', color=COLORS['text'])
    
    if content_lines:
        line_y = y + h - 0.7
        for line in content_lines:
            ax.text(x + 0.2, line_y, line, fontsize=7, color=COLORS['text'])
            line_y -= 0.25

# ============================================================================
# WIREFRAME 1: Dashboard
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_aspect('equal')

draw_header(ax, "SmartBid Control Tower - Dashboard")
draw_sidebar(ax)

# KPI Cards
kpi_cards = [
    ("Active RFPs", "24", 2.5),
    ("Win Rate", "32%", 5.5),
    ("Avg. Time", "2.5 days", 8.5),
    ("Pipeline", "₹580 Cr", 11.5)
]

for title, value, x in kpi_cards:
    card = FancyBboxPatch((x, 7.5), 2.5, 1.2, boxstyle="round,pad=0.05",
                          facecolor=COLORS['primary'], edgecolor=COLORS['border'],
                          linewidth=1.5, alpha=0.3)
    ax.add_patch(card)
    ax.text(x + 1.25, 8.3, value, fontsize=16, fontweight='bold', 
            color=COLORS['primary'], ha='center')
    ax.text(x + 1.25, 7.8, title, fontsize=8, color=COLORS['text'], ha='center')

# Recent RFPs Table
table_bg = Rectangle((2.5, 3), 13, 4, facecolor='white', 
                     edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(table_bg)
ax.text(2.7, 6.7, "Recent RFPs", fontsize=10, fontweight='bold')

# Table headers
headers = ["RFP ID", "Title", "Client", "Status", "Actions"]
for i, header in enumerate(headers):
    ax.text(2.7 + i * 2.5, 6.3, header, fontsize=8, fontweight='bold', color=COLORS['text'])

# Table rows (wireframe)
for row in range(5):
    y = 5.8 - row * 0.5
    for col in range(5):
        x = 2.7 + col * 2.5
        ax.plot([x, x + 2], [y, y], color=COLORS['light_gray'], linewidth=0.5)
        ax.text(x + 0.1, y - 0.15, "━━━", fontsize=6, color=COLORS['light_gray'])

# Charts placeholder
chart1 = Rectangle((2.5, 0.5), 6, 2.3, facecolor='white', 
                   edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(chart1)
ax.text(5.5, 2.5, "📊 Monthly Volume", fontsize=9, ha='center', fontweight='bold')
ax.plot([3, 4, 5, 6, 7, 8], [1.2, 1.5, 1.4, 1.8, 1.7, 2], 
        color=COLORS['primary'], linewidth=2, marker='o')

chart2 = Rectangle((9, 0.5), 6.5, 2.3, facecolor='white',
                   edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(chart2)
ax.text(12.25, 2.5, "📈 Win Rate Trend", fontsize=9, ha='center', fontweight='bold')
ax.bar([10, 11, 12, 13, 14], [1.2, 1.4, 1.5, 1.6, 1.8], width=0.6, 
       color=COLORS['accent'], alpha=0.5)

plt.tight_layout()
plt.savefig(output_dir / '01_dashboard.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Wireframe 1: Dashboard")

# ============================================================================
# WIREFRAME 2: RFP List View
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_aspect('equal')

draw_header(ax, "SmartBid Control Tower - RFP List")
draw_sidebar(ax)

# Filters bar
filters = Rectangle((2.5, 8.3), 13, 1, facecolor=COLORS['card'],
                    edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(filters)
ax.text(2.7, 8.8, "🔍 Search:", fontsize=8, va='center')
search_box = Rectangle((3.5, 8.6), 3, 0.4, facecolor='white',
                       edgecolor=COLORS['border'], linewidth=1)
ax.add_patch(search_box)

ax.text(7, 8.8, "Status:", fontsize=8, va='center')
dropdown = Rectangle((7.6, 8.6), 1.5, 0.4, facecolor='white',
                     edgecolor=COLORS['border'], linewidth=1)
ax.add_patch(dropdown)
ax.text(8.35, 8.8, "All ▼", fontsize=7, va='center', ha='center')

ax.text(9.5, 8.8, "Date Range:", fontsize=8, va='center')
date_box = Rectangle((10.4, 8.6), 2, 0.4, facecolor='white',
                     edgecolor=COLORS['border'], linewidth=1)
ax.add_patch(date_box)

# Add button
add_btn = FancyBboxPatch((14, 8.55), 1.3, 0.5, boxstyle="round,pad=0.02",
                         facecolor=COLORS['primary'], edgecolor=COLORS['border'],
                         linewidth=1)
ax.add_patch(add_btn)
ax.text(14.65, 8.8, "+ New RFP", fontsize=8, color='white', 
        ha='center', va='center', fontweight='bold')

# RFP Table
table = Rectangle((2.5, 1), 13, 7, facecolor='white',
                 edgecolor=COLORS['border'], linewidth=2)
ax.add_patch(table)

# Table headers
headers = ["✓", "RFP ID", "Title", "Client", "Deadline", "Status", "Score", "Actions"]
x_positions = [2.7, 3.2, 4.5, 8, 10.5, 12, 13.5, 14.5]
for header, x in zip(headers, x_positions):
    ax.text(x, 7.6, header, fontsize=8, fontweight='bold')
    
# Header underline
ax.plot([2.6, 15.3], [7.4, 7.4], color=COLORS['border'], linewidth=1.5)

# Table rows
for row in range(12):
    y = 7 - row * 0.5
    if row % 2 == 0:
        row_bg = Rectangle((2.6, y - 0.25), 12.7, 0.45, 
                          facecolor=COLORS['card'], alpha=0.3)
        ax.add_patch(row_bg)
    
    # Checkbox
    cb = Rectangle((2.75, y - 0.1), 0.15, 0.15, facecolor='white',
                   edgecolor=COLORS['border'], linewidth=0.5)
    ax.add_patch(cb)
    
    # Status badge
    status_colors = [COLORS['primary'], COLORS['accent'], '#27ae60', COLORS['light_gray']]
    status_color = status_colors[row % 4]
    badge = FancyBboxPatch((12, y - 0.12), 1.2, 0.2, boxstyle="round,pad=0.02",
                           facecolor=status_color, alpha=0.3,
                           edgecolor=status_color, linewidth=1)
    ax.add_patch(badge)
    
    # Action buttons
    for i, icon in enumerate(["👁", "✏", "🗑"]):
        ax.text(14.5 + i * 0.35, y, icon, fontsize=7)

# Pagination
ax.text(2.7, 0.5, "Showing 1-12 of 48", fontsize=7, color=COLORS['text'])
for i, page in enumerate(["← Prev", "1", "2", "3", "4", "Next →"]):
    ax.text(12 + i * 0.6, 0.5, page, fontsize=7, color=COLORS['primary'], ha='center')

plt.tight_layout()
plt.savefig(output_dir / '02_rfp_list.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Wireframe 2: RFP List View")

# ============================================================================
# WIREFRAME 3: RFP Detail Page
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_aspect('equal')

draw_header(ax, "SmartBid Control Tower - RFP Details")
draw_sidebar(ax)

# Breadcrumb
ax.text(2.7, 8.8, "Home > RFPs > RFP-2025-001", fontsize=7, color=COLORS['light_gray'])

# Title and status
ax.text(2.7, 8.4, "Supply of 11kV XLPE Cables", fontsize=12, fontweight='bold')
status_badge = FancyBboxPatch((9, 8.25), 1.5, 0.35, boxstyle="round,pad=0.05",
                              facecolor='#27ae60', alpha=0.3,
                              edgecolor='#27ae60', linewidth=1.5)
ax.add_patch(status_badge)
ax.text(9.75, 8.42, "COMPLETED", fontsize=8, color='#27ae60', 
        ha='center', va='center', fontweight='bold')

# Action buttons
actions = ["📄 Generate PDF", "✉️ Send", "✓ Approve"]
for i, action in enumerate(actions):
    btn = FancyBboxPatch((11 + i * 1.5, 8.25), 1.3, 0.35, boxstyle="round,pad=0.02",
                         facecolor=COLORS['primary'] if i == 2 else 'white',
                         edgecolor=COLORS['border'], linewidth=1)
    ax.add_patch(btn)
    ax.text(11.65 + i * 1.5, 8.42, action, fontsize=7, 
            color='white' if i == 2 else COLORS['text'],
            ha='center', va='center')

# Tabs
tabs = ["Overview", "Specifications", "Matches", "Pricing", "Audit"]
for i, tab in enumerate(tabs):
    tab_bg = Rectangle((2.5 + i * 2.6, 7.7), 2.5, 0.4,
                       facecolor=COLORS['primary'] if i == 0 else COLORS['card'],
                       edgecolor=COLORS['border'], linewidth=1)
    ax.add_patch(tab_bg)
    ax.text(3.75 + i * 2.6, 7.9, tab, fontsize=8, ha='center', va='center',
            color='white' if i == 0 else COLORS['text'], fontweight='bold')

# Content area - two columns
left_col = Rectangle((2.5, 3.5), 6.3, 4, facecolor='white',
                     edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(left_col)
ax.text(2.8, 7.2, "RFP Information", fontsize=9, fontweight='bold')

info_items = [
    ("RFP ID:", "RFP-2025-001"),
    ("Source:", "https://example.com/tender"),
    ("Client:", "Maharashtra State Power"),
    ("Deadline:", "2025-12-15"),
    ("Go/No-Go Score:", "85 (High Priority)"),
]

y_pos = 6.8
for label, value in info_items:
    ax.text(2.8, y_pos, label, fontsize=7, color=COLORS['light_gray'])
    ax.text(4.5, y_pos, value, fontsize=7, color=COLORS['text'])
    y_pos -= 0.3

ax.text(2.8, 5.8, "Scope:", fontsize=7, color=COLORS['light_gray'])
scope_box = Rectangle((2.8, 4), 5.5, 1.5, facecolor=COLORS['card'],
                      edgecolor=COLORS['border'], linewidth=1)
ax.add_patch(scope_box)
ax.text(3, 5.2, "Supply of 5000m of 11kV XLPE cables\nwith 3 core aluminum conductor...",
        fontsize=7, color=COLORS['text'], va='top')

# Right column - Matches
right_col = Rectangle((9.3, 3.5), 6.2, 4, facecolor='white',
                      edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(right_col)
ax.text(9.6, 7.2, "Product Matches (Top 3)", fontsize=9, fontweight='bold')

for i, (sku, score, color) in enumerate([
    ("XLPE-11KV-240-CU", "75%", '#27ae60'),
    ("XLPE-11KV-185-CU", "68%", '#f39c12'),
    ("XLPE-11KV-300-CU", "65%", '#e67e22')
]):
    match_card = FancyBboxPatch((9.6, 6.5 - i * 1.1), 5.5, 0.9,
                                boxstyle="round,pad=0.05",
                                facecolor=COLORS['card'],
                                edgecolor=COLORS['border'], linewidth=1)
    ax.add_patch(match_card)
    
    ax.text(9.8, 7.1 - i * 1.1, sku, fontsize=8, fontweight='bold')
    ax.text(9.8, 6.8 - i * 1.1, "11kV XLPE Insulated Cable", fontsize=7,
            color=COLORS['light_gray'])
    
    score_badge = FancyBboxPatch((14.2, 6.85 - i * 1.1), 0.7, 0.3,
                                 boxstyle="round,pad=0.02",
                                 facecolor=color, alpha=0.3,
                                 edgecolor=color, linewidth=1)
    ax.add_patch(score_badge)
    ax.text(14.55, 7 - i * 1.1, score, fontsize=8, color=color,
            ha='center', va='center', fontweight='bold')

# Bottom section - Pricing summary
pricing = Rectangle((2.5, 0.5), 13, 2.8, facecolor='white',
                    edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(pricing)
ax.text(2.8, 3, "Pricing Breakdown", fontsize=9, fontweight='bold')

price_items = [
    ("Material Cost:", "₹57,75,000"),
    ("Testing Cost:", "₹4,04,250"),
    ("Delivery:", "₹5,000"),
    ("Urgency Adjustment:", "₹8,66,250"),
]

x_pos = 2.8
for label, value in price_items:
    ax.text(x_pos, 2.5, label, fontsize=7, color=COLORS['light_gray'])
    ax.text(x_pos, 2.2, value, fontsize=8, color=COLORS['text'], fontweight='bold')
    x_pos += 3.2

ax.plot([2.7, 15.2], [1.8, 1.8], color=COLORS['border'], linewidth=1)
ax.text(12, 1.4, "Total Estimate:", fontsize=9, fontweight='bold')
ax.text(14.5, 1.4, "₹70,50,500", fontsize=11, color=COLORS['primary'],
        fontweight='bold', ha='right')

plt.tight_layout()
plt.savefig(output_dir / '03_rfp_detail.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Wireframe 3: RFP Detail Page")

# ============================================================================
# WIREFRAME 4: Submit RFP Form
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_aspect('equal')

draw_header(ax, "SmartBid Control Tower - Submit New RFP")
draw_sidebar(ax)

# Form container
form = Rectangle((3.5, 1.5), 11, 7.2, facecolor='white',
                edgecolor=COLORS['border'], linewidth=2)
ax.add_patch(form)

ax.text(8.5, 8.3, "Submit New RFP", fontsize=12, fontweight='bold', ha='center')
ax.text(8.5, 7.9, "Choose your submission method", fontsize=8, 
        color=COLORS['light_gray'], ha='center')

# Method tabs
method_tabs = ["URL", "Upload PDF", "Manual Entry"]
for i, method in enumerate(method_tabs):
    tab = FancyBboxPatch((4.5 + i * 3, 7.3), 2.5, 0.4, boxstyle="round,pad=0.02",
                         facecolor=COLORS['primary'] if i == 0 else COLORS['card'],
                         edgecolor=COLORS['border'], linewidth=1.5)
    ax.add_patch(tab)
    ax.text(5.75 + i * 3, 7.5, method, fontsize=8, ha='center', va='center',
            color='white' if i == 0 else COLORS['text'], fontweight='bold')

# URL input section
ax.text(4, 6.7, "RFP Source URL", fontsize=9, fontweight='bold')
url_input = Rectangle((4, 6.1), 9.5, 0.45, facecolor=COLORS['card'],
                      edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(url_input)
ax.text(4.2, 6.32, "https://example.com/tender/rfp-2025-...", fontsize=7,
        color=COLORS['light_gray'], va='center')

scrape_btn = FancyBboxPatch((11, 5.5), 2.5, 0.4, boxstyle="round,pad=0.02",
                            facecolor=COLORS['primary'],
                            edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(scrape_btn)
ax.text(12.25, 5.7, "🔍 Scrape & Process", fontsize=8, color='white',
        ha='center', va='center', fontweight='bold')

# OR divider
ax.plot([4, 13.5], [5.1, 5.1], color=COLORS['light_gray'], linewidth=1)
ax.text(8.5, 5.1, " OR ", fontsize=8, color=COLORS['light_gray'],
        ha='center', va='center', bbox=dict(facecolor='white', edgecolor='none'))

# Additional fields
fields = [
    ("RFP Title", 4.5),
    ("Client Name", 3.7),
    ("Deadline", 2.9),
    ("Quantity (meters)", 2.1),
]

for label, y in fields:
    ax.text(4, y + 0.3, label, fontsize=8, color=COLORS['text'])
    field_box = Rectangle((4, y), 4.5, 0.35, facecolor=COLORS['card'],
                         edgecolor=COLORS['border'], linewidth=1)
    ax.add_patch(field_box)

# Testing requirements
ax.text(9, 4.8, "Testing Requirements", fontsize=8, color=COLORS['text'])
tests = ["Type Test", "Routine Test", "Partial Discharge"]
for i, test in enumerate(tests):
    cb = Rectangle((9, 4.3 - i * 0.3), 0.15, 0.15, facecolor='white',
                   edgecolor=COLORS['border'], linewidth=1)
    ax.add_patch(cb)
    ax.text(9.3, 4.38 - i * 0.3, test, fontsize=7, va='center')

# Scope textarea
ax.text(9, 3.3, "Scope of Supply", fontsize=8, color=COLORS['text'])
scope_area = Rectangle((9, 2.1), 4.5, 1.1, facecolor=COLORS['card'],
                       edgecolor=COLORS['border'], linewidth=1)
ax.add_patch(scope_area)
ax.text(9.2, 3, "Enter detailed scope...", fontsize=7,
        color=COLORS['light_gray'], va='top')

# Action buttons
cancel_btn = FancyBboxPatch((9, 1.7), 2, 0.4, boxstyle="round,pad=0.02",
                            facecolor='white',
                            edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(cancel_btn)
ax.text(10, 1.9, "Cancel", fontsize=8, color=COLORS['text'],
        ha='center', va='center')

submit_btn = FancyBboxPatch((11.5, 1.7), 2, 0.4, boxstyle="round,pad=0.02",
                            facecolor=COLORS['primary'],
                            edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(submit_btn)
ax.text(12.5, 1.9, "Submit RFP", fontsize=8, color='white',
        ha='center', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '04_submit_rfp.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Wireframe 4: Submit RFP Form")

# ============================================================================
# WIREFRAME 5: Product Matching View
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_aspect('equal')

draw_header(ax, "SmartBid Control Tower - Product Matching")
draw_sidebar(ax)

ax.text(2.7, 8.6, "Product Matching Results", fontsize=11, fontweight='bold')
ax.text(2.7, 8.25, "RFP: Supply of 11kV XLPE Cables - 3 matches found", 
        fontsize=8, color=COLORS['light_gray'])

# Match cards (Top 3)
match_colors = ['#27ae60', '#f39c12', '#e67e22']
match_scores = ['85%', '72%', '68%']
match_skus = [
    ('XLPE-11KV-240-CU', '11kV XLPE Insulated Copper Cable 240 sq.mm'),
    ('XLPE-11KV-185-CU', '11kV XLPE Insulated Copper Cable 185 sq.mm'),
    ('XLPE-11KV-300-CU', '11kV XLPE Insulated Copper Cable 300 sq.mm')
]

for i, ((sku, desc), score, color) in enumerate(zip(match_skus, match_scores, match_colors)):
    y_base = 7.3 - i * 2.2
    
    # Match card
    card = FancyBboxPatch((2.5, y_base), 13, 2, boxstyle="round,pad=0.1",
                          facecolor='white',
                          edgecolor=color, linewidth=2)
    ax.add_patch(card)
    
    # Rank badge
    rank_badge = FancyBboxPatch((2.7, y_base + 1.6), 0.5, 0.3,
                                boxstyle="round,pad=0.02",
                                facecolor=color,
                                edgecolor='white', linewidth=1)
    ax.add_patch(rank_badge)
    ax.text(2.95, y_base + 1.75, f"#{i+1}", fontsize=9, color='white',
            ha='center', va='center', fontweight='bold')
    
    # SKU and description
    ax.text(3.4, y_base + 1.75, sku, fontsize=10, fontweight='bold')
    ax.text(3.4, y_base + 1.45, desc, fontsize=8, color=COLORS['light_gray'])
    
    # Match score
    score_circle = plt.Circle((14.5, y_base + 1.6), 0.35, 
                             facecolor=color, alpha=0.2,
                             edgecolor=color, linewidth=2)
    ax.add_patch(score_circle)
    ax.text(14.5, y_base + 1.6, score, fontsize=10, color=color,
            ha='center', va='center', fontweight='bold')
    ax.text(14.5, y_base + 1.15, "Match Score", fontsize=6,
            color=COLORS['light_gray'], ha='center')
    
    # Specification alignment
    specs = [
        ("Voltage", "Exact"),
        ("Conductor Size", "Exact" if i == 0 else "Partial"),
        ("Material", "Partial"),
        ("Insulation", "Exact")
    ]
    
    x_pos = 2.8
    for spec_name, alignment in specs:
        ax.text(x_pos, y_base + 0.85, spec_name, fontsize=7,
                color=COLORS['light_gray'])
        
        align_color = '#27ae60' if alignment == 'Exact' else '#f39c12'
        align_badge = FancyBboxPatch((x_pos, y_base + 0.4), 1.2, 0.25,
                                     boxstyle="round,pad=0.02",
                                     facecolor=align_color, alpha=0.2,
                                     edgecolor=align_color, linewidth=1)
        ax.add_patch(align_badge)
        ax.text(x_pos + 0.6, y_base + 0.52, f"✓ {alignment}", fontsize=6,
                color=align_color, ha='center', va='center')
        
        x_pos += 2.8
    
    # Select button
    select_btn = FancyBboxPatch((12.5, y_base + 0.15), 1.3, 0.35,
                                boxstyle="round,pad=0.02",
                                facecolor=COLORS['primary'] if i == 0 else 'white',
                                edgecolor=COLORS['border'], linewidth=1.5)
    ax.add_patch(select_btn)
    ax.text(13.15, y_base + 0.32, 
            "Selected ✓" if i == 0 else "Select",
            fontsize=7, 
            color='white' if i == 0 else COLORS['text'],
            ha='center', va='center', fontweight='bold')

# Action buttons at bottom
proceed_btn = FancyBboxPatch((12, 0.8), 3.5, 0.5, boxstyle="round,pad=0.02",
                             facecolor=COLORS['primary'],
                             edgecolor=COLORS['border'], linewidth=2)
ax.add_patch(proceed_btn)
ax.text(13.75, 1.05, "Proceed to Pricing →", fontsize=9, color='white',
        ha='center', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '05_product_matching.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Wireframe 5: Product Matching View")

# ============================================================================
# WIREFRAME 6: Pricing Breakdown
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_aspect('equal')

draw_header(ax, "SmartBid Control Tower - Pricing")
draw_sidebar(ax)

ax.text(2.7, 8.6, "Pricing Breakdown", fontsize=11, fontweight='bold')
ax.text(2.7, 8.25, "Selected: XLPE-11KV-240-CU | Quantity: 5000m", 
        fontsize=8, color=COLORS['light_gray'])

# Price band selector
ax.text(2.7, 7.8, "Select Pricing Strategy:", fontsize=9, fontweight='bold')
bands = [
    ("Aggressive", "95% of market", "#e74c3c"),
    ("Balanced", "Market rate", "#3498db"),
    ("Conservative", "110% premium", "#f39c12")
]

for i, (band, desc, color) in enumerate(bands):
    band_card = FancyBboxPatch((2.7 + i * 4.3, 6.9), 4, 0.7,
                               boxstyle="round,pad=0.05",
                               facecolor=color if i == 1 else 'white',
                               alpha=0.3 if i == 1 else 1,
                               edgecolor=color, linewidth=2)
    ax.add_patch(band_card)
    
    if i == 1:
        check = plt.Circle((3, 7.25), 0.15, facecolor=color,
                          edgecolor='white', linewidth=2)
        ax.add_patch(check)
        ax.text(3, 7.25, "✓", fontsize=10, color='white',
                ha='center', va='center', fontweight='bold')
    
    ax.text(3.3 + i * 4.3, 7.35, band, fontsize=9, fontweight='bold',
            color='white' if i == 1 else color)
    ax.text(3.3 + i * 4.3, 7.05, desc, fontsize=7,
            color='white' if i == 1 else COLORS['light_gray'])

# Cost breakdown table
table = Rectangle((2.5, 2.5), 13, 4.2, facecolor='white',
                 edgecolor=COLORS['border'], linewidth=2)
ax.add_patch(table)

ax.text(2.8, 6.4, "Cost Components", fontsize=9, fontweight='bold')

# Table header
headers = ["Component", "Unit Price", "Quantity", "Subtotal"]
x_positions = [2.8, 7, 10, 12.5]
for header, x in zip(headers, x_positions):
    ax.text(x, 5.9, header, fontsize=8, fontweight='bold', color=COLORS['text'])

ax.plot([2.7, 15.2], [5.7, 5.7], color=COLORS['border'], linewidth=1.5)

# Cost rows
costs = [
    ("Material Cost", "₹1,155", "5,000m", "₹57,75,000"),
    ("Type Testing", "₹2,500", "1 set", "₹2,50,000"),
    ("Routine Testing", "₹800", "per km", "₹1,54,250"),
    ("Delivery & Handling", "₹1,000", "5 trips", "₹5,000"),
    ("Urgency Adjustment (15%)", "-", "-", "₹8,66,250"),
]

y_pos = 5.3
for component, unit, qty, subtotal in costs:
    if y_pos != 5.3 and (y_pos - 5.3) / 0.5 % 2 == 0:
        row_bg = Rectangle((2.7, y_pos - 0.2), 12.5, 0.4,
                          facecolor=COLORS['card'], alpha=0.3)
        ax.add_patch(row_bg)
    
    ax.text(2.8, y_pos, component, fontsize=7, color=COLORS['text'])
    ax.text(7, y_pos, unit, fontsize=7, color=COLORS['light_gray'])
    ax.text(10, y_pos, qty, fontsize=7, color=COLORS['light_gray'])
    ax.text(13.5, y_pos, subtotal, fontsize=7, color=COLORS['text'], ha='right')
    y_pos -= 0.5

# Total section
ax.plot([2.7, 15.2], [2.7, 2.7], color=COLORS['border'], linewidth=2)
ax.text(11, 2.4, "Total Estimate:", fontsize=10, fontweight='bold')
ax.text(13.5, 2.4, "₹70,50,500", fontsize=12, color=COLORS['primary'],
        fontweight='bold', ha='right')

# Historical comparison
hist_box = Rectangle((2.5, 0.8), 6, 1.5, facecolor=COLORS['card'],
                     edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(hist_box)
ax.text(2.8, 2.1, "📊 Historical Comparison", fontsize=8, fontweight='bold')
ax.text(2.8, 1.8, "Similar tenders (last 12 months)", fontsize=7,
        color=COLORS['light_gray'])
ax.text(2.8, 1.5, "Median Price: ₹68,50,000", fontsize=7)
ax.text(2.8, 1.2, "Your Price: ₹70,50,500 (2.9% above median)", fontsize=7,
        color='#f39c12')

# Margin analysis
margin_box = Rectangle((9, 0.8), 6.5, 1.5, facecolor=COLORS['card'],
                       edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(margin_box)
ax.text(9.3, 2.1, "💰 Margin Analysis", fontsize=8, fontweight='bold')
ax.text(9.3, 1.8, "Base Margin: 15%", fontsize=7)
ax.text(9.3, 1.5, "Win Probability: 72%", fontsize=7, color='#27ae60')
ax.text(9.3, 1.2, "Recommended: Proceed with Balanced pricing", fontsize=7,
        color=COLORS['primary'], fontweight='bold')

# Action buttons
save_btn = FancyBboxPatch((2.5, 0.3), 2, 0.4, boxstyle="round,pad=0.02",
                          facecolor='white',
                          edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(save_btn)
ax.text(3.5, 0.5, "Save Draft", fontsize=8, color=COLORS['text'],
        ha='center', va='center')

generate_btn = FancyBboxPatch((12.5, 0.3), 3, 0.4, boxstyle="round,pad=0.02",
                              facecolor=COLORS['primary'],
                              edgecolor=COLORS['border'], linewidth=2)
ax.add_patch(generate_btn)
ax.text(14, 0.5, "Generate Proposal →", fontsize=9, color='white',
        ha='center', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '06_pricing_breakdown.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Wireframe 6: Pricing Breakdown")

# ============================================================================
# WIREFRAME 7: Analytics Dashboard
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_aspect('equal')

draw_header(ax, "SmartBid Control Tower - Analytics")
draw_sidebar(ax)

ax.text(2.7, 8.6, "Analytics Dashboard", fontsize=11, fontweight='bold')

# Date range filter
date_filter = FancyBboxPatch((12, 8.4), 3.5, 0.4, boxstyle="round,pad=0.02",
                             facecolor='white',
                             edgecolor=COLORS['border'], linewidth=1)
ax.add_patch(date_filter)
ax.text(13.75, 8.6, "📅 Last 90 Days ▼", fontsize=8,
        ha='center', va='center')

# KPI Cards Row 1
kpis_row1 = [
    ("Win Rate", "32%", "+8%", "#27ae60", 2.5),
    ("Avg Response Time", "2.5 days", "-4.5 days", "#27ae60", 5.8),
    ("RFPs Processed", "156", "+120%", "#27ae60", 9.1),
    ("Pipeline Value", "₹580 Cr", "+₹350 Cr", "#3498db", 12.4)
]

for title, value, change, color, x in kpis_row1:
    card = FancyBboxPatch((x, 7.3), 3, 1.1, boxstyle="round,pad=0.05",
                          facecolor='white',
                          edgecolor=COLORS['border'], linewidth=1.5)
    ax.add_patch(card)
    
    ax.text(x + 1.5, 8.15, value, fontsize=13, fontweight='bold',
            color=color, ha='center')
    ax.text(x + 1.5, 7.85, title, fontsize=7, color=COLORS['light_gray'],
            ha='center')
    ax.text(x + 1.5, 7.5, change, fontsize=7, color=color,
            ha='center', fontweight='bold')

# Chart 1 - Win Rate Trend
chart1 = Rectangle((2.5, 4.3), 6.3, 2.8, facecolor='white',
                   edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(chart1)
ax.text(2.8, 6.9, "📈 Win Rate Trend", fontsize=9, fontweight='bold')

months = ['J', 'F', 'M', 'A', 'M', 'J']
values = [18, 20, 24, 28, 30, 32]
x_chart = [3 + i * 0.9 for i in range(6)]
ax.plot(x_chart, [4.5 + v * 0.065 for v in values],
        color=COLORS['primary'], linewidth=2.5, marker='o', markersize=6)
ax.fill_between(x_chart, 4.5, [4.5 + v * 0.065 for v in values],
                alpha=0.2, color=COLORS['primary'])

for i, (x, v) in enumerate(zip(x_chart, values)):
    ax.text(x, 4.3, months[i], fontsize=7, ha='center',
            color=COLORS['light_gray'])

# Chart 2 - RFP Status Distribution
chart2 = Rectangle((9.2, 4.3), 6.3, 2.8, facecolor='white',
                   edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(chart2)
ax.text(9.5, 6.9, "📊 RFP Status Distribution", fontsize=9, fontweight='bold')

# Donut chart representation
center = (12.3, 5.5)
radius = 0.8
statuses = [
    ("Completed", 45, "#27ae60"),
    ("Processing", 30, "#3498db"),
    ("New", 15, "#f39c12"),
    ("Failed", 10, "#e74c3c")
]

start_angle = 90
for status, percentage, color in statuses:
    angle = percentage * 3.6
    wedge = mpatches.Wedge(center, radius, start_angle, start_angle + angle,
                           facecolor=color, alpha=0.7, edgecolor='white',
                           linewidth=2)
    ax.add_patch(wedge)
    start_angle += angle

# Inner circle for donut effect
inner_circle = plt.Circle(center, radius * 0.6, facecolor='white')
ax.add_patch(inner_circle)

# Legend
legend_y = 6.5
for status, percentage, color in statuses:
    legend_box = Rectangle((9.5, legend_y), 0.2, 0.15, facecolor=color, alpha=0.7)
    ax.add_patch(legend_box)
    ax.text(9.8, legend_y + 0.075, f"{status} ({percentage}%)", fontsize=7,
            va='center')
    legend_y -= 0.25

# Chart 3 - Processing Time Distribution
chart3 = Rectangle((2.5, 0.8), 6.3, 3.3, facecolor='white',
                   edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(chart3)
ax.text(2.8, 3.9, "⏱️ Processing Time Distribution", fontsize=9, fontweight='bold')

time_buckets = ['<1d', '1-2d', '2-3d', '3-5d', '>5d']
counts = [20, 45, 60, 25, 6]
x_bars = [3 + i * 1 for i in range(5)]
bar_heights = [c * 0.035 for c in counts]

for x, h, c in zip(x_bars, bar_heights, counts):
    bar = Rectangle((x - 0.3, 1.2), 0.6, h, facecolor=COLORS['primary'], alpha=0.7)
    ax.add_patch(bar)
    ax.text(x, 1.2 + h + 0.1, str(c), fontsize=7, ha='center')

for i, label in enumerate(time_buckets):
    ax.text(x_bars[i], 1.0, label, fontsize=7, ha='center',
            color=COLORS['light_gray'])

# Chart 4 - Top Clients
chart4 = Rectangle((9.2, 0.8), 6.3, 3.3, facecolor='white',
                   edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(chart4)
ax.text(9.5, 3.9, "🏢 Top Clients by Value", fontsize=9, fontweight='bold')

clients = [
    ("Maharashtra State", "₹180 Cr", 0.9),
    ("Delhi Metro Rail", "₹145 Cr", 0.75),
    ("NTPC Limited", "₹98 Cr", 0.5),
    ("Indian Railways", "₹87 Cr", 0.45),
]

y_client = 3.4
for client, value, bar_width in clients:
    ax.text(9.5, y_client, client, fontsize=7, color=COLORS['text'])
    ax.text(15, y_client, value, fontsize=7, color=COLORS['text'],
            ha='right', fontweight='bold')
    
    bar_bg = Rectangle((9.5, y_client - 0.2), 5, 0.15,
                       facecolor=COLORS['card'])
    ax.add_patch(bar_bg)
    bar_fill = Rectangle((9.5, y_client - 0.2), 5 * bar_width, 0.15,
                          facecolor=COLORS['primary'], alpha=0.6)
    ax.add_patch(bar_fill)
    
    y_client -= 0.6

plt.tight_layout()
plt.savefig(output_dir / '07_analytics.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Wireframe 7: Analytics Dashboard")

# ============================================================================
# WIREFRAME 8: Bid Co-Pilot (RAG Chat)
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_aspect('equal')

draw_header(ax, "SmartBid Control Tower - Bid Co-Pilot")
draw_sidebar(ax)

# Main content area with RFP on left, chat on right
rfp_panel = Rectangle((2.5, 1), 5.5, 7.7, facecolor='white',
                      edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(rfp_panel)

ax.text(2.8, 8.4, "Current RFP Context", fontsize=9, fontweight='bold')
ax.text(2.8, 8.1, "RFP-2025-001", fontsize=8, color=COLORS['primary'])
ax.text(2.8, 7.8, "Supply of 11kV XLPE Cables", fontsize=8)

# RFP summary
summary_box = Rectangle((2.8, 6.5), 4.9, 1.2, facecolor=COLORS['card'],
                        edgecolor=COLORS['border'], linewidth=1)
ax.add_patch(summary_box)
ax.text(3, 7.5, "Client: Maharashtra State Power", fontsize=7)
ax.text(3, 7.2, "Deadline: 2025-12-15", fontsize=7)
ax.text(3, 6.9, "Quantity: 5000m", fontsize=7)
ax.text(3, 6.6, "Status: Processing", fontsize=7, color=COLORS['primary'])

# Quick actions
ax.text(2.8, 6.1, "Quick Actions", fontsize=8, fontweight='bold')
actions = ["📄 View Full RFP", "🔍 Similar Tenders", "💰 Pricing History"]
for i, action in enumerate(actions):
    action_btn = FancyBboxPatch((2.8, 5.3 - i * 0.5), 4.9, 0.35,
                                boxstyle="round,pad=0.02",
                                facecolor='white',
                                edgecolor=COLORS['border'], linewidth=1)
    ax.add_patch(action_btn)
    ax.text(3.1, 5.48 - i * 0.5, action, fontsize=7, va='center')

# Suggested questions
ax.text(2.8, 3.5, "Suggested Questions", fontsize=8, fontweight='bold')
suggestions = [
    "What's the recommended SKU?",
    "Show me pricing breakdown",
    "What tests are required?"
]
for i, suggestion in enumerate(suggestions):
    sugg_chip = FancyBboxPatch((2.8, 2.9 - i * 0.45), 4.9, 0.3,
                               boxstyle="round,pad=0.02",
                               facecolor=COLORS['primary'], alpha=0.1,
                               edgecolor=COLORS['primary'], linewidth=1)
    ax.add_patch(sugg_chip)
    ax.text(3.1, 3.05 - i * 0.45, suggestion, fontsize=7, va='center',
            color=COLORS['primary'])

# Chat panel
chat_panel = Rectangle((8.5, 1), 7, 7.7, facecolor='white',
                       edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(chat_panel)

ax.text(8.8, 8.4, "🤖 Bid Co-Pilot", fontsize=10, fontweight='bold')
ax.text(14.8, 8.4, "🔄", fontsize=9, ha='right')

# Chat messages
messages = [
    ("user", "What's the best matching product for this RFP?", 7.5),
    ("bot", "Based on the specifications, I recommend XLPE-11KV-240-CU with 75% match score.\n\nKey alignments:\n✓ Voltage: 11kV (exact match)\n✓ Conductor size: 240 sq.mm (exact)\n✓ Insulation: XLPE (exact match)", 5.8),
    ("user", "Show me the pricing for this product", 4.8),
    ("bot", "Here's the pricing breakdown:\n\nMaterial: ₹57,75,000\nTesting: ₹4,04,250\nDelivery: ₹5,000\nTotal: ₹70,50,500\n\nThis is 2.9% above historical median.", 3.2),
]

for sender, text, y in messages:
    if sender == "user":
        # User message (right aligned, blue)
        msg_width = 5
        msg_box = FancyBboxPatch((14.7 - msg_width, y - 0.1), msg_width, 0.6,
                                 boxstyle="round,pad=0.05",
                                 facecolor=COLORS['primary'], alpha=0.2,
                                 edgecolor=COLORS['primary'], linewidth=1)
        ax.add_patch(msg_box)
        ax.text(14.5, y + 0.2, text, fontsize=7, ha='right', va='top',
                color=COLORS['text'], wrap=True)
        ax.text(14.7, y - 0.3, "You", fontsize=6, ha='right',
                color=COLORS['light_gray'])
    else:
        # Bot message (left aligned, gray)
        msg_width = 6.2
        msg_box = FancyBboxPatch((8.7, y - 0.1), msg_width, 1.3,
                                 boxstyle="round,pad=0.05",
                                 facecolor=COLORS['card'],
                                 edgecolor=COLORS['border'], linewidth=1)
        ax.add_patch(msg_box)
        ax.text(8.9, y + 1.1, text, fontsize=7, ha='left', va='top',
                color=COLORS['text'])
        ax.text(8.7, y - 0.3, "Co-Pilot", fontsize=6,
                color=COLORS['primary'])

# Input box
input_box = Rectangle((8.7, 1.2), 6.3, 0.45, facecolor=COLORS['card'],
                      edgecolor=COLORS['border'], linewidth=1.5)
ax.add_patch(input_box)
ax.text(8.9, 1.42, "Ask me anything about this RFP...", fontsize=7,
        color=COLORS['light_gray'], va='center')

send_btn = FancyBboxPatch((14.5, 1.25), 0.4, 0.35, boxstyle="round,pad=0.02",
                          facecolor=COLORS['primary'],
                          edgecolor=COLORS['border'], linewidth=1)
ax.add_patch(send_btn)
ax.text(14.7, 1.42, "➤", fontsize=10, color='white',
        ha='center', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '08_bid_copilot.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Wireframe 8: Bid Co-Pilot (RAG Chat)")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*70)
print("✅ ALL 8 WIREFRAMES GENERATED SUCCESSFULLY!")
print("="*70)
print(f"\n📁 Location: {output_dir.absolute()}\n")
print("Generated wireframes:")
print("  1. 01_dashboard.png - Main dashboard with KPIs & charts")
print("  2. 02_rfp_list.png - RFP list with filters & actions")
print("  3. 03_rfp_detail.png - Detailed RFP view with tabs")
print("  4. 04_submit_rfp.png - RFP submission form")
print("  5. 05_product_matching.png - Product matching results (Top 3)")
print("  6. 06_pricing_breakdown.png - Detailed pricing view")
print("  7. 07_analytics.png - Analytics dashboard with charts")
print("  8. 08_bid_copilot.png - RAG chat interface")
print("\n🎨 Wireframe Features:")
print("  ✅ Clean, professional layout structure")
print("  ✅ Standard header + sidebar navigation")
print("  ✅ Component hierarchy clearly shown")
print("  ✅ Interactive elements indicated (buttons, forms, filters)")
print("  ✅ Information density appropriate for each screen")
print("  ✅ Consistent design patterns across all screens")
print("  ✅ High-resolution 300 DPI for presentations")
print("\n💡 Usage:")
print("  - Perfect for stakeholder presentations")
print("  - Use as development reference")
print("  - Include in project documentation")
print("  - Guide for UI/UX implementation")
print("="*70)
