import os
import cv2
import re

# Step 1: Create a folder to save identified images if it doesn't exist
output_folder = 'identified_images'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Path to the folder containing your images
image_folder = '/home/yasheerah/vlm_drone/dataset_images'  # Replace with your image folder path

# Path to the text file containing the coordinates
text_file_path = '/home/yasheerah/vlm_drone/stadium_coordinates.txt'  # Replace with your text file path

# Regular expression to extract coordinates from the text
coord_pattern = re.compile(r'x(\d+)="([\d.]+)" y(\d+)="([\d.]+)"')

# Step 2: Read the text file and process each line
with open(text_file_path, 'r') as file:
    lines = file.readlines()

for line in lines:
    # Step 3: Extract the image number and stadium data
    parts = line.strip().split(',', 1)
    image_num = parts[0].strip()
    stadium_data = parts[1].strip()

    # Check if there are stadiums in the image
    if 'There are none' in stadium_data:
        continue  # Skip images without stadiums

    # Load the corresponding image
    image_path = os.path.join(image_folder, f'{image_num}.jpg')
    image = cv2.imread(image_path)

    if image is None:
        print(f"Warning: Image {image_num}.jpg not found!")
        continue

    # Get the image dimensions (width, height)
    height, width, _ = image.shape

    # Step 4: Extract stadium coordinates from the stadium data
    stadium_coords = coord_pattern.findall(stadium_data)

    # Convert the coordinates to pixel values and mark them on the image
    for coord in stadium_coords:
        x_normalized = float(coord[1])
        y_normalized = float(coord[3])

        # Convert normalized coordinates to pixel coordinates
        x_pixel = int(x_normalized * width / 100)
        y_pixel = int(y_normalized * height / 100)

        # Draw a circle at the stadium location
        cv2.circle(image, (x_pixel, y_pixel), radius=10, color=(0, 0, 255), thickness=2)

    # Step 5: Save the modified image to the 'identified_images' folder
    output_image_path = os.path.join(output_folder, f'{image_num}_identified.jpg')
    cv2.imwrite(output_image_path, image)
    print(f"Stadiums marked in image {image_num}.jpg and saved as {output_image_path}")
