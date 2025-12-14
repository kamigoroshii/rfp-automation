"""
Generate enhanced waterfall chart showing Market Opportunity & SmartBid Revenue Impact
Creates detailed waterfall chart with cumulative values at each step
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Create output directory
output_dir = Path("data/ppt_charts")
output_dir.mkdir(parents=True, exist_ok=True)

# Set dark theme
plt.style.use('dark_background')
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['xtick.labelsize'] = 9.5
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['figure.facecolor'] = '#1e1e1e'
plt.rcParams['axes.facecolor'] = '#2d2d2d'

# ============================================================================
# Waterfall Chart – Market Opportunity & SmartBid Revenue Impact
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 9))

# Data
categories = [
    'Total\nMarket',
    'Lost: <10%\nExplored',
    'Lost:\nAnalysis Gap',
    "Today's\nCaptured\nValue",
    'SmartBid\nRecovery',
    'Ops\nSavings',
    'Final Value\nRealized'
]

# Values (in ₹ Crores)
# Format: [start, loss1, loss2, milestone, gain1, gain2, end]
values = [2400, -2160, -120, 0, 1200, 3, 0]

# Calculate cumulative values
cumulative = [0]  # Starting positions
current = 2400

for i in range(1, len(values)):
    if categories[i] == "Today's\nCaptured\nValue":
        cumulative.append(current)
        # Don't change current, it stays at 120
    elif categories[i] == 'Final Value\nRealized':
        cumulative.append(current)
    else:
        cumulative.append(current)
        current += values[i]

# Final cumulative values to display
display_values = [2400, 240, 120, 120, 1320, 1323, 1323]

# Color scheme
colors = []
for i, cat in enumerate(categories):
    if cat == 'Total\nMarket':
        colors.append('#3498db')  # Blue for start
    elif 'Lost' in cat:
        colors.append('#e74c3c')  # Red for losses
    elif "Today's" in cat:
        colors.append('#7f8c8d')  # Gray for current state
    elif 'SmartBid' in cat:
        colors.append('#27ae60')  # Bright green for SmartBid
    elif 'Ops' in cat:
        colors.append('#52b788')  # Light green for ops savings
    elif 'Final' in cat:
        colors.append('#27ae60')  # Bright green for final
    else:
        colors.append('#2ecc71')

# Create bars
x = np.arange(len(categories))
bars = []

for i, (cat, val, cum, disp_val) in enumerate(zip(categories, values, cumulative, display_values)):
    if i == 0:  # First bar - Total Market
        bar = ax.bar(i, val, color=colors[i], alpha=0.95, 
                    edgecolor='white', linewidth=2, width=0.7)
    elif cat == "Today's\nCaptured\nValue":  # Milestone bar
        bar = ax.bar(i, disp_val, color=colors[i], alpha=0.95,
                    edgecolor='white', linewidth=2, width=0.7)
    elif cat == 'Final Value\nRealized':  # Final bar
        bar = ax.bar(i, disp_val, color=colors[i], alpha=0.95,
                    edgecolor='white', linewidth=2, width=0.7)
    else:  # Middle bars
        if val < 0:
            bar = ax.bar(i, abs(val), bottom=cum - abs(val),
                        color=colors[i], alpha=0.95,
                        edgecolor='white', linewidth=2, width=0.7)
        else:
            bar = ax.bar(i, val, bottom=cum,
                        color=colors[i], alpha=0.95,
                        edgecolor='white', linewidth=2, width=0.7)
    bars.append(bar)

# Draw connecting lines between bars
for i in range(len(categories) - 1):
    y_start = display_values[i]
    y_end = cumulative[i + 1] if i + 1 < len(cumulative) else display_values[i + 1]
    
    if categories[i + 1] != "Today's\nCaptured\nValue":
        ax.plot([i + 0.35, i + 0.65], [y_start, y_end], 
               'k--', linewidth=1.5, alpha=0.4)

# Add value labels on bars and cumulative values
for i, (bar, val, disp_val) in enumerate(zip(bars, values, display_values)):
    # Value change label (inside or near bar)
    if i == 0:  # Total Market
        y_pos = disp_val / 2
        label = f'₹{disp_val:,.0f} Cr'
    elif categories[i] == "Today's\nCaptured\nValue":
        y_pos = disp_val / 2
        label = f'₹{disp_val:,.0f} Cr\n(Current)'
    elif categories[i] == 'Final Value\nRealized':
        y_pos = disp_val / 2
        label = f'₹{disp_val:,.0f} Cr'
    else:
        if val > 0:
            y_pos = cumulative[i] + abs(val) / 2
            label = f'+₹{abs(val):,.0f} Cr'
        else:
            y_pos = cumulative[i] - abs(val) / 2
            label = f'–₹{abs(val):,.0f} Cr'
    
    ax.text(i, y_pos, label,
           ha='center', va='center',
           fontsize=11, fontweight='bold', color='white',
           bbox=dict(boxstyle='round,pad=0.5', 
                    facecolor='black', alpha=0.75, edgecolor='none'))
    
    # Cumulative value label above each bar (except last)
    if i < len(categories) - 1 and categories[i] != "Today's\nCaptured\nValue":
        ax.text(i, disp_val + 80, f'₹{disp_val:,.0f} Cr',
               ha='center', va='bottom',
               fontsize=10, fontweight='bold', color='cyan',
               bbox=dict(boxstyle='round,pad=0.3', 
                        facecolor='#1e1e1e', alpha=0.8, 
                        edgecolor='cyan', linewidth=1))

# Formatting
ax.set_ylabel('Revenue (₹ Crores)', fontsize=14, fontweight='bold', color='white')
ax.set_title('Market Opportunity & SmartBid Revenue Impact', 
             fontsize=20, fontweight='bold', pad=25, color='white')
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=10, fontweight='bold', color='white')
ax.set_ylim(-100, 2700)
ax.grid(axis='y', alpha=0.2, linestyle='--', color='grey')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.axhline(y=0, color='white', linewidth=0.8, alpha=0.5)

# Add legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#3498db', edgecolor='white', label='Starting Point'),
    Patch(facecolor='#e74c3c', edgecolor='white', label='Revenue Loss'),
    Patch(facecolor='#7f8c8d', edgecolor='white', label='Current State'),
    Patch(facecolor='#27ae60', edgecolor='white', label='SmartBid Impact'),
    Patch(facecolor='#52b788', edgecolor='white', label='Operational Savings')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10, 
         framealpha=0.92, fancybox=True, shadow=True)

# Add key annotation
ax.text(0.5, 0.97, '5% market capture → 55% with SmartBid', 
        transform=ax.transAxes, ha='center', fontsize=14, 
        fontweight='bold', color='cyan',
        bbox=dict(boxstyle='round,pad=0.7', facecolor='#1e1e1e', 
                 edgecolor='cyan', linewidth=2.5))

# Add arrow showing the transformation
ax.annotate('', xy=(6, 1323), xytext=(3, 120),
            arrowprops=dict(arrowstyle='->', lw=3, color='cyan', 
                          connectionstyle='arc3,rad=0.2'))

plt.tight_layout()
plt.savefig(output_dir / 'chart14_waterfall_smartbid_impact.png', dpi=300, 
            bbox_inches='tight', facecolor='#1e1e1e')
plt.close()

print("✅ Chart saved: chart14_waterfall_smartbid_impact.png")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*70)
print("✅ ENHANCED WATERFALL CHART GENERATED SUCCESSFULLY!")
print("="*70)
print(f"\n📁 Location: {output_dir.absolute()}\n")
print("Generated file:")
print("  14. chart14_waterfall_smartbid_impact.png")
print("\n📊 Revenue Flow (Left to Right):")
print("  1. Total Market: ₹2,400 Cr")
print("  2. Lost: <10% Explored: –₹2,160 Cr → Cumulative: ₹240 Cr")
print("  3. Lost: Analysis Gap: –₹120 Cr → Cumulative: ₹120 Cr")
print("  4. Today's Captured Value: ₹120 Cr (Current State - Gray)")
print("  5. SmartBid Recovery: +₹1,200 Cr → Cumulative: ₹1,320 Cr")
print("  6. Ops Savings: +₹3 Cr → Cumulative: ₹1,323 Cr")
print("  7. Final Value Realized: ₹1,323 Cr (Bright Green)")
print("\n🎯 Key Transformation:")
print("  📉 Current: 5% market capture (₹120 Cr)")
print("  📈 With SmartBid: 55% market capture (₹1,323 Cr)")
print("  🚀 Impact: 11x revenue increase!")
print("\n🎨 Features:")
print("  ✅ Complete waterfall with cumulative values at each step")
print("  ✅ Color-coded: Red (losses), Gray (current), Green (gains)")
print("  ✅ Cumulative values shown above bars in cyan boxes")
print("  ✅ Value changes shown inside bars")
print("  ✅ Connecting dotted lines showing flow")
print("  ✅ Cyan annotation: '5% → 55%' transformation")
print("  ✅ Arrow showing SmartBid impact")
print("  ✅ Dark background theme")
print("  ✅ 300 DPI print-ready quality")
print("="*70)
