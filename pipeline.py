from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import json

# Initialize the ChatGPT-4 model using ChatOpenAI
llm = ChatOpenAI(api_key='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', model_name='gpt-4', temperature=0)

# 1. Step 1: Extract object types from the user's input command using the LLM
step_1_template = """
Extract all types of objects the drone needs to find from the following mission description:
"{command}"

Output the result in JSON format with a list of object types.

Example output:
{{
    "object_types": ["village", "airfield"]
}}
"""

step_1_prompt = PromptTemplate(input_variables=["command"], template=step_1_template)

# Instead of using RunnableSequence, we simply use pipe (|)
step_1_chain = step_1_prompt | llm

# 2. Step 2: Use SAM model to find objects on the map (placeholder)
def find_objects(json_input):
    """
    Placeholder for SAM model to process input object types and output valid objects.
    For now, return a dummy dictionary of identified objects.
    """
    object_types = json.loads(json_input)["object_types"]
    # Dummy dictionary of found objects
    objects = {
        "village_1": {"type": "village", "coordinates": [55.123, 37.456]},
        "village_2": {"type": "village", "coordinates": [55.789, 37.987]},
        "airfield": {"type": "airfield", "coordinates": [55.234, 37.654]}
    }
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
    
    # Extract the text from the AIMessage object
    object_types_json = object_types_response.content  # Use 'content' to get the actual response text
    
    # Step 2: Find objects on the map (dummy example for now)
    objects_json = find_objects(object_types_json)
    
    # Step 3: Generate the flight plan
    flight_plan_response = step_3_chain.invoke({"command": command, "objects": objects_json})
    
    return flight_plan_response.content  # Return the response text from AIMessage

# Example usage
command = """Create a flight plan and mission through a mavproxy framework for the quadcopter to fly around each of the villages, circle over the airfield and land at the take-off point."""

# Run the full pipeline
flight_plan = generate_drone_mission(command)
print(flight_plan)
