import os
import re
from PIL import Image, ImageDraw

# # For MP (Uncomment this to get images of Mission Planner data)
# input_folder = "../benchmark-UAV-VLPA-nano-30/images"
# output_folder = "../benchmark-UAV-VLPA-nano-30/identified_images_mp"
# coordinate_file = "mp_coordinates.txt"
# latlong_file = "../benchmark-UAV-VLPA-nano-30/img_lat_long_data.txt"

# For VLM (Comment this for MP data results)
input_folder = "../benchmark-UAV-VLPA-nano-30/images"
output_folder = "identified_images_VLM"
coordinate_file = "VLM_coordinates.txt"
latlong_file = "../benchmark-UAV-VLPA-nano-30/img_lat_long_data.txt"

os.makedirs(output_folder, exist_ok=True)

def extract_coordinates(file_path):
    """Extract latitude/longitude bounds for each image from the file."""
    coords = {}
    current_img = None
    with open(file_path, 'r') as f:
        data = f.read()
    for line in data.splitlines():
        if 'Image' in line:
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

def parse_coordinates(file_path, image_name):
    """Parse coordinates for the given image from the coordinates file."""
    coordinates = []
    with open(file_path, 'r') as file:
        current_image = None
        for line in file:
            line = line.strip()
            if line.startswith("Image"):
                current_image = line.rstrip(':').split()[1] 
            elif current_image == image_name and "Latitude" in line:
                lat = float(line.split(":")[1].strip())
                coordinates.append((lat, coordinates[-1][1] if coordinates else None))
            elif current_image == image_name and "Longitude" in line:
                lon = float(line.split(":")[1].strip())
                coordinates[-1] = (coordinates[-1][0], lon)
    return coordinates

def normalize_coordinates(points, image_size, coord_bounds):
    """Normalize latitude/longitude to image dimensions."""
    print(coord_bounds)
    min_lat, max_lat, min_lon, max_lon = coord_bounds
    width, height = image_size

    normalized = [
        (
            int((lon - min_lon) / (max_lon - min_lon) * (width - 1)),
            height - int((lat - min_lat) / (max_lat - min_lat) * (height - 1))
        )
        for lat, lon in points
    ]
    return normalized

def process_images(input_folder, output_folder, coordinate_file, latlong_file):
    """Process all images in the input folder."""
    latlong_data = extract_coordinates(latlong_file)

    for image_file in os.listdir(input_folder):

        image_id = int(image_file.split(".")[0])
        coordinates = parse_coordinates(coordinate_file, f"{image_id}")

        if image_id not in latlong_data:
            print(f"Skipping {image_file}: Missing lat/long data.")
            continue

        latlong_bounds = latlong_data[image_id]
        coord_bounds = (latlong_bounds["SE_Lat"], latlong_bounds["NW_Lat"],
                        latlong_bounds["NW_Long"], latlong_bounds["SE_Long"])

        image_path = os.path.join(input_folder, image_file)
        image = Image.open(image_path).convert("RGBA")
        draw = ImageDraw.Draw(image)

        image_size = image.size
        normalized_points = normalize_coordinates(coordinates, image_size, coord_bounds)

        # # Draw lines and points for MP (Uncomment this to get images of Mission Planner data)
        # draw.line(normalized_points, fill="blue", width=3)
        # for i, (x, y) in enumerate(normalized_points):
        #     color = "red" if i == 0 else "green"
        #     label = "Home" if i == 0 else f"B{i}"
        #     draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=color, outline="black")
        #     draw.text((x + 5, y), label, fill="yellow")

        # Draw lines and points for VLM (Comment this for MP data)
        draw.line(normalized_points, fill="yellow", width=3)
        for i, (x, y) in enumerate(normalized_points):
            color = "red" if i == 0 else "green"
            label = "Home" if i == 0 else f"B{i}"
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=color, outline="black")
            draw.text((x + 5, y), label, fill="purple")

        rgb_image = image.convert("RGB")
        output_path = os.path.join(output_folder, image_file)
        rgb_image.save(output_path, "JPEG")
        print(f"Processed and saved {image_file}")

process_images(input_folder, output_folder, coordinate_file, latlong_file)
