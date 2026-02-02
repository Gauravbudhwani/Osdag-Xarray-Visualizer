import os
import sys
import xarray as xr

def get_girder_data():
    file_path = 'data/screening_task.nc'
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    # Load the full dataset
    try:
        ds = xr.open_dataset(file_path)
        print("Dataset loaded succesfully")
    except Exception as e:
        print(f"Could not load netCDF: {e}")
        return None

    # Elements for the central longitudinal girder as per Task 1
    target_elements = [15, 24, 33, 42, 51, 60, 69, 78, 83]
    
    # Filtering dataset for these elements
    # Using .sel() on the Element dimension
    try:
        girder_subset = ds.sel(Element=target_elements) #note here grinder_subset is the grinder data we were given in the pdf
        print(f"Extracted {len(girder_subset.Element)} elements.")
        # Should give 9 elements, Since there are 9 IDs in our list 

        # Spliting Mz (Moment) and Vy (Shear) into their own variables 
        # so they are easier to plot later.
        girder_subset['Mz_i'] = girder_subset['forces'].sel(Component='Mz_i')
        girder_subset['Mz_j'] = girder_subset['forces'].sel(Component='Mz_j')
        girder_subset['Vy_i'] = girder_subset['forces'].sel(Component='Vy_i')
        girder_subset['Vy_j'] = girder_subset['forces'].sel(Component='Vy_j')
        
        print("Successfully separated Mz and Vy data.")
        
        # Quick check to ensure values look real
        print(f"Sample Mz_i: {girder_subset['Mz_i'].values[0]:.4f}")
        
        return girder_subset

    except KeyError as e:
        print(f"Error extraction data: {e}")
        return None

if __name__ == "__main__":
    data = get_girder_data()