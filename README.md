This repository contains the code, data, and instructions for the paper:  
# "UAV-VLA: Vision-Language-Action System for Multicopter Mission Generation"

---

## Table of Contents
1. [Abstract](#abstract)
2. [Dataset](#dataset)
3. [Installation](#installation)


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

'''
docker run --gpus all -it <imagename>
'''

## Benchmark

The benchmark is stored in the folder benchmark-UAV-VLPA-nano-30. There are images, .txt and .csv files.

## Installation

To install requirements, run 

pip -r requirements.txt

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
