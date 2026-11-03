import os
import time
import pandas as pd
import requests

# 1. Complete Array of 50 Sub-Regional Coordinates across 10 Metropolitan Hubs
SUBREGION_COORDINATES = [
    {"city": "Delhi", "sub_region": "Central", "lat": 28.6139, "lon": 77.2090}, # Connaught Place
    {"city": "Delhi", "sub_region": "North", "lat": 28.7041, "lon": 77.1025},   # Rohini
    {"city": "Delhi", "sub_region": "South", "lat": 28.5355, "lon": 77.2610},   # Okhla / Saket
    {"city": "Delhi", "sub_region": "East", "lat": 28.6280, "lon": 77.2950},    # Laxmi Nagar
    {"city": "Delhi", "sub_region": "West", "lat": 28.6369, "lon": 77.0895},    # Janakpuri
    {"city": "Mumbai", "sub_region": "Central", "lat": 19.0760, "lon": 72.8777},# Dadar
    {"city": "Mumbai", "sub_region": "North", "lat": 19.2183, "lon": 72.9781},  # Thane / Borivali
    {"city": "Mumbai", "sub_region": "South", "lat": 18.9220, "lon": 72.8347},  # Nariman Point
    {"city": "Mumbai", "sub_region": "East", "lat": 19.0473, "lon": 72.8893},   # Chembur
    {"city": "Mumbai", "sub_region": "West", "lat": 19.1176, "lon": 72.8461},   # Andheri West
    {"city": "Bangalore", "sub_region": "Central", "lat": 12.9716, "lon": 77.5946}, # MG Road
    {"city": "Bangalore", "sub_region": "North", "lat": 13.0827, "lon": 77.5877},   # Yelahanka
    {"city": "Bangalore", "sub_region": "South", "lat": 12.8399, "lon": 77.6770},   # Electronic City
    {"city": "Bangalore", "sub_region": "East", "lat": 12.9698, "lon": 77.7500},    # Whitefield
    {"city": "Bangalore", "sub_region": "West", "lat": 12.9784, "lon": 77.5463},    # Rajajinagar
    {"city": "Hyderabad", "sub_region": "Central", "lat": 17.3850, "lon": 78.4867}, # Abids
    {"city": "Hyderabad", "sub_region": "North", "lat": 17.5020, "lon": 78.4800},   # Secunderabad / Kompally
    {"city": "Hyderabad", "sub_region": "South", "lat": 17.2403, "lon": 78.4294},   # Shamshabad
    {"city": "Hyderabad", "sub_region": "East", "lat": 17.3688, "lon": 78.5307},    # Uppal
    {"city": "Hyderabad", "sub_region": "West", "lat": 17.4435, "lon": 78.3772},    # HITEC City
    {"city": "Chennai", "sub_region": "Central", "lat": 13.0827, "lon": 80.2707},   # George Town
    {"city": "Chennai", "sub_region": "North", "lat": 13.1500, "lon": 80.3000},     # Ennore / Madhavaram
    {"city": "Chennai", "sub_region": "South", "lat": 12.9719, "lon": 80.2500},     # OMR IT Corridor
    {"city": "Chennai", "sub_region": "East", "lat": 13.0400, "lon": 80.2800},      # Mylapore
    {"city": "Chennai", "sub_region": "West", "lat": 13.0878, "lon": 80.2100},      # Anna Nagar
    {"city": "Kolkata", "sub_region": "Central", "lat": 22.5726, "lon": 88.3639},   # Esplanade
    {"city": "Kolkata", "sub_region": "North", "lat": 22.6500, "lon": 88.3700},     # Dum Dum
    {"city": "Kolkata", "sub_region": "South", "lat": 22.4800, "lon": 88.3600},     # Garia / Jadavpur
    {"city": "Kolkata", "sub_region": "East", "lat": 22.5800, "lon": 88.4500},      # Salt Lake / New Town
    {"city": "Kolkata", "sub_region": "West", "lat": 22.5900, "lon": 88.3100},      # Howrah
    {"city": "Ahmedabad", "sub_region": "Central", "lat": 23.0225, "lon": 72.5714}, # Ashram Road
    {"city": "Ahmedabad", "sub_region": "North", "lat": 23.1000, "lon": 72.5800},   # Chandkheda
    {"city": "Ahmedabad", "sub_region": "South", "lat": 22.9800, "lon": 72.5900},   # Maninagar
    {"city": "Ahmedabad", "sub_region": "East", "lat": 23.0300, "lon": 72.6300},    # Naroda
    {"city": "Ahmedabad", "sub_region": "West", "lat": 23.0300, "lon": 72.5000},    # SG Highway
    {"city": "Pune", "sub_region": "Central", "lat": 18.5204, "lon": 73.8567},      # Shivajinagar
    {"city": "Pune", "sub_region": "North", "lat": 18.6200, "lon": 73.8100},        # Pimpri Chinchwad
    {"city": "Pune", "sub_region": "South", "lat": 18.4500, "lon": 73.8500},        # Katraj
    {"city": "Pune", "sub_region": "East", "lat": 18.5600, "lon": 73.9100},         # Viman Nagar / Kharadi
    {"city": "Pune", "sub_region": "West", "lat": 18.5600, "lon": 73.7700},         # Hinjewadi
    {"city": "Jaipur", "sub_region": "Central", "lat": 26.9124, "lon": 75.7873},    # Pink City
    {"city": "Jaipur", "sub_region": "North", "lat": 26.9800, "lon": 75.8000},      # Amber Zone
    {"city": "Jaipur", "sub_region": "South", "lat": 26.8300, "lon": 75.8000},      # Sanganer
    {"city": "Jaipur", "sub_region": "East", "lat": 26.9000, "lon": 75.8500},       # Malviya Nagar
    {"city": "Jaipur", "sub_region": "West", "lat": 26.9200, "lon": 75.7300},       # Vaishali Nagar
    {"city": "Lucknow", "sub_region": "Central", "lat": 26.8467, "lon": 80.9462},   # Hazratganj
    {"city": "Lucknow", "sub_region": "East", "lat": 26.8600, "lon": 81.0200},      # Gomti Nagar Extension
    {"city": "Lucknow", "sub_region": "South", "lat": 26.7500, "lon": 80.8800},     # Amausi / Airport Zone
    {"city": "Lucknow", "sub_region": "North", "lat": 26.9200, "lon": 80.9500},     # Jankipuram
    {"city": "Lucknow", "sub_region": "West", "lat": 26.8300, "lon": 80.8800},      # Rajajipuram
]

