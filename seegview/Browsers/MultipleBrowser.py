from PyQt5.QtGui import QKeyEvent
import mne

from PyQt5.QtWidgets import (
    QMainWindow, 
    QApplication, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QLabel)

from PyQt5.QtCore import Qt

import numpy as np
import sys


from seegview.Managers.KeypressManager import KeybindingManager
from seegview.Managers.TimeManager import TimeManager
from seegview.Managers.AnnotationsManager import AnnotationsManager

from seegview.Widgets.MultipleTimeWidget import MultipleTimeWidget

from seegview.StyleSheets import minimalist_sheet

class MultipleBrowser(QMainWindow): 
    def __init__(
            self, 
            raw, 
            curr_channel, 
            curr_time, 
            window_duration, 
            num_traces, 
            annotations: mne.Annotations | None = None,
            ): 
        super().__init__()

        self.raw = raw
        self.curr_time = curr_time
        self.curr_channel = curr_channel
        self.window_duration = window_duration
        self.num_traces = num_traces

        # Initialize the annotations
        if annotations is None: 
            annotations = raw.annotations

        self.annotations = annotations
        self.display_annotations = True

        self.annot_manager = AnnotationsManager(
            annotations = self.annotations, 
            current_time = curr_time, 
            window_duration = window_duration
        )

        self.time_manager = TimeManager(
            initial_time = curr_time, 
            initial_duration = window_duration,
            max_time = raw.times[-1]
        )

        self.time_manager.register_annotations_manager(self.annot_manager)

        self.setWindowTitle("Multiple Browser")
        self.resize(1200, 800)
        self._setup_ui()
        self._update_display()

    def _setup_ui(self): 
        self.widget = MultipleTimeWidget(
            raw = self.raw, 
            curr_channel = self.curr_channel, 
            curr_time = self.curr_time, 
            window_duration = self.window_duration, 
            num_traces = self.num_traces
        )

        self.ch_names = self.widget.ch_names
        
                