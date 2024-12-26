This repository contains the code, data, and instructions for the paper:  
# "UAV-VLA: Vision-Language-Action System for Large Scale Aerial Mission Generation"

---

## Table of Contents
1. [Abstract](#abstract)
2. [Dataset](#dataset)
3. [Installation](#installation)
4. [Experimental Results](#experimental-results)


---
## Abstract
The UAV-VLA (Visual-Language-Action) system is a tool designed to facilitate communication with aerial robots. 
By integrating satellite imagery processing with the Visual Language Model (VLM) and the powerful capabilities of GPT, UAV-VLA enables users to generate general flight paths-and-action plans through simple text requests. 
This system leverages the rich contextual information provided by satellite images, allowing for enhanced decision-making and mission planning. 
The combination of visual analysis by VLM and natural language processing by GPT can provide the user with the path-and-action set, making aerial operations more efficient and accessible. The newly developed method showed the difference in the length of the created trajectory in 22\% and the mean error in finding the objects of interest on a map in 34.22 m by Euclidean distance in the K-Nearest Neighbors (KNN) approach.

This repository includes:
- The implementation of the UAV-VLA framework.
- Dataset and benchmark details.
- Code for simulation-based and real-world experiments.

##Docker

It is possible to run docker by

```
docker run --gpus all -it <imagename>
```

## Benchmark

The benchmark is stored in the folder benchmark-UAV-VLPA-nano-30. There are images, .txt and .csv files.

## Installation

To install requirements, run 

```
pip -r requirements.txt
```
!12GB VRAM minimum


## Mission generation

To generate commands for UAV, run
```
python3 generate_plans.py
```
It will produce the commands to /created_missions and visualizations to the /identified_new_data


## To create the path-plans

To generate commands, run
```
python3 generate_plans.py
```

## Experimental Results
To view the experimental results, you need to run the main.py script. This script automates the entire process of generating coordinates, calculating trajectory lengths, and producing visualizations.

How to View the Results:
Ensure that your system has at least 12GB of VRAM, as the experiment requires significant graphical resources.
Navigate into the folder ```experiments/```, run:
```
python3 main.py
```


### What Happens When You run main.py:

- Generate Home Positions

- Generate VLM Coordinates

- Generate MP Coordinates

- Calculate Trajectory Lengths

- Calculate RMSE (Root Mean Square Error)
  
- Plot Results

- Generate Identified Images:
The script generates images by overlaying the VLM and MP coordinates on the original images from the dataset.
These identified images are saved in:
identified_images_VLM (for VLM outputs).
identified_images_mp (for Mission Planner outputs).

-After running the script, you will be able to examine:
Text Files: Containing the generated coordinates, home positions, and RMSE data.
Images: Showing the identified coordinates overlaid on the images.
Plots: Comparing trajectory lengths and RMSE values.
