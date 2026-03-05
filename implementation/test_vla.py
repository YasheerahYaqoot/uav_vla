from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from python_tsp.heuristics import solve_tsp_local_search
from transformers import AutoModelForCausalLM, AutoProcessor, GenerationConfig
from PIL import Image
from time import time
import json
import requests
import torch
import os
import re
import csv
import numpy as np
import shutil
import xml.etree.ElementTree as ET
from outdoor_utils import outdoor_VLA_utils
from indoor_utils import indoor_VLA_utils
from plotting_utils import draw_dots_and_lines_on_image

class VLA():

    def __init__(self, image, command, indoor, outdoor):
        
        self.indoor = indoor
        self.outdoor = outdoor
        
        #---- deleting existing files
        files_to_delete = ['result_coordinates.txt']
        for file_name in files_to_delete:
            if os.path.exists(file_name):
                os.remove(file_name)

        #---- making mission directory
        mission_directory = 'created_missions'
        if os.path.exists(mission_directory):
            shutil.rmtree(mission_directory)  
        os.makedirs(mission_directory)  

        #---- making identified new data directory
        identified_new_data_directory = 'identified_new_data'
        if os.path.exists(identified_new_data_directory):
            shutil.rmtree(identified_new_data_directory)  
        os.makedirs(identified_new_data_directory)  

        self.list_of_the_resulted_coordinates_percentage = []
        self.list_of_the_resulted_coordinates_lat_lon = []
        self.list_of_optimized_coordinates = []

        self.number_of_samples = 1 #len(os.listdir('/VLM_Drone/dataset_images'))
        print('NUMBER_OF_SAMPLES',self.number_of_samples)

        #---- camera parameters
        self.camera_height = 4.4  # meters
        self.diagonal_fov = 78  # degrees

        #---- VLA Data
        self.image = image
        self.command = command

        #---- load the processor
        self.processor = AutoProcessor.from_pretrained(
                                                'cyan2k/molmo-7B-O-bnb-4bit',
                                                trust_remote_code=True,
                                                torch_dtype='auto',
                                                device_map='auto'
                                                )
        
        #---- load the model
        self.model = AutoModelForCausalLM.from_pretrained(
                                                    'cyan2k/molmo-7B-O-bnb-4bit',
                                                    trust_remote_code=True,
                                                    torch_dtype='auto',
                                                    device_map='auto'
                                                    )   
        #---- enter you OpenAI API key
        self.llm = ChatOpenAI(api_key='', model_name='gpt-4o', temperature=0)

    def set_templates(self):

        #---- Step 1: Extract object types from the user's input command using the LLM
        step_1_template = """
        Extract all types of objects the drone needs to find from the following mission description:
        "{command}"

        Output the result in JSON format with a list of object types.
        Example output:
        {{
            "object_types": ["horses", "cows in field", "farm land", "yellow corns", "center of yellow boxes", "chairs", "center of blue objects", "orange objects", "red tripod stands", "three legs of each red tripod stand", "each three legs of red tripod stands", "three legs end-point of each red tripod stands", "center of the X on yellow objects", "chair", "table with a red H"],
        }}
        """

        step_1_prompt = PromptTemplate(input_variables=["command"], template=step_1_template)

        self.step_1_chain = step_1_prompt | self.llm

        self.example_objects = '''
        {
                "village_1": {"type": "village", "coordinates": [1.5, 3.5]},
                "village_2": {"type": "village", "coordinates": [2.5, 6.0]},
                "airfield": {"type": "airfield", "coordinates": [8.0, 6.5]}
            }
        '''

        #---- Step 3: Generate flight plan using LLM and identified objects
        step_3_template = """
        Given the mission description: "{command}" and the following identified objects: {objects}, generate a flight plan in pseudo-language.

        The available commands are on the website:


        Some hints:
        - arm throttle: arm the copter
        - takeoff Z: lift Z meters
        - disarm: disarm the copter
        - mode rtl: return to home
        - mode circle: circle and observe at the current position
        - mode guided: change the mode to guided before takeoff
        - guided X Y Z: fly to the specified location (X,Y,Z)

        Use the identified objects to create the mission.

        Provide me only with commands string-by-string.


        Example output:


        arm throttle
        mode guided
        takeoff 100
        guided 43.237763722222226 -85.79224314444444 100
        guided 43.237765234234234 -85.79224314235235 100
        mode circle
        mode rtl
        disarm


        """

        step_3_prompt = PromptTemplate(input_variables=["command", "objects"], template=step_3_template)
        self.step_3_chain = step_3_prompt | self.llm
    
    def parse_points(self, points_str):
        # Fix the input string by ensuring it's properly formatted
        fixed_str = points_str.strip()
        
        # Parse the XML string
        root = ET.fromstring(fixed_str)

        # Initialize an empty dictionary for the output
        output = {}
        
        # Extract the building type from the alt attribute
        building_type = root.attrib.get('alt', '').strip().split(',')[0] if 'alt' in root.attrib else 'building'

        # Extract coordinates from attributes
        for i in range(1, 50):  # Assuming x1 to x5 and y1 to y5
            x_attr = f"x{i}"
            y_attr = f"y{i}"
            
            if x_attr in root.attrib and y_attr in root.attrib:
                x = float(root.attrib[x_attr])
                y = float(root.attrib[y_attr])
                output[f"{building_type}_{i}"] = {"type": building_type, "coordinates": [x, y]}

        return output

    def tsp_optimized_coordinates(self, coordinates):
        """
        Use TSP to optimize the path for a drone using Euclidean distance between coordinates.
        The coordinates should be in a dictionary format where each key represents a building 
        and each value is another dictionary with 'type' and 'coordinates' as keys.
        """
        coords = []
        names = []
        
        # Extract coordinates and names from the input dictionary
        for name, data in coordinates.items():
            if 'coordinates' in data:
                coords.append(data['coordinates'])
                names.append(name)
        
        # Calculate Euclidean distance matrix
        num_coords = len(coords)
        distance_matrix = np.zeros((num_coords, num_coords))

        for i in range(num_coords):
            for j in range(i + 1, num_coords):
                dist = np.linalg.norm(np.array(coords[i]) - np.array(coords[j]))
                distance_matrix[i][j] = distance_matrix[j][i] = dist

        # Line below changes closed path to open path 
        distance_matrix[:, 0] = 0

        # Solve the TSP using local search
        optimal_order = solve_tsp_local_search(distance_matrix)

        # Ensure that the optimal_order is a list of indices, not a list of lists
        if isinstance(optimal_order[0], list):  # This checks if it's a nested list
            optimal_order = optimal_order[0]  # Flatten the list

        # Reorder the coordinates according to the optimal TSP path
        optimized_coordinates = {names[i]: coordinates[names[i]] for i in optimal_order}

        return optimized_coordinates

    def find_objects(self, json_input, example_objects):
        """
        Process the mission description to find object coordinates on the map and return optimized coordinates using TSP.
        """
        search_string = str()
        find_objects_json_input = json_input.replace("`", "").replace("json","")    #[9::-3]
        
        find_objects_json_input_2 = json.loads(find_objects_json_input)

        for i in range(0, len(find_objects_json_input_2["object_types"])):
            sample = find_objects_json_input_2["object_types"][i]
            search_string = search_string + sample

        # Open file for writing
        with open('result_coordinates.txt', 'a') as file:
            
            for i in range(1, self.number_of_samples+1):
                print(f"Processing image {i}")
                string = self.image 
                
                # Process the image and text
                inputs = self.processor.process(
                    images=[Image.open(self.image)],
                    text=f'''
                    This is the aerial image of a room. Please, point all the next objects: {sample} 
                    '''
                )

                inputs = {k: v.to(self.model.device).unsqueeze(0) for k, v in inputs.items()}

                # Generate output; maximum 200 new tokens; stop generation when <|endoftext|> is generated
                output = self.model.generate_from_batch(
                    inputs,
                    GenerationConfig(max_new_tokens=2000, stop_strings="<|endoftext|>"),
                    tokenizer=self.processor.tokenizer
                )

                generated_tokens = output[0, inputs['input_ids'].size(1):]
                generated_text = self.processor.tokenizer.decode(generated_tokens, skip_special_tokens=True)

                parsed_points = self.parse_points(generated_text)

                print('\n')

                image_number = i

                # Optimize coordinates using TSP and append to the list
                optimized_coordinates = self.tsp_optimized_coordinates(parsed_points)

                print(optimized_coordinates)
                print('\n')

                if self.indoor:
                    image_metrics = indoor_VLA_utils.calculate_real_world_size(self.image, self.camera_height, self.diagonal_fov)
                    result_coordinates = indoor_VLA_utils.process_coordinates(optimized_coordinates, self.camera_height, self.diagonal_fov, image_metrics)
                elif self.outdoor:
                    csv_file_path = 'parsed_coordinates.csv'
                    coordinates_dict = outdoor_VLA_utils.read_coordinates_from_csv(csv_file_path)
                    result_coordinates = outdoor_VLA_utils.recalculate_coordinates(parsed_points, image_number, coordinates_dict)

                draw_dots_and_lines_on_image(self.image, optimized_coordinates, output_path='identified_new_data/identified.png')

                self.list_of_the_resulted_coordinates_percentage.append(parsed_points)
                self.list_of_optimized_coordinates.append(optimized_coordinates)
                self.list_of_the_resulted_coordinates_lat_lon.append(result_coordinates)

                print(result_coordinates)

                # Writing the coordinates to the file in the required format
                file.write(f"Image {i}:\n")
                for building, value in result_coordinates.items():
                    file.write(f"Object_{i} coordinates:\n")
                    file.write(f"x = {value['coordinates'][0]}\n")
                    file.write(f"y = {value['coordinates'][1]}\n\n")

        return json.dumps(optimized_coordinates), self.list_of_the_resulted_coordinates_percentage, self.list_of_the_resulted_coordinates_lat_lon, self.list_of_optimized_coordinates

    def generate_drone_mission(self):
        # Step 1: Extract object types
        self.set_templates()
        object_types_response = self.step_1_chain.invoke({"command": self.command})
        object_types_json = object_types_response.content  # Use 'content' to get the actual response text

        # Step 2: Find objects on the map
        t1_find_objects = time()
        objects_json, list_of_the_resulted_coordinates_percentage, list_of_the_resulted_coordinates_lat_lon, list_of_optimized_coordinates = self.find_objects(object_types_json, self.example_objects)
        t2_find_objects = time()

        del_t_find_objects = (t2_find_objects - t1_find_objects)
        print('Length of optimized coordinates:', len(list_of_the_resulted_coordinates_lat_lon))

        #print('objects_json =', objects_json)

        # Step 3: Generate the flight plan
        t1_generate_drone_mission = time()

        if not list_of_the_resulted_coordinates_lat_lon:
            return del_t_find_objects, time() - t1_generate_drone_mission

        for i in range(1,len(list_of_the_resulted_coordinates_lat_lon)+1): 
            flight_plan_response = self.step_3_chain.invoke({"command": self.command, "objects": list_of_the_resulted_coordinates_lat_lon[i]})
        #print('flight_plan_response = ', flight_plan_response)
            with open(f"created_missions/mission{i}.txt","w") as file:   
                file.write(str(flight_plan_response.content))

            # print(flight_plan_response.content)
        print("Mission text file saved")
        t2_generate_drone_mission = time()
        del_t_generate_drone_mission = (t2_generate_drone_mission - t1_generate_drone_mission)

        return flight_plan_response.content, del_t_find_objects, del_t_generate_drone_mission  # Return the response text from AIMessage


def main():
    image = "scene.jpg"
    command = """Create a flight plan for the quadcopter to fly around each of the "horses", "cows in field", "farm land", "yellow corns" at the height 1.5m return to home and land at the take-off point."""
    vla = VLA(image, command, indoor=True, outdoor=False)
    flight_plan, vlm_model_time, mission_generation_time = vla.generate_drone_mission()
    total_computational_time = vlm_model_time + mission_generation_time

    # Evaluation time
    print('-------------------------------------------------------------------')
    print('Time to get VLM results: ', vlm_model_time, 'sec')
    print('Time to get Mission Text files: ', mission_generation_time, 'sec')
    print('Total Computational Time: ', total_computational_time, 'sec')
    
if __name__ == "__main__":
    main()                  # Comment this if running on server