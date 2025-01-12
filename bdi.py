import webbrowser
import time
import pandas as pd
import os
import requests
import re
from urllib.parse import urlparse, parse_qs
from typing import Tuple, Optional
import pyperclip 

def extract_lat_lng_from_google_maps(url: str) -> Tuple[Optional[float], Optional[float]]:
    """Extract coordinates from various Google Maps URL formats."""
    # Handle clipboard input if no URL provided
    if not url:
        url = pyperclip.paste()
        if not ('google.com/maps' in url):
            return None, None
        print("Using URL from clipboard")
    
    # First try the @lat,lng format
    match = re.search(r'@([-\d.]+),([-\d.]+)', url)
    if match:
        return float(match.group(1)), float(match.group(2))
    
    # Try the ll=lat,lng format
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if 'll' in query_params:
        try:
            lat, lng = query_params['ll'][0].split(',')
            return float(lat), float(lng)
        except (ValueError, IndexError):
            return None, None
            
    return None, None

def get_postcode_from_coords(lat: float, lng: float) -> Optional[str]:
    """Get nearest postcode from coordinates using postcodes.io API."""
    url = f"https://api.postcodes.io/postcodes?lon={lng}&lat={lat}"
    
    try:
        response = requests.get(url, timeout=5)  # Added timeout
        response.raise_for_status()  # Raise exception for bad status codes
        
        data = response.json()
        if data['result'] and len(data['result']) > 0:
            postcode = data['result'][0]['postcode']
            return postcode
        else:
            print("No postcode found for these coordinates")
    except requests.exceptions.Timeout:
        print("API request timed out")
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    
    return None

def process_input(user_input: str) -> Optional[str]:
    """Process user input - either postcode or Google Maps URL."""
    # If empty input, try clipboard
    if not user_input.strip():
        user_input = pyperclip.paste()
        print("Using clipboard content")
    
    # Check if input is a Google Maps URL
    if 'google.com/maps' in user_input:
        lat, lng = extract_lat_lng_from_google_maps(user_input)
        if lat and lng:
            return get_postcode_from_coords(lat, lng)
        else:
            print("Could not extract coordinates from URL")
            return None
    
    # If not a URL, validate postcode format
    postcode = user_input.strip().upper()
    if re.match(r'^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$', postcode):
        return postcode
    else:
        print("Invalid postcode format")
        return None

def load_optimized_csv():
    """Load and optimize the postcodes CSV file."""
    columns_needed = ['pcds', 'oa21cd']
    dtype_dict = {
        'pcds': 'string',
        'oa21cd': 'string'
    }
    
    # Look for postcodes.csv in the same directory as this script
    csv_path = os.path.join(os.path.dirname(__file__), 'postcodes.csv')
    
    if not os.path.exists(csv_path):
        print(f"Error: Cannot find postcodes.csv at {csv_path}")
        print("Please ensure postcodes.csv is in the same directory as bdi.py")
        return None
        
    print("Loading postcode database...")
    try:
        df = pd.read_csv(csv_path, 
                        usecols=columns_needed,
                        dtype=dtype_dict,
                        encoding='latin1')
        df['clean_pcd'] = df['pcds'].str.replace(" ", "").str.upper()
        return df
    except Exception as e:
        print(f"Error loading CSV: {str(e)}")
        return None

def get_oa_from_postcode(postcode, df):
    """Get Output Area code for a postcode."""
    # Remove spaces and convert to uppercase
    postcode = postcode.replace(" ", "").upper()
    
    # Look up the postcode
    result = df[df['clean_pcd'] == postcode]
    
    if len(result) == 0:
        raise Exception(f"Postcode {postcode} not found in dataset")
    
    # Get the OA code
    oa_code = result.iloc[0]['oa21cd']
    print(f"Found Output Area code: {oa_code}")
    return oa_code

def open_ons_maps(postcode, df):
    try:
        oa_code = get_oa_from_postcode(postcode, df)
        
        # Format postcode for URL (replace spaces with +)
        url_postcode = postcode.replace(" ", "+").lower()
        
        # Base URLs for all visualizations
        urls = [
            f"https://find-energy-certificate.service.gov.uk/find-a-certificate/search-by-postcode?postcode={url_postcode}",
            f"https://www.ons.gov.uk/census/maps/choropleth/identity/ethnic-group/ethnic-group-tb-6a/white?oa={oa_code}",
            f"https://www.ons.gov.uk/census/maps/choropleth/population/household-deprivation/hh-deprivation/household-is-not-deprived-in-any-dimension?oa={oa_code}",
            f"https://www.ons.gov.uk/census/maps/choropleth/housing/tenure-of-household/hh-tenure-5a/rented-social-rented?oa={oa_code}"
        ]
        
        # Open each URL in a new tab
        for url in urls:
            webbrowser.open_new_tab(url)
            
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    """Main program loop."""
    df = load_optimized_csv()
    if df is None:
        return
    
    print("\nBDI - British Deprivation Index Lookup")
    print("--------------------------------------")
    print("Enter a postcode, Google Maps URL, or press Enter to use clipboard")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("\nEnter postcode or URL (or 'quit'): ").strip()
            
            if user_input.lower() == 'quit':
                break
                
            postcode = process_input(user_input)
            if postcode:
                print(f"Opening maps for postcode: {postcode}")
                open_ons_maps(postcode, df)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
