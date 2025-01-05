# UAV-VLA: Vision-Language-Action System for Large Scale Aerial Mission Generation

---

## Table of Contents
1. [Abstract](#abstract)
2. [Benchmark](#benchmark)
3. [Installation](#installation)
4. [Mission Generation](#mission-generation)
5. [Path-Plans Creation](#path-plan-creation)
6. [Experimental Results](#experimental-results)


---
## Abstract
The UAV-VLA (Visual-Language-Action) system is a tool designed to facilitate communication with aerial robots. 
By integrating satellite imagery processing with the Visual Language Model (VLM) and the powerful capabilities of GPT, UAV-VLA enables users to generate general flight paths-and-action plans through simple text requests. 
This system leverages the rich contextual information provided by satellite images, allowing for enhanced decision-making and mission planning. 
The combination of visual analysis by VLM and natural language processing by GPT can provide the user with the path-and-action set, making aerial operations more efficient and accessible. The newly developed method showed the difference in the length of the created trajectory in 22\% and the mean error in finding the objects of interest on a map in 34.22 m by Euclidean distance in the K-Nearest Neighbors (KNN) approach.


This repository includes:
- The implementation of the UAV-VLA framework.
- Dataset and benchmark details.
- Code for simulation-based experiments in Mission Planner.

### UAV-VLA Framework

<div align="center">
  <img src="https://github.com/user-attachments/assets/b2e92daf-b21b-47b8-ab38-3e20ac6b18e6" alt="UAV_VLA_Title_image" width="400"/>
</div>

## Benchmark

The images of the benchmark are stored in the folder ```benchmark-UAV-VLPA-nano-30/images```. The metadata files are ```benchmark-UAV-VLPA-nano-30/img_lat_long_data.txt``` and ```benchmark-UAV-VLPA-nano-30/parsed_coordinates.csv```.

## Installation

It is possible to run docker by

```
docker run --gpus all -it <imagename>
```

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
It will produce the commands and store the text files in the folder ```/created_missions``` and visualizations of the identified points on the benchmark images in the folder ```/identified_new_data```.


## Path-Plans Creation

To generate commands, run
```
python3 run_vlm.py
```

Some examples of the path generated can be seen below:

<div align="center">
  <img src="https://github.com/user-attachments/assets/386f7e78-83aa-4915-aa33-ec7fbdc6dd40" alt="examples_path_generated" width="600"/>
</div>

## Experimental Results

To view the experimental results, you need to run the main.py script. This script automates the entire process of generating coordinates, calculating trajectory lengths, and producing visualizations.

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
The script generates images by overlaying the VLM and Mission Planner (human-generated) coordinates on the original images from the dataset.
These identified images are saved in:
identified_images_VLM (for VLM outputs).
identified_images_mp (for Mission Planner outputs).

After running the script, you will be able to examine:

- Text Files: Containing the generated coordinates, home positions, and RMSE data.
- Images: Showing the identified coordinates overlaid on the images.
- Plots: Comparing trajectory lengths and RMSE values.

### Trajectory Bar Chart:

<div align="center">
  <img src="https://github.com/user-attachments/assets/e27a0c86-e54a-433a-822c-dc68297fdd37" alt="traj_bar_chart" width="600"/>
</div>

### Error Box Plot:

<div align="center">
  <img src="https://github.com/user-attachments/assets/52f9afcf-ba3f-4cc2-bb37-bf48475a077b" alt="error_box_plot" width="500"/>
</div>

### Error Comparison Table:

<div align="center">

|    | Metric   |   KNN Error |   DTW RMSE |   Interpolation RMSE |
|----|----------|-------------|------------|----------------------|
|  1 | Mean     |     34.2218 |    307.265 |              409.538 |
|  2 | Median   |     26.0456 |    318.462 |              395.593 |
|  3 | Max      |    112.493  |    644.574 |              727.936 |

</div>

## Simulation Video (Mission Planner Environment)

The generated mission from the UAV-VLA framework was tested in the ArduPilot Mission Planner. The simulation can be seen below.

https://github.com/user-attachments/assets/562f2ee7-13e5-44a0-bb0f-6c109a958123



