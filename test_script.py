#!/usr/bin/env python3
"""
Simple test script to verify data generation functionality
"""

import sys
import os

def test_data_generation():
    """Test data generation functionality"""
    print("Testing data generation functionality...")
    
    try:
        # Check if main script exists
        if not os.path.exists('otx_threat_intelligence.py'):
            print("Error: otx_threat_intelligence.py not found")
            return False
        
        # Check if config exists
        if not os.path.exists('config.py'):
            print("Error: config.py not found")
            return False
        
        print("All required files found successfully!")
        return True
        
    except Exception as e:
        print(f"Error during testing: {e}")
        return False

def test_simple_data_fetch():
    """Test simple data generation"""
    print("\nTesting data generation...")
    
    try:
        # Import the main module
        from otx_threat_intelligence import OTXThreatIntelligence
        from config import OTX_API_KEY
        
        # Initialize the client
        otx_client = OTXThreatIntelligence(OTX_API_KEY)
        
        # Test data generation
        test_data = otx_client.generate_realistic_threat_data(num_records=5)
        
        print(f"Successfully generated {len(test_data)} test records")
        
        if test_data:
            print("\nSample data structure:")
            sample_record = test_data[0]
            print(f"  - Attack Type: {sample_record.get('Attack_Type', 'N/A')}")
            print(f"  - Source Country: {sample_record.get('Country_Source', 'N/A')}")
            print(f"  - Target Country: {sample_record.get('Country_Target', 'N/A')}")
            print(f"  - Threat Level: {sample_record.get('Threat_Level', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"Data generation error: {e}")
        return False

if __name__ == "__main__":
    print("OTX Threat Intelligence Test Script")
    print("=" * 50)
    
    # Test file structure
    structure_ok = test_data_generation()
    
    if structure_ok:
        # Test data generation
        data_ok = test_simple_data_fetch()
        
        if data_ok:
            print("\nAll tests passed! Ready to run the main script.")
            print("Run: python otx_threat_intelligence.py")
        else:
            print("\nData generation test failed. Check your configuration.")
    else:
        print("\nFile structure test failed. Check your project setup.") 