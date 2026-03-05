# UAV-VLA: Vision-Language-Action System for Large Scale Aerial Mission Generation

---
This repository is for the research paper accepted in Proc. ACM/IEEE Int. Conf. on Human Robot Interaction (HRI 2025)

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
The dataset contains **30 satellite images** representing different environments used to evaluate UAV mission generation.

## Installation

Make sure you have a docker container with NVIDIA CUDA running on it.
Clone the repository and install dependencies.

To install requirements, run 

```
pip install -r requirements.txt
```
!12GB VRAM minimum


## Mission generation

The entire UAV-VLA pipeline is executed using a single script. You have to add your API key in ```generate_plans.py``` (line 90). Then run:

```
python3 generate_plans.py
```

This script performs the following steps:

1. Extract mission objects from the text command using an LLM

2. Detect objects in satellite images using the Vision-Language Model

3. Convert detected pixel coordinates into geographic coordinates

4. Optionally optimize waypoint order using Traveling Salesman Problem (TSP)

5. Generate UAV mission commands

Generated missions and intermediate results are automatically savein the ```experiments/``` folder.

As a result of this script, you will also find the total computational time time of the UAV-VLA system which is approximately **5 minutes and 24 seconds**.

## TSP vs No-TSP Mode

The system supports two trajectory generation modes.
The mode is selected inside ```generate_plans.py```.

``` python
vla = VLA(command, with_tsp=True, without_tsp=False)
```
### No-TSP Mode

The UAV visits objects in the order detected by the VLM.
``` python
vla = VLA(command, with_tsp=False, without_tsp=True)
```

The output identified images and trajectory plots are saved in ```experiments/results_no_tsp/``` folder.

### Experimental Results

The script generates images by overlaying the VLM and Mission Planner (human-generated) coordinates on the original images from the dataset.
These identified images are saved in ```experiments/``` (for VLM outputs) and ```benchmark-UAV-VLPA-nano-30/``` (for Mission Planner outputs).

After running the script, you will be able to examine:

- Text Files: Containing the generated coordinates, home positions, and RMSE data.
- Images: Showing the identified coordinates overlaid on the images.
- Plots: Comparing trajectory lengths and RMSE values.

#### Trajectory Bar Chart:

<div align="center">
  <img src="https://github.com/user-attachments/assets/e27a0c86-e54a-433a-822c-dc68297fdd37" alt="traj_bar_chart" width="600"/>
</div>

#### Error Box Plot:

<div align="center">
  <img src="https://github.com/user-attachments/assets/52f9afcf-ba3f-4cc2-bb37-bf48475a077b" alt="error_box_plot" width="500"/>
</div>

#### Error Comparison Table:

The errors were calculated using different approaches including K-Nearest Neighbor (KNN), Dynamic Time Warping (DTW), and Linear Interpolation.

<div align="center">

|    | Metric   |   KNN Error (m) |   DTW RMSE (m) |   Interpolation RMSE (m) |
|----|----------|-----------------|----------------|--------------------------|
|  1 | Mean     |     34.2218     |    307.265     |              409.538     |
|  2 | Median   |     26.0456     |    318.462     |              395.593     |
|  3 | Max      |     112.493     |    644.574     |              727.936     |

</div>

### TSP Mode

The waypoints are reordered using the Traveling Salesman Problem (TSP) to minimize trajectory length.
```python
vla = VLA(command, with_tsp=True, without_tsp=False)
```

Using TSP results in approximately 20% reduction in trajectory length. The output identified images and trajectory plots are saved in ```experiments/results_tsp/``` folder.

### Experimental Results

The script generates images by overlaying the VLM and Mission Planner (human-generated) coordinates on the original images from the dataset.
These identified images are saved in ```experiments/``` (for VLM outputs) and ```benchmark-UAV-VLPA-nano-30/``` (for Mission Planner outputs).

After running the script, you will be able to examine:

- Text Files: Containing the generated coordinates, home positions, and RMSE data.
- Images: Showing the identified coordinates overlaid on the images.
- Plots: Comparing trajectory lengths and RMSE values.

#### Trajectory Bar Chart:

<div align="center">
  <img width="600" height="600" alt="traj_bar_chart" src="https://github.com/user-attachments/assets/b2da3155-1820-4444-a0c8-7c909ea3afff" />
</div>

#### Error Box Plot:

<div align="center">
  <img width="500" height="600" alt="error_box_plot" src="https://github.com/user-attachments/assets/15ef036f-0803-4d31-991c-8a4330118927" />
</div>


#### Error Comparison Table:

The errors were calculated using different approaches including K-Nearest Neighbor (KNN), Dynamic Time Warping (DTW), and Linear Interpolation.

<div align="center">

|    | Metric   |   KNN Error (m) |   DTW RMSE (m) |   Interpolation RMSE (m) |
|----|----------|-----------------|----------------|--------------------------|
|  1 | Mean     |     45.16       |    259.07      |              354.46      |
|  2 | Median   |     26.89       |    235.48      |              308.91      |
|  3 | Max      |    336.22       |   719.48       |              734.32      |

</div>

## Flight Plans
Some examples of the path generated can be seen below:

<div align="center">
  <img src="https://github.com/user-attachments/assets/386f7e78-83aa-4915-aa33-ec7fbdc6dd40" alt="examples_path_generated" width="600"/>
</div>

## Simulation Video (Mission Planner Environment)

The generated mission from the UAV-VLA framework was tested in the ArduPilot Mission Planner. The simulation can be seen below.

https://github.com/user-attachments/assets/562f2ee7-13e5-44a0-bb0f-6c109a958123



