"""
test_ecg_widget.py - Simple test application for ECGWidget

Requires the Brainheart package
"""

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent

from seegview.Widgets.ECGWidget import ECGWidget
import mne


class ECGTestWindow(QMainWindow):
    
    def __init__(self, raw):
        super().__init__()
        
        self.raw = raw
        self.current_time = 0.0
        self.window_duration = 10.0
        
        self.setWindowTitle("ECG Widget Test")
        self.resize(1200, 600)
        
        self._apply_dark_theme()
        
        self._setup_ui()
    
    def _apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #0d0d0d;
                color: #e0e0e0;
                font-family: 'Monospace', 'Courier New', monospace;
            }
            
            QLabel, QCheckBox {
                color: #a0a0a0;
                font-size: 11px;
            }
            
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border: 1px solid #2a2a2a;
                background-color: transparent;
            }
            
            QCheckBox::indicator:checked {
                background-color: #88c0d0;
                border: 1px solid #88c0d0;
            }
            
            QCheckBox::indicator:hover {
                border: 1px solid #3a3a3a;
            }
        """)
    
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(main_layout)
        
        # Create ECG widget
        try:
            self.ecg_widget = ECGWidget(
                raw=self.raw,
                curr_time=self.current_time,
                window_duration=self.window_duration,
                show_peaks=True,
                show_artifacts=True
            )
            main_layout.addWidget(self.ecg_widget)
        except ValueError as e:
            print(f"Error creating ECG widget: {e}")
            return
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Right:
            # Scroll forward
            self.current_time += self.window_duration / 4
            max_time = self.raw.times[-1] - self.window_duration
            self.current_time = min(self.current_time, max_time)
            self.ecg_widget.update_display(curr_time=self.current_time)
            
        elif event.key() == Qt.Key_Left:
            # Scroll backward
            self.current_time -= self.window_duration / 4
            self.current_time = max(0, self.current_time)
            self.ecg_widget.update_display(curr_time=self.current_time)
            
        elif event.key() == Qt.Key_Home:
            # Zoom in (decrease window duration)
            self.window_duration = max(1.0, self.window_duration * 0.8)
            self.ecg_widget.update_display(window_duration=self.window_duration)
            
        elif event.key() == Qt.Key_End:
            # Zoom out (increase window duration)
            max_dur = self.raw.times[-1]
            self.window_duration = min(max_dur, self.window_duration * 1.25)
            self.ecg_widget.update_display(window_duration=self.window_duration)
        
        elif event.key() == Qt.Key_Escape:
            # Close window
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    from brainheart.demo import raw
    
    window = ECGTestWindow(raw)
    window.show()
    
    sys.exit(app.exec_())