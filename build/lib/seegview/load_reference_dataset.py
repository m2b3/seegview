import mne_bids
import mne

from seegview.config import bids_root

def load(index = 1):
    ext = "vhdr" #extension for the recording
    subject = "4r3o" #sample
    sess = "postimp"
    datatype = "ieeg"
    suffix = "ieeg"
    run = "01"
    extension = "vhdr"
    bids_paths = mne_bids.BIDSPath(root = bids_root, 
                                session = sess, 
                                subject = subject, 
                                datatype = datatype, 
                                suffix = suffix,
                                run = run, 
                                extension= extension
                                )
    bids_path = bids_paths.match()[index]
    #Load
    raw = mne_bids.read_raw_bids(bids_path)
    raw.load_data()
    return raw