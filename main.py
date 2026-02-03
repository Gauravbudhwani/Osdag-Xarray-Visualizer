import os
import sys
import xarray as xr
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Importing the data files
from data.node import nodes
from data.element import members

def get_girder_data():
    file_path = 'data/screening_task.nc'
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    # Loading the full dataset
    try:
        ds = xr.open_dataset(file_path)
        print("Dataset loaded succesfully")
    except Exception as e:
        print(f"Could not load netCDF: {e}")
        return None

    # Defining all girders as per the Task 2 PDF requirements
    # I need all these elements to be extracted now
    all_girders = [
        13, 22, 31, 40, 49, 58, 67, 76, 81,  # Girder 1
        14, 23, 32, 41, 50, 59, 68, 77, 82,  # Girder 2
        15, 24, 33, 42, 51, 60, 69, 78, 83,  # Girder 3 (Central)
        16, 25, 34, 43, 52, 61, 70, 79, 84,  # Girder 4
        17, 26, 35, 44, 53, 62, 71, 80, 85   # Girder 5
    ]
    
    # Filtering dataset for these elements
    try:
        girder_subset = ds.sel(Element=all_girders) #note here grinder_subset is the grinder data we were given in the pdf 
        print(f"Extracted {len(girder_subset.Element)} elements (All Girders).")

        # Spliting Mz (Moment) and Vy (Shear) into their own variables 
        girder_subset['Mz_i'] = girder_subset['forces'].sel(Component='Mz_i')
        girder_subset['Mz_j'] = girder_subset['forces'].sel(Component='Mz_j')
        girder_subset['Vy_i'] = girder_subset['forces'].sel(Component='Vy_i')
        girder_subset['Vy_j'] = girder_subset['forces'].sel(Component='Vy_j')
        
        print("Successfully separated Mz and Vy data.")
        return girder_subset

    except KeyError as e:
        print(f"Error extraction data: {e}")
        return None

def plot_diagrams(data, element_ids):
    # Creating two subplots: Top for Shear, Bottom for Moment. we will be able to see both on browers in a single tab
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("Shear Force Diagram (SFD)", "Bending Moment Diagram (BMD)"),
        vertical_spacing=0.15
    )

    # Lists to hold the continuous line data
    shear_x, shear_y = [], []
    moment_x, moment_y = [], []

    print("Processing elements for 2D plotting...")

    for elem in element_ids:
        n_start, n_end = members[elem]
        x_start = nodes[n_start][0]
        x_end = nodes[n_end][0]

        vy_i = data['Vy_i'].sel(Element=elem).item()
        vy_j = data['Vy_j'].sel(Element=elem).item()
        mz_i = data['Mz_i'].sel(Element=elem).item()
        mz_j = data['Mz_j'].sel(Element=elem).item()

        shear_x.extend([x_start, x_end])
        shear_y.extend([vy_i, vy_j])
        
        moment_x.extend([x_start, x_end])
        moment_y.extend([mz_i, mz_j])

    # Adding Shear Force Trace
    fig.add_trace(go.Scatter(
        x=shear_x, y=shear_y, mode='lines+markers', name='Shear Force',
        line=dict(color='blue'), fill='tozeroy'
    ), row=1, col=1)

    # Add Bending Moment Trace
    fig.add_trace(go.Scatter(
        x=moment_x, y=moment_y, mode='lines+markers', name='Bending Moment',
        line=dict(color='red'), fill='tozeroy'
    ), row=2, col=1)

    fig.update_layout(height=800, title_text="Task 1: Central Longitudinal Girder Analysis", showlegend=False)
    fig.update_xaxes(title_text="Distance (m)", row=2, col=1)
    fig.update_yaxes(title_text="Shear Force (kN)", row=1, col=1)
    fig.update_yaxes(title_text="Bending Moment (kNm)", row=2, col=1)
    fig.show()