def fetch_subregion_climate_grid(
    coords_list=SUBREGION_COORDINATES,
    start_date="2020-01-01",
    end_date="2024-12-31",
) -> pd.DataFrame:
    """Loops through all 50 sub-regional coordinates, fetches live historical daily weather metrics
    from the Open-Meteo API, and saves the output to data/micro_intracity_grid.csv.
    """
    records = []
    print(f"[INFO] Fetching live API data for {len(coords_list)} sub-regional zones...")
    
    for idx, item in enumerate(coords_list, start=1):
        url = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={item['lat']}&longitude={item['lon']}&"
            f"start_date={start_date}&end_date={end_date}&"
            f"daily=temperature_2m_max,apparent_temperature_max,precipitation_sum,wind_speed_10m_max&"
            f"timezone=Asia/Kolkata"
        )
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()["daily"]
                df_temp = pd.DataFrame(data)
                
                # Attach location metadata to match required schema
                df_temp["city"] = item["city"]
                df_temp["sub_region"] = item["sub_region"]
                df_temp["lat"] = item["lat"]
                df_temp["lon"] = item["lon"]
                
                records.append(df_temp)
                print(f"[{idx}/{len(coords_list)}] Successfully fetched: {item['city']} ({item['sub_region']} Zone)")
            else:
                print(f"[WARNING] [{idx}/{len(coords_list)}] Received status {response.status_code} for {item['city']} ({item['sub_region']})")
        except Exception as e:
            print(f"[ERROR] [{idx}/{len(coords_list)}] Failed API request for {item['city']} ({item['sub_region']}): {e}")
        
        # Pause 0.2 seconds between calls to respect Open-Meteo rate limits
        time.sleep(0.2)
        
    if not records:
        raise ValueError("No API data was retrieved. Check internet connection or API availability.")
        
    # Combine all 50 individual location dataframes into one master grid
    micro_df = pd.concat(records, ignore_index=True)
    
    # Save directly to the path expected by Module 3, 4, 5, and 6
    os.makedirs("data/processed", exist_ok=True)
    output_path = "data/processed/micro_intracity_grid.csv"
    micro_df.to_csv(output_path, index=False)
    
    print(f"[COMPLETE] Micro-grid dataset compiled with {len(micro_df)} rows and stored at '{output_path}'.")
    return micro_df

if __name__ == "__main__":
    fetch_subregion_climate_grid()