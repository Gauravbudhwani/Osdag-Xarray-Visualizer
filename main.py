import xarray as xr
import pandas as pd
import sys
import os

def get_girder_data():
    file_path = 'data/screening_task.nc'
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    # Load the full dataset
    try:
        ds = xr.open_dataset(file_path)
        print("Dataset loaded successfully")
    except Exception as e:
        print(f"Failed to load netCDF: {e}")
        return None

    # Elements for the central longitudinal girder as per Task 1
    target_elements = [15, 24, 33, 42, 51, 60, 69, 78, 83]
    
    # Filtering dataset for these elements
    # Using .sel() on the Element dimension 
    try:
        girder_subset = ds.sel(Element=target_elements) #note here grinder_subset is the grinder data we were given in the pdf
        print(f"Extracted {len(girder_subset.Element)} elements for the central girder")
        # Should give 9 elements, Since there are 9 IDs in our list 
    except KeyError:
        print("Error: Could not find specified Element IDs in the dataset")
        return None

    # Quickly checking to make sure we have the Mz and Vy data needed for plotting
    check_vars = ['Mz_i', 'Mz_j', 'Vy_i', 'Vy_j']
    missing = [v for v in check_vars if v not in girder_subset]
    
    if missing:
        print(f"Warning: Missing variables: {missing}")
    else:
        print("All required force variables (Mz, Vy) found.")
        # Just printing first value of Mz_i to check
        print(f"Sample Mz_i: {girder_subset['Mz_i'].values[0]:.2f}")

    return girder_subset

if __name__ == "__main__":
    data = get_girder_data()
    
    if data is not None:
        print("\nReady for plotting...")