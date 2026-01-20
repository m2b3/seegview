import pyqtgraph as pg
import numpy as np

class PSDWidget(pg.PlotWidget): 
    def __init__(
            self, 
            psd, 
            curr_channel = None
    ): 
        super().__init__()
        self.data = psd.data
        self.ch_names = psd.ch_names
        self.freqs = psd.freqs

        if curr_channel is None: 
            curr_channel = self.ch_names[0]
        self.curr_channel = curr_channel

        self._setup_ui()

    def _setup_ui(self): 
        self.setLabel("left", "PSD")
        self.setLabel("bottom", "Freq(Hz)")

        self.line_item = self.plot([], [])

    def _update_display(
            self, 
            curr_channel_name: str | None = None, 
            curr_channel: int | None = None, 
    ): 
        if curr_channel_name is not None: 
            if curr_channel_name in self.ch_names: 
                curr_channel = self.ch_names.index(curr_channel_name)
            else: 
                curr_channel = None
            if curr_channel is not None:                     
                self.curr_channel = curr_channel
            
            self.redraw()
        
    def redraw(
            self
    ): 
        new_data = self.data[self.curr_channel, :]
        self.line_item.setData(self.freqs, new_data)