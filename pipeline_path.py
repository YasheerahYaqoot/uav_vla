from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import json
from transformers import AutoModelForCausalLM, AutoProcessor, GenerationConfig
from PIL import Image
import requests
import torch
import os


#import molmo_inference
# Initialize the ChatGPT-4 model using ChatOpenAI
llm = ChatOpenAI(api_key='', model_name='gpt-4o', temperature=0)

LIST_OF_ANSWERS = []

NUMBER_OF_SAMPLES = 2 #len(os.listdir('/VLM_Drone/dataset_images'))
print('NUMBER_OF_SAMPLES',NUMBER_OF_SAMPLES)

# load the processor
processor = AutoProcessor.from_pretrained(
    'cyan2k/molmo-7B-O-bnb-4bit',
    trust_remote_code=True,
    torch_dtype='auto',
    device_map='auto'
)

# load the model
model = AutoModelForCausalLM.from_pretrained(
    'cyan2k/molmo-7B-O-bnb-4bit',
    trust_remote_code=True,
    torch_dtype='auto',
    device_map='auto'
)


command = """Create a flight plan and mission through a mavproxy framework for the quadcopter to fly around each of the buildings, circle over the stadium and land at the take-off point."""
# 1. Step 1: Extract object types from the user's input command using the LLM


step_1_template = """
Extract all types of objects the drone needs to find from the following mission description:
"{command}"

Output the result in JSON format with a list of object types.

Example output:
{{
    "object_types": ["village", "airfield", "stadium", "tennis court", "building", "ponds", "crossroad", "roundabout"]
}}
"""

step_1_prompt = PromptTemplate(input_variables=["command"], template=step_1_template)

# Instead of using RunnableSequence, we simply use pipe (|)
step_1_chain = step_1_prompt | llm

print(step_1_chain)

# 2. Step 2: Use SAM model to find objects on the map (placeholder)
def find_objects(json_input):
    """
    Placeholder for SAM model to process input object types and output valid objects.
    For now, return a dummy dictionary of identified objects.
    """

    for i in range(1, NUMBER_OF_SAMPLES):
        print(i)
        string = '/dataset_images/' + str(i) + '.jpg' 
    #process the image and text
        inputs = processor.process(
            images=[Image.open('dataset_images/' + str(i) + '.jpg')],
            text="This is the satellite image of a city. Please, point all the {objects_json}."
        )



    # move inputs to the correct device and make a batch of size 1
        inputs = {k: v.to(model.device).unsqueeze(0) for k, v in inputs.items()}

        #generate output; maximum 200 new tokens; stop generation when <|endoftext|> is generated
        output = model.generate_from_batch(
            inputs,
            GenerationConfig(max_new_tokens=200, stop_strings="<|endoftext|>"),
            tokenizer=processor.tokenizer
        )

        # with torch.autocast(device_type="cuda", enabled=True, dtype=torch.bfloat16):
        #   output = model.generate_from_batch(
        #       inputs,
        #       GenerationConfig(max_new_tokens=200, stop_strings="<|endoftext|>"),
        #       tokenizer=processor.tokenizer
        #   )

        # model.to(dtype=torch.bfloat16)
        # inputs["images"] = inputs["images"].to(torch.bfloat16)
        # output = model.generate_from_batch(
        #     inputs,
        #     GenerationConfig(max_new_tokens=200, stop_strings="<|endoftext|>"),
        #     tokenizer=processor.tokenizer
        # )

        # only get generated tokens; decode them to text
        generated_tokens = output[0,inputs['input_ids'].size(1):]
        generated_text = processor.tokenizer.decode(generated_tokens, skip_special_tokens=True)

        # print the generated text
        print('molmo_output =', generated_text)

        f.write(str(i) + ', ' + generated_text + '\n')
        
        # LIST_OF_ANSWERS.append(generated_text)
        
        # # LIST_OF_ANSWERS.append('/n')

        # f.writelines(LIST_OF_ANSWERS)
        # # f.writelines(generated_text)
        # f.write('\n')
        # f.close()



    #object_types = json.loads(json_input)["object_types"]
    # Dummy dictionary of found objects
    
    
    objects = {
    }
    
    '''
        "village_1": {"type": "village", "coordinates": [55.123, 37.456]},
        "village_2": {"type": "village", "coordinates": [55.789, 37.987]},
        "airfield": {"type": "airfield", "coordinates": [55.234, 37.654]}
    }
    '''
    
    return json.dumps(objects)

# 3. Step 3: Generate flight plan using LLM and identified objects
step_3_template = """
Given the mission description: "{command}" and the following identified objects: {objects}, generate a flight plan in pseudo-language.

The available commands are:
- arm_throttle: start
- disarm: land at the current position
- mode_circle: circle and observe at the current position
- mode_guided(location): fly to the specified location

Use the identified objects to create the mission.

Example output:
arm_throttle
mode_guided(village_1)
mode_guided(village_2)
mode_circle
mode_rtl
disarm
"""

step_3_prompt = PromptTemplate(input_variables=["command", "objects"], template=step_3_template)
step_3_chain = step_3_prompt | llm

# Full pipeline function
def generate_drone_mission(command):
    # Step 1: Extract object types
    object_types_response = step_1_chain.invoke({"command": command})
    print('object_types_response =', object_types_response)
    
    # Extract the text from the AIMessage object
    object_types_json = object_types_response.content  # Use 'content' to get the actual response text
    print('object_types_json =', object_types_json)

    # Step 2: Find objects on the map (dummy example for now)
    objects_json = find_objects(object_types_json)
    print('objects_json =', objects_json)

    
    # Step 3: Generate the flight plan
    flight_plan_response = step_3_chain.invoke({"command": command, "objects": objects_json})
    print('flight_plan_response = ', flight_plan_response)
    
    return flight_plan_response.content  # Return the response text from AIMessage

# Example usage

# Run the full pipeline
flight_plan = generate_drone_mission(command)
print(flight_plan)
