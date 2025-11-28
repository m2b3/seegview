# sEEG Visualizer

An interactive plotting suite for stereoelectroencephalography (sEEG) data visualization.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installing from Source

1. **Clone or download this repository:**
   ```bash
   git clone https://github.com/m2b3/seegview.git
   cd seegview
   ```

2. **Install the package:**
   ```bash
   pip install .
   ```

### Installing in Development Mode

If you're actively developing the package and want changes to be immediately reflected:

```bash
pip install -e .
```

### Fresh Computer Setup

If you're starting from a completely fresh computer:

1. **Install Python:**
   - Download and install Python from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Verify installation:**
   ```bash
   python --version
   pip --version
   ```

3. **Follow the installation steps above**

### Virtual Environment (Recommended)

It's recommended to install the package in a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the package
pip install .
```

### Usage

This package provides an example script, found in test_ecg_widget.py. The reference data comes from (1), with subject "sub-4r3o". To run the file, please download the subject's folder from https://dabi.loni.usc.edu/dsi/W4SNQ7HR49RL, and add the destination of its parent directory in config.py. 

The example script also uses a Freesurfer parcellation (2), ran locally. Please consult the Freesurfer website on installation instructions, and how to run recon-all. Add the destination of the Freesurfer output directory to config.py. 

Afterwards, you can run the script as follows: 

```bash
   python -i .\seegview\test_visualizer_full.py
```

## Dependencies

The package automatically installs the following dependencies:

- numpy 
- PyQt5
- pyqtgraph 
- mne
- mne_bids 
- pyvistaqt 
- pyvista

## Bibliography

1. Paulk, A. C. et al. Local and distant cortical responses to single pulse intracranial stimulation in the human brain are differentially modulated by specific stimulation parameters. Brain Stimulat. 15, 491–508 (2022). 

2. Fischl, B. FreeSurfer. Neuroimage 62, 774–781 (2012).
