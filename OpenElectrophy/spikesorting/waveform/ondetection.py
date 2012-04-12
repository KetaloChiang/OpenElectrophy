







import quantities as pq
import numpy as np

from tools import initialize_waveform, get_following_peak, remove_limit_spikes

class AlignWaveformOnDetection:
    """
    Align spike waveform on the original signal where detected
    This is fast but other method with interpolation give better results.
    
    
    """
    name = 'Align waveform on detection'


    def run(self, spikesorter, sign = '-', left_sweep = 1*pq.ms, right_sweep = 1*pq.ms):
        s = spikesorter

        sr = s.signalSamplingRate
        swL = int((left_sweep*sr).simplified)
        swR = int((right_sweep*sr).simplified)
        #~ print swL, (left_sweep*sr)
        wsize = swL + swR + 1
        trodness = s.filteredBandAnaSig.shape[0]
        
        # clean
        remove_limit_spikes(spikesorter, swL, swR)
        
        
        # Initialize
        initialize_waveform(spikesorter, wsize)
        s.waveformSamplingRate = s.signalSamplingRate
        s.leftSweep =swL
        s.rightSweep = swR
        
        # take individual waveform
        n = 0
        for seg, indexes in enumerate(s.spikeIndexArray):

            for ind in indexes :
                for rc in range(len(s.recordingChannels)):
                    sig = s.filteredBandAnaSig[rc, seg]
                    s.spikeWaveforms[n,rc, :] = sig[ind-swL:ind+swR+1]
                n += 1


