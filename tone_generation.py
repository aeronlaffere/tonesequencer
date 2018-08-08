import numpy as np

def generate_tone(f=185, duration=0.125, Fs=44100, volume=1, simple=True):
    waveform = np.sin(2 * np.pi * np.arange(duration * Fs) * f / Fs) * volume
    if not simple:
        waveform += np.sin(2 * np.pi * np.arange(duration * Fs) * (2 * f) / Fs) * volume + np.sin(2 * np.pi * np.arange(duration * Fs) * (3 * f) / Fs) * volume
    #if f != 0:
        #waveform = waveform/max(waveform)*0.5
    waveform = ramp(waveform)
    return(waveform)

def generate_tone_sequence(low_trials, high_trials, separation='8va', synchrony='interleaved', base_frequencies=[369.99, 415.30, 466.16], training=False, training_volume=0, target_band='high'):
    low_waveform = np.array([])
    high_waveform = np.array([])
    for sequence in low_trials:
        for tone in sequence:
            low_waveform = np.append(low_waveform, generate_tone(f=base_frequencies[tone], duration=1/6, volume=0.2))
            low_waveform = np.append(low_waveform, generate_tone(f=0, duration=1/6)) # silence
        low_waveform = np.append(low_waveform, generate_tone(f=0, duration=2/6))
    for sequence in high_trials:
        for tone in sequence:
            if synchrony == 'interleaved':
                high_waveform = np.append(high_waveform, generate_tone(f=0, duration=1/6)) # silence
            high_waveform = np.append(high_waveform, generate_tone(f=2*base_frequencies[tone]*((2**(1/12))**-1), duration=1/6, volume=0.2)) if separation=='8va' else np.append(high_waveform, generate_tone(f=4*base_frequencies[tone]*((2**(1/12))**-1), duration=1/6, volume=0.2))
            if synchrony == 'synchronous':
                high_waveform = np.append(high_waveform, generate_tone(f=0, duration=1/6)) # silence
        high_waveform = np.append(high_waveform, generate_tone(f=0, duration=2 * 1/6))
    if training == True:
        waveform = low_waveform + (high_waveform * training_volume) if target_band == 'low' else high_waveform + (low_waveform * training_volume)
    else:
        waveform = low_waveform + high_waveform
    # waveform = waveform/max(waveform)
    waveform = 0.33 * waveform
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