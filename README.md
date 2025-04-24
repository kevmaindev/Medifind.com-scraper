# Medifind.com scraper

This script is designed to scrape doctor data based on specialty, city, and state from a specific website. It retrieves information such as latitude, longitude, and doctor details, and saves the data in JSON format.

## Requirements

- Python 3.x
- Libraries: `curl_cffi`, `rich`, `fake_useragent`

## Installation
 
1. **Clone the repository**:
   ```bash
   git clone https://github.com/kevmaindev/Medifind.com-scraper.git
   cd Medifind.com scraper
   ```

2. **Install the required libraries**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running the script, ensure you have the following:

- **API URLs**: Set the `placeId_url`, `lat_lon_url`, and `doctors_url` variables in the script to the appropriate API endpoints.
- **Specialties**: Add the specialties you want to scrape to the `specialties` list.
- **City and State**: Set the `city` and `state` variables to the desired location.

## Usage

Run the script using Python:

```bash
python scraper.py
```

The script will:

1. Create necessary directories to store the data.
2. Fetch latitude and longitude for the specified city and state.
3. Retrieve doctor data for each specialty.
4. Save the data in JSON files within the `DATA` directory.

## Data Storage

The data is stored in the following directory structure:

```
DATA/
└── STATE/
    └── CITY/
        └── SPECIALTY/
            └── physicians.json
```

## Notes

- **Rate Limiting**: The script includes a random delay between API requests to avoid being blocked. Adjust the `REQUEST_DELAY` variable as needed.
- **Error Handling**: The script includes basic error handling and will skip specialties that have already been processed.

## Example

To scrape data for cardiologists in New York City:

```python
city = 'New York'
state = 'NY'
specialties = ['Cardiology']
```

Run the script, and the data will be saved in `DATA/NY/New York/Cardiology/physicians.json`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or support, please contact me on github.

---

**Disclaimer**: This script is for educational purposes only. Ensure you comply with the terms of service of the website you are scraping.
