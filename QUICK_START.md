# Quick Start Guide

## 🚀 View the Interactive Visualization

Simply open **`comprehensive_analysis_visualization.html`** in any web browser!

## ✨ New Feature: Top 10 Fastest Growing Counties

At the top of the visualization, you'll now see an interactive ranking section with:

### How to Use

1. **Filter by Demographic**: Click any of the four filter buttons:
   - **All Ages** - Total population growth
   - **65+ Aggregate** - Combined 65-79 and 80+ age groups
   - **65-79** - Traditional senior population
   - **80+** - Elderly population

2. **View Rankings**: The display automatically updates to show the top 10 counties for the selected demographic

3. **Identify FDOT D5 Counties**: Counties in FDOT District 5 are:
   - **Highlighted in blue** with a gradient background
   - Display "FDOT District 5" badge
   - Stand out from other counties

4. **See Population Details**: Each county card shows:
   - Rank position (1-10)
   - County name
   - Growth percentage (2025-2050)
   - 2025 population
   - 2050 projected population

### Key Insights from Rankings

#### 🏆 Top Overall Growth (All Ages):
- **SUMTER (D5)**: 53.81% - Highest total population growth
- **OSCEOLA (D5)**: 48.17% - 3rd place, strong growth
- **FLAGLER (D5)**: 43.07% - 4th place

#### 👴 65+ Aggregate Leaders:
- **OSCEOLA (D5)**: 104.95% - More than doubling senior population!
- **ORANGE (D5)**: 55.95% - 5th place
- **LAKE (D5)**: 50.55% - 10th place

#### 🎯 80+ Age Group Champions:
- **OSCEOLA (D5)**: 220.05% - Extraordinary growth in elderly population
- **ORANGE (D5)**: 152.56% - 3rd place

### What This Means

**5 of 9 FDOT District 5 counties** appear in the top 10 fastest growing counties across various demographics, demonstrating the significant growth pressure on District 5 infrastructure and services.

**FDOT District 5 - Central Florida (9 counties):**
Brevard, Flagler, Lake, Marion, Orange, Osceola, Seminole, Sumter, and Volusia

## 🔬 NEW: Statistical County Comparison

Compare growth trends between any two counties with statistical analysis!

### How to Use:

1. **Select FDOT D5 County**: Choose from the District 5 dropdown
2. **Select Comparison County**: Choose any Florida county to compare against
3. **Select Demographic**: Choose age group (All Ages, 65+, 65-79, or 80+)
4. **Run Statistical Test**: Click button to perform OLS regression analysis

### What You'll See:

- ✅ **Statistical Significance Badge**: Green if significant (p < 0.05), gray if not
- 📊 **Growth Metrics**: Both counties' growth percentages
- 📈 **Growth Difference**: Absolute difference between counties
- 🔢 **P-value**: Statistical significance measure
- 💡 **Interpretation**: Plain-English explanation of results

### Example Use Case:

Compare **OSCEOLA (D5)** vs **MIAMI-DADE** for 65+ Aggregate to see if Osceola's explosive senior growth is statistically significant compared to Miami-Dade.

---

## 📊 NEW: Multi-County Growth Comparison

Visualize and compare population trends across multiple counties simultaneously!

### How to Use:

1. **Select Multiple Counties**: Hold Ctrl (Windows) or Cmd (Mac) and click to select multiple counties
   - District 5 counties are grouped at the top for easy selection
2. **Choose Demographic**: Select the age group to analyze
3. **Toggle View Mode**:
   - **Growth Rate (%)**: Shows percentage growth from 2025 baseline (normalized)
   - **Actual Population**: Shows absolute population numbers
4. **Update Chart**: Click to refresh the visualization

### View Modes Explained:

**Growth Rate (%) Mode:**
- All counties start at 0% (2025 baseline)
- Shows relative growth independent of county size
- Great for comparing growth *patterns* and *rates*
- Example: 20% growth means population increased by 20% since 2025

**Actual Population Mode:**
- Shows real population numbers
- Useful for understanding *magnitude* and *scale*
- Compare absolute populations side-by-side
- Example: See that Orange County has much higher absolute numbers than Sumter

### Example Use Cases:

1. **Compare all D5 counties**: See which District 5 counties are growing fastest
2. **D5 vs Major Counties**: Compare District 5 against Miami-Dade, Broward, Hillsborough
3. **Similar-sized counties**: Compare counties with similar baseline populations
4. **Regional analysis**: Select geographically adjacent counties

---

## 📊 Complete Features

Your visualization includes:

1. **Top 10 Rankings** - Interactive county rankings with demographic filters
2. **Statistical County Comparison** 🔬 (NEW!) - Test significance between any two counties
3. **Multi-County Growth Comparison** 📊 (NEW!) - Compare multiple counties with toggle views
4. **Key Statistics Cards** - Quick overview of growth metrics
5. **Growth Comparison Chart** - Grouped bar chart (FDOT D5 vs. Florida)
6. **Time Series Chart** - Population projections over time
7. **Regression Analysis** - Full OLS statistical results
8. **Methodology Section** - Complete documentation

## 🔄 Update the Data

To refresh with new data:

```bash
# 1. Update the Excel files with new data
# 2. Run the analysis script
python statistical_analysis.py

# 3. Reload the HTML file in your browser
# The ranking section will automatically load from analysis_results.json
```

## 📱 Works Everywhere

The visualization is fully responsive and works on:
- 💻 Desktop computers
- 📱 Tablets
- 📲 Mobile phones
- 🌐 All modern web browsers (Chrome, Firefox, Safari, Edge)

## 🎨 Interactivity

- **Hover** over any chart element for detailed information
- **Zoom** and pan on charts using Plotly toolbar
- **Download** charts as PNG images
- **Click** demographic filters to change rankings
- **Responsive** design adapts to screen size

## 📈 Key Statistics to Note

- **OSCEOLA County (D5)** shows exceptional growth across all age groups
- **District 5 counties** represent 5 of top 10 in multiple categories
- **80+ age group** shows dramatic growth (100%+ in many counties)
- **Statistical significance** confirmed (p = 0.001132)

---

**Need Help?** Check the full `README.md` for detailed documentation.

**Created:** November 2025  
**Analysis Period:** 2025-2050

