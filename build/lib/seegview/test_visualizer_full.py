from PyQt5.QtWidgets import QApplication
import sys
import os
from seegview.load_reference_dataset import load

import numpy as np

from seegview.Browsers.TFRBrowser import TFRBrowser

from seegview.Widgets.BrainSurfaceWidget import BrainSurfaceWidget
from seegview.Widgets.MRISliceView import MRIViewer

from seegview.config import freesurfer_root

import nibabel as nib

app = QApplication(sys.argv)

raw = load(0)

##############
# TFR Browser
##############


freqs = np.arange(50) + 2
picks = np.arange(10) + 65
tf = raw.copy().pick(picks).compute_tfr(method = "morlet", freqs = freqs, decim = 100)

tfr_browser = TFRBrowser(
    tf = tf,
    raw = raw)

#############
# MRI Slice Viewer
#############
subject = "sub-4r3o"

t1 = nib.load(
    os.path.join(
        freesurfer_root, subject, "mri", "T1.mgz" 
    )
)
mri_widget = MRIViewer(t1, raw.info)
tfr_browser.channel_manager.register_widget(mri_widget)

#############
# Surface Viewer
#############
surface_widget = BrainSurfaceWidget(subject, freesurfer_root)
# load appropriate transformation for this dataset
vox2ras = t1.header.get_vox2ras()
vox2ras_tkr = t1.header.get_vox2ras_tkr()
trans = vox2ras_tkr @ np.linalg.inv(vox2ras)

surface_widget.add_sensors(raw.info)
surface_widget.link_channel_manager(tfr_browser.channel_manager)

tfr_browser.show()
mri_widget.show()
surface_widget.show()

sys.exit(app.exec_())