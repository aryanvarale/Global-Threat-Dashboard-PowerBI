# Power BI Cybersecurity Threat Intelligence Dashboard

This project creates a comprehensive cybersecurity threat intelligence dashboard using Power BI with realistic threat data generation.

## Features

- **Realistic Threat Data**: Generates comprehensive cybersecurity threat data with real-world scenarios
- **Automated Data Processing**: Classifies attack types and determines severity levels
- **Power BI Integration**: Exports data to CSV format for easy Power BI import
- **Comprehensive Logging**: Detailed logging for monitoring and debugging
- **Error Handling**: Robust error handling for data processing

## Screenshots

### Power BI Setup Example
![Power BI Setup Example](images/Setup1.png)

### Power BI Report Example
![Power BI Report Example](images/BI_Report.png)

## Prerequisites

- Python 3.7 or higher
- Power BI Desktop (for local development)
- Power BI Service account (for automated refresh)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/cybersecurity-threat-dashboard.git
cd cybersecurity-threat-dashboard
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Threat Data
```bash
python otx_threat_intelligence.py
```

This will create `live_cyberattacks.csv` with realistic threat data.

### 4. Import into Power BI
1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Select `live_cyberattacks.csv`
4. Load the data

## Data Schema

The generated CSV contains the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| Timestamp | Data collection timestamp | 2024-01-15T10:30:00.000Z |
| Attack_Type | Type of cyber attack | "Ransomware Attack" |
| Country_Source | Attacker's country | "Russia" |
| Country_Target | Victim's country | "United States" |
| Latitude | Geographic coordinate | 37.7749 |
| Longitude | Geographic coordinate | -122.4194 |
| City_Source | Attacker's city | "Moscow" |
| City_Target | Victim's city | "New York" |
| IP_Source | Attacker's IP address | "192.168.1.100" |
| IP_Target | Victim's IP address | "8.8.8.8" |
| Organization_Source | Attacker organization | "CyberCriminals Inc" |
| Organization_Target | Victim organization | "Microsoft Corporation" |
| Protocol | Network protocol | "HTTPS" |
| Port | Port number | 443 |
| Threat_Level | Severity level | "High" |
| Threat_Score | Threat score (0-100) | 85 |

## Power BI Setup

### Map Visualization
1. Add Map visual to your report
2. Drag `Latitude` to Latitude field well
3. Drag `Longitude` to Longitude field well
4. Drag `Number_of_Attacks` to Size field well
5. (Optional) Drag `Attack_Type` to Legend field well

### Recommended Visualizations
- **Live Attacks Map**: Geographic visualization of threat locations
- **Top Attacked Countries**: Bar chart showing most targeted countries
- **Attack Distribution**: Pie chart of attack types
- **Security Level Breakdown**: Donut chart of threat severity levels
- **Threat Heatmap**: Matrix showing threat intensity by type
- **Recent Attacks Table**: Detailed log of recent threat events

## Project Structure

```
cybersecurity-threat-dashboard/
├── images/
│   ├── Setup1.png
│   └── BI_Report.png
├── otx_threat_intelligence.py
├── config.py
├── requirements.txt
├── README.md
├── powerbi_setup_guide.md
├── map_field_mapping.md
└── test_script.py
```

## Data Refresh

### Manual Refresh
- Re-run the Python script: `python otx_threat_intelligence.py`
- Refresh in Power BI: Home → Refresh

### Automated Refresh (Power BI Service)
1. Publish your .pbix file to Power BI Service
2. Settings → Datasets → Scheduled refresh
3. Set refresh every 15 minutes (Pro license required)

## Configuration

Edit `config.py` to customize:
- Output file name
- Default coordinates
- Data generation parameters

## Troubleshooting

### Common Issues
1. **No data points on map**: Check that Latitude/Longitude are numeric
2. **All points in same location**: Verify coordinates have variation
3. **Map not loading**: Check internet connection for map tiles
4. **Performance issues**: Reduce data points or enable clustering

### Logs
Check `otx_data_fetch.log` for detailed error messages and debugging information.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

## License

This project is for educational and research purposes.

---

**Happy threat hunting!** 