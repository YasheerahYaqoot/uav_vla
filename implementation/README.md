# VLA Framework – Real-World Implementation

This folder contains the **implementation of the Vision-Language-Action (VLA) framework for real-world drone experiments**.  
The system allows a drone to **interpret a natural language command and generate an executable mission plan** based on a provided image of the environment.

The implementation demonstrates the **practical deployment of the VLA framework for autonomous mission generation and execution**.

---

# Main Script

The main script used to run the system is ```test_vla.py```.


This script performs the full pipeline:

1. Reads the input image of the environment
2. Interprets the mission command
3. Identifies mission targets using the VLM
4. Converts the detected objects into geographic coordinates
5. Generates a UAV mission file

---

# How to Run

### 1. Add Your Image

Place the environment image inside the appropriate input directory used by the script.

### 2. Add the Command

Open the file ```test_vla.py```. 
Modify the mission command in the script to describe the desired UAV mission.

Example:

```python
command = "Create a flight plan to fly around all the crops in the field and return to home."
```

### 3. Run the Script
```
python3 test_vla.py
```

The system will generate the corresponding UAV mission file automatically.

## Real-World Experiments

The VLA framework was evaluated in **two real-world experimental scenarios**.

---

### Experiment 1 – Agricultural Environment

**Objective:**  
Evaluate the **real-time applicability of the developed model in an agricultural environment**.

In this experiment, the drone was tasked with generating and executing mission plans based on aerial imagery of an agricultural field.

The goal was to verify that the system can:

- Interpret mission instructions  
- Identify relevant objects in outdoor environments  
- Generate executable mission plans for UAV navigation  

![Exp1](https://github.com/user-attachments/assets/7bc25e78-f92a-439c-98c5-9c7323f6bdb6)

---

### Experiment 2 – Indoor Environment

**Objective:**  
Evaluate the **generalizability of the developed model in an indoor environment (unseen environment)**.

This experiment tested the ability of the framework to operate in a **previously unseen indoor environment**, validating that the system can generalize beyond the outdoor conditions used during development.

The system generated UAV mission commands based on the indoor scene and executed them autonomously.

![Exp2](https://github.com/user-attachments/assets/b73185f4-8ba4-4068-86fa-13bc3df6d3b9)


