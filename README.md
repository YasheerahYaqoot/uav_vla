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



## Dataset

## Installation

To generate actions, run
```
python3 generate_plans.py
```
