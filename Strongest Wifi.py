import pywifi
import json

def scan_wifi():
    wifi_dict = {}  # Use a dictionary to store WiFi networks with MAC address as the key

    try:
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

    except Exception as e:
        return f"Error: {str(e)}"

    if not wifi_dict:
        return "No WiFi networks found."

    # Sort the dictionary by signal strength in descending order
    sorted_wifi = sorted(wifi_dict.items(), key=lambda x: x[1]["signal_strength"], reverse=True)

    # Take the top 2 networks with the strongest signal strength
    top_2_networks = sorted_wifi[:2]

    # Create a dictionary to store the top 2 networks with MAC addresses as keys
    top_2_dict = {mac: network for mac, network in top_2_networks}

    # Write the WiFi details of the top 2 networks to a JSON file
    with open('strongest_wifi.json', 'w') as json_file:
        json.dump(top_2_dict, json_file)

    return "Top 2 Networks:\n" + "\n".join([f"SSID: {network['ssid']}, Signal Strength: {network['signal_strength']} dBm" for mac, network in top_2_networks])

# Call the scan_wifi function to scan for WiFi networks and write the result to the JSON file
result = scan_wifi()
print(result)  # Print the result for testing
