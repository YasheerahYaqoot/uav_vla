import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Radius of Earth in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_trajectory(file_path):
    with open(file_path, 'r') as file:
        total_trajectory_lengths = {}
        current_image = None
        coordinates = []

        for line in file:
            line = line.strip()

            if line.startswith("Image"):
                if current_image and coordinates:
                    total_length = 0
                    for i in range(len(coordinates) - 1):
                        lat1, lon1 = coordinates[i]
                        lat2, lon2 = coordinates[i + 1]
                        total_length += haversine(lat1, lon1, lat2, lon2)
                    total_trajectory_lengths[current_image] = total_length
                current_image = line.rstrip(':')
                coordinates = []

            elif "Latitude" in line:
                lat = float(line.split(":")[1].strip())
                coordinates.append((lat, coordinates[-1][1] if coordinates else None))
            elif "Longitude" in line:
                lon = float(line.split(":")[1].strip())
                coordinates[-1] = (coordinates[-1][0], lon)

        if current_image and coordinates:
            total_length = 0
            for i in range(len(coordinates) - 1):
                lat1, lon1 = coordinates[i]
                lat2, lon2 = coordinates[i + 1]
                total_length += haversine(lat1, lon1, lat2, lon2)
            total_trajectory_lengths[current_image] = total_length

    return total_trajectory_lengths

def trajectory_results(file1, file2, output_file, total_images=30):
    mp_lengths = calculate_trajectory(file1)
    vlm_lengths = calculate_trajectory(file2)

    with open(output_file, 'w') as file:
        for i in range(1, total_images + 1):
            image = f"Image {i}"
            mp_length = mp_lengths.get(image, 0)
            vlm_length = vlm_lengths.get(image, 0)
            file.write(f"{image}:\n")
            file.write(f"Trajectory length from VLM: {vlm_length:.2f} km\n")
            file.write(f"Trajectory length from MP: {mp_length:.2f} km\n\n")


mp_file = "mp_coordinates.txt"
vlm_file = "VLM_coordinates.txt"
output_file = "traj_length.txt"

trajectory_results(mp_file, vlm_file, output_file)
print("Trajectory lengths written to traj_length.txt.")
