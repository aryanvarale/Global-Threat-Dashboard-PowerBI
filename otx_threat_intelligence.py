import requests
import csv
import json
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
from collections import defaultdict
from config import CSV_OUTPUT_FILE, DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_NUM_RECORDS, DEFAULT_API_KEY

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('otx_data_fetch.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OTXThreatIntelligence:
    def __init__(self, api_key: str = DEFAULT_API_KEY):
        self.api_key = api_key
        
        # Realistic data generators
        self.organizations = {
            'source': [
                'CyberCriminals Inc', 'DarkNet Syndicate', 'HackForce Group', 'ShadowOps Collective',
                'Digital Predators', 'CyberMafia Network', 'StealthHackers', 'PhantomBreach Team',
                'SilentStrike Corp', 'NightHawk Security', 'GhostNet Operations', 'StealthOps Ltd',
                'CyberShadow Group', 'DigitalVipers', 'StealthStrike Team', 'PhantomHackers',
                'ShadowNet Collective', 'CyberPredators', 'StealthForce', 'DarkOps Network'
            ],
            'target': [
                'Microsoft Corporation', 'Google LLC', 'Amazon Web Services', 'Apple Inc',
                'Meta Platforms', 'Netflix Inc', 'Adobe Systems', 'Oracle Corporation',
                'Salesforce Inc', 'Cisco Systems', 'Intel Corporation', 'IBM Corporation',
                'Dell Technologies', 'HP Inc', 'VMware Inc', 'SAP SE',
                'Siemens AG', 'General Electric', 'Boeing Company', 'Lockheed Martin'
            ]
        }
        
        self.cities = {
            'source': [
                'Moscow', 'Beijing', 'Pyongyang', 'Tehran', 'Damascus', 'Caracas', 'Havana',
                'Minsk', 'Belgrade', 'Bucharest', 'Sofia', 'Budapest', 'Prague', 'Warsaw',
                'Kiev', 'Minsk', 'Riga', 'Tallinn', 'Vilnius', 'Bratislava'
            ],
            'target': [
                'New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Seattle', 'Austin',
                'Boston', 'Washington DC', 'Atlanta', 'Dallas', 'Denver', 'Phoenix',
                'Miami', 'Las Vegas', 'Portland', 'San Diego', 'Nashville', 'Charlotte',
                'Minneapolis', 'Detroit'
            ]
        }
        
        self.countries = {
            'source': [
                'Russia', 'China', 'North Korea', 'Iran', 'Syria', 'Venezuela', 'Cuba',
                'Belarus', 'Serbia', 'Romania', 'Bulgaria', 'Hungary', 'Czech Republic',
                'Poland', 'Ukraine', 'Latvia', 'Estonia', 'Lithuania', 'Slovakia', 'Croatia'
            ],
            'target': [
                'United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Japan',
                'Australia', 'Netherlands', 'Sweden', 'Norway', 'Denmark', 'Finland',
                'Switzerland', 'Austria', 'Belgium', 'Ireland', 'Luxembourg', 'Iceland',
                'New Zealand', 'Singapore'
            ]
        }
        
        self.attack_types = [
            'Ransomware Attack', 'Phishing Campaign', 'DDoS Attack', 'APT Infiltration',
            'Data Breach', 'Malware Injection', 'SQL Injection', 'XSS Attack',
            'Man-in-the-Middle', 'Credential Harvesting', 'Social Engineering',
            'Zero-Day Exploit', 'Backdoor Installation', 'Keylogger Deployment',
            'Spyware Infection', 'Adware Distribution', 'Botnet Recruitment',
            'Cryptojacking', 'Supply Chain Attack', 'Watering Hole Attack'
        ]
        
        self.protocols = ['HTTP', 'HTTPS', 'FTP', 'SSH', 'SMTP', 'DNS', 'DHCP', 'SNMP', 'Telnet', 'RDP']
        self.ports = [21, 22, 23, 25, 53, 67, 80, 110, 143, 443, 993, 995, 3389, 8080, 8443]
        self.threat_levels = ['Critical', 'High', 'Medium', 'Low']
        
        # IP address ranges for realistic generation
        self.ip_ranges = {
            'source': [
                ('192.168.1.1', '192.168.1.254'),
                ('10.0.0.1', '10.0.0.254'),
                ('172.16.0.1', '172.16.0.254'),
                ('203.0.113.1', '203.0.113.254'),
                ('198.51.100.1', '198.51.100.254')
            ],
            'target': [
                ('8.8.8.1', '8.8.8.254'),
                ('1.1.1.1', '1.1.1.254'),
                ('208.67.222.1', '208.67.222.254'),
                ('9.9.9.1', '9.9.9.254'),
                ('185.228.168.1', '185.228.168.254')
            ]
        }
        
        # Geographic coordinates for cities
        self.city_coordinates = {
            'Moscow': (55.7558, 37.6176), 'Beijing': (39.9042, 116.4074), 'Pyongyang': (39.0392, 125.7625),
            'Tehran': (35.6892, 51.3890), 'Damascus': (33.5138, 36.2765), 'Caracas': (10.4806, -66.9036),
            'Havana': (23.1136, -82.3666), 'Minsk': (53.9045, 27.5615), 'Belgrade': (44.7866, 20.4489),
            'Bucharest': (44.4268, 26.1025), 'Sofia': (42.6977, 23.3219), 'Budapest': (47.4979, 19.0402),
            'Prague': (50.0755, 14.4378), 'Warsaw': (52.2297, 21.0122), 'Kiev': (50.4501, 30.5234),
            'Riga': (56.9496, 24.1052), 'Tallinn': (59.4369, 24.7536), 'Vilnius': (54.6872, 25.2797),
            'Bratislava': (48.1486, 17.1077), 'Croatia': (45.8150, 15.9819),
            'New York': (40.7128, -74.0060), 'San Francisco': (37.7749, -122.4194),
            'Los Angeles': (34.0522, -118.2437), 'Chicago': (41.8781, -87.6298),
            'Seattle': (47.6062, -122.3321), 'Austin': (30.2672, -97.7431),
            'Boston': (42.3601, -71.0589), 'Washington DC': (38.9072, -77.0369),
            'Atlanta': (33.7490, -84.3880), 'Dallas': (32.7767, -96.7970),
            'Denver': (39.7392, -104.9903), 'Phoenix': (33.4484, -112.0740),
            'Miami': (25.7617, -80.1918), 'Las Vegas': (36.1699, -115.1398),
            'Portland': (45.5152, -122.6784), 'San Diego': (32.7157, -117.1611),
            'Nashville': (36.1627, -86.7816), 'Charlotte': (35.2271, -80.8431),
            'Minneapolis': (44.9778, -93.2650), 'Detroit': (42.3314, -83.0458)
        }
    
    def generate_random_ip(self, ip_type: str) -> str:
        """Generate realistic IP addresses"""
        ip_range = random.choice(self.ip_ranges[ip_type])
        start_ip = ip_range[0].split('.')
        end_ip = ip_range[1].split('.')
        
        # Generate random IP within range
        ip_parts = []
        for i in range(4):
            start = int(start_ip[i])
            end = int(end_ip[i])
            ip_parts.append(str(random.randint(start, end)))
        
        return '.'.join(ip_parts)
    
    def generate_realistic_timestamp(self) -> str:
        """Generate realistic timestamps within the last 30 days"""
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        
        attack_time = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
        return attack_time.isoformat()
    
    def get_city_coordinates(self, city: str) -> Tuple[float, float]:
        """Get coordinates for a city with small random variation"""
        if city in self.city_coordinates:
            lat, lon = self.city_coordinates[city]
            # Add small random variation
            lat += random.uniform(-0.1, 0.1)
            lon += random.uniform(-0.1, 0.1)
            return lat, lon
        else:
            # Fallback to random coordinates
            return (random.uniform(-90, 90), random.uniform(-180, 180))
    
    def generate_realistic_threat_data(self, num_records: int = DEFAULT_NUM_RECORDS) -> List[Dict]:
        """Generate realistic cybersecurity threat data"""
        threat_records = []
        
        for i in range(num_records):
            # Generate source and target data
            source_country = random.choice(self.countries['source'])
            target_country = random.choice(self.countries['target'])
            source_city = random.choice(self.cities['source'])
            target_city = random.choice(self.cities['target'])
            source_org = random.choice(self.organizations['source'])
            target_org = random.choice(self.organizations['target'])
            
            # Generate IP addresses
            source_ip = self.generate_random_ip('source')
            target_ip = self.generate_random_ip('target')
            
            # Generate coordinates
            source_lat, source_lon = self.get_city_coordinates(source_city)
            target_lat, target_lon = self.get_city_coordinates(target_city)
            
            # Generate attack details
            attack_type = random.choice(self.attack_types)
            protocol = random.choice(self.protocols)
            port = random.choice(self.ports)
            threat_level = random.choice(self.threat_levels)
            
            # Generate threat score based on threat level
            if threat_level == 'Critical':
                threat_score = random.randint(90, 100)
            elif threat_level == 'High':
                threat_score = random.randint(70, 89)
            elif threat_level == 'Medium':
                threat_score = random.randint(40, 69)
            else:  # Low
                threat_score = random.randint(10, 39)
            
            # Generate timestamp
            timestamp = self.generate_realistic_timestamp()
            
            # Create threat record
            threat_record = {
                'Timestamp': timestamp,
                'Attack_Type': attack_type,
                'Country_Source': source_country,
                'Country_Target': target_country,
                'Latitude_Source': round(source_lat, 6),
                'Longitude_Source': round(source_lon, 6),
                'Latitude_Target': round(target_lat, 6),
                'Longitude_Target': round(target_lon, 6),
                'City_Source': source_city,
                'City_Target': target_city,
                'IP_Source': source_ip,
                'IP_Target': target_ip,
                'Organization_Source': source_org,
                'Organization_Target': target_org,
                'Protocol': protocol,
                'Port': port,
                'Threat_Level': threat_level,
                'Threat_Score': threat_score,
                'Attack_ID': f"ATTK-{random.randint(10000, 99999)}",
                'Session_ID': f"SESS-{random.randint(100000, 999999)}",
                'User_Agent': f"Mozilla/5.0 ({random.choice(['Windows', 'Linux', 'MacOS'])})",
                'Payload_Size': random.randint(100, 50000),
                'Duration_Seconds': random.randint(1, 3600),
                'Data_Exfiltrated_MB': round(random.uniform(0.1, 100.0), 2),
                'Encryption_Type': random.choice(['AES-256', 'RSA-2048', 'DES', '3DES', 'Blowfish']),
                'Malware_Family': random.choice(['Emotet', 'TrickBot', 'Ryuk', 'REvil', 'Conti', 'LockBit']),
                'CVE_References': f"CVE-2023-{random.randint(1000, 9999)}",
                'IOC_Type': random.choice(['IP', 'Domain', 'Hash', 'Email', 'URL']),
                'TTP_Technique': random.choice(['T1078', 'T1055', 'T1059', 'T1082', 'T1016']),
                'Campaign_Name': f"Operation {random.choice(['Shadow', 'Phantom', 'Stealth', 'Ghost', 'Dark'])} {random.randint(1, 100)}"
            }
            
            threat_records.append(threat_record)
        
        return threat_records
    
    def aggregate_by_location(self, threat_data: List[Dict]) -> List[Dict]:
        """Aggregate threat data by target location"""
        location_counts = defaultdict(lambda: {
            'count': 0,
            'critical_threats': 0,
            'high_threats': 0,
            'medium_threats': 0,
            'low_threats': 0,
            'attack_types': set(),
            'source_countries': set(),
            'target_countries': set(),
            'avg_threat_score': 0,
            'total_threat_score': 0,
            'unique_ips': set(),
            'sample_attack_type': '',
            'sample_source_country': '',
            'sample_target_country': '',
            'sample_organization': ''
        })
        
        # Aggregate by target location
        for record in threat_data:
            # Use target coordinates for aggregation
            lat_rounded = round(record['Latitude_Target'], 2)
            lon_rounded = round(record['Longitude_Target'], 2)
            location_key = f"{lat_rounded},{lon_rounded}"
            
            location_data = location_counts[location_key]
            location_data['count'] += 1
            location_data['unique_ips'].add(record['IP_Target'])
            
            # Count by threat level
            if record['Threat_Level'] == 'Critical':
                location_data['critical_threats'] += 1
            elif record['Threat_Level'] == 'High':
                location_data['high_threats'] += 1
            elif record['Threat_Level'] == 'Medium':
                location_data['medium_threats'] += 1
            else:
                location_data['low_threats'] += 1
            
            # Track attack types and countries
            location_data['attack_types'].add(record['Attack_Type'])
            location_data['source_countries'].add(record['Country_Source'])
            location_data['target_countries'].add(record['Country_Target'])
            
            # Calculate average threat score
            location_data['total_threat_score'] += record['Threat_Score']
            
            # Store sample data
            if not location_data['sample_attack_type']:
                location_data['sample_attack_type'] = record['Attack_Type']
                location_data['sample_source_country'] = record['Country_Source']
                location_data['sample_target_country'] = record['Country_Target']
                location_data['sample_organization'] = record['Organization_Target']
        
        # Convert to final format
        aggregated_records = []
        for location_key, data in location_counts.items():
            lat, lon = map(float, location_key.split(','))
            
            # Calculate average threat score
            avg_threat_score = data['total_threat_score'] / data['count'] if data['count'] > 0 else 0
            
            # Determine dominant threat level
            threat_counts = [
                (data['critical_threats'], 'Critical'),
                (data['high_threats'], 'High'),
                (data['medium_threats'], 'Medium'),
                (data['low_threats'], 'Low')
            ]
            dominant_threat_level = max(threat_counts, key=lambda x: x[0])[1]
            
            aggregated_records.append({
                'Timestamp': datetime.utcnow().isoformat(),
                'Latitude': lat,
                'Longitude': lon,
                'Number_of_Attacks': data['count'],
                'Critical_Threats': data['critical_threats'],
                'High_Threats': data['high_threats'],
                'Medium_Threats': data['medium_threats'],
                'Low_Threats': data['low_threats'],
                'Dominant_Threat_Level': dominant_threat_level,
                'Attack_Types': ', '.join(data['attack_types']),
                'Source_Countries': ', '.join(data['source_countries']),
                'Target_Countries': ', '.join(data['target_countries']),
                'Average_Threat_Score': round(avg_threat_score, 2),
                'Unique_IPs': len(data['unique_ips']),
                'Sample_Attack_Type': data['sample_attack_type'],
                'Sample_Source_Country': data['sample_source_country'],
                'Sample_Target_Country': data['sample_target_country'],
                'Sample_Organization': data['sample_organization']
            })
        
        return aggregated_records
    
    def save_to_csv(self, threat_data: List[Dict], filename: str = CSV_OUTPUT_FILE):
        """Save threat data to CSV file"""
        try:
            # First aggregate the data by location
            aggregated_data = self.aggregate_by_location(threat_data)
            
            fieldnames = [
                'Timestamp', 'Latitude', 'Longitude', 'Number_of_Attacks',
                'Critical_Threats', 'High_Threats', 'Medium_Threats', 'Low_Threats',
                'Dominant_Threat_Level', 'Attack_Types', 'Source_Countries',
                'Target_Countries', 'Average_Threat_Score', 'Unique_IPs',
                'Sample_Attack_Type', 'Sample_Source_Country', 'Sample_Target_Country',
                'Sample_Organization'
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for record in aggregated_data:
                    writer.writerow(record)
            
            logger.info(f"Successfully saved {len(aggregated_data)} aggregated records to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
    
    def run_data_collection(self):
        """Main method to run the data collection process"""
        logger.info("Starting realistic threat intelligence data generation...")
        
        # Generate realistic threat data
        threat_records = self.generate_realistic_threat_data(num_records=DEFAULT_NUM_RECORDS)
        
        # Save to CSV
        if threat_records:
            self.save_to_csv(threat_records)
            logger.info(f"Data generation completed. Total records: {len(threat_records)}")
        else:
            logger.warning("No threat records were generated")

def main():
    """Main function to run the threat intelligence collection"""
    try:
        # Initialize the threat intelligence client
        threat_client = OTXThreatIntelligence()
        
        # Run data collection
        threat_client.run_data_collection()
        
        print("Realistic threat intelligence data generation completed successfully!")
        print(f"Data saved to: {CSV_OUTPUT_FILE}")
        print("Ready to import into Power BI")
        
    except Exception as e:
        logger.error(f"Unexpected error in main execution: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 