import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration settings
CSV_OUTPUT_FILE = 'live_cyberattacks.csv'

# Default coordinates (San Francisco)
DEFAULT_LATITUDE = 37.7749
DEFAULT_LONGITUDE = -122.4194

# Data generation settings
DEFAULT_NUM_RECORDS = 500
DEFAULT_API_KEY = 'demo_key_for_github' 