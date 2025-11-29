import pyqtgraph as pg
import numpy as np

# Temporary Fix
non_selected_pen = pg.mkPen(color= (255//2, 255//2, 255//2), width = 1)
selected_pen = pg.mkPen(color= (255, 255, 255), width = 1)

class MultipleTimeWidget(pg.PlotWidget): 
    """A class for plotting Multiple Time Traces, EEG-style

    Args:
        pg (_type_): _description_
    """
    def __init__(
            self, 
            raw, 
            curr_channel, 
            curr_time, 
            window_duration, 
            num_traces
    ): 
        super().__init__()
        
        self.raw = raw
        
        self.ch_names = raw.ch_names
        self.sfreq = raw.info["sfreq"]

        self.curr_channel = curr_channel
        
        # Window Parameters
        self.curr_time = curr_time
        self.window_duration = window_duration

        self.num_traces = num_traces

        self._setup_ui()

    def _setup_ui(self): 
        self.setLabel("left", "V")
        self.setLabel("bottom", "Time(s)")
        self._set_line_items()

    def _set_line_items(self): 
        self.line_items = []
        for i in range(self.num_traces): 
            self.line_items.append(self.plot([], []))
    
    def _update_display(
            self, 
            curr_channel_name: str | None = None, 
            curr_channel: int | None = None,
            curr_time: float | None = None, 
            window_duration: float | None = None,
            num_traces: int | None = None
    ): 
        if curr_channel_name is not None: 
            if curr_channel_name in self.ch_names: 
                curr_channel = self.ch_names.index(curr_channel_name)
            else: 
                curr_channel = None
        if curr_channel is not None: 
            self.curr_channel = curr_channel
        if curr_time is not None: 
            self.window_duration = window_duration
        if num_traces is not None: 
            self.num_traces = num_traces
        self.redraw()
    
    def redraw(
            self
    ): 
        start_idx_raw = int(self.curr_time*self.sfreq)
        end_idx_raw = int((self.curr_time + self.window_duration)*self.sfreq)
        times = self.curr_time + np.arange(end_idx_raw - start_idx_raw)/self.sfreq
        
        # Modify this later, this is just a proof of concept for now    
        curr_channels = self._get_current_channels()
        raw_traces, _ = self.raw[curr_channels, start_idx_raw: end_idx_raw]
        # Now need to offset
        offset = np.max(np.std(raw_traces, axis = -1)) * 2
        offsets = np.arange(self.num_traces) * offset
        offsets = offsets[:, None]

        raw_traces_offset = raw_traces - offsets
        for i in range(self.num_traces): 
            if curr_channels[i] == self.curr_channel: 
                pen = selected_pen
            else: 
                pen = non_selected_pen
            
            self.line_items[i].setData(
                times, 
                raw_traces_offset[i, :])
            self.line_items[i].setPen(pen)
        
    
    def _get_current_channels(self): 
        # Try to display the selected in the middle
        start_channel = self.curr_channel - self.num_traces//2
        start_channel = max(start_channel, 0)
        return np.arange(self.num_traces) + start_channel