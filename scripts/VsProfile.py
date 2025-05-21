import os
import matplotlib.pyplot as plt

# Function to read data from the file and extend depth to 31 if needed
def read_data(filepath):
    depths = []
    velocities = []

    with open(filepath, 'r') as file:
        lines = file.readlines()

        # Skip the header if present
        if lines[0].lower().startswith("m"):
            lines = lines[1:]

        for line in lines:
            parts = line.strip().split()
            if len(parts) == 4:
                depth = float(parts[0])
                velocity = float(parts[2])  # use the 3rd column
                depths.append(depth)
                velocities.append(velocity)

    # If the last depth is less than 30, extend to 31
    if depths and depths[-1] < 30:
        last_depth = depths[-1]
        last_velocity = velocities[-1]
        extended_depth = 31.0

        # Append the extra point
        depths.append(extended_depth)
        velocities.append(last_velocity)  # or extrapolate if needed

    return depths, velocities


# Function to plot the velocity profile
def plot_velocity_profile(depths, velocities, file_name, parent_folder):
    plt.figure(figsize=(5, 8))
    plt.plot(velocities, depths, marker='o', color='red', linewidth=5, markersize=2)

    plt.gca().invert_yaxis()  # Depth increases downward
    plt.ylim(30, 0)  # Show only up to 30 meters

    # Custom ticks for x-axis (from 500 to 1500 with a step of 500)
    plt.xticks(range(500, 1600, 500))

    # Custom ticks for y-axis (every 5 meters)
    plt.yticks(range(0, 31, 5))

    plt.xlabel("Velocity (m/s)")
    plt.ylabel("Depth (m)")
    sitecode = file_name.replace("_ModelFile.txt", "")
    plt.title(f"Velocity Profile ( {sitecode} )")
    plt.grid(True)
    plt.tight_layout()

    # Save the figure in the modelfig folder inside the parent folder
    modelfig_folder = os.path.join(parent_folder, "modelfig")
    os.makedirs(modelfig_folder, exist_ok=True)  # Create the modelfig folder if it doesn't exist

    # Construct the output file path
    output_path = os.path.join(modelfig_folder, f"{os.path.splitext(file_name)[0]}_velocity_profile.png")
    
    # Save the plot
    plt.savefig(output_path)
    plt.close()
    # plt.show()

# Main function to process all .txt files in the parent folder
def process_all_txt_files(parent_folder):
    # Get a list of all .txt files in the parent folder
    txt_files = [f for f in os.listdir(parent_folder) if f.endswith('.txt') and 'ibc' not in f.lower()]
    
    if not txt_files:
        print("No .txt files found in the selected folder.")
        return

    # Process each .txt file
    for txt_file in txt_files:
        file_path = os.path.join(parent_folder, txt_file)
        print(f"Processing file: {file_path}")
        
        # Read data from the file
        depths, velocities = read_data(file_path)
        
        # Plot the velocity profile for each file and save in modelfig folder
        plot_velocity_profile(depths, velocities, txt_file, parent_folder)

# Example usage

file = input("Enter the Directory Folder (Ex. 'E:\Model Files'): ")

parent_folder = rf"{file}"  
process_all_txt_files(parent_folder)
