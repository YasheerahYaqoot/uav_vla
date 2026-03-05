from flask import Flask, request, send_file
import json
from PIL import Image
import os
import test_vla  # assuming output.py contains your processing code

app = Flask(__name__)

@app.route('/upload_mission', methods=['POST'])
def upload_mission():
    # Retrieve the image and the command string from the POST request.
    image_file = request.files.get('image')
    command_str = request.form.get('command', '')
    if image_file is None:
        return "No image provided", 400

    # Save the received image.
    received_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene.jpg")
    try:
        image = Image.open(image_file.stream)
        image.save(received_image_path)
        print("Image saved as", received_image_path)
    except Exception as e:
        return f"Error processing image: {str(e)}", 500

    # Print out the received command string.
    print("Received command:", command_str)
    # Optionally, if you need to convert it back to a dictionary:
    try:
        command_dict = json.loads(command_str)
    except Exception as e:
        return f"Error decoding command: {str(e)}", 400

    # Call your output.main() function, passing the image path and command.
    test_vla.main(received_image_path, command_dict)

    # Assume the output.main() function creates a mission file at a known path.
    base_path = os.path.dirname(os.path.abspath(__file__))
    mission_file_path = os.path.join(base_path, "created_missions", "mission.txt")
    
    try:
        return send_file(mission_file_path, as_attachment=True, download_name="mission.txt")
    except Exception as e:
        return f"Error sending file: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)