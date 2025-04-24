import json
import random
import sys
import time  
from typing import Dict, List
from curl_cffi import requests
from rich import print
from fake_useragent import UserAgent
from format_json import all_docs
import os


city_input = input("Enter the city (ie ..'Columbus'): ")
state_input = input("Enter the state (abbreviation)(ie ..'OH'): ")


city = city_input.strip().title()  
state = state_input.strip().upper()  



specialties = ["Internal Medicine","Family Medicine"]  # Add more specialties as needed

Data_folder = 'DATA'
data_city_dir = f'{Data_folder}/{state}/{city}'
os.makedirs(data_city_dir, exist_ok=True)

placeId_url = 'https://www.medifind.com/api/autocomplete/location'
lat_lon_url = 'https://www.medifind.com/api/location/search/geoPlace'
doctors_url = 'https://www.medifind.com/api/search/doctors/specialtySearch'

# Delay between API requests in seconds
REQUEST_DELAY = random.uniform(3,8)  # Adjust this value as needed

def get_headers(specialty):
    referer_url = f'https://www.medifind.com/specialty/{specialty}/US/{state}/{city}'
    return {
            'User-Agent': UserAgent().random,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            #'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': referer_url,
            'Content-Type': 'application/json',
            'Authorization': 'null',
            'DNT': '1',
            'Sec-GPC': '1',
            'Alt-Used': 'www.medifind.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=4',
        }

def get_placeId(specialty):
    headers = get_headers(specialty)

    params = {
        'input': f'{city}, {state}, US',
    }
    try:
        response = requests.get(placeId_url, params=params, headers=headers, timeout=100000)
        response.raise_for_status()  # Raise an error for bad status codes
    except Exception as e:
        print(f"Error in get_placeId: {str(e)}")
        return None

    placeid = response.json()['predictions'][0].get('value')
    return placeid

def get_lat_lon(specialty):
    headers = get_headers(specialty)
    params = {
        'placeId': get_placeId(specialty),
    }
    try:
        response = requests.get(lat_lon_url, params=params, headers=headers, timeout=100000)
        response.raise_for_status()  # Raise an error for bad status codes
    except Exception as e:
        print(f"Error in get_lat_lon: {str(e)}")
        return None

    lat, lon = response.json()['result'].get('lat'), response.json()['result'].get('lon')
    return lat, lon

def get_doctors(size, state, specialty, lat, lon, page=1):
    headers = get_headers(specialty)

    json_data = {
        'specialty': [specialty,],
        'radius': 'state',
        'lat': lat,
        'lon': lon,
        'country': 'US',
        'state': state,
        'fidelity': 3,
        'languages': [],
        'size': size,
        'page': page,
        'sort': 'relevance',
        'gender': None,
        'doctorYearsExperience': 0,
        'type': 'specialtySearch',
        'showFeaturedCards': True,
        'telemedicine': False,
        'acceptsNewPatients': False,
        'appointmentAssistOptIn': False,
    }
    try:
        response = requests.post(doctors_url, headers=headers, json=json_data, timeout=100000)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except Exception as e:
        print(f"Error in get_doctors: {str(e)}")
        return None

def write_data(data: List[Dict], data_json_file: str):
    """Write all data to the JSON file in a line format"""
    try:
        with open(data_json_file, 'w', encoding='utf-8') as f:
            f.write('[\n')
            for i, item in enumerate(data):
                json_str = json.dumps(item, ensure_ascii=False)
                if i < len(data) - 1:
                    json_str += ','
                f.write(json_str + '\n')
            f.write(']')
    except Exception as e:
        print(f"Error writing data to file: {str(e)}")
        raise

def append_data(data: List[Dict], data_json_file: str):
    """Append data to the JSON file using the write_data function"""
    try:
        # Read existing data if the file exists
        if os.path.exists(data_json_file):
            with open(data_json_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            existing_data.extend(data)  # Append new data
            write_data(existing_data, data_json_file)  # Write all data back in line format
        else:
            write_data(data, data_json_file)  # If file doesn't exist, create it
    except Exception as e:
        print(f"Error appending data to file: {str(e)}")
        raise

def main():
    for specialty in specialties:
        specialty_dir = f'{data_city_dir}/{specialty}'
        os.makedirs(specialty_dir, exist_ok=True)
        data_json_file = f'{specialty_dir}/physicians.json'

        if os.path.exists(data_json_file):
            print(f"Specialty {specialty} already processed. Skipping...")
            continue

        lat, lon = get_lat_lon(specialty)
        if lat is None or lon is None:
            print(f"Failed to get latitude and longitude for {specialty}.")
            continue

        # Add delay before making the next API request
        time.sleep(REQUEST_DELAY)

        initial_size = 0
        json_data = get_doctors(initial_size, state, specialty, lat, lon)
        if json_data is None:
            print(f"Failed to get data for specialty {specialty}.")
            continue

        new_size = json_data.get('totalResults', 0)
        print(f"Total results for {specialty}: {new_size}")

        if new_size > 0:
            # Add delay before making the next API request
            time.sleep(REQUEST_DELAY)

            if new_size <= 2000:
                json_data = get_doctors(new_size, state, specialty, lat, lon, page=1)
                if json_data is not None:
                    docs = all_docs(json_data)
                    if docs:  # Ensure docs is not None or empty
                        write_data(docs, data_json_file)
                        print(f"Data for {specialty} saved to {data_json_file}")
                    else:
                        print(f"No valid data to save for {specialty}.")
                else:
                    print(f"Failed to retrieve data for {specialty} with updated size.")
            else:
                remaining_size = new_size
                page = 1
                while remaining_size > 0:
                    # Subtract a random number (e.g., between 1 and 10) from 2000 for each request
                    random_subtraction = random.randint(200,350)
                    request_size = min(2000 - random_subtraction, remaining_size)
                    
                    # Ensure request_size is at least 1 to avoid invalid requests
                    request_size = max(request_size, 1)
                    print(f"Request size for {specialty} page {page}: {request_size}")
                    
                    json_data = get_doctors(request_size, state, specialty, lat, lon, page=page)
                    if json_data is not None:
                        docs = all_docs(json_data)
                        if docs:  # Ensure docs is not None or empty
                            if page == 1:
                                write_data(docs, data_json_file)
                            else:
                                append_data(docs, data_json_file)
                            print(f"Data for {specialty} page {page} saved to {data_json_file}")
                        else:
                            print(f"No valid data to save for {specialty} page {page}.")
                    else:
                        print(f"Failed to retrieve data for {specialty} page {page}.")
                    
                    # Update remaining_size
                    remaining_size -= request_size
                    page += 1
                    time.sleep(REQUEST_DELAY)  # Add delay between requests
        else:
            print(f"No results found for {specialty}.")
        time.sleep(REQUEST_DELAY)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('Error:', e)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)