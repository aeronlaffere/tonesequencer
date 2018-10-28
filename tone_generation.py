import numpy as np

def generate_tone(f=185, duration=0.125, Fs=44100, volume=1):

    waveform = np.sin(2 * np.pi * np.arange(duration * Fs) * f / Fs) * volume

    waveform = ramp(waveform)
    
    return(waveform)

def generate_tone_sequence(low_trials, high_trials, target_band, distractor_volume=1, base_frequencies=[369.99, 415.30, 466.16]):
    
    low_waveform = np.array([])
    high_waveform = np.array([])

    for sequence in low_trials:
        for tone in sequence:
            low_waveform = np.append(low_waveform, generate_tone(f=base_frequencies[tone], duration=1/6, volume=0.8))
            low_waveform = np.append(low_waveform, generate_tone(f=0, duration=1/6)) # silence
        low_waveform = np.append(low_waveform, generate_tone(f=0, duration=2/6)) # silence
    
    for sequence in high_trials:
        for tone in sequence:
            high_waveform = np.append(high_waveform, generate_tone(f=0, duration=1/6)) # silence
            high_waveform = np.append(high_waveform, generate_tone(f=2*base_frequencies[tone]*((2**(1/12))**-1), duration=1/6, volume=(2/5)*0.8))
        high_waveform = np.append(high_waveform, generate_tone(f=0, duration=2*1/6)) # silence

    if target_band == 'low':
        waveform = low_waveform + (high_waveform * distractor_volume)
    elif target_band == 'high':
        waveform = high_waveform + (low_waveform * distractor_volume)
    elif target_band == 'passive':
        waveform = high_waveform + low_waveform

    return(waveform)

def ramp(waveform, ramp_dur=0.1, Fs=44100):
    note_dur = len(waveform)/Fs
    ramp_dur = ramp_dur * note_dur
    onset = np.sin(np.pi * np.linspace(0,1,Fs*ramp_dur)/2)**2
    middle = np.ones(int(Fs * (note_dur - 2 * ramp_dur)))
    offset = onset[::-1]
    ramp = np.concatenate((onset, middle, offset))
    waveform = waveform * ramp
    return(waveform)
