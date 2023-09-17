import pywifi
import json

# Function to load Arduino data from the database JSON file
def load_database_data(filename):
    try:
        with open(filename, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print("Database file not found.")
        return {}

# Function to write Arduino data to a JSON file
def write_arduino_data_to_json(arduino_info):
    filename = "react.json"
    with open(filename, 'w') as json_file:
        json.dump(arduino_info, json_file, indent=4)

# Function to scan WiFi networks and access load cells
def scan_wifi_and_access_load_cells(database_filename):
    try:
        wifi_dict = {}  # Use a dictionary to store WiFi networks with MAC address as the key
        strongest_network = None

        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]  # Select the first WiFi interface

        iface.scan()
        scan_results = iface.scan_results()

        for result in scan_results:
            ssid = result.ssid
            mac_address = result.bssid  # Use MAC address as the key
            signal_strength = result.signal

            wifi_dict[mac_address] = {
                "ssid": ssid,
                "signal_strength": signal_strength
            }

        # Find the network with the strongest signal
        strongest_mac = max(wifi_dict, key=lambda k: wifi_dict[k]["signal_strength"])
        strongest_network = wifi_dict[strongest_mac]

        if not strongest_network:
            print("No WiFi networks found.")
        else:
            # Check if the strongest MAC address is in the database
            database_data = load_database_data(database_filename)
            if strongest_mac in database_data:
                arduino_info = database_data[strongest_mac]
                
                # Update the WiFi strength with the latest value
                arduino_info["wifi-strength"] = strongest_network["signal_strength"]
                
                # Include the MAC address in the Arduino data
                arduino_info["mac-address"] = strongest_mac
                
                # Write the combined Arduino data to the "react.json" file
                write_arduino_data_to_json(arduino_info)
                
                print(f"Strongest Network: {strongest_network['ssid']} ({strongest_network['signal_strength']} dBm)")
                print(f"Arduino Name: {arduino_info['name']}")
                print(f"Latest WiFi strength and MAC address written to 'react.json'.")
            else:
                print(f"Strongest Network: {strongest_network['ssid']} ({strongest_network['signal_strength']} dBm)")
                print("Arduino not found in database.")
                
    except Exception as e:
        print(f"Error: {str(e)}")

# Call the scan_wifi_and_access_load_cells function to run it
scan_wifi_and_access_load_cells('database.json')
