import numpy as np
from scipy.spatial import cKDTree
from scipy.interpolate import interp1d
from fastdtw import fastdtw
from math import radians, sin, cos, sqrt, atan2
import re

# Haversine distance between two GPS points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

def parse_coordinates(filename):
    coordinates = {}
    with open(filename, 'r') as file:
        data = file.read()
    
    images = re.split(r'Image \d+\:', data)  
    for i, image_data in enumerate(images[1:], 1):
        image_name = f"Image {i}.jpg"
        coords = []
        matches = re.findall(r'Latitude: ([\d.-]+)\s+Longitude: ([\d.-]+)', image_data)
        
        for match in matches:
            lat, lon = float(match[0]), float(match[1])
            coords.append((lat, lon))
        
        coordinates[image_name] = coords
    
    return coordinates

## -----------------------------INTERPOLATION METHOD --------------------------------------------------------------------
def interpolate_path(path, num_points):
    lats, lons = zip(*path)
    x = np.linspace(0, 1, len(path))
    x_interp = np.linspace(0, 1, num_points)
    
    lat_interp = interp1d(x, lats, kind='linear')(x_interp)
    lon_interp = interp1d(x, lons, kind='linear')(x_interp)
    
    return list(zip(lat_interp, lon_interp))

## -----------------------------DTW METHOD FOR MSE AND RMSE ---------------------------------------------------------------------
def compute_dtw_mse_rmse(trajectory1, trajectory2):
    distance, path = fastdtw(trajectory1, trajectory2, dist=lambda x, y: haversine(x[0], x[1], y[0], y[1]))
    squared_errors = [haversine(trajectory1[i][0], trajectory1[i][1], trajectory2[j][0], trajectory2[j][1])**2 for i, j in path]
    mse = np.mean(squared_errors)
    rmse = np.sqrt(mse)
    return mse, rmse


mp_coordinates = parse_coordinates('mp_coordinates.txt')
vlm_coordinates = parse_coordinates('VLM_coordinates.txt')

# For writing in text file
with open("rmse.txt", "w") as file:
    for image in mp_coordinates.keys():
        if image in vlm_coordinates:
            mp_path = mp_coordinates[image]
            vlm_path = vlm_coordinates[image]
            
            if mp_path and vlm_path:
                reference_point = mp_path[0] 
                mse_dtw, rmse_dtw = compute_dtw_mse_rmse(mp_path, vlm_path)
                num_points = max(len(mp_path), len(vlm_path))
                mp_path_interp = interpolate_path(mp_path, num_points)
                vlm_path_interp = interpolate_path(vlm_path, num_points)
                squared_errors_interp = [haversine(lat1, lon1, lat2, lon2)**2 for (lat1, lon1), (lat2, lon2) in zip(mp_path_interp, vlm_path_interp)]
                mse_interp = np.mean(squared_errors_interp)
                rmse_interp = np.sqrt(mse_interp)
                file.write(f"\nResults for {image}:\n")
                file.write(f"DTW-based Root Mean Squared Error (RMSE): {rmse_dtw:.6f} km\n")
                file.write(f"Interpolation-based Root Mean Squared Error (RMSE): {rmse_interp:.6f} km\n")
            else:
                file.write(f"Error: Path for {image} is empty in one of the files.\n")
        else:
            file.write(f"Path for {image} not found in both files.\n")

# # For printing the data in terminal
# for image in mp_coordinates.keys():
#     if image in vlm_coordinates:
#         mp_path = mp_coordinates[image]
#         vlm_path = vlm_coordinates[image]
        
#         if mp_path and vlm_path:
#             reference_point = mp_path[0] 
#             mse_dtw, rmse_dtw = compute_dtw_mse_rmse(mp_path, vlm_path)
#             num_points = max(len(mp_path), len(vlm_path))
#             mp_path_interp = interpolate_path(mp_path, num_points)
#             vlm_path_interp = interpolate_path(vlm_path, num_points)
#             squared_errors_interp = [haversine(lat1, lon1, lat2, lon2)**2 for (lat1, lon1), (lat2, lon2) in zip(mp_path_interp, vlm_path_interp)]
#             mse_interp = np.mean(squared_errors_interp)
#             rmse_interp = np.sqrt(mse_interp)
#             print(f"\nResults for {image}:")
#             # print(f"DTW-based Mean Squared Error (MSE): {mse_dtw:.6f} km^2")
#             print(f"DTW-based Root Mean Squared Error (RMSE): {rmse_dtw:.6f} km\n")
#             print(f"Interpolation-based Root Mean Squared Error (RMSE): {rmse_interp:.6f} km\n")
#         else:
#             print(f"Error: Path for {image} is empty in one of the files.")
#     else:
#         print(f"Path for {image} not found in both files.")