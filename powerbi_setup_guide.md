# Power BI Setup Guide for Cybersecurity Threat Intelligence

## Quick Start: Import Data into Power BI

### Step 1: Load Data
1. **Open Power BI Desktop**
2. **Get Data** → **Text/CSV**
3. **Browse** and select `live_cyberattacks.csv`
4. **Load** the data

### Step 2: Basic Data Model
1. **Go to Model view**
2. **Create relationships** if needed (usually not required for single table)
3. **Set data types**:
   - Timestamp → DateTime
   - Threat_Score → Whole Number
   - Latitude/Longitude → Decimal Number

## Recommended Visualizations

### 1. Executive Dashboard (Top Section)

#### Threat Overview Cards
- **Total Threats Today**
  - Visual: Card
  - Field: Count of records
  - Filter: Timestamp = Today

- **High Severity Threats**
  - Visual: Card
  - Field: Count of records
  - Filter: Threat_Level = "High"

- **Medium Severity Threats**
  - Visual: Card
  - Field: Count of records
  - Filter: Threat_Level = "Medium"

- **Low Severity Threats**
  - Visual: Card
  - Field: Count of records
  - Filter: Threat_Level = "Low"

#### Top Attacked Countries
- Visual: Bar Chart
- Axis: `Country_Target`
- Values: `Number of Attacks`
- Sort: Descending by `Number of Attacks`

#### Attack Distribution by Type
- Visual: Bar Chart or Donut Chart
- Axis/Legend: `Attack_Type`
- Values: `Number of Attacks`

### 2. Geographic Threat Map

#### Live Attacks Map
- Visual: Map (or Filled Map for country-level)
- Latitude: `Latitude`
- Longitude: `Longitude`
- Size: `Number of Attacks`
- Legend (Optional): `Attack_Type` or `Threat_Level`
- Tooltip: `Attack_Type`, `IP_Source`, `Country_Target`, `Threat_Score`

### 3. Threat Heatmap & Details

#### Threat Heatmap
- Visual: Matrix or Table
- Rows: `Attack_Type`
- Columns: `Threat_Level`
- Values: `Number of Attacks`

#### Detailed Threat Log
- Visual: Table
- Columns: `Timestamp`, `Attack_Type`, `IP_Source`, `Country_Target`, `Threat_Level`, `Organization_Source`, `Protocol`, `Port`

### 4. Security Level Breakdown

#### Security Level Donut Chart
- Visual: Donut Chart
- Legend: `Threat_Level`
- Values: `Number of Attacks`

## Data Refresh in Power BI

### Power BI Desktop
- To refresh data after running `otx_threat_intelligence.py`, go to **Home** tab → **Refresh**.

### Power BI Service (for Auto-Refresh)
1. **Publish** your `.pbix` file to Power BI Service.
2. Go to **Settings** → **Datasets** → **Scheduled refresh**.
3. Configure the refresh frequency (e.g., every 15 minutes with a Pro license).

This guide provides a structured approach to building your Power BI threat intelligence dashboard. Remember to experiment with different visualizations and filters to best suit your analytical needs. 