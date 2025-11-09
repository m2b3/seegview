import mne
import numpy as np

from scipy.stats import norm


def jackknife_CI_percentile(jackknife_psds, psd, alpha = 0.95): 
    lower_q = (1-alpha)/2
    upper_q = 1-lower_q
    lower = np.percentile(jackknife_psds, q = lower_q*100, axis = -1)
    upper = np.percentile(jackknife_psds, q = upper_q*100, axis = -1)
    return lower, upper

def jackknife_CI_z_score(jackknife_psds, psd, alpha = 0.95): 
    n = jackknife_psds.shape[-1]
    jackknife_var = (n-1)/n*np.sum(np.square(jackknife_psds - psd[..., np.newaxis]), axis = -1)
    jackknife_se = np.sqrt(jackknife_var)
    CI_width = norm.ppf((1-alpha)/2 + alpha)*jackknife_se
    return psd - CI_width, psd + CI_width
    
def welch_with_CI(freqs, psds, CI_func = jackknife_CI_z_score, alpha = 0.95):
    jackknife_psds = get_jackknife_psds(psds)
    psd = np.mean(psds, axis = -1)
    jackknife_psd = np.mean(jackknife_psds, axis = -1)
    bias = psd - jackknife_psd

    lower, upper = CI_func(jackknife_psds, psd, alpha)

    return freqs, psd, bias, lower, upper
    

def get_psds(raw, picks, psd_func, fs, onsets, ends, n_jobs, dB, fmax): 

    psds_to_concat = [] 
    for onset, end in zip(onsets, ends): 
        data = raw.get_data(picks = picks, start = onset, stop = end)
        psds_period, freqs = psd_func(
            data, 
            sfreq = fs,
            n_fft = int(fs*3),
            fmax = fmax,
            average = False, 
            output = "power", 
            n_jobs = n_jobs)
        psds_to_concat.append(psds_period)
    
    psds = np.concat(psds_to_concat, axis = -1)
    if dB: 
        psds = 20*np.log10(psds)
    return freqs, psds

def get_jackknife_psds(psds):
    n = psds.shape[-1]
    summed_psds = np.sum(psds, axis = -1)
    jackknife_data = summed_psds[..., np.newaxis] - psds
    return jackknife_data/(n-1)