## -------------------Trajectory Lengths ------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline

def read_trajectory_data(file_path):
    vlm_lengths = []
    mp_lengths = []
    images = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("Image"):
                images.append(line.split(":")[0])
            elif "Trajectory length from VLM" in line:
                vlm_lengths.append(float(line.split(":")[1].strip().split()[0]))
            elif "Trajectory length from MP" in line:
                mp_lengths.append(float(line.split(":")[1].strip().split()[0]))
    return images, vlm_lengths, mp_lengths

file_path = "traj_length.txt"
images, vlm_lengths, mp_lengths = read_trajectory_data(file_path)
assert len(images) == len(vlm_lengths) == len(mp_lengths), "Data mismatch!"

# Deviations
deviations = [abs(vlm - mp) for vlm, mp in zip(vlm_lengths, mp_lengths)]
x = np.arange(len(images))
x_smooth = np.linspace(x.min(), x.max(), 500)
deviation_smooth = make_interp_spline(x, deviations)(x_smooth)

plt.figure(figsize=(12, 6))
plt.bar(x - 0.2, vlm_lengths, width=0.4, label='VLM', align='center', alpha=0.8, color='blue')
plt.bar(x + 0.2, mp_lengths, width=0.4, label='MP', align='center', alpha=0.8, color='green')
plt.plot(x_smooth, deviation_smooth, label='Deviation (Smoothed)', color='red', linewidth=2)
plt.xticks(x, images, rotation=90)
plt.xlabel("Images")
plt.ylabel("Trajectory Length (km)")
plt.title("Comparison of Trajectory Lengths from VLM and MP with Deviations")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

## ---------------------------------RMSE Graph ------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def read_rmse_data(file_path):
    images = []
    dtw_rmse = []
    interp_rmse = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("Results for Image"):
                images.append(line.split(":")[0].split()[-1])
            elif "DTW-based Root Mean Squared Error (RMSE)" in line:
                dtw_rmse.append(float(line.split(":")[1].strip().split()[0]))
            elif "Interpolation-based Root Mean Squared Error (RMSE)" in line:
                interp_rmse.append(float(line.split(":")[1].strip().split()[0]))
    
    return images, dtw_rmse, interp_rmse

file_path = "rmse.txt"
images, dtw_rmse, interp_rmse = read_rmse_data(file_path)
assert len(images) == len(dtw_rmse) == len(interp_rmse), "Data mismatch!"

data = pd.DataFrame({
    "Image": images,
    "DTW RMSE (km)": dtw_rmse,
    "Interpolation RMSE (km)": interp_rmse
})

# Box Plot
plt.figure(figsize=(8, 6))
data = {
    "DTW RMSE": dtw_rmse,
    "Interpolation RMSE": interp_rmse
}
plt.boxplot(data.values(), labels=data.keys(), patch_artist=True)
plt.title("Error Distribution b/w VLM and MP Methods")
plt.ylabel("Error (km)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Error Comparison Table
from tabulate import tabulate

print(" ")
print('-----------------------Error Comparison Table-----------------------')
aggregates = {
    "Metric": ["Mean", "Median", "Max"],
    "DTW RMSE": [np.mean(dtw_rmse), np.median(dtw_rmse), np.max(dtw_rmse)],
    "Interpolation RMSE": [np.mean(interp_rmse), np.median(interp_rmse), np.max(interp_rmse)],
}

print(tabulate(pd.DataFrame(aggregates), headers="keys", tablefmt="grid"))
