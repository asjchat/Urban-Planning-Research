"""
Statistical Analysis of 65+ Population Growth
FDOT District 5 vs. Florida State
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import json

# Phase 1: Data Preparation and Aggregation

# Define FDOT D5 counties - Central Florida (9 counties)
D5_COUNTIES = ['BREVARD', 'FLAGLER', 'LAKE', 'MARION', 
               'ORANGE', 'OSCEOLA', 'SEMINOLE', 'SUMTER', 'VOLUSIA']

print("=" * 80)
print("PHASE 1: DATA PREPARATION AND AGGREGATION")
print("=" * 80)

# Load the population projection data
print("\nLoading data from Excel files...")
df = pd.read_excel('Age Projections - Florida (1).xlsx')

print(f"Data shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nFirst few rows:")
print(df.head(20))

# Identify county and age group columns
county_col = 'County'
age_col = 'Age/Sex'

# Forward-fill the County column (county names appear only once, then NaN for subsequent rows)
df[county_col] = df[county_col].ffill()
print("\nCounty column forward-filled.")
print(f"\nUnique counties after filling: {df[county_col].unique()[:15]}")  # Show first 15

# Identify year columns (2025 to 2050)
year_columns = [col for col in df.columns if isinstance(col, int) and 2025 <= col <= 2050]
print(f"\nYear columns identified: {year_columns}")

# Clean year columns - remove commas and convert to numeric
for year in year_columns:
    if df[year].dtype == 'object':
        df[year] = df[year].astype(str).str.replace(',', '').replace('nan', np.nan)
    df[year] = pd.to_numeric(df[year], errors='coerce')

print("\nYear columns cleaned and converted to numeric.")

# Filter for 65-79 and 80+ age groups
print("\nFiltering for age groups: 65-79 and 80+")
df_65plus = df[df[age_col].isin(['65-79', '80+'])].copy()

print(f"Filtered data shape: {df_65plus.shape}")
print(f"Unique age groups: {df_65plus[age_col].unique()}")
print(f"Unique counties: {df_65plus[county_col].unique()}")

# Calculate 65+ Aggregate for Florida and D5 counties
print("\n" + "=" * 80)
print("CALCULATING 65+ AGGREGATE")
print("=" * 80)

# Create 65+ Aggregate for Florida
florida_65plus = df_65plus[df_65plus[county_col].str.upper() == 'FLORIDA']
if len(florida_65plus) > 0:
    florida_aggregate = florida_65plus[year_columns].sum()
    florida_row = pd.DataFrame({
        county_col: ['FLORIDA'],
        age_col: ['65+ Aggregate']
    })
    for year in year_columns:
        florida_row[year] = florida_aggregate[year]
    print("\nFlorida 65+ Aggregate created:")
    print(florida_row)
else:
    print("\nWarning: No Florida state data found!")
    print(f"Available counties (first 20): {df_65plus[county_col].unique()[:20]}")
    florida_row = None

# Create 65+ Aggregate for D5 counties
d5_data = df_65plus[df_65plus[county_col].str.upper().isin(D5_COUNTIES)]
print(f"\nD5 counties found: {d5_data[county_col].unique()}")
print(f"D5 data shape: {d5_data.shape}")

if len(d5_data) > 0:
    d5_aggregate = d5_data[year_columns].sum()
    d5_row = pd.DataFrame({
        county_col: ['FDOT D5 Aggregate'],
        age_col: ['65+ Aggregate']
    })
    for year in year_columns:
        d5_row[year] = d5_aggregate[year]
    print("\nFDOT D5 Aggregate created:")
    print(d5_row)
else:
    print("\nWarning: No D5 county data found!")
    d5_row = None

# Combine into final dataset
if florida_row is not None and d5_row is not None:
    final_df = pd.concat([florida_row, d5_row], ignore_index=True)
    print("\n" + "=" * 80)
    print("FINAL DATASET FOR REGRESSION")
    print("=" * 80)
    print(final_df)
else:
    print("\nError: Could not create final dataset!")
    exit(1)

# Phase 2: Regression Model Setup
print("\n" + "=" * 80)
print("PHASE 2: REGRESSION MODEL SETUP")
print("=" * 80)

# Transform to long format
long_data = []
for _, row in final_df.iterrows():
    region = row[county_col]
    for year in year_columns:
        long_data.append({
            'County': region,
            'Year': int(year),
            'Population': row[year]
        })

df_long = pd.DataFrame(long_data)
print("\nData transformed to long format:")
print(df_long.head(10))
print(f"\nTotal observations: {len(df_long)}")

# Feature Engineering
df_long['Year_Centered'] = df_long['Year'] - 2025
df_long['Region_D5'] = (df_long['County'] == 'FDOT D5 Aggregate').astype(int)

print("\nFeature engineering complete:")
print(df_long.head(10))

# Phase 3: Statistical Regression
print("\n" + "=" * 80)
print("PHASE 3: STATISTICAL REGRESSION (OLS)")
print("=" * 80)

# Run OLS regression with interaction term
formula = 'Population ~ Year_Centered * Region_D5'
print(f"\nModel formula: {formula}")

model = smf.ols(formula=formula, data=df_long)
results = model.fit()

print("\n" + "=" * 80)
print("FULL REGRESSION SUMMARY")
print("=" * 80)
print(results.summary())

# Phase 4: Conclusion
print("\n" + "=" * 80)
print("PHASE 4: STATISTICAL CONCLUSION")
print("=" * 80)

# Extract P-value for interaction term
interaction_pvalue = results.pvalues['Year_Centered:Region_D5']
print(f"\nP-value for interaction term (Year_Centered:Region_D5): {interaction_pvalue:.6f}")

# Statistical significance threshold
alpha = 0.05
is_significant = interaction_pvalue < alpha

print(f"Significance level (alpha): {alpha}")
print(f"Is the difference statistically significant? {is_significant}")

print("\n" + "=" * 80)
print("FINAL CONCLUSION")
print("=" * 80)

if is_significant:
    conclusion = (
        f"The 65+ population growth rate in the FDOT D5 Aggregate is "
        f"STATISTICALLY SIGNIFICANTLY DIFFERENT from the State of Florida "
        f"(p-value = {interaction_pvalue:.6f} < 0.05).\n\n"
        f"The interaction coefficient indicates that the annual growth rate "
        f"differs between the two regions."
    )
else:
    conclusion = (
        f"The 65+ population growth rate in the FDOT D5 Aggregate is "
        f"NOT STATISTICALLY SIGNIFICANTLY DIFFERENT from the State of Florida "
        f"(p-value = {interaction_pvalue:.6f} >= 0.05).\n\n"
        f"There is insufficient evidence to conclude that the growth trends "
        f"differ between the two regions."
    )

print(conclusion)

# Calculate growth percentages for visualization
print("\n" + "=" * 80)
print("GROWTH PERCENTAGES (2025-2050)")
print("=" * 80)

# Get detailed age group data for visualization
detailed_data = []

# For each region and age group, calculate growth
for region in ['FLORIDA', 'FDOT D5 Aggregate']:
    # Get 65+ Aggregate
    region_data = final_df[final_df[county_col] == region]
    if len(region_data) > 0:
        pop_2025 = region_data[2025].values[0]
        pop_2050 = region_data[2050].values[0]
        growth_pct = ((pop_2050 - pop_2025) / pop_2025) * 100
        detailed_data.append({
            'Region': region,
            'AgeGroup': '65+ Aggregate',
            'Growth_Pct': round(growth_pct, 2),
            'Pop_2025': int(pop_2025),
            'Pop_2050': int(pop_2050)
        })
        print(f"\n{region} - 65+ Aggregate:")
        print(f"  2025 Population: {pop_2025:,.0f}")
        print(f"  2050 Population: {pop_2050:,.0f}")
        print(f"  Growth: {growth_pct:.2f}%")

# Get individual age groups (65-79 and 80+)
for age_group in ['65-79', '80+']:
    for region in ['FLORIDA', 'FDOT D5 Aggregate']:
        if region == 'FLORIDA':
            county_filter = df_65plus[county_col].str.upper() == 'FLORIDA'
        else:
            county_filter = df_65plus[county_col].str.upper().isin(D5_COUNTIES)
        
        age_data = df_65plus[(df_65plus[age_col] == age_group) & county_filter]
        
        if len(age_data) > 0:
            pop_2025 = age_data[2025].sum()
            pop_2050 = age_data[2050].sum()
            growth_pct = ((pop_2050 - pop_2025) / pop_2025) * 100
            detailed_data.append({
                'Region': region,
                'AgeGroup': age_group,
                'Growth_Pct': round(growth_pct, 2),
                'Pop_2025': int(pop_2025),
                'Pop_2050': int(pop_2050)
            })
            print(f"\n{region} - {age_group}:")
            print(f"  2025 Population: {pop_2025:,.0f}")
            print(f"  2050 Population: {pop_2050:,.0f}")
            print(f"  Growth: {growth_pct:.2f}%")

# Calculate county-level rankings
print("\n" + "=" * 80)
print("CALCULATING COUNTY-LEVEL RANKINGS")
print("=" * 80)

county_rankings = []

# Get all counties except Florida state total
all_counties = [c for c in df[county_col].unique() if c != 'FLORIDA']
print(f"\nProcessing {len(all_counties)} counties...")

for county in all_counties:
    county_data = df[df[county_col] == county]
    
    # Calculate "All Ages" growth (Total population)
    total_data = county_data[county_data[age_col] == 'Total']
    if len(total_data) > 0:
        pop_2025_total = total_data[2025].values[0]
        pop_2050_total = total_data[2050].values[0]
        if pop_2025_total > 0:
            growth_pct_total = ((pop_2050_total - pop_2025_total) / pop_2025_total) * 100
        else:
            growth_pct_total = 0
    else:
        pop_2025_total = 0
        pop_2050_total = 0
        growth_pct_total = 0
    
    # Calculate 65+ Aggregate growth
    county_65plus = county_data[county_data[age_col].isin(['65-79', '80+'])]
    if len(county_65plus) > 0:
        pop_2025_65plus = county_65plus[2025].sum()
        pop_2050_65plus = county_65plus[2050].sum()
        if pop_2025_65plus > 0:
            growth_pct_65plus = ((pop_2050_65plus - pop_2025_65plus) / pop_2025_65plus) * 100
        else:
            growth_pct_65plus = 0
    else:
        pop_2025_65plus = 0
        pop_2050_65plus = 0
        growth_pct_65plus = 0
    
    # Calculate 65-79 growth
    county_6579 = county_data[county_data[age_col] == '65-79']
    if len(county_6579) > 0:
        pop_2025_6579 = county_6579[2025].values[0]
        pop_2050_6579 = county_6579[2050].values[0]
        if pop_2025_6579 > 0:
            growth_pct_6579 = ((pop_2050_6579 - pop_2025_6579) / pop_2025_6579) * 100
        else:
            growth_pct_6579 = 0
    else:
        pop_2025_6579 = 0
        pop_2050_6579 = 0
        growth_pct_6579 = 0
    
    # Calculate 80+ growth
    county_80plus = county_data[county_data[age_col] == '80+']
    if len(county_80plus) > 0:
        pop_2025_80plus = county_80plus[2025].values[0]
        pop_2050_80plus = county_80plus[2050].values[0]
        if pop_2025_80plus > 0:
            growth_pct_80plus = ((pop_2050_80plus - pop_2025_80plus) / pop_2025_80plus) * 100
        else:
            growth_pct_80plus = 0
    else:
        pop_2025_80plus = 0
        pop_2050_80plus = 0
        growth_pct_80plus = 0
    
    # Check if it's a D5 county
    is_d5 = county.upper() in D5_COUNTIES
    
    county_rankings.append({
        'County': county,
        'Is_D5': is_d5,
        'All_Ages': {
            'Growth_Pct': round(growth_pct_total, 2),
            'Pop_2025': int(pop_2025_total),
            'Pop_2050': int(pop_2050_total)
        },
        '65+_Aggregate': {
            'Growth_Pct': round(growth_pct_65plus, 2),
            'Pop_2025': int(pop_2025_65plus),
            'Pop_2050': int(pop_2050_65plus)
        },
        '65-79': {
            'Growth_Pct': round(growth_pct_6579, 2),
            'Pop_2025': int(pop_2025_6579),
            'Pop_2050': int(pop_2050_6579)
        },
        '80+': {
            'Growth_Pct': round(growth_pct_80plus, 2),
            'Pop_2025': int(pop_2025_80plus),
            'Pop_2050': int(pop_2050_80plus)
        }
    })

print(f"County rankings calculated for {len(county_rankings)} counties")

# Show top 10 for each category
for category in ['All_Ages', '65+_Aggregate', '65-79', '80+']:
    sorted_counties = sorted(county_rankings, key=lambda x: x[category]['Growth_Pct'], reverse=True)
    top_10 = sorted_counties[:10]
    print(f"\n{category} - Top 10 Fastest Growing Counties:")
    for i, county in enumerate(top_10, 1):
        d5_marker = " [D5]" if county['Is_D5'] else ""
        print(f"  {i}. {county['County']}{d5_marker}: {county[category]['Growth_Pct']:.2f}%")

# Export results to JSON for HTML visualization
output = {
    'growth_data': detailed_data,
    'regression_results': {
        'r_squared': float(results.rsquared),
        'adj_r_squared': float(results.rsquared_adj),
        'f_statistic': float(results.fvalue),
        'f_pvalue': float(results.f_pvalue),
        'interaction_pvalue': float(interaction_pvalue),
        'is_significant': bool(is_significant),
        'coefficients': {
            'Intercept': float(results.params['Intercept']),
            'Year_Centered': float(results.params['Year_Centered']),
            'Region_D5': float(results.params['Region_D5']),
            'Year_Centered:Region_D5': float(results.params['Year_Centered:Region_D5'])
        },
        'conclusion': conclusion
    },
    'time_series': df_long.to_dict('records'),
    'county_rankings': county_rankings
}

with open('analysis_results.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\n" + "=" * 80)
print("Results exported to analysis_results.json")
print("=" * 80)

# Generate county-level time series data for comparisons
print("\n" + "=" * 80)
print("GENERATING COUNTY TIME SERIES DATA")
print("=" * 80)

county_time_series = []

for county in all_counties:
    county_data = df[df[county_col] == county]
    
    # For each demographic category
    for age_category in ['Total', '65+ Aggregate', '65-79', '80+']:
        if age_category == '65+ Aggregate':
            # Sum 65-79 and 80+
            category_data = county_data[county_data[age_col].isin(['65-79', '80+'])]
            if len(category_data) > 0:
                for year in year_columns:
                    pop = category_data[year].sum()
                    county_time_series.append({
                        'County': county,
                        'Is_D5': county.upper() in D5_COUNTIES,
                        'Category': age_category,
                        'Year': year,
                        'Population': int(pop)
                    })
        else:
            # Get specific category
            category_data = county_data[county_data[age_col] == age_category]
            if len(category_data) > 0:
                for year in year_columns:
                    pop = category_data[year].values[0]
                    county_time_series.append({
                        'County': county,
                        'Is_D5': county.upper() in D5_COUNTIES,
                        'Category': age_category,
                        'Year': year,
                        'Population': int(pop)
                    })

print(f"Generated time series data for {len(county_time_series)} data points")

# Update output with county time series
output['county_time_series'] = county_time_series
output['d5_counties'] = D5_COUNTIES

# Re-export with updated data
with open('analysis_results.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\n" + "=" * 80)
print("Results updated with county time series data")
print("=" * 80)

