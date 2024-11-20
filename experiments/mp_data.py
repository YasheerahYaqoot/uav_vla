import os

input_directory = '/home/yasheerah/uav_vla/experiments/mission_planner_data/waypoints/'
output_txt = '/home/yasheerah/uav_vla/experiments/mp_coordinates.txt'

output_content = ""

def extract_number(filename):
    return int(filename.split('.')[0])

# Loop over each file in numerical order
for idx, filename in enumerate(sorted(os.listdir(input_directory), key=extract_number), start=1):
    if filename.endswith('.waypoints'):
        file_path = os.path.join(input_directory, filename)

        with open(file_path, 'r') as file:
            waypoints_data = file.readlines()

        output_content += f"Image {idx}:\n"

        home_line = waypoints_data[1].strip().split('\t')
        home_lat = home_line[8]
        home_lon = home_line[9]
        
        output_content += "  Home Position:\n"
        output_content += f"    Latitude: {home_lat}\n"
        output_content += f"    Longitude: {home_lon}\n"

        for building_idx, line in enumerate(waypoints_data[2:], start=1):
            building_data = line.strip().split('\t')
            building_lat = building_data[8]
            building_lon = building_data[9]
            output_content += f"  Building {building_idx}:\n"
            output_content += f"    Latitude: {building_lat}\n"
            output_content += f"    Longitude: {building_lon}\n"

        output_content += "\n"

with open(output_txt, 'w') as f:
    f.write(output_content)

print("Data has been saved to", output_txt)
