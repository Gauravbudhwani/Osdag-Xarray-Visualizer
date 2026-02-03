# Osdag Structural Visualizer (Screening Task 2026)

This repository contains the Python-based visualization tool developed for the **Osdag 2026 Screening Task**. The project analyzes structural forces from an Xarray dataset and generates both 2D engineering diagrams and a 3D full-bridge visualization similar to professional structural analysis software (e.g., MIDAS).

##  Features

### Task 1: 2D Analysis (Central Girder)
- **Data Extraction**: Programmatically extracts Bending Moment (`Mz`) and Shear Force (`Vy`) values for the central longitudinal girder (Elements 15–83).
- **Visualization**: Generates interactive **Shear Force Diagrams (SFD)** and **Bending Moment Diagrams (BMD)** using Plotly.
- **Continuity**: Ensures continuous plotting logic by mapping element start/end nodes to physical coordinates.

### Task 2: 3D Bridge Visualization
- **Full Structure**: Visualizes all 5 girders of the bridge in a 3D space.
- **MIDAS-Style Extrusion**: Implements a vertical extrusion logic where the force magnitude is mapped to the Y-axis (height), creating 3D "ribbons" that represent the forces acting on the bridge.
- **Interactivity**: Fully rotatable and zoomable 3D model for detailed inspection.

---

##  Tech Stack
- **Python 3.x**
- **Xarray** (Data handling for NetCDF `.nc` files)
- **Plotly** (Interactive 2D and 3D plotting)
- **NumPy & Pandas** (Data manipulation)

---

## 📂 Project Structure

```text
Osdag-Xarray-Visualizer/
│
├── data/
│   ├── screening_task.nc    # The Xarray dataset containing force values
│   ├── node.py              # Node coordinate data
│   └── element.py           # Element connectivity data
│
├── main.py                  # Core script for data extraction and visualization
├── requirements.txt         # List of dependencies
└── README.md                # Project documentation
```

---

## ⚙️ Setup & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/Gauravbudhwani/Osdag-Xarray-Visualizer.git
cd Osdag-Xarray-Visualizer
```

### 2. Create a Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install xarray plotly pandas numpy netCDF4
```

### 4. Run the Analysis

```bash
python main.py
```

This will open two browser tabs: one for the 2D diagrams and one for the 3D bridge visualization.

---

##  Results

### 1. 2D Shear & Bending Diagrams
The code successfully isolates the central girder and plots the sawtooth shear pattern and continuous bending moments.

### 2. 3D "MIDAS-Style" Visualization
The 3D view displays the Bending Moment (Mz) for the entire bridge structure, with magnitude represented by height.

---

##  Video Demonstration
A short video demonstrating the code execution and interactive plots can be found here:

(https://youtu.be/L6FE4eBpJ0c?si=58xWBrAPz8fV8C6K)

---

## 📝 License
This submission is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License as per FOSSEE guidelines.

**Author**: Budhwani Gaurav Pratap
