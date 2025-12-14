"""
Generate waterfall chart showing Market Opportunity & Revenue Recovery
Creates waterfall chart as PNG for PowerPoint showing revenue flow
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
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['figure.facecolor'] = '#1e1e1e'
plt.rcParams['axes.facecolor'] = '#2d2d2d'

# ============================================================================
# Waterfall Chart – Market Opportunity & Revenue Recovery
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 8))

# Data
categories = [
    'Total\nOpportunity',
    'Lost: <10%\nExplored',
    'Lost: Analysis\nGap',
    'SmartBid\nRecovery',
    'Ops Savings\n(₹2-5 Cr)',
    'Final\nValue'
]

# Values (in ₹ Crores)
values = [2400, -2160, -120, 1200, 3, 0]  # Last is calculated

# Calculate cumulative values for positioning
cumulative = [0]
current = 2400

for i, val in enumerate(values[1:], 1):
    if i < len(values) - 1:  # Not the final value
        cumulative.append(current)
        current += val
    else:  # Final value
        cumulative.append(current)

# Colors: green for positive, red for negative, blue for start/end
colors = []
for i, val in enumerate(values):
    if i == 0:  # Start
        colors.append('#3498db')
    elif i == len(values) - 1:  # End
        colors.append('#2ecc71')
    elif val > 0:  # Positive
        colors.append('#2ecc71')
    else:  # Negative
        colors.append('#e74c3c')

# Create bars
x = np.arange(len(categories))
bars = []

for i, (cat, val, cum) in enumerate(zip(categories, values, cumulative)):
    if i == 0:  # First bar starts from 0
        bar = ax.bar(i, val, color=colors[i], alpha=0.9, 
                    edgecolor='white', linewidth=2)
    elif i == len(categories) - 1:  # Last bar shows final value
        bar = ax.bar(i, cum, color=colors[i], alpha=0.9,
                    edgecolor='white', linewidth=2)
    else:  # Middle bars
        bar = ax.bar(i, abs(val), bottom=cum if val < 0 else cum,
                    color=colors[i], alpha=0.9,
                    edgecolor='white', linewidth=2)
    bars.append(bar)

# Draw connecting lines between bars
for i in range(len(categories) - 2):
    if i == 0:
        y_start = values[0]
    else:
        y_start = cumulative[i] + (values[i] if values[i] > 0 else 0)
    
    y_end = cumulative[i + 1]
    
    ax.plot([i + 0.4, i + 0.6], [y_start, y_end], 
           'k--', linewidth=1.5, alpha=0.5)

# Add value labels on bars
for i, (bar, val, cum) in enumerate(zip(bars, values, cumulative)):
    if i == 0:  # First bar
        y_pos = val / 2
        label = f'₹{val:,.0f} Cr'
    elif i == len(categories) - 1:  # Last bar
        y_pos = cum / 2
        label = f'₹{cum:,.0f} Cr'
    else:
        if val > 0:
            y_pos = cum + abs(val) / 2
            label = f'+₹{abs(val):,.0f} Cr'
        else:
            y_pos = cum - abs(val) / 2
            label = f'-₹{abs(val):,.0f} Cr'
    
    ax.text(i, y_pos, label,
           ha='center', va='center',
           fontsize=11, fontweight='bold', color='white',
           bbox=dict(boxstyle='round,pad=0.4', 
                    facecolor='black', alpha=0.7, edgecolor='none'))

# Formatting
ax.set_ylabel('Revenue (₹ Crores)', fontsize=14, fontweight='bold', color='white')
ax.set_title('Market Opportunity & Revenue Recovery', 
             fontsize=19, fontweight='bold', pad=25, color='white')
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11, fontweight='bold', color='white')
ax.set_ylim(-200, 2600)
ax.grid(axis='y', alpha=0.2, linestyle='--', color='grey')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.axhline(y=0, color='white', linewidth=0.8, alpha=0.5)

# Add legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#3498db', edgecolor='white', label='Starting Point'),
    Patch(facecolor='#e74c3c', edgecolor='white', label='Revenue Loss'),
    Patch(facecolor='#2ecc71', edgecolor='white', label='Revenue Gain/Final')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=11, 
         framealpha=0.9, fancybox=True, shadow=True)

# Add insight annotation
ax.text(0.5, 0.95, '90% opportunity loss → SmartBid recovers 50% of total market', 
        transform=ax.transAxes, ha='center', fontsize=12, 
        fontweight='bold', color='cyan',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e1e1e', 
                 edgecolor='cyan', linewidth=2))

plt.tight_layout()
plt.savefig(output_dir / 'chart13_waterfall_revenue.png', dpi=300, 
            bbox_inches='tight', facecolor='#1e1e1e')
plt.close()

print("✅ Chart saved: chart13_waterfall_revenue.png")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*60)
print("✅ WATERFALL CHART GENERATED SUCCESSFULLY!")
print("="*60)
print(f"\n📁 Location: {output_dir.absolute()}\n")
print("Generated file:")
print("  13. chart13_waterfall_revenue.png")
print("\n📊 Revenue Flow:")
print("  1. Total Opportunity: ₹2,400 Cr")
print("  2. Lost: <10% Explored: -₹2,160 Cr → ₹240 Cr")
print("  3. Lost: Analysis Gap: -₹120 Cr → ₹120 Cr")
print("  4. SmartBid Recovery: +₹1,200 Cr → ₹1,320 Cr")
print("  5. Ops Savings: +₹3 Cr → ₹1,323 Cr")
print("  6. Final Value: ₹1,323 Cr")
print("\n🎯 Key Insights:")
print("  ✅ 90% opportunity currently lost to poor discovery")
print("  ✅ SmartBid recovers 50% of total market (₹1,200 Cr)")
print("  ✅ Additional ₹2-5 Cr operational savings")
print("  ✅ Final value: ₹1,323 Cr (55% of total opportunity)")
print("\n🎨 Features:")
print("  ✅ Waterfall chart with cumulative flow")
print("  ✅ Color-coded (Blue=start, Red=loss, Green=gain)")
print("  ✅ Connecting lines between bars")
print("  ✅ Value labels on all segments")
print("  ✅ Dark background theme")
print("  ✅ 300 DPI print-ready quality")
print("="*60)
