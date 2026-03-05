from PIL import Image
import numpy as np

class indoor_VLA_utils():

    def calculate_real_world_size(self, image_path, camera_height, diagonal_fov, aspect_ratio=(16,9)):
        image = Image.open(image_path)
        img_width_px, img_height_px = image.size
        
        # Convert diagonal FOV from degrees to radians
        diagonal_fov = np.deg2rad(diagonal_fov)

        # Compute horizontal and vertical FOV
        diagonal_ratio = np.sqrt(aspect_ratio[0]**2 + aspect_ratio[1]**2)
        horizontal_fov = 2 * np.arctan(np.tan(diagonal_fov / 2) * (aspect_ratio[0] / diagonal_ratio))
        vertical_fov = 2 * np.arctan(np.tan(diagonal_fov / 2) * (aspect_ratio[1] / diagonal_ratio))

        # Compute real-world dimensions in meters
        real_width_m = 2 * camera_height * np.tan(horizontal_fov / 2)
        real_height_m = 2 * camera_height * np.tan(vertical_fov / 2)

        # Compute pixel-to-meter ratios
        pixel_to_meter_x = real_width_m / img_width_px
        pixel_to_meter_y = real_height_m / img_height_px

        return {
            "image_width_px": img_width_px,
            "image_height_px": img_height_px,
            "real_world_width_m": real_width_m,
            "real_world_height_m": real_height_m,
            "pixel_to_meter_x": pixel_to_meter_x,
            "pixel_to_meter_y": pixel_to_meter_y
        }
    
    def process_coordinates(self, coordinates, diagonal_fov_degrees, altitude, image_metrics):
        """
        Process the input image and text file, converting normalized coordinates to Cartesian coordinates.
        Uses dynamically computed real-world image dimensions.
        """
        width_m = image_metrics["real_world_width_m"]
        height_m = image_metrics["real_world_height_m"]
        
        # Set x and y axis in meters
        x_axis = height_m / 2
        y_axis = width_m / 2
        
        # Define Cartesian coordinate system bounds
        NW_Lat = -y_axis
        NW_Long = -x_axis
        SE_Lat = y_axis
        SE_Long = x_axis

        coords = []
        names = []
        
        # Extract coordinates and names from the input dictionary
        for name, data in coordinates.items():
            if 'coordinates' in data:
                coords.append(data['coordinates'])
                names.append(name)
        
        num_coords = len(coords)
        object_coordinates = {}

        for i in range(num_coords):
            normalized_x = float(coords[i][0])
            normalized_y = float(coords[i][1])
            
            # Convert normalized coordinates to Cartesian
            cartesian_y = NW_Lat - (normalized_x / 100) * (NW_Lat - SE_Lat)
            cartesian_x = NW_Long + (normalized_y / 100) * (SE_Long - NW_Long)
            
            object_coordinates[names] = {
                'type': 'three legs of red tripod stands',
                'coordinates': [cartesian_x, cartesian_y]
            }

        return object_coordinates