from setuptools import setup, find_packages

setup(
    name = "seegview", 
    version = "0.1.0", 
    packages = find_packages(), 
    install_requires = [     
        "numpy", 
        "scipy",
        "PyQt5", 
        "pyqtgraph", 
        "mne", 
        "mne_bids", 
        "pyvistaqt", 
        "pyvista", 
        "nibabel", 
        "nilearn"
    ], 
    extras_require = {
        "docs": ["brainheart"]
    }
)