---ommitting files names, script pointed to my personal documents
import duckdb
import pandas as pd

# 1. Load Excel sheets
excel_file = "Data_Analysis_Exercise_Data_1.xlsx"
sites = pd.read_excel(excel_file, sheet_name=" Site Info")
tenants = pd.read_excel(excel_file, sheet_name="Tenant Lease Up")

# Clean column names
sites.columns = sites.columns.str.strip()
tenants.columns = tenants.columns.str.strip()

# 2. SQL Join using DuckDB: Filter for sites with ZERO additional tenants
query = """
    SELECT 
        s."Site Number",
        s."Year Built",
        s."Site classification",
        s."Tower Type",
        s.Height,
        s.State,
        s.Capex,
        s."Anchor Tenant Name",
        COUNT(t."Additional Tenant Name") AS Add_Tenant_Count
    FROM sites s
    LEFT JOIN tenants t ON s."Site Number" = t."Site Number"
    GROUP BY 
        s."Site Number", s."Year Built", s."Site classification", 
        s."Tower Type", s.Height, s.State, s.Capex, 
        s."Anchor Tenant Name"
    HAVING Add_Tenant_Count = 0;
"""

unleased = duckdb.query(query).to_df()

# 3. Calculate Lease-Up Potential Score (0 - 100)
# Uses provided site features + public market growth trends (e.g. TX/AZ densification)
def calc_leaseup_score(row):
    score = 0.0
    
    # Site Classification (Urban centers have highest capacity/densification demand)
    if row['Site classification'] == 'Urban':
        score += 35.0
    elif row['Site classification'] == 'Suburban':
        score += 25.0
    else:  # Rural
        score += 10.0
        
    # Geographic Growth Markets (TX & AZ represent top 5G expansion corridors)
    if row['State'] in ['TX', 'AZ']:
        score += 15.0
    else:
        score += 10.0
        
    # Structural Type (Self-Supporting Towers & Monopoles allow easier co-location)
    if row['Tower Type'] == 'SST':
        score += 25.0
    elif row['Tower Type'] == 'Monopole':
        score += 20.0
    elif row['Tower Type'] == 'Guyed Tower':
        score += 18.0
    else:
        score += 5.0
        
    # Height Profile (Taller structures accommodate more RAD centers)
    if row['Height'] >= 200:
        score += 15.0
    elif row['Height'] >= 160:
        score += 12.0
    elif row['Height'] >= 120:
        score += 8.0
    else:
        score += 4.0
        
    # Asset Vintage (Newer sites built to modern loading standards)
    if row['Year Built'] >= 2021:
        score += 10.0
    elif row['Year Built'] >= 2019:
        score += 7.0
    else:
        score += 4.0
        
    return score

unleased['Leaseup_Score'] = unleased.apply(calc_leaseup_score, axis=1)

# 4. Group strictly into Two Main Categories
# Threshold set at >= 65 for High Potential
unleased['Lease_Up_Potential'] = unleased['Leaseup_Score'].apply(
    lambda s: 'High Lease Up Potential' if s >= 65 else 'Low Lease Up Potential'
)

# 5. Stack Rank Sites
unleased = unleased.sort_values(by=['Leaseup_Score', 'Capex'], ascending=[False, True]).reset_index(drop=True)
unleased['Stack_Rank'] = unleased.index + 1

# Select final clean columns
final_output = unleased[[
    'Stack_Rank',
    'Site Number',
    'Lease_Up_Potential',
    'Leaseup_Score',
    'Site classification',
    'State',
    'Tower Type',
    'Height',
    'Year Built',
    'Anchor Tenant Name',
    'Capex'
]]

# 6. Summary & Export
print("==================================================")
print("     STACK RANKING: LEASE-UP POTENTIAL SUMMARY    ")
print("==================================================\n")
print(f"Total Single-Tenant Sites: {len(final_output)}\n")
print(final_output['Lease_Up_Potential'].value_counts())

final_output.to_csv("Stack_Ranked_Unleased_Sites.csv", index=False)
print("\nExported clean results to 'Stack_Ranked_Unleased_Sites.csv'")
