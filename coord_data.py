import re

# Path to your files
stadium_file = '/home/yasheerah/vlm_drone/stadium_coordinates.txt'
latlong_file = '/home/yasheerah/vlm_drone/lat_long_data.txt'

# Function to extract coordinates from the text data
def extract_coordinates(data):
    coords = {}
    current_img = None
    for line in data.splitlines():
        if 'Image' in line:
            # Extract image number
            current_img = int(re.search(r'Image: (\d+)', line).group(1))
            coords[current_img] = {}
        elif 'NW Corner Lat' in line:
            coords[current_img]['NW_Lat'] = float(re.search(r'NW Corner Lat: ([\d\-.]+)', line).group(1))
        elif 'NW Corner Long' in line:
            coords[current_img]['NW_Long'] = float(re.search(r'NW Corner Long: ([\d\-.]+)', line).group(1))
        elif 'SE Corner Lat' in line:
            coords[current_img]['SE_Lat'] = float(re.search(r'SE Corner Lat: ([\d\-.]+)', line).group(1))
        elif 'SE Corner Long' in line:
            coords[current_img]['SE_Long'] = float(re.search(r'SE Corner Long: ([\d\-.]+)', line).group(1))
    return coords

# Function to extract stadium points
def extract_stadium_points(data):
    points = {}
    for line in data.splitlines():
        match = re.match(r'(\d+),\s*<points (.*?)</points>', line)
        if match:
            img_num = int(match.group(1))
            points_str = match.group(2)
            coords = re.findall(r'x\d+="([\d.]+)"\s*y\d+="([\d.]+)"', points_str)
            points[img_num] = [(float(x), float(y)) for x, y in coords]
    return points

# Function to convert normalized points to lat/long
def convert_to_latlong(image_num, points, latlong_data):
    NW_Lat = latlong_data[image_num]['NW_Lat']
    NW_Long = latlong_data[image_num]['NW_Long']
    SE_Lat = latlong_data[image_num]['SE_Lat']
    SE_Long = latlong_data[image_num]['SE_Long']
    
    latlong_points = []
    for x, y in points:
        lat = NW_Lat - (y / 100) * (NW_Lat - SE_Lat)
        long = NW_Long + (x / 100) * (SE_Long - NW_Long)
        latlong_points.append((lat, long))
    
    return latlong_points

# Read files
with open(latlong_file, 'r') as file:
    latlong_data = extract_coordinates(file.read())

with open(stadium_file, 'r') as file:
    stadium_points = extract_stadium_points(file.read())

# Convert all points to lat/long
converted_data = {}
for img_num, points in stadium_points.items():
    converted_data[img_num] = convert_to_latlong(img_num, points, latlong_data)

# Output the converted coordinates
for img_num, coords in converted_data.items():
    print(f"Image {img_num}:")
    for lat, long in coords:
        print(f"Latitude: {lat}, Longitude: {long}")
