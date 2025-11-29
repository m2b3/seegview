from PyQt5.QtWidgets import QApplication
import sys
import os

from seegview.load_reference_dataset import load

import numpy as np

from seegview.Widgets.MultipleTimeWidget import MultipleTimeWidget

from seegview.Managers.TimeManager import TimeManager
from seegview.Managers.KeypressManager import KeybindingManager

app = QApplication(sys.argv)

raw = load(0)

# The Multiple Browser
browser = MultipleTimeWidget(
    raw, 
    curr_channel = 0, 
    curr_time = 0.0, 
    window_duration = 10.0,
    num_traces = 10
)

keybinding_manager = KeybindingManager(browser)
browser.show()
browser.redraw()