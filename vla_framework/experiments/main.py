import os
import mp_data
import traj_calc
import rmse_data
import graphs
import identified_images  
import shutil

def main(without_tsp, with_tsp):

    if without_tsp:
        identified_new_data_directory = 'results_no_tsp'
        if os.path.exists(identified_new_data_directory):
            shutil.rmtree(identified_new_data_directory)  
        os.makedirs(identified_new_data_directory)
        os.makedirs('results_no_tsp/plots', exist_ok=True)
        os.makedirs('results_no_tsp/identified_images_VLM_no_tsp', exist_ok=True)
        os.makedirs('../benchmark-UAV-VLPA-nano-30/identified_images_mp_no_tsp', exist_ok=True)

        # Step 1: Generate VLM Coordinates
        print("Generating VLM coordinates...")
        results_file = '../result_coordinates_no_tsp.txt'
        VLM_data_file = 'results_no_tsp/VLM_coordinates_no_tsp.txt'
        shutil.copy(results_file, VLM_data_file)

        # Step 2: Generate MP Coordinates
        print("Generating MP coordinates...")
        mp_file = 'results_no_tsp/mp_coordinates_no_tsp.txt'
        mp_data.process_mp_data(
            input_directory='../benchmark-UAV-VLPA-nano-30/mission_planner_data/waypoints_no_tsp/',
            output_txt=mp_file
        )

        # Step 3: Calculate Trajectory Lengths
        print("Calculating trajectory lengths...")
        traj_file = 'results_no_tsp/traj_length_no_tsp.txt'
        traj_calc.trajectory_results(mp_file, VLM_data_file, traj_file)

        # Step 4: Calculate RMSE Data
        print("Calculating RMSE...")
        rmse_data_file = 'results_no_tsp/rmse_no_tsp.txt'
        rmse_data.calculate_rmse(mp_file, VLM_data_file, rmse_data_file)

        # Step 5: Plot Results
        print("Plotting results...")

        # Plot Trajectory Length Comparison
        bar_chart = 'results_no_tsp/plots/traj_bar_chart.png'
        images, vlm_lengths, mp_lengths = graphs.read_trajectory_data("results_no_tsp/traj_length_no_tsp.txt")
        deviations = [vlm - mp for vlm, mp in zip(vlm_lengths, mp_lengths)]
        graphs.plot_trajectory_length_comparison(vlm_lengths, mp_lengths, deviations, images, bar_chart)

        # Plot RMSE Boxplot
        box_plot = 'results_no_tsp/plots/error_box_plot.png'
        images, knn_errors, dtw_rmse, interp_rmse = graphs.read_rmse_data(rmse_data_file)
        graphs.plot_rmse_boxplot(knn_errors, dtw_rmse, interp_rmse, box_plot)

        # Print RMSE Comparison Table
        graphs.print_rmse_comparison_table(knn_errors, dtw_rmse, interp_rmse)

        # Step 6: Generate Identified Images for VLM
        print("Generating identified images for VLM...")
        identified_images.process_images(
            input_folder='../benchmark-UAV-VLPA-nano-30/images/',  # Adjust this path as needed
            output_folder='results_no_tsp/identified_images_VLM_no_tsp',  # VLM output folder
            coordinate_file='results_no_tsp/VLM_coordinates_no_tsp.txt', 
            latlong_file='../benchmark-UAV-VLPA-nano-30/img_lat_long_data.txt', 
            is_vlm=True
        )

        # Step 7: Generate Identified Images for MP
        print("Generating identified images for MP...")
        identified_images.process_images(
            input_folder='../benchmark-UAV-VLPA-nano-30/images/',  # Adjust this path as needed
            output_folder='../benchmark-UAV-VLPA-nano-30/identified_images_mp_no_tsp',  # MP output folder
            coordinate_file='results_no_tsp/mp_coordinates_no_tsp.txt', 
            latlong_file='../benchmark-UAV-VLPA-nano-30/img_lat_long_data.txt', 
            is_vlm=False
        )

    elif with_tsp:
        identified_new_data_directory = 'results_tsp'
        if os.path.exists(identified_new_data_directory):
            shutil.rmtree(identified_new_data_directory)  
        os.makedirs(identified_new_data_directory)
        os.makedirs('results_tsp/plots', exist_ok=True)
        os.makedirs('results_tsp/identified_images_VLM_tsp', exist_ok=True)
        os.makedirs('../benchmark-UAV-VLPA-nano-30/identified_images_mp_tsp', exist_ok=True)

        # Step 1: Generate VLM Coordinates
        print("Generating VLM coordinates...")
        results_file = '../result_coordinates_tsp.txt'
        VLM_data_file = 'results_tsp/VLM_coordinates_tsp.txt'
        shutil.copy(results_file, VLM_data_file)

        # Step 2: Generate MP Coordinates
        print("Generating MP coordinates...")
        mp_file = 'results_tsp/mp_coordinates_tsp.txt'
        mp_data.process_mp_data(
            input_directory='../benchmark-UAV-VLPA-nano-30/mission_planner_data/waypoints_tsp/',
            output_txt=mp_file
        )

        # Step 3: Calculate Trajectory Lengths
        print("Calculating trajectory lengths...")
        traj_file = 'results_tsp/traj_length_tsp.txt'
        traj_calc.trajectory_results(mp_file, VLM_data_file, traj_file)

        # Step 4: Calculate RMSE Data
        print("Calculating RMSE...")
        rmse_data_file = 'results_tsp/rmse_tsp.txt'
        rmse_data.calculate_rmse(mp_file, VLM_data_file, rmse_data_file)

        # Step 5: Plot Results
        print("Plotting results...")

        # Plot Trajectory Length Comparison
        bar_chart = 'results_tsp/plots/traj_bar_chart.png'
        images, vlm_lengths, mp_lengths = graphs.read_trajectory_data("results_tsp/traj_length_tsp.txt")
        deviations = [vlm - mp for vlm, mp in zip(vlm_lengths, mp_lengths)]
        graphs.plot_trajectory_length_comparison(vlm_lengths, mp_lengths, deviations, images, bar_chart)

        # Plot RMSE Boxplot
        box_plot = 'results_tsp/plots/error_box_plot.png'
        images, knn_errors, dtw_rmse, interp_rmse = graphs.read_rmse_data(rmse_data_file)
        graphs.plot_rmse_boxplot(knn_errors, dtw_rmse, interp_rmse, box_plot)

        # Print RMSE Comparison Table
        graphs.print_rmse_comparison_table(knn_errors, dtw_rmse, interp_rmse)

        # Step 6: Generate Identified Images for VLM
        print("Generating identified images for VLM...")
        identified_images.process_images(
            input_folder='../benchmark-UAV-VLPA-nano-30/images/',  # Adjust this path as needed
            output_folder='results_tsp/identified_images_VLM_tsp',  # VLM output folder
            coordinate_file='results_tsp/VLM_coordinates_tsp.txt', 
            latlong_file='../benchmark-UAV-VLPA-nano-30/img_lat_long_data.txt', 
            is_vlm=True
        )

        # Step 7: Generate Identified Images for MP
        print("Generating identified images for MP...")
        identified_images.process_images(
            input_folder='../benchmark-UAV-VLPA-nano-30/images/',  # Adjust this path as needed
            output_folder='../benchmark-UAV-VLPA-nano-30/identified_images_mp_tsp',  # MP output folder
            coordinate_file='results_tsp/mp_coordinates_tsp.txt', 
            latlong_file='../benchmark-UAV-VLPA-nano-30/img_lat_long_data.txt', 
            is_vlm=False
        )

if __name__ == "__main__":
    main(without_tsp=True, with_tsp=False)