def plot_3d_bridge(data, all_girders_dict, plot_type='Mz'):
    # plot_type can be 'Mz' (Moment) or 'Vy' (Shear)
    fig = go.Figure()
    
    # Scaling factor! 
    # Force values are small (like 6.0), but bridge is big. 
    # We need to scale the force up so it's visible in 3D.
    scale = 0.5 if plot_type == 'Mz' else 1.0
    
    print(f"Generating 3D {plot_type} plot...")

    # 1. Drawing the basic wireframe of the bridge (Grey lines)
    # This will help in visualizing the structure context
    for elem_id, node_pair in members.items():
        n1, n2 = node_pair
        x = [nodes[n1][0], nodes[n2][0]]
        y = [nodes[n1][1], nodes[n2][1]] # This is usually 0.0
        z = [nodes[n1][2], nodes[n2][2]]
        
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color='lightgrey', width=2),
            showlegend=False,
            hoverinfo='skip'
        ))

    # 2. Draw the extruded Force Diagrams for each girder
    colors = ['orange', 'cyan', 'magenta', 'yellow', 'lime']
    
    for i, (girder_name, elements) in enumerate(all_girders_dict.items()):
        
        # building the 3D line for this specific girder
        x_vals, y_vals, z_vals = [], [], []
        
        var_i = f"{plot_type}_i" # e.g., Mz_i
        var_j = f"{plot_type}_j" # e.g., Mz_j

        for elem in elements:
            n1, n2 = members[elem]
            
            # Base coordinates of the element
            x1, y1, z1 = nodes[n1]
            x2, y2, z2 = nodes[n2]
            
            # getting force values
            val_i = data[var_i].sel(Element=elem).item()
            val_j = data[var_j].sel(Element=elem).item()

            # EXTRUSION LOGIC:
            # I mapped the force magnitude to the Y-axis (vertical)
            # Original Y is usually 0, so I added the scaled force to it.
            y_force_1 = y1 + (val_i * scale)
            y_force_2 = y2 + (val_j * scale)

            x_vals.extend([x1, x2])
            y_vals.extend([y_force_1, y_force_2])
            z_vals.extend([z1, z2])

        # Adding the 3D ribbon/line for this girder
        fig.add_trace(go.Scatter3d(
            x=x_vals, y=y_vals, z=z_vals,
            mode='lines',
            name=f"{girder_name} ({plot_type})",
            line=dict(color=colors[i % len(colors)], width=5)
        ))

    # Layout settings for a nice 3D view
    title = "3D Bending Moment Diagram" if plot_type == 'Mz' else "3D Shear Force Diagram"
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X (Length)',
            yaxis_title='Y (Force Magnitude)',
            zaxis_title='Z (Width)',
            aspectmode='data' # this will keeps the proportions real
        ),
        height=800
    )
    fig.show()

if __name__ == "__main__":
    data = get_girder_data()
    
    if data is not None:
        # Task 1: 2D Plot for Central Girder
        central_girder = [15, 24, 33, 42, 51, 60, 69, 78, 83]
        plot_diagrams(data, central_girder)
        
        # Task 2: 3D Plots for ALL Girders
        # Defining the groups as per given in PDF
        girders_dict = {
            'Girder 1': [13, 22, 31, 40, 49, 58, 67, 76, 81],
            'Girder 2': [14, 23, 32, 41, 50, 59, 68, 77, 82],
            'Girder 3': [15, 24, 33, 42, 51, 60, 69, 78, 83],
            'Girder 4': [16, 25, 34, 43, 52, 61, 70, 79, 84],
            'Girder 5': [17, 26, 35, 44, 53, 62, 71, 80, 85]
        }
        
        # Plot Bending Moment in 3D
        plot_3d_bridge(data, girders_dict, plot_type='Mz')
        
        # uncomment the below code for Shear Force in 3D 
        # plot_3d_bridge(data, girders_dict, plot_type='Vy')